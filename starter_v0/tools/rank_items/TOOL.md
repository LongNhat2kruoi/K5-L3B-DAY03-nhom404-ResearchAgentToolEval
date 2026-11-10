---
name: rank_items
track: bonus
kind: local_formatter
requires_env: []
inputs: [items, sort_by, descending]
outputs: [items, item_count]
side_effect: false
---
# rank_items

Ranks items already returned by another tool. It does not fetch or search.
