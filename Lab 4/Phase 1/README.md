# Phase 1
## Solution
Mở IDA Pro 32bit.  
![image](https://user-images.githubusercontent.com/44528004/118391115-e038d700-b65c-11eb-9578-893e47006865.png)  

Có thể dễ dàng thấy được có 1 chuỗi `All your base are belong to us.` gán cứng được push vào stack trước khi gọi hàm `strings_not_equal`. Từ đó có thể suy ra, nếu chuỗi nhập và chuỗi trên không bằng nhau thì chương trình sẽ thực thi hàm `explode_bomb` tức là kích nổ bomb.  
> Vậy chuỗi cần nhập để phá bomb là `All your base are belong to us.`  

### Kiểm tra kết quả
```
└─$ ./bomb
Welcome to my fiendish little bomb. You have 6 phases with
which to blow yourself up. Have a nice day!
All your base are belong to us.
Phase 1 defused. How about the next one?
```  
> Chính xác!
