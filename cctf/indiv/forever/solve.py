from pwn import *

elf = ELF("./forever_linux")

p = process("./forever_linux")
p.recvuntil(b">> ")
p.sendline(b"nikola")

for i in range(867502):
    print(i)
    print(p.recvuntil(b":"))
    p.readline()
    sum = eval(p.readline().decode('UTF-8'))
    print(sum)
    print(p.recvuntil(b">> "))
    p.sendline(str(sum))
    print(p.readline())

p.readline()
