# Task 19 local path findings

| file | line | finding | secret | environment record | suitable to commit | recommendation |
|---|---:|---|---|---|---|---|
| `docs/spec-v3/08-review/MAC_CONTINUATION_CHECK_2026-07-29.md` | 19 | Absolute path `/Users/moff/onedrive/chatgpt/chengdu_majiang_AItrainer` | NO | YES | CONDITIONAL | Preserve only if historical environment evidence is desired; later use a separately approved documentation change to generalize it. |
| `docs/changelog.md` | 82 | Windows user-local WinGet path | NO | YES | YES_WITH_CONTEXT | Historical record; optional later username generalization. |
| `docs/changelog.md` | 94 | Windows user-local application path | NO | YES | YES_WITH_CONTEXT | Historical record; optional later username generalization. |

Public GitHub URLs and generic OneDrive references are not secrets. No existing file was modified.
