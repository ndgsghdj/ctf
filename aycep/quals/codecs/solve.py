from pwn import *
import codecs

elf = context.binary = ELF('./codec')
context.log_level = 'debug'

# p = process()
p = remote('34.87.173.177', 21001)

p.recvuntil('>>')
p.sendline(b'Yes')
p.recvline()

rand_str = p.recvline()

p.sendafter('>>', rand_str)
p.recvuntil('uppercase\n')

rand_str = p.recvline()
ans = rand_str.decode().upper().encode()
p.sendafter('>>', ans)

p.recvuntil('rot13\n')

rand_str = p.recvline()
ans = codecs.encode(rand_str.decode(), 'rot13').encode()

p.sendafter('>>', ans)

print(p.recvline())
print(p.recvline())

ans = "If ya wanna win, ya gotta want it!"

p.sendline(ans)

print(p.recvall())
