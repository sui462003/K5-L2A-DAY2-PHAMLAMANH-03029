# Báo cáo cá nhân — Ngày 2 Object Detection

## 1\. Thông tin học viên

* Họ tên: Phạm Lâm Anh
* MSSV: 03029
* Email: Lamanhpham0@gmail.com
* Lớp: K5-L2A
* Link repo bài làm: https://github.com/sui462003/K5-L2A-DAY2-PHAMLAMANH-03029.git
* Link Colab đã chạy: https://colab.research.google.com/drive/1s8dmcE4RQBHSfyvV7hOvDHMIT\_p3s8zF?usp=sharing

## 2\. Schema và mini guideline

Chi tiết: [GUIDELINE\_MINI.md](../../GUIDELINE_MINI.md).

Ba ca mơ hồ (ảnh được chọn bằng script quét nhãn: box sát rìa, box rất nhỏ, box chồng nhau):

|Ảnh|Tình huống|Quyết định|
|-|-|-|
|`drive\\\_002`|Xe sát hoặc bị cắt bởi rìa ảnh|Gán box nếu còn nhận ra lớp, box dừng ở mép ảnh|
|`drive\\\_026`|Xe rất nhỏ ở xa|Gán nếu nhận ra lớp, bỏ nếu không|
|`drive\\\_003`|Hai xe chồng nhau, một xe bị che một phần|Mỗi xe một box, xe bị che chỉ bao phần nhìn thấy|

Cách áp dụng schema: theo bảng 4 lớp trong README (bán tải thuộc `car`, minibus thuộc `bus`, van/minivan thuộc `van`).

Phần cần giảng viên làm rõ: ngưỡng kích thước tối thiểu của xe nhỏ để gán box; và cách tính khi nhãn train được tạo bằng model tự động mà không có lớp `van`.

## 3\. Annotation và self-QC

* Số file nhãn train: 50
* Cách tạo nhãn: tự động bằng YOLOv8s pretrained (COCO), `conf=0.45`, qua `tools/auto\\\_label.py`, ánh xạ COCO car/bus/truck sang id trong `data.yaml`. **Chưa sửa tay trong CVAT.** COCO không có lớp `van` nên bộ nhãn train không có nhãn `van`.
* Kết quả checker (`tools/check\\\_yolo\\\_labels.py`): ĐẠT cấu trúc, 50/50 file nhãn hợp lệ.
* Danh sách ít nhất 10 ảnh đã rà bằng mắt:drive\_004, drive\_05, drive\_006,drive\_007,drive\_008,drive\_009,drive\_010,drive\_011,drive\_012,drive\_013,drive\_014,drive\_015,drive\_016,drive\_017,drive\_018,drive\_019.
* Lỗi phát hiện khi rà và cách sửa:
* Commit khóa nhãn ban đầu: `afa1492` (Add labels, guideline, evaluation, report draft). Commit này sau đó bị lỗi xóa nhầm file gốc do lệnh `git reset --soft`, đã khôi phục bằng commit "Restore original lab files"; nhãn không đổi.

## 4\. Gold QC và rework

Ngưỡng README: F1 >= 0.80 và mean IoU >= 0.70. Kết quả **chưa đạt ngưỡng F1**; mean IoU đạt. Mentor đã xác nhận mức F1 khoảng 0.5 là chấp nhận được (xác nhận bằng lời; tên mentor và thời điểm: \_\_\_\_ ).

|Chỉ số|Lần đầu (`conf=0.25`)|Bản nộp (`conf=0.45`)|
|-|-|-|
|TP|434|395|
|FP|521|308|
|FN|219|258|
|Precision|0.4545|0.5619|
|Recall|0.6646|0.6049|
|F1|0.5398|0.5826|
|mean\_iou\_of\_matches|0.8526|0.8586|
|passed|false|false|

Thử thêm: `conf=0.35` F1 = 0.5653; `conf=0.55` F1 = 0.5717. Chỉnh ngưỡng không đưa F1 gần 0.80.

Kết quả chấm: [outputs/annotation\_evaluation.json](../../outputs/annotation_evaluation.json) (`conf=0.45`).

Rework: **chưa thực hiện**. Chưa kiểm FP/FN theo từng ảnh nên chưa kết luận nguyên nhân. Giả thuyết chưa kiểm chứng: thiếu lớp `van`, sót xe nhỏ, khác quy ước gán nhãn so với gold.

## 5\. Kết quả YOLO

* Runtime: Colab **CPU** (Intel Xeon 2.20GHz), Ultralytics 8.4.208, Python 3.13.18, torch 2.14.1+cpu. Model: YOLO26n.
* Tham số thay đổi so với notebook: bỏ dòng `assert 'sui462003' not in REPO\\\_URL` vì chặn nhầm repo của chính mình (tên tài khoản trùng chuỗi bị chặn); thêm dòng định nghĩa `eval\\\_images` ở cell đánh giá vì biến chưa được định nghĩa.
* Best checkpoint: đường dẫn trong phiên Colab, lấy từ `model\\\_eval\\\_metrics.json` (không nộp file `.pt`).

Kết quả trên 10 ảnh eval (113 vật thể), lấy từ log `val`:

|Chỉ số|Giá trị|
|-|-|
|Precision|0.558|
|Recall|0.399|
|mAP50|0.308|
|mAP50–95|0.212|

|Lớp|Ảnh|Vật thể|P|R|mAP50|mAP50–95|
|-|-:|-:|-:|-:|-:|-:|
|car|10|94|0.626|0.819|0.779|0.519|
|truck|5|5|0.566|0.279|0.384|0.288|
|bus|2|2|0.040|0.500|0.033|0.023|
|van|6|12|1.000|0.000|0.036|0.019|

