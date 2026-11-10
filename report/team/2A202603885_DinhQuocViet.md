# Báo cáo cá nhân — Đinh Quốc Việt - 2A202603885

## 1. Thông tin thành viên

- Họ tên: Đinh Quốc Việt
- MSSV: 2A202603885
- Email: 26ai.vietdq3@vinuni.edu.vn
- GitHub: KemmVSAI

## 2. Phần việc phụ trách

- **CP4:** xây dựng bộ eval nhóm và kiểm tra routing, arguments, boundary và hành vi multi-turn của research agent.

## 3. Đóng góp cụ thể

- Viết đúng 10 case trong `starter_v0/data/eval_group.json`: 5 single-turn và 5 multi-turn.
- Thiết kế case cho tool mới `rss`, tool `wiki`, `fetch`, `timeline`, `lookup`, `social_search`, `clarify`, cùng case out-of-scope không được gọi tool.
- Chạy group eval bằng provider OpenRouter và phân tích `failures`, `observed_mismatch`, `actual_tool_calls` trong run JSON.
- Điều chỉnh wording của case multi-turn và rule xử lý lượt mới để agent chỉ thực hiện trạng thái cuối cùng, không gọi lại mode cũ hoặc gọi lặp tool.
- Cập nhật bảng B3 trong báo cáo nhóm.

## 4. Bằng chứng

- Eval cases: `starter_v0/data/eval_group.json`
- Run cuối: `starter_v0/runs/v3_B_group_openrouter_20261110T195538902469.json`
- Báo cáo nhóm: `report/team/group_report.md`, mục B3
- Kết quả: 10/10 case pass; `provider_error_cases=0`; case, routing, argument và multiturn accuracy đều đạt 1.0.
- AI/công cụ đã dùng và cách tự kiểm tra: dùng Codex để hỗ trợ đọc cấu trúc harness, tạo case và phân tích log; tự kiểm tra bằng cách chạy lại eval provider thật, đối chiếu `actual_tool_calls` với `expect`, kiểm tra đủ 5 single + 5 multi và chạy pytest.

## 5. Tự đánh giá

- Hoàn thành bộ eval nhóm đúng schema và có độ phủ cho cả routing, arguments, missing information, out-of-scope và multi-turn.
- Kết quả cuối đạt 10/10 trên run hợp lệ.
- Hướng cải thiện: bổ sung thêm case kiểm tra boundary gửi Telegram sau khi user xác nhận và case lỗi dữ liệu trả về từ các tool live.
