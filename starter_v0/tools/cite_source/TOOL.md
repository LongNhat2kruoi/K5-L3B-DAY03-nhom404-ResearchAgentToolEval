---
name: cite_source
track: bonus
kind: local_formatter
requires_env: []
inputs: [title, url, source_type, author, date, arxiv_id]
outputs: [citation, tier, label, source_type]
side_effect: false
---
# cite_source

Builds one citation line for a source the agent already found, following
`company_policy/source-citation-policy.md`: every item needs a source URL, and the
source is tiered (1 = primary/official/paper, 2 = reputable news, 3 = social or unknown).
Tier 3 and unknown sources get the label "early signal / unverified". arXiv sources
are labelled as preprints and include the arXiv ID.

It does not fetch anything. Bad input (empty title, non-http URL, unknown
`source_type`) returns an error dict instead of raising.
