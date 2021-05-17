# Phase 6

## Solution

Tiếp tục phân tích Phase 6 

Đây là đoạn pseudocode của Phase này

```c
unsigned int __cdecl phase_6(int a1)
{
  int v1; // ecx
  int v2; // esi
  int v3; // ebx
  int *v4; // eax
  int i; // ebx
  _DWORD *v6; // edx
  int v7; // eax
  int v8; // ecx
  int v9; // ebx
  int *v10; // eax
  int v11; // ecx
  int v12; // edx
  int v13; // esi
  int v15; // [esp+10h] [ebp-44h]
  int v16[6]; // [esp+14h] [ebp-40h] BYREF
  int v17[5]; // [esp+2Ch] [ebp-28h] BYREF
  char v18; // [esp+40h] [ebp-14h] BYREF
  unsigned int v19; // [esp+44h] [ebp-10h]

  v19 = __readgsdword(0x14u);
  read_six_numbers(a1, (int)v16);
  v2 = 0;
  while ( 1 )
  {
    if ( (unsigned int)(v16[v2] - 1) > 5 )
      explode_bomb(v1);
    if ( ++v2 == 6 )
      break;
    v3 = v2;
    do
    {
      if ( *(&v15 + v2) == v16[v3] )
        explode_bomb(v1);
      ++v3;
    }
    while ( v3 <= 5 );
  }
  v4 = v16;
  do
  {
    *v4 = 7 - *v4;
    ++v4;
  }
  while ( v17 != v4 );
  for ( i = 0; i != 6; ++i )
  {
    v8 = v16[i];
    v7 = 1;
    v6 = &node1;
    if ( v8 > 1 )
    {
      do
      {
        v6 = (_DWORD *)v6[2];
        ++v7;
      }
      while ( v7 != v8 );
    }
    v17[i] = (int)v6;
  }
  v9 = v17[0];
  v10 = v17;
  v11 = v17[0];
  do
  {
    v12 = v10[1];
    *(_DWORD *)(v11 + 8) = v12;
    ++v10;
    v11 = v12;
  }
  while ( &v18 != (char *)v10 );
  *(_DWORD *)(v12 + 8) = 0;
  v13 = 5;
  do
  {
    if ( *(_DWORD *)v9 < **(_DWORD **)(v9 + 8) )
      explode_bomb(v12);
    v9 = *(_DWORD *)(v9 + 8);
    --v13;
  }
  while ( v13 );
  return __readgsdword(0x14u) ^ v19;
}
```

## Bắt đầu phân tích từng phần 

```c
 v19 = __readgsdword(0x14u);
  read_six_numbers(a1, (int)v16);
  v2 = 0;
  while ( 1 )
  {
    if ( (unsigned int)(v16[v2] - 1) > 5 )
      explode_bomb(v1);
    if ( ++v2 == 6 )
      break;
    v3 = v2;
    do
    {
      if ( *(&v15 + v2) == v16[v3] )
        explode_bomb(v1);
      ++v3;
    }
    while ( v3 <= 5 );
  }
```

Ở phần đầu này thì chương trình gọi hàm `read_six_number()` như ở phase 2 và lưu vào biến `a1`

Ở trong vòng `while` tiếp theo thì chương trình lần lượt:

### Kiểm tra nếu một trong 6 chữ số nhập vào lớn hơn 6 ( `(unsigned int)(v16[v2] - 1) > 5` ) thì sẽ nổ `bomb` và thoát chương trình ( Tuy nhiên vì ở đây, lấy ra một số `unsigned` nên các số nhập vào sẽ lớn hơn hoặc bằng 0 )
### Tiếp theo kiểm tra tất cả các phần tử phải khác nhau, nếu giống nhau (`*(&v15 + v2) == v16[v3]`) thì sẽ nổ `bom` và thoát chương trình

Vậy 6 số nhập vào sẽ là các số nguyên nằm trong khoảng từ `0` đến `6`



Phân tích đoạn tiếp theo:

```c
  v4 = v16;
  do
  {
    *v4 = 7 - *v4;
    ++v4;
  }
  while ( v17 != v4 );
```

Đoạn này sẽ lấy các phần từ nhập vào sẽ đó tính toán lại bằng cách lấy (7 - (giá trị của phần tử) ) vd: ban đầu là 4 thì sau sẽ là 7 - 4  = 3 ...

## Đoạn tiếp theo này thì hầu hết là sẽ đọc code assembly chứ không thể tiếp tục phân tích bằng pseudocode nữa
### Sử dụng `gdb` để debug

