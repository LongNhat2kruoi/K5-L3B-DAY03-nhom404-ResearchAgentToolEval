---
name: rss
track: bonus
kind: live_api
provider: RSS/Atom feed (URL do user cung cấp)
requires_env: []
inputs: [feed_url, limit]
outputs: [items]
side_effect: false
---
# rss

Đọc một RSS/Atom feed và trả về danh sách item chuẩn (title, url, source,
summary, date) để nối thẳng vào `format`.

Dùng khi user cung cấp URL feed hoặc muốn tin mới nhất từ một nguồn có RSS.
Không dùng khi user chỉ đưa URL bài viết (dùng `fetch`) hoặc muốn tìm kiếm
theo từ khóa (dùng `lookup` / `social_search`).
