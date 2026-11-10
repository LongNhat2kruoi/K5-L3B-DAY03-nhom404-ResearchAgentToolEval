# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm:
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: OpenRouter — `openai/gpt-4o-mini` (preflight pass)

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Ví dụ: "Research agent: tìm tin theo từ khóa / theo tài khoản, đọc URL, tổng hợp thành digest, và gửi lên Telegram khi được xác nhận."

**Cách chạy UI:**

> Lệnh chạy UI (ví dụ `streamlit run app.py`) và dependency đã thêm vào `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL:

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
|  |  |  |
|  |  |  |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.
2.
3.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

- `system_prompt.md` (v1): bỏ 3 lệnh xấu của starter (đoán thay vì hỏi, gửi ngay không xác nhận, ép một bước); thêm rule out-of-scope (không gọi tool cho câu ngoài research), clarify khi thiếu screenname/URL, chỉ gửi Telegram sau khi user xác nhận, cho phép gọi nhiều tool cho request đa nguồn.
- `tools.yaml` (v2): viết lại description mọi tool theo cấu trúc "làm gì — khi nào dùng — khi nào KHÔNG dùng"; ghi rõ convention args (screenname không có @, lookup.query là từ khóa gốc, topic=news cho tin tức, timeframe, search_type); send bắt buộc confirmed=true.
- `system_prompt.md` (v3): thêm ví dụ few-shot cho luồng xác nhận send (clarify yes_no → send confirmed=true). Fix cuối cùng đưa base eval lên 20/20.
- Tool mới `rss` (CP3): đọc một RSS/Atom feed do user cung cấp và trả `items` chuẩn (title, url, source, summary, date) để nối thẳng vào `format`. Agent nên gọi khi user đưa URL feed hoặc xin tin mới nhất từ nguồn có RSS; không dùng cho URL bài viết đơn lẻ (`fetch`) hay tìm theo từ khóa (`lookup`).

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo hành vi gốc của starter prompt |  | case_accuracy 0.70; tool_routing 0.75; argument 0.70; multiturn 1.00 | `starter_v0/runs/v0_B_base_openrouter_20261110T174930141588.json` |
| v1 | system_prompt.md | Bỏ lệnh xấu starter + thêm rule out-of-scope / clarify / xác nhận send / multi-tool | 0.70 | 0.95 | `starter_v0/runs/v1_B_base_openrouter_20261110T182700490998.json` |
| v2 | tools.yaml | Description rõ khi nào dùng/không dùng + convention args + boundary send | 0.95 | 0.95 | `starter_v0/runs/v2_B_base_openrouter_20261110T183016897405.json` |
| v3 | system_prompt.md | Few-shot example luồng xác nhận send | 0.95 | 1.00 | `starter_v0/runs/v3_B_base_openrouter_20261110T183249782005.json` |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R08_out_of_scope | out_of_scope | `send(text="Nguyên hàm của x^2...")` | Câu hỏi toán ngoài phạm vi research nhưng agent vẫn gọi tool `send` thay vì từ chối không gọi tool | Thêm rule out-of-scope vào system prompt: câu ngoài research/news → không gọi tool |
| R10_missing_handle | missing_info | `timeline(screenname="sama")` | User không nêu account nhưng agent tự đoán handle `sama` thay vì gọi `clarify` | Rule: thiếu screenname → `clarify`, không đoán |
| R11_missing_url | missing_info | `fetch(url="https://example.com/article")` | User nói "bài này" không có link, agent bịa URL `example.com` thay vì hỏi lại | Rule: thiếu URL → `clarify` xin link |
| R12_confirm_before_send | wrong_boundary | `send(text="Bản tin này đã được đăng...")` | Gửi Telegram ngay khi user chưa xác nhận; thiếu `clarify` yes/no trước khi gửi | Boundary `send`: chỉ gửi khi `confirmed=true` sau khi user xác nhận |
| R13_parallel_web_and_tweets | wrong_tool (case) / wrong_arg_value (observed) | `lookup(query="AI news", timeframe="day")`, `social_search(query="AI", search_type="Latest")` | Đã gọi đủ 2 tool nhưng `lookup` sai args: `query` phải là `"AI"` (thừa chữ `news`) và thiếu `topic="news"` | Viết lại description `lookup` trong tools.yaml: `query` = từ khóa gốc, `topic=news` cho tin tức |
| R14_out_of_scope_coding | out_of_scope | `send(text="hàm Fibonacci...")` | Câu coding ngoài phạm vi nhưng agent gọi `send` (vừa sai scope vừa gửi nội dung lung tung) | Rule out-of-scope + boundary `send` như R08/R12 |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_rss_feed_routing | RSS URL → tool mới | `rss(feed_url=...)` | PASS |
| G02_wiki_stable_knowledge | Kiến thức nền ổn định | `wiki(title="Large language model", lang="vi")` | PASS |
| G03_out_of_scope_no_tool | Coding ngoài scope | `no_tool` | PASS |
| G04_fetch_explicit_url | Đọc URL cụ thể | `fetch(url=...)` | PASS |
| G05_missing_article_url | Thiếu URL | `clarify(response_type="text")` | PASS |
| G06_multiturn_timeline_limit | Carryover account + limit | `timeline(screenname="sama", limit=3)` | PASS |
| G07_multiturn_news_timeframe | Carryover query + timeframe | `lookup(query="AI", topic="news", timeframe="day", max_results=4)` | PASS |
| G08_multiturn_social_search_type | Đổi mode social search | `social_search(query="agent evaluation", search_type="Top", limit=2)` | PASS |
| G09_multiturn_rss_limit | Carryover RSS URL + limit | `rss(feed_url=..., limit=2)` | PASS |
| G10_multiturn_fetch_url | Carryover URL sang lượt tóm tắt | `fetch(url=...)` | PASS |

Run: `starter_v0/runs/v3_B_group_openrouter_20261110T195538902469.json` — 10/10, `provider_error_cases=0`, case/routing/argument/multiturn accuracy đều 1.0.

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/rss/`) | `starter_v0/tools/rss/tool.py`, đăng ký trong `tools/__init__.py` + `artifacts/tools.yaml`, eval case `G01_rss_feed_routing` | Đọc feed RSS/Atom thật (BBC News) trả đúng items chuẩn | Chỉ đọc URL user cung cấp, không side effect, không cần API key |
| Unit test tool mới (4 test) | `pytest` output: 71 passed, 0 failed | Happy path + limit; URL thiếu scheme → ValueError và không gọi mạng; HTTP 429 → error dict; XML hỏng → ParseError dict | Tool luôn trả error dict, không raise |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: 4 test cho `rss`. Ví dụ lỗi unit test bắt được nhưng eval không bắt: model có thể truyền `feed_url` không có scheme (`"khong-phai-url"`); eval case không cover input xấu kiểu này, unit test xác nhận tool trả `ValueError` dict và không gọi mạng.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

-

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