Đầu tiên ta nhìn vào pseudocode thì thấy chương trình sẽ thực hiện tính toán cho đến đoạn code cuối này mới kiểm tra điều kiện. Nên mình đã đặt breakpoint ngay trước hàm này để xem chương trình làm gì.

```c
  do
  {
    if ( *(_DWORD *)v9 < **(_DWORD **)(v9 + 8) )
      explode_bomb(v12);
    v9 = *(_DWORD *)(v9 + 8);
    --v13;
  }
  while ( v13 );
```

Đây là đoạn code assembly của đoạn code c trên
![image](https://user-images.githubusercontent.com/31529599/118448433-328cfd00-b71c-11eb-9a06-5d7c42f0c6ba.png)

Tiến hành debug
![image](https://user-images.githubusercontent.com/31529599/118471923-7c80dd80-b732-11eb-8fd7-5d333da8ba58.png)


Ở đoạn debug này thì chương trình sẽ ` cmp    dword ptr [ebx], eax <0x804c16c>`  trong đó `ebx` đang trỏ tới `node5` và `eax` trỏ tới `ebx+8` chính là `node5+8`

Ở trên nơi hiển thị giá trị các thanh ghi, ta thấy `ecx` đang trỏ tới `node1` và có giá trị `0x804c13c`

![image](https://user-images.githubusercontent.com/31529599/118470892-5444af00-b731-11eb-80d9-5755ec913fb1.png)

Xem vùng nhớ tại `node1` (`0x804c13c`)

![image](https://user-images.githubusercontent.com/31529599/118471064-88b86b00-b731-11eb-9b30-d3abd90d2cf6.png)

Thống kê lại các `node` ta có:

`0x804c13c` -> `node1` có giá trị `0x3af`

`0x0804c148` -> `node2` có giá trị `0x59`

`0x0804c154` -> `node3` có giá trị `0x160`

`0x0804c160` -> `node4` có giá trị `0x186` 

`0x0804c16c` -> `node5` có giá trị `0x5c`

`0x804c178` -> `node6` có giá trị `0x397`

Vậy ở câu lênh `cmp` thì `ebx` là `node5` có giá trị `0x5c` và `eax` có giá trị `0x186` thì sẽ tương ứng với `node4`

Câu lệnh tiếp theo ` jge    phase_6+224 <phase_6+224>`, chương trình kiểm tra nếu giá trị ở `ebx` (`node5`) lớn hơn hoặc bằng giá trị ở `eax`(`node4`) thì sẽ nhảy đến lệnh tiếp theo thực hiện theo tăng `ebx` lên `8` đơn vị và tiếp tục kiểm tra `cmp` như câu lệnh trên, nếu sai thì sẽ nổ `bomb` và kết thúc chương trình `call   explode_bomb <explode_bomb>`

![image](https://user-images.githubusercontent.com/31529599/118472894-9373ff80-b733-11eb-8e8b-724da3051379.png)

Cứ như vậy chương trình sẽ kiểm tra cứ như vậy cho 5 vòng lặp cho đến khi `esi` == `0` (ban đầu `esi` = 5`)


Vì ở đây `ebx` = `0x5c` < `eax` = `0x186` nên chương trình sẽ nổ bomb là thoát chương trình
![image](https://user-images.githubusercontent.com/31529599/118471923-7c80dd80-b732-11eb-8fd7-5d333da8ba58.png)


Sau phân tích ở trên thì ta đoán chương trình có `6` `node` và input nhập vào cũng là từ `1` đến `6` cho nên khả năng cao sẽ liên quan đến nhau


Để mà chương trình không nổ `bomb` và in ra chuỗi ta mong muốn thì phải đúng được tất cả điều kiện trong 5 vòng lặp trên, Theo như phân tích ở trên thì để đúng được tất cả vòng lặp thì `Nodex > Nodex > Nodex > Nodex > Nodex > Nodex` với các `node` là liên tiếp nhau tương ứng với giá trị thì ta có `Node1 > Node6 > Node4 > Node3 > Node5 > Node2`

Vậy ta đoán thì thứ tự nhập vào sẽ là `1 6 4 3 5 2` tuy nhiên trước khi đến đoạn xử lí và so sánh với các `Node` thì chương trình đã thực hiện tính lại các giá trị nhập vào bằng cách lấy `7` trừ đi chính nó như đã phân tích ở trên vậy nên để có mảng `1 6 4 3 5 2` thì input sẽ là `6 1 3 4 2 5`

## Chạy thử chương trình và xem kết quả
![image](https://user-images.githubusercontent.com/31529599/118502376-d8a82980-b753-11eb-8bd7-68d5778faa3d.png)

# Đúng, vậy bomb đã được giải hoàn tất mà không cần phân tích hết tất cả source :))




