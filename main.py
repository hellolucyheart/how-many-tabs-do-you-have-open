"""How Many Tabs Do You Have Open? entry.

Writes one number, digits only, to ``/output/entry.txt`` -- the one
path the grader reads. The gate allows UTF-8 text of 1 to 5
characters, so the program checks its own length before writing and
writes the digits with no trailing newline and nothing else in the
file.

The number is an honest count, not a magic constant: it is the size
of one real browser session, counted tab by tab. Below is the session
itself -- every open tab, grouped by the part of life it belongs to.
Read-later articles that will never be read later. Videos queued
for a evening that never comes. Docs left open mid-debug, a work
board mid-sprint, carts abandoned at the shipping step, a group chat
214 messages deep, and a Wikipedia rabbit hole that started with
"quick question" and ended at the dancing plague of 1518.

One hundred and thirty-seven tabs. Each one was opened for a reason
and none of them was ever closed, because closing a tab feels like
admitting you will never get to it -- and you might. That is the
whole confession: not a big number picked to shock, but the exact
tally of a browser that has become a second memory, kept open
because the first one is full.

The program is deterministic on purpose: the grader runs it twice,
and both runs must produce the same entry. It reads nothing from
the network, the environment, or the git history -- the tabs live in
this file, and this file alone. The count is derived, every run,
by counting the list.
"""

import os
from pathlib import Path

