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



