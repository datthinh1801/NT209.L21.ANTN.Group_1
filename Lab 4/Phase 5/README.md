# Phase 5
## Solution
Mở IDA Pro 32bit và xem pseudocode.  

```c
unsigned int __cdecl phase_5(int input_string)
{
  int i; // eax
  char v3[7]; // [esp+11h] [ebp-17h] BYREF
  unsigned int v4; // [esp+18h] [ebp-10h]

  v4 = __readgsdword(0x14u);
  if ( string_length(input_string) != 6 )
    explode_bomb();

  for ( i = 0; i != 6; ++i )
    v3[i] = array_3249[*(_BYTE *)(input_string + i) & 0xF];

  v3[6] = 0;
  if ( strings_not_equal(v3, "oilers") )
    explode_bomb();
  return __readgsdword(0x14u) ^ v4;
}
```

Ở phase này, chúng ta phải nhập một chuỗi 6 ký tự thì mới thỏa mãn câu lệnh `if` đầu tiên.  

Ở vòng lặp `for`, từng ký tự của `input_string` sẽ được `&` với `0xF`, kết quả nhận được sẽ là `index` để truy xuất tới phần tử của mảng `array_3249`. Sau đó, giá trị của phần tử này sẽ được gán vào chuỗi `v3` ở vị trí `i` tương ứng.  

> Mảng `array_3249` chứa các giá trị sau:  
>
>![image](https://user-images.githubusercontent.com/44528004/118393329-cef5c780-b668-11eb-84e2-4f12a2e3662c.png)  

Sau khi đã gán xong 6 giá trị, nếu `v3` khác `oilers` thì bomb nổ.  

Chương trình dịch ngược để tìm chuỗi cần nhập:  

```c
#include <iostream>
#include <string>
#include <stdio.h>
using namespace std;

int main()
{
    string array_3249 = "maduiersnfotvbyl";
    string res = "oilers";

    for (int j = 0; j < 6; ++j)
    {
        for (int i = 0; i <= 255; ++i)
        {
            int s = i & 0xf;
            if (s < array_3249.length() && s == array_3249.find(res[j]))
            {
                if (isalnum(i))
                {
                    cout << char(i) << " - " << res[j] << endl;
                }
            }
        }
        cout << "------------------------------------" << endl;
    }
    return 0;
}
```  

Kết quả:  

```
J - o
Z - o
j - o
z - o
------------------------------------
4 - i
D - i
T - i
d - i
t - i
------------------------------------
O - l
o - l
------------------------------------
5 - e
E - e
U - e
e - e
u - e
------------------------------------
6 - r
F - r
V - r
f - r
v - r
------------------------------------
7 - s
G - s
W - s
g - s
w - s
------------------------------------
```  

Vì có nhiều kết quả đúng, nên chúng ta chỉ cần chọn 1.  
> Chọn J4O567  

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
J4O567
Good work!  On to the next...
```
> Chính xác.
