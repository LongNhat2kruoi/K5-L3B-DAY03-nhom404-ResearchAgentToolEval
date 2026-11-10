# Báo cáo nhóm — Day 03 Research Agent Tool Eval

## 1. Thông tin nhóm

- Tên nhóm: `nhom404`
- Lớp: `L3B`
- Provider/model: OpenRouter / `openai/gpt-4o-mini`
- Repo: https://github.com/LongNhat2kruoi/K5-L3B-DAY03-nhom404-ResearchAgentToolEval
- Branch nộp: `main`
- Thành viên và phân công chi tiết: xem [`TEAM.md`](../../TEAM.md)

## 2. Mục tiêu và cách tiếp cận — Phần A

### A1. Agent làm được gì

Research Agent hỗ trợ tìm kiếm web/news, tìm social posts, đọc URL, đọc RSS,
tra cứu Wikipedia và company policy, tìm paper arXiv, format/rank/deduplicate
kết quả. Agent có khả năng hỏi lại khi thiếu thông tin và phải xin xác nhận
trước khi thực hiện action tool `send`.

**Chạy UI:**

```powershell
cd starter_v0
pip install -r requirements.txt
streamlit run app.py
```

UI local dùng URL do Streamlit in ra, thông thường là `http://localhost:8501`.
Public deployment URL: chưa triển khai, cần bổ sung trước khi nộp nếu giảng
viên yêu cầu link public.

### A2. Tool agent có

| Tool | Chức năng | Tool mới của nhóm |
|---|---|---|
| `clarify` | Hỏi lại khi thiếu thông tin hoặc cần confirmation | Không |
| `timeline` | Lấy bài đăng gần đây của một account | Không |
| `social_search` | Tìm social posts theo keyword | Không |
| `lookup` | Tìm kiếm web/news | Không |
| `fetch` | Đọc URL cụ thể | Không |
| `format` | Format các item đã có thành markdown | Không |
| `send` | Gửi Telegram sau khi user xác nhận | Không |
| `policy` | Tìm trong company policy nội bộ | Không |
| `papers` | Tìm paper trên arXiv | Không |
| `paper_text` | Tải và trích text paper arXiv | Không |
| `wiki` | Lấy summary Wikipedia cho kiến thức ổn định | Có |
| `rss` | Đọc RSS/Atom feed do user cung cấp | Có |
| `rank_items` | Xếp hạng item đã có theo score/title/source | Có |
| `dedupe_items` | Loại bỏ item trùng theo URL/title/source | Có |

### A3. Câu hỏi mẫu

1. `Tìm tin tức AI mới nhất trong hôm nay.`
2. `Show recent posts from an account.` rồi bổ sung `Use karpathy, latest 3 posts.`
3. `What is a large language model?`
4. `Read this RSS feed: https://vnexpress.net/rss/tin-moi-nhat.rss`
5. `Send this message to Telegram: Research demo is ready.`

## 3. Giải pháp

- **CP1/CP2:** Phạm Nguyên Khoa setup provider, chạy baseline và tối ưu
  `system_prompt.md`/`tools.yaml` theo từng hypothesis.
- **CP3:** Phạm Đức Vinh triển khai `wiki`, gồm validation, mapping Wikipedia
  response, error handling và 5 unit tests offline.
- **CP4:** Đinh Quốc Việt viết 10 team eval case, gồm 5 single-turn và 5
  multi-turn, đồng thời phân tích routing/arguments/boundary.
- **CP5:** Lê Sỹ Long Nhật triển khai Streamlit UI, live chat, transcript và
  execution trace gắn với tool loop thật.
- **Bonus:** Nhóm có 4 tool mới được ghi nhận trong các báo cáo cá nhân:
  `wiki`, `rss`, `rank_items`, `dedupe_items`; mỗi tool có ít nhất 3 test.

## 4. Kết quả và bằng chứng — Phần B

### B1. Version Evidence

Các số liệu dưới đây lấy theo báo cáo cá nhân của người phụ trách CP1/CP2 và
chỉ dùng run có `provider_error_cases=0` và đủ `measured_cases`.

| Version | Thay đổi | Hypothesis | Metric trước | Metric sau | Run |
|---|---|---|---:|---:|---|
| v0 | Starter baseline | Đo lỗi routing/argument/boundary ban đầu | — | `case_accuracy=0.75` | `starter_v0/runs/v0_B_base_openrouter_20261110T173439967037.json` |
| v1 | `system_prompt.md` | Bỏ hướng dẫn đoán và thêm rule `clarify` | 0.75 | 0.85 | `starter_v0/runs/v1_B_base_openrouter_20261110T182009730230.json` |
| v2 | `tools.yaml` | Mô tả rõ response type, args và tool boundary | 0.85 | 0.95 | `starter_v0/runs/v2_B_base_openrouter_20261110T182216985761.json` |
| v3 | Prompt + `send` declaration | Confirmation boundary và multi-tool rules rõ hơn | 0.95 | 0.95 | `starter_v0/runs/v3_B_base_openrouter_20261110T183138786948.json` |

`v3` còn failure `M06_switch_tool`; đây là limitation đã được ghi trong báo
cáo cá nhân và không được che giấu bằng cách bỏ case.

### B2. Failure Analysis

Các failure chính của baseline:

