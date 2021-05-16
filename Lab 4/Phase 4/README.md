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

Xem pseudocode hàm `func4()`.  

```c
int __cdecl func4(int a1, int a2, int a3)
{
  int v3; // eax
  int v4; // ebx
  int result; // eax

  v3 = (a3 - a2) / 2;
  v4 = v3 + a2;
  if ( v3 + a2 > a1 )
    return v4 + func4(a1, a2, v4 - 1);
  result = v3 + a2;
  if ( v4 < a1 )
    result = v4 + func4(a1, v4 + 1, a3);
  return result;
}
```  

Có thể thấy, đây là 1 hàm đệ quy, vậy để đơn giản hóa, chúng ta sẽ brute-force giá trị `a1` (tương đương `num_1`) cho đến khi giá trị trả về của hàm bằng `21`.  

Python script để brute-force:  
```python
def func4(a1, a2, a3):
    v3 = (a3 - a2) // 2
    v4 = v3 + a2

    if v4 > a1:
        return v4 + func4(a1, a2, v4 - 1)
    if v4 < a1:
        return v4 + func4(a1, v4 + 1, a3)
    return v4


for i in range(15):
    if func4(i, 0, 14) == 21:
        print(i)
        break
```  
> Giá trị nhận được là `6`.  

Vậy 2 số cần nhập là `6` và `21`.  

## Kiểm tra kết quả
```
└─$ ./bomb
Welcome to my fiendish little bomb. You have 6 phases with
which to blow yourself up. Have a nice day!
All your base are belong to us.
Phase 1 defused. How about the next one?
1 2 4 7 11 16
That's number 2.  Keep going!
0 310
Halfway there!
6 21
So you got that one.  Try this one.
```
> Chính xác!
