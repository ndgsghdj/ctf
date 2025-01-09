from pwn import *

elf = ELF("./forever_linux")

context.log_level = 'debug'

p = process("./forever_linux")
p.recvuntil(b">> ")
p.sendline(b"nikola")

p.recvlines(5)
calculation = p.recvline().decode()
print(calculation)
answer = eval(calculation)
p.sendlineafter('>>', str(answer))

for i in range(2, 867503):
	p.recvuntil(':\n')
	calculation = p.recvline().decode()
	print(calculation)
	answer = str(int(eval(calculation)))
	p.sendlineafter('>>', answer)

print(p.recvall())
