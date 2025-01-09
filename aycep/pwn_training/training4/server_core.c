#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/slab.h>
#include <linux/uaccess.h>
#include <linux/miscdevice.h>
#include <linux/ioctl.h>
#include <linux/types.h>
#include <linux/list.h>
#include <linux/mutex.h>

#define IOC_MAGIC '\xca'

#define DO_CREATE  _IOWR(IOC_MAGIC, 0, struct req)
#define DO_READ    _IOWR(IOC_MAGIC, 1, struct req) 
#define DO_NOTE    _IOWR(IOC_MAGIC, 2, struct req) 
#define DO_DELETE  _IOWR(IOC_MAGIC, 3, struct req) 
#define DO_SYNC    _IOWR(IOC_MAGIC, 4, struct req) 

struct mutex servercore_mutex;

struct req {
    uint64_t idx;
    uint64_t info_addr;
    uint64_t note_size;
    uint64_t note_addr;
};

struct data_unit {
    char info[0x3e0];
    uint64_t idx;
    uint64_t note_size; 
    uint64_t note_addr; 
    uint64_t sync_data;
}; // Size is 0x400 -- kmalloc-1k

void * data_array[0x30] = {0};
unsigned int data_count = 0;

static int open_module(struct inode *inode, struct file *filp);
static long ioctl_module(struct file *filp, unsigned int cmd, unsigned long arg);

static struct file_operations fops = {
	open : open_module,
	unlocked_ioctl : ioctl_module
};

static struct miscdevice servercore = {
    .minor      = 53,
    .name       = "servercore",
    .fops       = &fops,
    .mode	    = 0666,
};

static int open_module(struct inode *inode, struct file *filp) {
	return 0;
}

static int sync_function(uint64_t target, uint64_t repeat) {
    pr_info("Target is at 0x%llx\n", target); 
    pr_info("Sync complete\n"); 
    return 0; 
}

