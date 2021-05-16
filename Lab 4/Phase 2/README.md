# Phase 2
## Solution
Dùng **gdb** để phân tích chương trình như sau:  

Đầu tiên, ngay sau khi chương trình đọc xong 6 số nguyên, giá trị của số đầu tiên sẽ được so sánh với số `0`. Nếu số đầu tiên khác `0` thì chương trình sẽ tiếp tục, ngược lại thì bomb nổ.  
![image](https://user-images.githubusercontent.com/44528004/118391547-f6479700-b65e-11eb-86da-84730acefc3b.png)  
> Có thể xem stack ở bên dưới, `esp + 4` đang chứa địa chỉ của số nguyên đầu tiên.

Tiếp theo.  

![image](https://user-images.githubusercontent.com/44528004/118391679-c9e04a80-b65f-11eb-9f7e-7c17e88b587a.png)  
![image](https://user-images.githubusercontent.com/44528004/118391738-19267b00-b660-11eb-913f-623ed4f6ab2d.png)  


Ở đây, `ebx` chính là giá trị `index` của 6 số được nhập, với `ebx=1` tương đương số thứ nhất và `ebx=6` tương đương số thứ 6. Trong mỗi vòng lặp, giá trị `index` này sẽ được cộng với giá trị của số nguyên tại vị trí tương ứng. Sau đó, kết quả của phép cộng sẽ được so sánh với giá trị của số nguyên tiếp theo.  
> `dword prt [esp + ebx*4]` chính là giá trị của số nguyên thứ `ebx`, và `dword prt [esp + ebx*4 + 4]` chính là giá trị của số nguyên kế tiếp.  

Vậy chúng ta cần nhập vào 6 số nguyên thỏa mãn các điều kiện sau:
1. Số đầu tiên khác `0`.
2. Tổng của một số với `index` của số đó phải bằng với giá trị của số kế tiếp.  
> Chọn numbers[1] = 1  
> => numbers[2] = numbers[1] + 1 = 2  
> => numbers[3] = numbers[2] + 2 = 4  
> => numbers[4] = numbers[3] + 3 = 7  
> => numbers[5] = numbers[4] + 4 = 11  
> => numbers[6] = numbers[5] + 5 = 16  

## Kiểm tra kết quả
```
└─$ ./bomb
Welcome to my fiendish little bomb. You have 6 phases with
which to blow yourself up. Have a nice day!
All your base are belong to us.
Phase 1 defused. How about the next one?
1 2 4 7 11 16
That's number 2.  Keep going!
```
