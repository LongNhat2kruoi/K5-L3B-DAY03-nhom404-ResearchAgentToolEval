---
name: dedupe_items
track: bonus
kind: local_formatter
requires_env: []
inputs: [items, key]
outputs: [items, removed_count]
side_effect: false
---
# dedupe_items

Removes duplicate research items by URL, title, or source. It only processes
items already supplied by the user or another tool.
