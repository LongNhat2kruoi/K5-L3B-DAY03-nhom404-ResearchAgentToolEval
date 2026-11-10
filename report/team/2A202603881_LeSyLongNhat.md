# Báo cáo cá nhân — Lê Sỹ Long Nhật

## 1. Thông tin thành viên

- Họ tên: Lê Sỹ Long Nhật
- MSSV: 2A202603881
- Email: 26ai.nhatlsl@vinuni.edu.vn
- GitHub username: `longnhat2kruoi`
- Vai trò: Nhóm trưởng

## 2. Phần việc phụ trách

- Hoàn thiện CP5 — User Interface, live chat, execution logs và transcript.
- Thực hiện bonus: hơn 3 tool mới, mỗi tool có tối thiểu 3 unit test.
- Tổng hợp và kiểm tra integration giữa UI, agent loop và tool registry.

## 3. Đóng góp cụ thể

### CP5 — User Interface

- Tạo Streamlit UI tại `starter_v0/app.py`.
- Kết nối UI với `run_model_tool_loop` hiện có, không tạo tool-calling giả ở frontend.
- Thêm box riêng `Execution Logs / Tool Calling Trace`.
- Hiển thị các event thực tế của agent:
  - `query_received`
  - `agent_started`
  - `query_analyzed`
  - `tool_selected`
  - `tool_started`
  - `tool_completed`
  - `tool_failed`
  - `final_response`
  - `agent_completed`
- Hiển thị `request_id`, timestamp, tool name, purpose, input, output, status và duration.
- Thêm sanitization để không hiển thị các field dạng API key, token, password hoặc secret.
- Sửa `chat.py` để hỗ trợ `event_sink`, request correlation và execution duration.
- Chạy live chat và lưu transcript trong `starter_v0/transcripts/`.

### Bonus — Hơn 3 tool mới

Đã tích hợp và kiểm thử 4 tool:

| Tool | Chức năng | Unit tests |
|---|---|---:|
| `wiki` | Lấy tóm tắt Wikipedia | 5 |
| `rss` | Đọc RSS/Atom feed | 4 |
| `rank_items` | Xếp hạng research items | 3 |
| `dedupe_items` | Loại bỏ research items trùng nhau | 3 |

Mỗi tool có `tool.py`, `TOOL.md`, registry entry trong `tools/__init__.py` và
declaration trong `artifacts/tools.yaml`.

## 4. Bằng chứng

- UI: [`starter_v0/app.py`](../../starter_v0/app.py)
- Execution trace: [`starter_v0/execution_trace.py`](../../starter_v0/execution_trace.py)
- Agent/chat integration: [`starter_v0/chat.py`](../../starter_v0/chat.py)
- Trace tests: [`starter_v0/tests/test_execution_trace.py`](../../starter_v0/tests/test_execution_trace.py)
- Bonus tool tests: [`starter_v0/tests/test_bonus_tools.py`](../../starter_v0/tests/test_bonus_tools.py)
- Bonus eval cases: [`starter_v0/data/eval_bonus.json`](../../starter_v0/data/eval_bonus.json)
- Group report: [`report/team/group_report.md`](group_report.md)

Kết quả kiểm thử gần nhất:

```text
99 passed, 14 skipped
```

Streamlit đã được kiểm tra khởi động thành công bằng lệnh:

```powershell
python -m streamlit run app.py --server.headless true --server.port 8510
```

Trace sanitization và Python syntax cũng đã được kiểm tra bằng unit test và
`py_compile`.

AI/công cụ đã dùng:

- Codex/AI assistant để phân tích repository, triển khai code và viết test.
- PowerShell để chạy lệnh, kiểm tra file và khởi động Streamlit.
- `pytest` để kiểm thử offline.
- `py_compile` để kiểm tra syntax.
- Streamlit để kiểm tra UI startup.

Kết quả được tự kiểm tra bằng test suite, contract test, syntax check và kiểm
tra khởi động UI thực tế; không dựa trên kết quả giả lập.

## 5. Tự đánh giá

Đã hoàn thành phần CP5 về UI, execution trace và integration với tool-calling
loop. Đã hoàn thành bonus về 4 tool mới và tối thiểu 3 unit test cho mỗi tool.

Các phần còn phụ thuộc vào nhóm là public deployment URL, thông tin commit/PR
cuối và việc hoàn thiện các báo cáo cá nhân còn lại của thành viên khác.