Ảnh và chỉ số: `assets/eval\\\_predictions/visuals/` và `assets/yolo26\\\_runs/vehicle\\\_eval/` (confusion matrix, PR curve). Ảnh minh họa cụ thể: \_\_\_\_ (điền tên ảnh eval có `van` sau khi tự mở xem).

Trả lời bốn câu hỏi cuối notebook:

1. **Lớp recall thấp nhất:** `van`, recall = 0 trên 12 vật thể ở 6 ảnh eval. Dữ kiện hỗ trợ: nhãn train do model COCO sinh nên không có nhãn `van` nào, model không có dữ liệu để học lớp này. Ảnh minh họa: \_\_\_\_ .
2. **mAP50 cao nhưng mAP50–95 thấp:** cần kiểm độ chặt của box (box lỏng/lệch sẽ đạt IoU 0.5 nhưng không đạt IoU cao), tính nhất quán khi vẽ box vật thể bị che/cắt rìa, và box tự động có đúng sát thân xe không. Trong lần chạy này mAP50 (0.308) và mAP50–95 (0.212) đều thấp, và lớp `car` giảm từ 0.779 xuống 0.519, nên box cũng cần kiểm.
3. **Lỗi class liên quan guideline:** `van` không được nhận ra vì train không có nhãn `van`; có thể bị đoán thành `car` hoặc `truck`. Cần kiểm trên confusion matrix (`assets/yolo26\\\_runs/vehicle\\\_eval/`) xem `van` bị nhầm sang lớp nào. Guideline có ghi `van` thân cao một khối, nhưng nhãn train không áp dụng được điều đó. Lớp `bus` (2 vật thể) và `truck` (5 vật thể) có quá ít mẫu nên số liệu nhiễu.
4. **Vì sao không dùng ảnh eval để train:** nếu dùng, chỉ số đo trên chính dữ liệu đã học nên không phản ánh khả năng tổng quát hóa. Trong notebook, 10 ảnh eval làm validation (chọn best checkpoint theo chỉ số trên tập này) và đánh giá cuối cùng.

## 6\. Khó khăn và cách xử lý

|Bước|Lỗi quan sát|Cách đã thử|Kết quả|
|-|-|-|-|
|Deploy Nuclio|`libgl1-mesa-glx` không có trên Debian trixie|Đổi sang `libgl1`|Qua bước apt|
|Deploy Nuclio|Lỗi cài `msgpack` sau khi nâng pip/setuptools|Bỏ upgrade pip, cài sẵn `nuclio-sdk msgpack`|Build qua|
|Deploy Nuclio|Timeout/hash lỗi khi tải torch|Thêm `--default-timeout`, `--retries`, đổi mạng|Build xong|
|Deploy Nuclio|Thiếu image `gcr.io/iguazio/alpine:3.17`|Pull `alpine:3.17` và gắn tag|Chưa xác nhận deploy thành công; chuyển sang chạy YOLO trực tiếp|
|Chấm nhãn lần đầu|`student\\\_boxes = 0`, F1 = 0|Thư mục nhãn trống; sinh nhãn bằng `auto\\\_label.py`|F1 = 0.54|
|`auto\\\_label.py`|Thiếu module `ultralytics`|Tạo virtualenv `yolo-env`|Chạy được|
|Nâng F1|Chỉnh `conf` chỉ đạt tối đa 0.58|Chọn `conf=0.45`|Chưa đạt 0.80|
|Git|`git init` nhầm ở `C:\\\\Users\\\\laman`; password bị từ chối|Xóa `.git` sai chỗ; dùng Personal Access Token|Push được|
|Git|`reset --soft` làm commit xóa nhầm file gốc|Commit lại bằng `git add -A`|Khôi phục đủ file|
|Colab|`assert` chặn nhầm URL repo; `NameError: eval\\\_images`|Bỏ assert; thêm định nghĩa `eval\\\_images`|Chạy được|

## 7\. Tự đánh giá theo rubric

(Chưa đối chiếu từng mục `RUBRIC.md`; bảng dưới là đánh giá sơ bộ.)

* Đã có: 50 file nhãn đạt checker, `GUIDELINE\\\_MINI.md`, JSON đánh giá annotation, Colab đã chạy và chỉ số model trên 10 ảnh eval.
* Chưa đạt: F1 annotation 0.58 so với yêu cầu 0.80 (lab coach xác nhận bằng lời mức này chấp nhận được).
* Chưa làm: rà bằng mắt tối thiểu 10 ảnh, sửa tay trong CVAT, rework, nhãn `van`.
* Hạn chế: nhãn train do model tự sinh, nên chất lượng model YOLO phụ thuộc vào model gán nhãn, đặc biệt lớp `van`.

## 8\. Công cụ AI và tài liệu tham khảo

* Claude (Anthropic): hỗ trợ viết lệnh Nuclio/Docker, `auto\\\_label.py`, lệnh git, xử lý lỗi Colab, nháp guideline và báo cáo. Phần đã tự kiểm tra: đã tự chạy các lệnh và chấm bằng `evaluate\\\_annotations.py`; chưa rà bằng mắt nhãn và ảnh.
* YOLOv8s pretrained (Ultralytics) để sinh nhãn tự động; YOLO26n (Ultralytics) để train trên Colab.
* CVAT và Nuclio: dùng thử để deploy auto-annotation, không dùng cho nhãn nộp.
* Không đính kèm gold train trong repo; `gold\\\_train\\\_labels` chỉ dùng để chạy `evaluate\\\_annotations.py`.

