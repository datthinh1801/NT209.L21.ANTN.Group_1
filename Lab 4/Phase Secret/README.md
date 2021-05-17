# Secret
## Solution
Sau đây sẽ là bài phân tích Secret Phase

Ta để ý là sau mối phase (từ phase 1 -> 6) sẽ gọi một hàm `phase_defused()`

![image](https://user-images.githubusercontent.com/31529599/118503837-2e310600-b755-11eb-882f-706a03b521d8.png)

Mở hàm đó và phân tích
```c
unsigned int phase_defused()
{
  char v1; // [esp+14h] [ebp-68h] BYREF
  char v2; // [esp+18h] [ebp-64h] BYREF
  char v3[80]; // [esp+1Ch] [ebp-60h] BYREF
  unsigned int v4; // [esp+6Ch] [ebp-10h]

  v4 = __readgsdword(0x14u);
  if ( num_input_strings == 6 )
  {
    if ( __isoc99_sscanf(&secret_string, "%d %d %s", &v1, &v2, v3) == 3 && !strings_not_equal(v3, "DrEvil") )
    {
      puts("Curses, you've found the secret phase!");
      puts("But finding it and solving it are quite different...");
      secret_phase();
    }
    puts("Congratulations! You've defused the bomb!");
  }
  return __readgsdword(0x14u) ^ v4;
}
```
Ta thấy trong hàm này sẽ gọi `secret_phase` nên ta biết được hàm này sẽ là secret phase cần giải

Tiến hành phân tích, ở câu lệnh `if` đầu tiên thì chương trình sẽ kiểm tra biến `num_input_strings` có bằng `6` hay không nên mình đoán biến này là biến đếm cho `6` chuỗi nhập vào của `6` phase. Tuy nhiên mình đã phân tích và thấy đúng như vậy.

Ở trong hàm `read_line()` sau khi đọc một chuỗi vào thì chương trình sẽ thực hiện tăng biến `num_input_string` lên `1` và biến này được lưu trong phân vùng `bss` nên được sài `global`

![image](https://user-images.githubusercontent.com/31529599/118505293-7d2b6b00-b756-11eb-8411-dbfb2b237b57.png)

Vậy có nghĩa là để hàm `phase_defused()` gọi được hàm `secret_phase()` thì chúng ta phải pass được tất cả `6` phase của chương trình `bomb` này

Và ở câu lệnh `if` tiếp theo (` if ( __isoc99_sscanf(&secret_string, "%d %d %s", &v1, &v2, v3) == 3 && !strings_not_equal(v3, "DrEvil") )`) chương trình thực hiện đọc từ địa chỉ tại `secret_string` `2` biến int và `1` biến string được lưu lần lượt vào `v1`, `v2`, `v3` và kiểm tra `sscanf()` có đọc đủ được `3` giá trị hay không (==3) và kiểm tra giá trị của `v3` có bằng `DrEvil` hay không. Nếu một trong hai điều kiện sai thì chương trình sẽ chỉ in ra chuỗi `Congratulations! You've defused the bomb!` chứ chưa giải được `secret_phase`

Sau một vài bước `debug` đơn giản thì ta biết `secret_string` chính là địa chỉ nơi lưu chuỗi của `phase_4` mà `phase_4` đã nhập vào `2` số tương ứng với `v1` và `v2` cho nên ta cần thêm chuỗi `DrEvil` để tương ứng với `v3` và thỏa điều kiện `if`. Và vì `phase_4` chỉ sử dụng `2` số đầu, nên khi thêm chuỗi thứ 3 vào sau thì sẽ không ảnh hưởng đến kết quả của `phase_4` 

Chuỗi input của `phase_4` = `6 21 DrEvil`

## Phân tích `secret_phase()`

Đoạn pseudocode của `secret_phase()`

```c
unsigned int secret_phase()
{
  const char *v0; // eax
  int v1; // ecx
  int v2; // ebx
  int v3; // ecx

  v0 = read_line();
  v2 = strtol(v0, 0, 10);
  if ( (unsigned int)(v2 - 1) > 1000 )
    explode_bomb(v1);
  if ( fun7(&n1, v2) != 3 )
    explode_bomb(v3);
  puts("Wow! You've defused the secret stage!");
  return phase_defused();
}
```

Đầu tiên chương trình sẽ nhập vào một chuỗi sau đó sử dụng hàm `strtol()` để phân tích chuỗi này thành số vd `"123"` sẽ thành số `123` và lưu vào `v2`

Tiếp theo kiểm tra, nếu số đó lớn hơn `1001` thì sẽ nổ `bomb` và thoát chương trình vì vậy số nhập vào phải `<=1000` và vì số này là `unsigned` nên sẽ `>0`

Tiếp theo đó chương trình sẽ truyền `v2` vào trong hàm `fun7()` và kiểm tra kết quả trả về có bằng `3` hay không nếu khác sẽ nổ `bomb` và thoát chương trình -> ouput của `fun7` với input `v2` sẽ phải bằng `3` để chúng ta pass được phase này.

### Phân tích hàm `fun7()`
```c
int __cdecl fun7(_DWORD *a1, int a2)
{
  int result; // eax

  if ( !a1 )
    return -1;
  if ( *a1 > a2 )
    return 2 * fun7(a1[1], a2);
  result = 0;
  if ( *a1 != a2 )
    result = 2 * fun7(a1[2], a2) + 1;
  return result;
}
```

Với `a1` là `&n1` và `a2` là `v2`

Đây là một hàm đệ quy, nếu sẽ trả về kết quả cho hai trường hợp:
#### chẵn với câu lệnh `if( *a1 > a2)` 
#### lẻ với câu lệnh `if(*a1 != a2`

vì kết quả ta mong muốn là `3` cho nên `result` phải rơi vào trường hợp sau, và điều kiện dừng sẽ chính là `*a1` == `a2` nghĩa là `a2` >= `a1` và `a2` sẽ bằng một giá trị trong vùng nhớ mà `a1 + n` 

Ta bắt đầu `debug` bằng `gdb` để xong các giá trị tại `&n1`

![image](https://user-images.githubusercontent.com/31529599/118510489-355b1280-b75b-11eb-903a-a4ffbf34f0eb.png)

`n1` đang trỏ tới `0x804x088`

Ta xem vùng nhớ tại `n1`

![image](https://user-images.githubusercontent.com/31529599/118510675-5facd000-b75b-11eb-87d6-432c89f873a2.png)

Từ địa chỉ trên suy ra mảng `a1` = {0x24, 0x8, 0x32, 0x16, 0x2d, 0x06, 0x6b, 0x28, 0x1, 0x63,.... }
`*a1==a2` cho nên ta sẽ thử tư mảng `n1` xem kết quả nào ra output bằng `3` 

Thử lần lượt và ta thấy `0x6b` sẽ cho kết quả bằng 3 tương ứng

## Chạy lại chương trình và nhập input vừa phân tích được 

![image](https://user-images.githubusercontent.com/31529599/118511577-3f314580-b75c-11eb-9a31-3e263ec66990.png)


# Xong, vây là ta đã phân tích thành công `secret_phase`