# One browser session, counted tab by tab. The categories add up to
# the honest total: 29 + 21 + 24 + 16 + 13 + 12 + 11 + 6 + 5 = 137.
TABS = {
    "read_later": [
        "Why We Never Finish Anything We Start",
        "The Quiet Cost of Keeping Every Tab Open",
        "How Memory Works (And Why Yours Feels Full)",
        "A 40-Year-Old Recipe for Perfect Fried Rice",
        "The Man Who Lived Alone on an Island for 30 Years",
        "What Happens to Your Brain on Too Much News",
        "The Best Mechanical Keyboards of 2026, Ranked",
        "How to Learn Anything in 20 Hours",
        "The Lost Art of Doing Nothing",
        "Why Your Sleep Schedule Is Ruining Your Mornings",
        "Inside the World's Smallest Apartment",
        "The Science of Procrastination (Read Later, Obviously)",
        "How Bees Decide Where to Live",
        "A Beginner's Guide to Sourdough That Actually Works",
        "The History of the Humble Paperclip",
        "Why We Love Sad Songs",
        "The Town That Banned Cars",
        "How to Talk to Anyone About Anything",
        "The Secret Life of Airport Luggage",
        "What Your Handwriting Says About You (Probably Nothing)",
        "The Last Lighthouse Keeper",
        "How Instant Noodles Conquered the World",
        "The Psychology of the 'Unread' Badge",
        "Why Cats Knock Things Off Tables",
        "A Field Guide to Cloud Shapes",
        "The Man Who Memorized Pi to 100,000 Digits",
        "How to Fix a Leaky Faucet Without Calling Anyone",
        "The Economics of Free Shipping",
        "Why Do We Dream About Falling?",
    ],
    "youtube": [
        "I Lived on $1 a Day for 30 Days",
        "The Untold History of the QWERTY Keyboard",
        "Lo-fi Beats to Open Tabs To",
        "How SpaceX Catches a Rocket With Chopsticks",
        "Every Chess Opening Explained in 12 Minutes",
        "The World's Most Isolated House",
        "I Tried Morning Routines of Billionaires",
        "Why Airplanes Board Back to Front (Sometimes)",
        "The Sound of Rain on a Tin Roof - 10 Hours",
        "How Movies Fake Rain",
        "The Man Who Built a Log Cabin Alone",
        "What If the Moon Disappeared Tomorrow?",
        "I Ranked Every Noodle in the Supermarket",
        "The Secret Ingredient Chefs Never Tell You",
        "How Your Phone Battery Actually Dies",
        "The Greatest Comeback in Football History",
        "Why We Say 'Um' So Much",
        "Restoring a 100-Year-Old Pocket Watch",
        "The Physics of a Perfect Free Kick",
        "I Spent 24 Hours in the World's Smallest Hotel Room",
        "How Animators Draw Water",
    ],
    "docs_research": [
        "Python docs - pathlib",
        "MDN - Array.prototype.map",
        "Stack Overflow - 'Why is my loop slow?'",
        "GitHub - make.fun skill.md",
        "Wikipedia - List of cognitive biases",
        "RFC 9110 - HTTP Semantics",
        "PostgreSQL docs - Window Functions",
        "Tailwind CSS - Flexbox cheatsheet",
        "Docker docs - Multi-stage builds",
        "TypeScript Handbook - Generics",
        "React docs - useEffect, again",
        "Bash manual - Job Control",
        "SQLite docs - Query Planner",
        "Kubernetes docs - Pod Lifecycle",
        "Nginx docs - proxy_pass pitfalls",
        "OpenAPI spec - 3.1 changes",
        "Redis docs - Eviction policies",
        "CSS Tricks - Centering Things, 2026 Edition",
        "Go docs - Effective Go",
        "Rust Book - Ownership, chapter 4",
        "Vim cheatsheet (the same one, third year running)",
        "Regex101 - testing a pattern from Tuesday",
        "JSON Schema - validation keywords",
        "Linux man pages - tar flags I always forget",
    ],
    "work": [
        "Jira - board, sprint 47",
        "PR #312 - 'fix: tabs, again'",
        "CI pipeline - build #1,204 (failing)",
        "Grafana - dashboard nobody looks at",
        "Incident #88 - postmortem draft",
        "Calendar - tomorrow's 9am that could've been an email",
        "Docs - onboarding page, half-written",
        "Spreadsheet - budget v7 FINAL (2).xlsx",
        "Email - inbox (4,821 unread)",
        "Slack - #general, 37 mentions",
        "Figma - homepage redesign, v12",
        "Notion - meeting notes, March",
        "Ticket queue - the one from last month",
        "Staging env - 'works on my machine'",
        "Deploy checklist - step 3 of 9",
        "Standup notes - yesterday's, still open",
    ],
    "shopping": [
        "Cart - mechanical keyboard (3 items)",
        "Cart - 'buy later' shelf, 14 items",
        "Price tracker - headphones, down $4 since June",
        "Sneakers - size 43, sold out everywhere",
        "Wishlist - a lamp I do not need",
        "Comparison - 6 blenders, one winner",
        "Checkout - abandoned at the shipping step",
        "Coupon page - expired yesterday, obviously",
        "Review - 'is this chair worth it?' (2,314 answers)",
        "Second-hand - vintage camera, 'mint condition'",
        "Groceries - cart from last Tuesday",
        "Flight search - somewhere warm, any date",
        "Book - the sequel I haven't finished the first of",
    ],
    "social": [
        "X - timeline, scrolled to 2019 somehow",
        "X - a thread I'll 'read later'",
        "Reddit - r/whatisthisthing, top of all time",
        "Reddit - 'what's a tab hoarder's intervention?'",
        "Messages - group chat, 214 unread",
        "Messages - 'we should hang out soon' (2024)",
        "Discord - server #7, muted but open",
        "Instagram - a reel, then forty more",
        "YouTube comments - the argument I'm not in",
        "LinkedIn - 'congratulate Priya on her new role'",
        "Forum - 'solved' thread, solution on page 9",
        "Email - newsletter #312, unopened",
    ],
    "wikipedia_rabbit_hole": [
        "List of inventors killed by their own inventions",
        "The Voynich manuscript",
        "Time travel in fiction",
        "The great molasses flood of 1919",
        "List of unusual deaths in the 21st century",
        "The phantom time hypothesis",
        "Bloop (the sound, not the fish)",
        "The dancing plague of 1518",
        "Library of Alexandria",
        "The man who sued himself",
        "Eternal return (and why I'm still here)",
    ],
    "music_podcasts": [
        "Playlist - 'songs to close tabs to'",
        "Podcast - episode 214, 38 minutes in",
        "Podcast - 'the one about tab hoarding'",
        "Album - full discography, track 3",
        "Radio - a station from another country",
        "Lyrics - the song stuck in my head since Tuesday",
    ],
    "bills_banking": [
        "Electric bill - due Friday, tab opened Monday",
        "Bank - statement, page 2 of 9",
        "Insurance - renewal quote, unread",
        "Subscription audit - 'you pay for how many?'",
        "Tax form - 'I'll do it this weekend'",
    ],
}

OUTPUT_PATH = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.txt"
MAX_CHARS = 5


def count_open_tabs() -> int:
    """Count every tab in the session, group by group."""
    return sum(len(tabs) for tabs in TABS.values())


def main() -> None:
    count = count_open_tabs()
    text = str(count)
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(f"entry must be 1-{MAX_CHARS} characters, got {len(text)}")
    if not text.isdigit():
        raise ValueError(f"entry must be digits only, got {text!r}")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    print(f"open tabs: {count} -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
