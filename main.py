#!/usr/bin/env python3
"""Funniest Sign on a Haunted Server Room Door: read before entering."""

import os
import sys

ENTRY = "CAUTION: Ghost in the server room. It has root access and no password. Backups are its idea of a joke."
MAX_LEN = 120
OUT_PATH = "/output/entry.txt"
ENCODING = "utf-8"
EXIT_REJECTED = 1
SENTENCE_FLOOR = 3
WORD_FLOOR = 12


def format_problem(name, message):
    """Build the single line printed when a rule fails."""
    return f"rejected: {name}: {message}"


def reject(problem):
    """Print the rejection to stderr and exit with status 1."""
    print(f"rejected: {problem}", file=sys.stderr)
    raise SystemExit(EXIT_REJECTED)


def _clean_words(line):
    """Split the line into lowercase words without punctuation."""
    words = []
    for raw in line.split():
        cleaned = raw.strip(".,!?;:'\"()").lower()
        if cleaned:
            words.append(cleaned)
    return words


def _has_word(line, wanted):
    """True when one of the wanted words appears as a whole word."""
    return wanted in _clean_words(line)


def guard_not_empty(line):
    """The line must contain something besides whitespace."""
    return line.strip() != ""


def guard_short_enough(line):
    """The line must fit inside the 120-character limit."""
    return len(line) <= MAX_LEN


def guard_has_letters(line):
    """The line must contain at least one letter."""
    for ch in line:
        if ch.isalpha():
            return True
    return False


def guard_no_control(line):
    """No character may be a control character."""
    return not any(ord(ch) < 32 for ch in line)


def guard_no_edge_space(line):
    """No leading or trailing space is allowed."""
    return line.strip() == line


def guard_even_spacing(line):
    """No doubled spaces and no embedded newlines."""
    return line.find("  ") == -1 and line.count("\n") == 0


def guard_ends_stop(line):
    """The line must end with a full stop."""
    return line.rstrip()[-1:] == "."


def guard_is_sign(line):
    """It has to read like a warning sign."""
    return line.startswith("CAUTION")


def guard_mentions_ghost(line):
    """The sign has to name the haunting."""
    return "ghost" in line.lower()


def guard_enough_sentences(line):
    """A real sign needs at least three sentences."""
    return line.count(".") >= SENTENCE_FLOOR


def guard_enough_words(line):
    """A real sign needs at least twelve words."""
    return len(_clean_words(line)) >= WORD_FLOOR


def guard_mentions_root(line):
    """The ghost has to hold root access."""
    return "root" in line.lower()


def guard_mentions_password(line):
    """The sign has to mention the missing password."""
    return "password" in line.lower()


def guard_ends_joke(line):
    """The punchline has to close on 'joke.'."""
    return line.rstrip().lower().endswith("joke.")


RULES = [
    ("not_empty", guard_not_empty, "entry is empty"),
    ("is_sign", guard_is_sign, "entry must read like a warning sign"),
    ("mentions_ghost", guard_mentions_ghost, "entry must name the haunting"),
    ("has_letters", guard_has_letters, "entry has no letters"),
    ("short_enough", guard_short_enough, "entry is longer than the limit"),
    ("no_control", guard_no_control, "entry has control characters"),
    ("no_edge_space", guard_no_edge_space, "entry has leading or trailing space"),
    ("even_spacing", guard_even_spacing, "entry has ragged spacing"),
    ("ends_stop", guard_ends_stop, "entry must end with a full stop"),
    ("enough_sentences", guard_enough_sentences, "entry needs at least three sentences"),
    ("enough_words", guard_enough_words, "entry needs at least twelve words"),
    ("mentions_root", guard_mentions_root, "entry must give the ghost root access"),
    ("mentions_password", guard_mentions_password, "entry must mention the missing password"),
    ("ends_joke", guard_ends_joke, "entry must close on 'joke.'"),
]


def first_failure(line):
    """Return the first failing rule as (name, message), or None."""
    for name, guard, message in RULES:
        if not guard(line):
            return (name, message)
    return None


def check_entry(line):
    """Walk the rule table; the first failure rejects the entry."""
    failed = first_failure(line)
    if failed is not None:
        name, message = failed
        print(format_problem(name, message), file=sys.stderr)
        raise SystemExit(EXIT_REJECTED)


def expected_bytes():
    """The exact bytes the output file must contain."""
    return (ENTRY + "\n").encode(ENCODING)


def write_output():
    """Create the output folder if needed and write the entry."""
    folder = os.path.dirname(OUT_PATH)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(OUT_PATH, "w", encoding=ENCODING) as handle:
        handle.write(ENTRY + "\n")


def verify_output():
    """Re-read the output and reject the run if it differs."""
    with open(OUT_PATH, "rb") as handle:
        written = handle.read()
    if written != expected_bytes():
        reject("output_mismatch: written bytes differ from entry")


def emit_entry():
    """Validate the fixed entry, write it, and verify the bytes."""
    check_entry(ENTRY)
    write_output()
    verify_output()


def main():
    """Entry point: validate, then emit."""
    emit_entry()


if __name__ == "__main__":
    main()
