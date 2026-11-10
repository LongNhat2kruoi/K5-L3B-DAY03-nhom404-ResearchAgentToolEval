# Báo cáo cá nhân — Phạm Nguyên Khoa - 2A202603795

## 1. Thông tin thành viên

- Họ tên: Phạm Nguyên Khoa
- MSSV: 2A202603795
- Email: pnkvlog1508@gmail.com

## 2. Phần việc phụ trách

- **CP1:** setup môi trường (venv, `.env`, preflight, pytest) và chạy baseline v0.
- **CP2:** tối ưu `artifacts/system_prompt.md` và `artifacts/tools.yaml` qua 3 vòng v1 → v3, ghi `artifacts/version_log.csv`.

## 3. Đóng góp cụ thể

**CP1.** Cài môi trường, kiểm tra 4 key (OpenRouter, Tavily, Firecrawl, RapidAPI) bằng preflight và smoke test từng tool. Chạy baseline v0 với prompt và tools gốc: 15/20 case pass (`case_accuracy` 0.75). 5 case fail, gồm `R08` out_of_scope, `R10` và `R11` missing_info, `R12` wrong_boundary, `R13` wrong_tool/arg. Nguyên nhân chung là prompt gốc cố ý bảo agent "đừng hỏi, cứ đoán", "cứ gửi luôn" và "chỉ làm một bước".

**CP2.** Mỗi version sửa một giả thuyết, đo lại trên 20 case của `eval_base.json`:

| Version | Sửa gì | Giả thuyết | `case_accuracy` |
|---|---|---|---:|
| v0 | Bản gốc | Baseline | 0.75 |
| v1 | `system_prompt.md`: bỏ đoạn "đừng hỏi, cứ đoán"; thêm rule gọi `clarify` khi thiếu handle/URL/topic | Dòng "cứ đoán" là nguyên nhân các lỗi missing_info | 0.85 |
| v2 | `tools.yaml` (`clarify`): mô tả rõ `response_type` (text / yes_no / choice) và bắt buộc truyền | Sau v1 agent đã gọi đúng `clarify` nhưng quên `response_type` vì mô tả mơ hồ | 0.95 |
| v3 | `system_prompt.md` + `tools.yaml` (`send`): bỏ dòng "cứ gửi luôn" và "chỉ một bước"; thêm rule xác nhận chỉ áp cho `send` kèm ví dụ, rule ngoài phạm vi, rule nhiều tool; `send` bắt buộc `confirmed` | Agent hỏi nội dung thay vì xin xác nhận yes/no vì prompt vẫn bảo gửi luôn | 0.95 |

Điều rút ra từ v3:
- Lần thử đầu của v3 tụt xuống 0.80 vì rule xác nhận viết quá rộng, khiến agent hỏi xác nhận cả khi chỉ xem tweet (`R01`). Tôi giới hạn rule chỉ cho `send` và thêm một ví dụ cụ thể thì R12 mới pass.
- Bản v3 cuối vẫn còn một case fail là `M06_switch_tool`: rule "gọi nhiều tool riêng" làm agent giữ thừa `social_search` khi user bảo bỏ Twitter. Tôi thêm mệnh đề giới hạn nhưng chưa sửa được. Đây là trade-off đã ghi trong `version_log.csv`, chưa giải quyết.
- Run của model có dao động nhỏ giữa các lần chạy dù temperature 0 (ví dụ `R06` lúc pass lúc fail khi không đổi gì liên quan), nên tôi chạy lại v3 nhiều lần mới kết luận.

## 4. Bằng chứng

- **File/commit/PR:**
  - Run hợp lệ (`provider_error_cases == 0`, `measured_cases == total_cases`): `starter_v0/runs/v0_B_base_openrouter_20261110T173439967037.json`, `v1_B_base_openrouter_20261110T182009730230.json`, `v2_B_base_openrouter_20261110T182216985761.json`, `v3_B_base_openrouter_20261110T183138786948.json`.
  - 4 file run v3 còn lại trong `runs/` là các lần thử trung gian, giữ làm bằng chứng về regression.
  - Log: `starter_v0/artifacts/version_log.csv` (dòng v0–v3, có hash, giả thuyết, metric trước và sau).
  - Commit: `7ddd716` (thêm tên vào TEAM.md và tạo báo cáo), `7656d34` (điền tên nhóm, lớp), `dde9e4d` (log v0), `b2a76d8` (CP2: prompt, tools, log v1–v3). Branch: `2A202603795-PhamNguyenKhoa`.
  - `pytest tests/test_tool_contract.py` xanh sau mỗi lần sửa `tools.yaml`.
- **AI/công cụ đã dùng và cách tự kiểm tra kết quả:** Dùng Claude Code để đọc repo, đề xuất và sửa prompt/tools, chạy eval. Tôi không tin điểm tự báo mà tự kiểm tra bằng cách đọc `failures` và `actual_tool_calls` trong từng run JSON, chạy lại v3 nhiều lần để loại trừ dao động, và chạy `pytest` contract test sau mỗi thay đổi `tools.yaml`. Mỗi hypothesis trong bảng trên đều dựa vào nội dung run JSON, không dựa vào cảm giác. Không có run hay metric nào được tạo ngoài các run thật ở trên.

## 5. Tự đánh giá

- **Làm tốt:** đưa `case_accuracy` từ 0.75 lên 0.95, mỗi vòng có giả thuyết và run làm bằng chứng. Phát hiện được regression ở v3 và ghi lại trung thực thay vì chỉ giữ kết quả đẹp.
- **Chưa tốt:** v3 chưa đạt 100%, còn case `M06`. Chỉ có 20 case nên một case lệch đã làm điểm thay đổi 0.05, và tôi chưa có bộ case riêng của nhóm để đo kỹ hơn.
- **Nếu có thêm một vòng:** thử diễn đạt lại rule nhiều tool để không ảnh hưởng case đổi nguồn (`M06`), rồi chạy mỗi version vài lần lấy trung bình để giảm nhiễu.