static long ioctl_module(struct file *filp, unsigned int cmd, unsigned long arg) {
    struct req user_data; 
    struct data_unit * data_unit = NULL; 
    void * note = 0; 
    char buf[1024] = {0}; 
    int ret = 0;
    
    memset(&user_data, 0, sizeof(user_data));
    memset(buf, 0, sizeof(buf));
    
    if (copy_from_user(&user_data, (struct req __user *)arg, sizeof(user_data)) != 0) {
		return -1;
    } 
    pr_info("Copy from user done\n"); 
    
    if (user_data.note_size > 0x1000) {
        pr_info("Note size too big\n");
        return -1;
    }
    
    mutex_lock(&servercore_mutex); 
    
    switch(cmd) {
        case DO_CREATE: { 
            // Check if data_count is greater or equal to 0x30 -- if so, fail
            if (data_count >= 0x30) {
                mutex_unlock(&servercore_mutex); 
                pr_info("No space left!\n"); 
                return -1; 
                break;
            }
            
            // Create the data_unit object
            data_unit = kzalloc(sizeof(struct data_unit), GFP_KERNEL);
            
            // Copy the info into the data_unit object
            ret = copy_from_user(buf, (void __user *) user_data.info_addr, 0x3e0-1);
            memcpy(&data_unit->info, buf, 0x3e0-1); 
            memset(buf, 0, sizeof(buf));
            
            // Set idx
            data_unit->idx = data_count; 
            
            //Set sync_data
            data_unit->sync_data = (uint64_t)sync_function; 
            
            // Tell the user where our object is - heap leak
            *(uint64_t *)buf = (uint64_t)data_unit; 
            ret = copy_to_user((void __user *)user_data.note_addr, buf, 0x8);
            memset(buf, 0, sizeof(buf));
            
            // Add the data_unit object into the array and increment data_count
            data_array[data_count] = data_unit; 
            data_count = data_count + 1; 
            
            // Unlock the mutex and return
            mutex_unlock(&servercore_mutex); 
            return 0; 
            break;
        }
        case DO_READ: {
            // Check for out of bounds
            if (user_data.idx > (data_count - 1)) {
                mutex_unlock(&servercore_mutex); 
                pr_info("Invalid idx\n"); 
                return -1; 
                break;
            }
            data_unit = data_array[user_data.idx]; 
            
            // Copy the info
            memcpy(buf, &data_unit->info, 0x3e0-1); 
            ret = copy_to_user((void __user *)user_data.info_addr, buf, 0x3e0-1);
            
            //Copy the note if there is one
            if (data_unit->note_addr != 0 && data_unit->note_addr != 0x10) {
                memset(buf, 0x0, sizeof(buf)); 
                memcpy(buf, (void *)data_unit->note_addr, data_unit->note_size-1); 
                ret = copy_to_user((void __user *)user_data.note_addr, buf, data_unit->note_size); 
            }
            
            mutex_unlock(&servercore_mutex); 
            return 0; 
            break;
        }
        case DO_NOTE: {

            // Check for out of bounds
            if (user_data.idx > (data_count - 1)) {
                mutex_unlock(&servercore_mutex); 
                pr_info("Invalid idx\n"); 
                return -1; 
                break;
            }
            data_unit = data_array[user_data.idx]; 
            
            // Check that the user is not giving 0 as the note size
            if (user_data.note_size == 0) {
                mutex_unlock(&servercore_mutex); 
                pr_info("Invalid note size\n"); 
                return -1; 
                break;
            }
            
            // If note exists, free it.
            if (data_unit->note_addr != 0 && data_unit->note_addr != 0x10) {
                kfree((void *)data_unit->note_addr); 
                data_unit->note_addr = 0x0; 
                data_unit->note_size = 0x0; 
            }
            
            // Create new note - Allocates a block of memory which data and size is determined by user
            note = kmalloc(user_data.note_size, GFP_KERNEL); 
            data_unit->note_addr = (uint64_t)note; 
            data_unit->note_size = user_data.note_size; 
            ret = copy_from_user(note, (void __user *) user_data.note_addr, user_data.note_size);
            
            // Unlock mutex and return
            mutex_unlock(&servercore_mutex); 
            return 0; 
        }
        case DO_DELETE: {
            if (user_data.idx > (data_count - 1)) {
                mutex_unlock(&servercore_mutex); 
                pr_info("Invalid idx\n"); 
                return -1; 
                break;
            }
            data_unit = data_array[user_data.idx]; 
            
            // Free data unit object - Bug: The note is zeroed after it is freed
            if (data_unit->note_addr != 0 && data_unit->note_addr != 0x10) {
                kfree((void *)data_unit->note_addr); 
                data_unit->note_addr = 0; 
            }
            kfree(data_unit); // data_unit in data_array is not zeroed after it is freed -- use after free!
            
            mutex_unlock(&servercore_mutex); 
            return 0; 
            break;
        }
        case DO_SYNC: {
            if (user_data.idx > (data_count - 1)) {
                mutex_unlock(&servercore_mutex); 
                pr_info("Invalid idx\n"); 
                return -1; 
                break;
            }
            data_unit = data_array[user_data.idx]; 
            
            // Execute sync function
            ret = ((int (*)(uint64_t, uint64_t))data_unit->sync_data)((uint64_t)data_unit, (uint64_t)data_unit); 
            
            mutex_unlock(&servercore_mutex); 
            return 0; 
        }
        default: 
            mutex_unlock(&servercore_mutex); 
            return -1;
            break;
    }
    return 0;
}

static int servercore_init(void) {
    mutex_init(&servercore_mutex);
	return misc_register(&servercore);
}

static void servercore_exit(void) {
	 misc_deregister(&servercore);
}

module_init(servercore_init);
module_exit(servercore_exit);

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("ROP LLC's Core Server!!! VERY SECURE, DO NOT BREAK IN");
MODULE_AUTHOR("Kaligula Armblessed, CEO of ROP LLC.");
