from pwn import *

elf = context.binary = ELF('./task')
context.log_level = 'debug'

p = gdb.debug('./task')
p.interactive()
