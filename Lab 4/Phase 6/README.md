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

