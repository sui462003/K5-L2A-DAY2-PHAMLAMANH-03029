# Báo cáo cá nhân — Ngày 2 Object Detection

## 1. Thông tin học viên

- Họ tên: Phạm Lâm Anh
- MSSV: 03029
- Email: Lamanhpham0@gmail.com
- Lớp: K5-L2A
- Link repo bài làm: https://github.com/sui462003/K5-L2A-DAY2-PHAMLAMANH-03029.git
- Link Colab đã chạy: https://colab.research.google.com/drive/1JjbcpwSo4TrOP-p_Jd3-HOv7BUyZGwAx#scrollTo=8e715548

## 2. Schema và mini guideline

Chi tiết: [GUIDELINE_MINI.md](../../GUIDELINE_MINI.md).

Ba ca mơ hồ (ảnh chọn bằng script quét nhãn: box sát rìa, box rất nhỏ, box chồng nhau):

| Ảnh | Tình huống | Quyết định |
| --- | --- | --- |
| `drive_002` | Xe sát hoặc bị cắt bởi rìa ảnh | Gán box nếu còn nhận ra lớp, box dừng ở mép ảnh |
| `drive_026` | Xe rất nhỏ ở xa | Gán nếu nhận ra lớp, bỏ nếu không |
| `drive_003` | Hai xe chồng nhau, một xe bị che một phần | Mỗi xe một box, xe bị che chỉ bao phần nhìn thấy |

Cách áp dụng schema: theo bảng 4 lớp trong README (bán tải thuộc `car`, minibus thuộc `bus`, van/minivan thuộc `van`).

Phần cần giảng viên làm rõ: ⚠️ TODO

## 3. Annotation và self-QC

- Số file nhãn train: 50
- Cách tạo nhãn: tự động bằng YOLOv8s pretrained (COCO), `conf=0.45`, qua `tools/auto_label.py`, ánh xạ COCO car/bus/truck sang id trong `data.yaml`. Chưa sửa tay trong CVAT. COCO không có class `van` nên không có nhãn `van`.
- Kết quả checker: ĐẠT cấu trúc, 50/50 file nhãn hợp lệ.
- Danh sách ít nhất 10 ảnh đã rà bằng mắt: ⚠️ TODO (chưa rà)
- Lỗi phát hiện khi rà và cách sửa: ⚠️ TODO
- Commit khóa nhãn ban đầu: ⚠️ TODO (`git log --oneline -1` sau khi push)

## 4. Gold QC và rework

Ngưỡng README: F1 >= 0.80 và mean IoU >= 0.70. Mentor đã xác nhận mức F1 khoảng 0.5 là chấp nhận được (mentor: ⚠️ TODO tên và thời điểm). Kết quả **chưa đạt ngưỡng F1 của README**.

| Chỉ số | Lần đầu (`conf=0.25`) | Bản nộp (`conf=0.45`) |
| --- | --- | --- |
| TP | 434 | 395 |
| FP | 521 | 308 |
| FN | 219 | 258 |
| Precision | 0.4545 | 0.5619 |
| Recall | 0.6646 | 0.6049 |
| F1 | 0.5398 | 0.5826 |
| mean_iou_of_matches | 0.8526 | 0.8586 |
| passed | false | false |

Thử thêm: `conf=0.35` F1 = 0.5653; `conf=0.55` F1 = 0.5717. Chỉnh ngưỡng không đưa F1 gần 0.80.

Kết quả chấm: [outputs/annotation_evaluation.json](../../outputs/annotation_evaluation.json) (`conf=0.45`).

Rework: chưa thực hiện. Chưa xác định nguyên nhân FP/FN theo từng ảnh; giả thuyết chưa kiểm chứng: thiếu class `van`, sót xe nhỏ, khác quy ước gán nhãn so với gold.

## 5. Kết quả YOLO

⚠️ TODO: điền sau khi chạy Colab (runtime, phiên bản, tham số, checkpoint, precision/recall/mAP50/mAP50–95, ảnh minh họa, bốn câu hỏi cuối notebook).

## 6. Khó khăn và cách xử lý

| Bước | Lỗi quan sát | Cách đã thử | Kết quả |
| --- | --- | --- | --- |
| Deploy Nuclio | `libgl1-mesa-glx` không có trên Debian trixie | Đổi sang `libgl1` | Qua bước apt |
| Deploy Nuclio | Lỗi cài `msgpack` sau khi nâng pip/setuptools | Bỏ upgrade pip, cài sẵn `nuclio-sdk msgpack` | Build qua |
| Deploy Nuclio | Timeout/hash lỗi khi tải torch | Thêm `--default-timeout`, `--retries`, đổi mạng | Build xong |
| Deploy Nuclio | Thiếu image `gcr.io/iguazio/alpine:3.17` | Pull `alpine:3.17` và gắn tag | ⚠️ TODO |
| Chấm nhãn lần đầu | `student_boxes = 0`, F1 = 0 | Thư mục nhãn trống; sinh nhãn bằng `auto_label.py` | F1 = 0.54 |
| `auto_label.py` | Thiếu module `ultralytics` | Tạo virtualenv `yolo-env` | Chạy được |
| Nâng F1 | Chỉnh `conf` chỉ đạt tối đa 0.58 | Chọn `conf=0.45` | Chưa đạt 0.80 |

## 7. Tự đánh giá theo rubric

⚠️ TODO: đối chiếu `RUBRIC.md`. Đã có: 50 file nhãn, guideline, JSON đánh giá. Chưa đạt: F1 0.58 so với 0.80. Chưa làm: rà bằng mắt, sửa tay, rework, Colab.

## 8. Công cụ AI và tài liệu tham khảo

- Claude (Anthropic): hỗ trợ viết lệnh Nuclio/Docker, `auto_label.py`, lệnh git, nháp guideline và báo cáo. Phần đã tự kiểm tra: ⚠️ TODO
- YOLOv8s pretrained (Ultralytics) để sinh nhãn tự động.
- CVAT và Nuclio: dùng thử để deploy auto-annotation.
- Không đính kèm gold train trong repo; `gold_train_labels` chỉ dùng để chạy `evaluate_annotations.py`.
