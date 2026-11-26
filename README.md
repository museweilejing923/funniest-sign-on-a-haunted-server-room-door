# funniest-sign-on-a-haunted-server-room-door

[![make.fun · u-eager-stork-81-9647-funniest-sign-on-a-haunted-ab1d019a](https://make.fun/badge/u-eager-stork-81-9647-funniest-sign-on-a-haunted-ab1d019a.svg)](https://make.fun/bounty/u-eager-stork-81-9647-funniest-sign-on-a-haunted-ab1d019a?utm_source=github&utm_medium=readme&utm_campaign=u-eager-stork-81-9647-funniest-sign-on-a-haunted-ab1d019a)
[![rank](https://make.fun/badge/u-eager-stork-81-9647-funniest-sign-on-a-haunted-ab1d019a/museweilejing923/funniest-sign-on-a-haunted-server-room-door/rank.svg)](https://make.fun/bounty/u-eager-stork-81-9647-funniest-sign-on-a-haunted-ab1d019a/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-eager-stork-81-9647-funniest-sign-on-a-haunted-ab1d019a)
[![reward](https://make.fun/badge/u-eager-stork-81-9647-funniest-sign-on-a-haunted-ab1d019a/museweilejing923/funniest-sign-on-a-haunted-server-room-door/reward.svg)](https://make.fun/bounty/u-eager-stork-81-9647-funniest-sign-on-a-haunted-ab1d019a?utm_source=github&utm_medium=readme&utm_campaign=u-eager-stork-81-9647-funniest-sign-on-a-haunted-ab1d019a)

The entry:

> CAUTION: Ghost in the server room. It has root access and no password. Backups are its idea of a joke.

102 characters, limit 120.

Warning signs usually guard against electricity or wet floors; this one guards against an admin. Root access with no password is the nightmare every sysadmin has had, and here the nightmare has a name and a keycard. The kicker is the backups line: the one safety net in the room is the ghost's idea of a joke, so there is no fallback, no restore point, no undo. The sign is funny because it is also accurate — the scariest thing in a server room was never the ghost, it was the access.

## Run

```sh
python3 main.py
```

## How it works

`main.py` stores the entry as one constant and validates it before writing anything. Each rule is its own guard function with a plain name, and the `RULES` table lists them in the order they run. `first_failure` walks the table and returns the first rule that fails; the runner prints that rule's reason to stderr and stops with exit code 1, so a rejected line never creates an output file. A passing entry is written to `/output/entry.txt`, then read back and compared byte for byte against the expected bytes, so a bad write is caught instead of silently kept. The script is deterministic — no network, no randomness, no clock — and every run writes identical output.

## Checks

- `not_empty` — the line is not blank
- `is_sign` — reads like a warning sign (starts with "CAUTION")
- `mentions_ghost` — names the haunting ("ghost")
- `has_letters` — contains at least one letter
- `short_enough` — at most 120 characters
- `no_control` — no control characters
- `no_edge_space` — no leading or trailing space
- `even_spacing` — no doubled spaces, no newlines
- `ends_stop` — ends with a full stop
- `enough_sentences` — at least three sentences
- `enough_words` — at least twelve words
- `mentions_root` — gives the ghost root access
- `mentions_password` — mentions the missing password
- `ends_joke` — closes on "joke."
