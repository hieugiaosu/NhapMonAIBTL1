# IntroductionToAIBTL1

## Chuẩn bị Thư Viện
chạy lệnh sau để cài đặt thư viện:
```
    pip install -r requirement.txt
```
## Về luật chơi
Tham khảo tại: [game link](https://www.coolmathgames.com/0-bloxorz)
<br>
Một số lưu ý về mô phỏng:
- một nút nhẹ là một nút chỉ cần nằm trên nút đó là có thể kích hoạt (trong mô phỏng là dạng hình tròn)
- một nút nặng là một nút phải đứng trên nút đó là có thể kích hoạt (trong mô phỏng là dấu X trên ô)
- Trong trò chơi trên có nút tách làm 2 nhưng trong mô phỏng này không có và coi như không tồn tại testcasse có nút đó

## Không gian trạng thái
Ta thấy để giải bài toán trò chơi này, ta cần quan tâm ba thành phần sau:
- Bàn chơi (board)
- Khối di chuyển (Cube) (đúng ra phải đặt là box mà lỡ đặt cube rồi nên lười sửa)
- Các nút (Button)
Vì vậy ta có không gian trạng thái sau:
### State
Đối với khối di chuyển (Cube), vì ta thấy 1 cube gồm 2 cube nhỏ hơn nên 1 cube sẽ được định nghĩa gồm 2 khối lập phương nhỏ hơn. Vậy state của 1 cube là tọa độ của 2 khối lập phương đó theo dạng **(hàng,cột)** với kiểu dữ liệu **tuple**. Trong đó **firstCube** và **secondCube** lần lượt chứa tọa độ của từng khối lập phương và tuân theo quy tắc sau:
-Nếu khối di chuyển đang nằm thẳng đứng **firstCube == secondCube**
-Nếu khối di chuyển nằm ngang theo chiều cùng 1 hàng, tọa độ cột của **firstCube** phải nhỏ hơn **secondCube**
-Nếu khối di chuyển nằm dọc theo chiều cùng 1 cột, tọa đồ hàng của của **firstCube** phải nhỏ hơn **secondCube**
ví dụ về tọa đọ hợp lệ:
```
    firstCube = (1,1)
    secondCube = (1,1)
    ###
    firstCube = (1,1)
    secondCube = (1,2)  ### Ngược lại là không hợp lệ
    ###
    firstCube = (1,1)
    secondCube = (2,1)  ### ngược lại là không hợp lệ
```
Đối với bàn chơi (board), board là một **dictionary** trong python với các key là tọa độ **(hàng, cột)** của ô nào đó với key ở kiểu **tuple**, value của mỗi key là một số **int**. Trong đó value gồm:
-0 ứng với không có ô đó
-1 ứng với ô yếu (ô không được đứng trên đó, hay số khối lập phương nhỏ có tọa độ tại ô đó tối đa là 1)
-2 ứng với ô bình thường (ô có thể đứng trên đó, hay số khối lập phương nhỏ có tọa độ tại ô đó tối đa là 2)
-3 ứng vô vị trí đích (vị trí ta muốn đứng trên đó)
ví dụ:
Đây là một kiểu của board:
```
{ (0,0):2, (0,1):1, (0,2):1, (0,3):2, (0,4):3, (0,5):2, (0,6):0}
```
Đây là hình ảnh mô phỏng board trên: 
<br>

![alt](https://i.imgur.com/OA7oB4y.png)
<br>

Đối với các nút bấm (button), các nút bấm được chứa trong buttonList là một **Dictionary** với key là tọa độ đặt nút bấm đó. Kiểu của key là **tuple**, value tương ứng là một **List** vói phần tử đầu là kiểu của nút bấm (1 cho nút chỉ cần 1 khối lập phương để kích hoạt, 2 cho nút cần 2 khối lập phương phương để kích hoạt). Phần tử thứ hai là một **List** chứ các tuple là tọa độ các ô sẽ xuất hiện (nếu chưa tồn tại) hoặc mất đi (nếu đã tồn tại) khi bấm nút đó.
## Các file được viết:
### Seting.py
Bao gồm các setting cơ bản để hiển thị visualize được định nghĩa trong class setting gồm
```
    self.cellWidth #### Kích thước của 1 ô, kiểu dữ liệu số
    self.alpha ### độ nghiêng khi vẽ của 1 ô, kiểu dữ liệu số
    self.color ### mã màu rgb khi vẽ bàn chơi với,kiểu dử liệu list các tuple
               ### Với các phần tử trong list này lần lượt là mã rgb cho màu của
               ### background, ô chịu được sức nặng yếu, ô bình thường, ô đích, nút nhẹ và nút nặng

```