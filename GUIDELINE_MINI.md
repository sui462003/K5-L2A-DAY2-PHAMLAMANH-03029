# Mini guideline — bài làm cá nhân

## Định nghĩa lớp

| Lớp | Định nghĩa của bạn | Ví dụ/điểm phân biệt |
| --- | --- | --- |
| `car` | Xe con chở người cỡ nhỏ: sedan, hatchback, SUV, taxi, xe bán tải | Thân thấp, một khối; bán tải vẫn là `car`, không phải `truck` |
| `truck` | Xe tải chở hàng, xe đầu kéo | Có thùng hàng hoặc rơ-moóc phía sau, thân cao và dài hơn `car` |
| `bus` | Xe buýt, minibus chở khách | Thân dài, nhiều cửa sổ dọc thân, chở nhiều khách |
| `van` | Xe van, minivan chở hàng hoặc chở người | Thân cao một khối, mũi ngắn, nhỏ hơn `bus` và cao hơn `car` |

## Quy tắc chung

- Box bám sát vật thể nghĩa là: cạnh box sát phần nhìn thấy của thân xe, không chừa viền thừa, không cắt mất bánh hay mui xe.
- Vật thể bị che khuất: vẫn gán box nếu phần nhìn thấy đủ để nhận ra lớp; box chỉ bao phần nhìn thấy.
- Vật thể bị cắt bởi rìa ảnh: gán box đến sát mép ảnh nếu còn đủ để nhận ra lớp; bỏ nếu chỉ còn một mảnh nhỏ.
- Vật thể rất nhỏ/mơ hồ: chỉ gán khi nhận ra được lớp; quá nhỏ hoặc không rõ lớp thì không gán, và áp dụng nhất quán cho mọi ảnh.

## Ghi lại quyết định cho ít nhất ba ca mơ hồ

| Ảnh | Tình huống | Quyết định cuối | Lý do theo schema |
| --- | --- | --- | --- |
| `drive_002` | Xe nằm sát hoặc bị cắt bởi rìa ảnh | Gán box nếu còn nhận ra lớp, box dừng ở mép ảnh | Lớp mô tả loại vật thể; phần nhìn thấy đủ để nhận diện thì cần box |
| `drive_026` | Xe rất nhỏ ở xa | Gán nếu nhận ra lớp, bỏ nếu không | Chỉ gán khi có thể xác định lớp; giữ ngưỡng này nhất quán |
| `drive_003` | Hai xe chồng lên nhau, một xe bị che một phần | Mỗi xe một box riêng, xe bị che chỉ bao phần nhìn thấy | Bị che một phần vẫn cần box nếu đủ nhận diện lớp |
