# Phase 4
## Solution
Mở IDA Pro 32bit và xem pseudocode.  
```c
unsigned int __cdecl phase_4(int a1)
{
  unsigned int num_1; // [esp+4h] [ebp-18h] BYREF
  int num_2; // [esp+8h] [ebp-14h] BYREF
  unsigned int v4; // [esp+Ch] [ebp-10h]

  v4 = __readgsdword(0x14u);
  if ( __isoc99_sscanf(a1, "%d %d", &num_1, &num_2) != 2 || num_1 > 14 )
    explode_bomb();
  if ( func4(num_1, 0, 14) != 21 || num_2 != 21 )
    explode_bomb();
  return __readgsdword(0x14u) ^ v4;
}
```  

Đầu tiên, chúng ta có thể nhận thấy nếu chương trình không đọc được 2 số nguyên hoặc đọc được 2 số nhưng số thứ nhất > `14` thì bomb nổ.  

Tiếp theo, nếu giá trị trả về của hàm `func4(num_1, 0, 14) != 21` hoặc `num_2 != 21` thì bomb nổ.  
> Vậy ta phải nhập vào 2 số nguyên với số thứ nhất > `14`, số thứ 2 bằng `21` và giá trị trả về của hàm `func4(num_1, 0, 14)` phải bằng `21`.
