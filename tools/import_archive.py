#!/usr/bin/env python3
"""Turn the archive of the Tumblr blog into this site's _posts.

The archive is github.com/jsnhff/mechanical-turk-diaries, whose entries/*.md hold
all 357 posts with their Tumblr ids, dates and text. This reads them and writes
one file per post into _posts/, so a post's address here is its address on Tumblr:
/post/<id>/.

    python3 tools/import_archive.py ~/mechanical-turk-diaries/entries

The text is people's own words, so it is not run through a Markdown processor
that would quietly change it (curly quotes, ellipses, dashes). Each paragraph
becomes a <p>, a line break inside one becomes a <br>, and the only formatting
kept is what the Tumblr posts had: *italics*, ***bold italics*** and links.

Dates are shown as Tumblr showed them, in the blog's own timezone (US/Eastern),
which is not always the day the archive's GMT timestamp falls on.
"""
import glob
import html
import os
import re
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")


def inline(text):
    """Escape, then keep the three kinds of formatting the posts use."""
    t = html.escape(text, quote=False)
    # a link, whose text may run across a line break
    t = re.sub(
        r"\[([^\]]+)\]\(([^)\s]+)\)",
        lambda m: '<a href="%s">%s</a>' % (m.group(2), re.sub(r"\s*\n\s*", " ", m.group(1)).strip()),
        t,
    )
    t = re.sub(r"\*\*\*(?=\S)(.+?)(?<=\S)\*\*\*", r"<strong><em>\1</em></strong>", t)
    # *emphasis*: not touching a word on its left (so "f***" stays as written) and not empty
    t = re.sub(r"(?<![\w*])\*(?=[^\s*])([^*\n]+?)(?<=[^\s*])\*(?![\w*])", r"<em>\1</em>", t)
    return t


def paragraphs(body):
    out = []
    for p in re.split(r"\n\s*\n", body.strip()):
        p = p.strip("\n")
        if not p.strip():
            continue
        # a line that is only the tail of a link belongs to the line before it
        p = re.sub(r"\n(\]\([^)]+\))", r"\1", p)
        out.append("<p>%s</p>" % inline(p).replace("\n", "<br>\n"))
    return "\n".join(out)


def set_title(t):
    """A title's apostrophes and quotation marks as a typographer sets them. The words are untouched;
    the body of a story is not touched at all (its straight marks are feet and inches, which are right)."""
    t = re.sub(r"(^|[\s(\[])'(?=\w)", "\\1\u2018", t)               # an opening single quote: 'diaspora'
    t = re.sub(r"(?<=\w)'(?=\w)", "\u2019", t)                 # don't, Amazon's
    t = re.sub(r"(?<=\w)'(?=[\s.,;:!?)]|$)", "\u2019", t)       # a closing apostrophe
    t = re.sub(r'(^|[\s(\[])"', "\\1\u201c", t)                 # an opening double quote
    t = t.replace('"', "\u201d")                                   # the rest close
    return t


def ordinal_date(dt):
    # "Feb. 27 2014": the short month, a full stop, the day, the year
    return "%s. %d %d" % (dt.strftime("%b"), dt.day, dt.year)


def main(src):
    files = sorted(glob.glob(os.path.join(src, "*.md")))
    if not files:
        sys.exit("no entries in " + src)
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_posts")
    os.makedirs(here, exist_ok=True)
    for old in glob.glob(os.path.join(here, "*.html")):
        os.remove(old)
    n = 0
    for f in files:
        text = open(f, encoding="utf-8").read()
        _, fm, body = text.split("---", 2)
        meta = {}
        for k, v in re.findall(r"^(\w+): (.*)$", fm, re.M):
            meta[k] = v
        title = re.sub(r'\\(["\\])', r"\1", meta["title"][1:-1])
        title = set_title(title)
        tid = meta["id"].strip('"')
        when = datetime.strptime(meta["date"].replace(" GMT", ""), "%Y-%m-%d %H:%M:%S").replace(tzinfo=UTC)
        local = when.astimezone(ET)
        lines = body.strip().split("\n")
        assert lines[0].startswith("# "), f
        text_html = paragraphs("\n".join(lines[1:]))
        notes = int(meta.get("note_count", "0"))
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60] or tid
        name = "%s-%s.html" % (local.strftime("%Y-%m-%d"), slug)
        esc_title = title.replace("\\", "\\\\").replace('"', '\\"')
        with open(os.path.join(here, name), "w", encoding="utf-8") as out:
            out.write(
                "---\n"
                'title: "%s"\n'
                "date: %s\n"
                'tumblr_id: "%s"\n'
                "notes: %d\n"
                'shown: "%s"\n'
                'month: "%s"\n'
                "permalink: /post/%s/\n"
                "---\n%s\n" % (esc_title, when.strftime("%Y-%m-%d %H:%M:%S +0000"), tid, notes, ordinal_date(local), local.strftime("%Y-%m"), tid, text_html)
            )
        n += 1
    print("wrote %d posts" % n)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/mechanical-turk-diaries/entries"))
