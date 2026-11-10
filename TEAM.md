# Team

## Thông tin nhóm

- Tên nhóm: nhom404
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-nhom404-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo: https://github.com/LongNhat2kruoi/K5-L3B-DAY03-nhom404-ResearchAgentToolEval
- Nhánh nộp: `main`
- Commit chốt: (cập nhật trước khi nộp bài)

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Phạm Nguyên Khoa | 2A202603795 | pnkvlog1508@gmail.com |        |         |
|   2 |        |      |       |        |         |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## Pham Nguyen Khoa-2A202603795

### Phần việc phụ trách

- CP1: setup môi trường và chạy baseline v0.
- CP2: tối ưu `artifacts/system_prompt.md` và `artifacts/tools.yaml` qua v1 → v3.

### Đóng góp cụ thể

- Chạy baseline v0 (`case_accuracy` 0.75), phân tích 5 case fail.
- Sửa prompt/tools qua 3 vòng, mỗi vòng một giả thuyết: v1 0.85, v2 0.95, v3 0.95 (còn case `M06` fail, đã ghi trong log).
- Ghi `artifacts/version_log.csv` cho v0–v3.

### Bằng chứng

- Run: `starter_v0/runs/v0_B_base_openrouter_20261110T173439967037.json`, `v1_B_base_openrouter_20261110T182009730230.json`, `v2_B_base_openrouter_20261110T182216985761.json`, `v3_B_base_openrouter_20261110T183138786948.json`.
- Log: `starter_v0/artifacts/version_log.csv`.
- Commit `dde9e4d`, `b2a76d8` trên branch `2A202603795-PhamNguyenKhoa`.
- Báo cáo cá nhân: `report/team/2A202603795_PhamNguyenKhoa.md`.

## HoVaTen-MSSV

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-