| Failure | Nguyên nhân | Cách xử lý |
|---|---|---|
| `R08_out_of_scope` | Model gọi tool cho yêu cầu ngoài research | Thêm out-of-scope rule vào system prompt |
| `R10_missing_handle` | Model tự đoán account | Bắt buộc dùng `clarify` khi thiếu handle |
| `R11_missing_url` | Model tự đoán URL | Bắt buộc hỏi lại URL |
| `R12_confirm_before_send` | Gửi khi chưa được xác nhận | `clarify(response_type=yes_no)` trước `send` |
| `R13_parallel_web_and_tweets` | Sai query/topic khi gọi nhiều nguồn | Viết rõ convention args trong `tools.yaml` |
| `M06_switch_tool` | Có thể giữ tool cũ sau khi user đổi nguồn | Cần thêm một vòng tối ưu rule multi-turn |

### B3. Team Eval Cases

Evidence: `starter_v0/data/eval_group.json` và run
`starter_v0/runs/v3_B_group_openrouter_20261110T195538902469.json`.

| Case | What it tests | Expected behavior | Result |
|---|---|---|---|
| `G01_rss_feed_routing` | RSS URL routing | `rss` | PASS |
| `G02_wiki_stable_knowledge` | Stable knowledge | `wiki` | PASS |
| `G03_out_of_scope_no_tool` | Out-of-scope | `no_tool` | PASS |
| `G04_fetch_explicit_url` | Specific URL | `fetch` | PASS |
| `G05_missing_article_url` | Missing URL | `clarify` | PASS |
| `G06_multiturn_timeline_limit` | Account + limit carryover | `timeline` | PASS |
| `G07_multiturn_news_timeframe` | News timeframe | `lookup` | PASS |
| `G08_multiturn_social_search_type` | Social mode correction | `social_search` | PASS |
| `G09_multiturn_rss_limit` | RSS limit carryover | `rss` | PASS |
| `G10_multiturn_fetch_url` | URL carryover | `fetch` | PASS |

Theo báo cáo CP4: 10/10 case pass, `provider_error_cases=0`, routing,
argument và multi-turn accuracy đều đạt 1.0.

### B4. Live Chat Evidence

Live chat và transcript do người phụ trách CP5 thực hiện. Evidence nằm trong:

```text
starter_v0/transcripts/*.transcript.json
```

Luồng cần thể hiện trong transcript:

1. Request research bình thường.
2. Request thiếu account/URL → `clarify` → user bổ sung thông tin.
3. Request gửi Telegram → agent hỏi confirmation trước khi gọi `send`.

### B5a. Tool mới, unit test và UI

| Hạng mục | Evidence | Kết quả |
|---|---|---|
| `wiki` | `starter_v0/tools/wiki/`, `test_tools_todo.py` | 5 test, gồm happy path, validation, 404 và HTTP error |
| `rss` | `starter_v0/tools/rss/`, `test_tools_todo.py` | 4 test, gồm mapping, URL invalid, HTTP error và XML invalid |
| `rank_items` | `starter_v0/tools/rank_items/`, `test_bonus_tools.py` | 3 test |
| `dedupe_items` | `starter_v0/tools/dedupe_items/`, `test_bonus_tools.py` | 3 test |
| UI | `starter_v0/app.py` | Streamlit UI và execution trace box |
| Trace integration | `starter_v0/execution_trace.py`, `test_execution_trace.py` | Correlated events và credential sanitization |

Kết quả test được ghi trong báo cáo cá nhân CP5:

```text
99 passed, 14 skipped
```

14 test skipped là các stub challenge cũ trong `test_tools_todo.py`; cần hoàn
thiện nếu muốn đạt bonus test challenge `0 skipped`.

### B5. Bonus Evidence

| Bonus | Evidence | Trạng thái |
|---|---|---|
| Hơn 3 tool mới | `wiki`, `rss`, `rank_items`, `dedupe_items` + unit tests | Hoàn thành |
| Telegram thật | `send` và confirmation boundary | Chưa gửi thật |
| Small Local Model | Ollama runs | Chưa thực hiện |
| Test challenge | `pytest` | Chưa đạt `0 skipped` |

### B7. Small Local Model Challenge

Chưa thực hiện. Không có run Ollama hợp lệ hoặc metric local được ghi nhận.

## 5. Khó khăn và cách xử lý

- API provider và các live tools phụ thuộc credentials trong `.env`; không đưa
  secrets vào repository.
- Kết quả model có thể dao động dù `temperature=0`; nhóm đã ghi nhận run thật
  và failure thay vì tự điều chỉnh metric.
- Tool live được unit test offline bằng `fake_http` để không gọi API thật khi
  chạy pytest.
- Public UI URL chưa được deploy; hiện cần dùng local Streamlit hoặc deploy
  bằng Cloudflare Tunnel/Streamlit Cloud trước khi nộp nếu bắt buộc.

## 6. Tổng hợp đóng góp

| Thành viên | Phần việc |
|---|---|
| Phạm Nguyên Khoa | CP1 setup, baseline, CP2 prompt/tool optimization, version log |
| Đinh Quốc Việt | CP4 team eval và phân tích routing/multi-turn |
| Phạm Đức Vinh | CP3 tool `wiki`, registry, declaration và unit tests |
| Lê Sỹ Long Nhật | Nhóm trưởng, CP5 UI/trace/transcript và bonus 4 tool |

Chi tiết được lưu trong 4 báo cáo cá nhân tại `report/team/`.

## 7. Hạn chế và hướng cải thiện

- Chạy thêm một vòng tối ưu để xử lý `M06_switch_tool`.
- Cập nhật chính xác commit cuối trước khi nộp.
- Bổ sung public demo URL.
- Hoàn thiện 14 test skip để đạt `pytest 0 failed, 0 skipped`.
- Nếu làm bonus local model, chạy ít nhất hai model Ollama và ghi B7.

## 8. Tài liệu tham khảo

- `README.md`
- `CHECKPOINTS.md`
- `RUBRIC.md`
- `RULES.md`
- `starter_v0/README.md`
- `docs/TOOL-SETUP.md`
