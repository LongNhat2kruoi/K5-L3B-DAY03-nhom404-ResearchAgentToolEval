# Team

## Thông tin nhóm

- Tên nhóm: `nhom404`
- Lớp: `L3B`
- Repo nhóm: `K5-L3B-DAY03-nhom404-ResearchAgentToolEval`
- URL repo: https://github.com/LongNhat2kruoi/K5-L3B-DAY03-nhom404-ResearchAgentToolEval
- Nhánh nộp: `main`
- Commit chốt: cập nhật trước khi nộp bài

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
| 1 | Phạm Nguyên Khoa | 2A202603795 | pnkvlog1508@gmail.com | `Neronmen` | CP1/CP2: setup, baseline, prompt và versioning |
| 2 | Đinh Quốc Việt | 2A202603885 | 26ai.vietdq3@vinuni.edu.vn | `KemmVSAI` | CP4: team eval và phân tích routing |
| 3 | Phạm Đức Vinh | 2A202603849 | 26ai.vinhpd@vinuni.edu.vn | `vindpd203` | CP3: tool `wiki` và unit test |
| 4 | Lê Sỹ Long Nhật | 2A202603881 | 26ai.nhatlsl@vinuni.edu.vn | `longnhat2kruoi` | Nhóm trưởng; CP5 và bonus hơn 3 tool mới |

## Phân công và đóng góp

### Phạm Nguyên Khoa — 2A202603795

- CP1: setup môi trường, `.env`, preflight, pytest và baseline `v0`.
- CP2: tối ưu `system_prompt.md`, `tools.yaml` qua `v1` → `v3` và ghi `version_log.csv`.
- Evidence: `report/team/2A202603795_PhamNguyenKhoa.md` và các run `v0`–`v3` được liệt kê trong báo cáo cá nhân.

### Đinh Quốc Việt — 2A202603885

- CP4: viết đúng 10 team eval case, gồm 5 single-turn và 5 multi-turn.
- Kiểm tra routing, arguments, boundary và multi-turn behavior.
- Evidence: `starter_v0/data/eval_group.json` và run group `v3_B_group_openrouter_20261110T195538902469.json`.

### Phạm Đức Vinh — 2A202603849

- CP3: thiết kế, triển khai và kiểm thử tool `wiki`.
- Đăng ký tool trong registry và `tools.yaml`.
- Viết 5 unit tests offline với mocked HTTP.
- Evidence: `starter_v0/tools/wiki/` và `report/team/2A202603849_PhamDucVinh.md`.

### Lê Sỹ Long Nhật — 2A202603881

- Nhóm trưởng và phụ trách CP5.
- Tạo Streamlit UI, live chat, transcript và `Execution Logs / Tool Calling Trace`.
- Tích hợp execution events với agent loop, request correlation, duration và secret sanitization.
- Thực hiện bonus hơn 3 tool mới: `wiki`, `rss`, `rank_items`, `dedupe_items`, mỗi tool có tối thiểu 3 test.
- Evidence: `report/team/2A202603881_LeSyLongNhat.md`.

## Báo cáo cá nhân

Mỗi thành viên có báo cáo tại:

```text
report/team/2A202603795_PhamNguyenKhoa.md
report/team/2A202603885_DinhQuocViet.md
report/team/2A202603849_PhamDucVinh.md
report/team/2A202603881_LeSyLongNhat.md
```
