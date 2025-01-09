from pwn import *
from string import ascii_lowercase, ascii_uppercase, digits
import random

context.log_level = 'debug'

def generate_random_string():
	return "".join([random.choice(ascii_lowercase + ascii_uppercase + digits) for _ in range(32)])

def find_seed(target, max=1000000):
	for seed in range(max):
		random.seed(seed)
		test = generate_random_string()
		if test == target:
			return seed

p = remote('tcp.ybn.sg', 28480)

target = (p.recvline()).decode()
target = target.split('is')[-1].strip()
target = target.replace('"', '')
seed = find_seed(str(target))

random.seed(seed)
payload = generate_random_string()

for i in range(160):
	payload = generate_random_string()
	p.sendlineafter(':', payload)

p.interactive()
