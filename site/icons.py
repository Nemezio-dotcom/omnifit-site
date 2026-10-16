"""Gold line-SVG replacements for every emoji / pictograph the pages use.

build.py swaps each character below for an inline <svg class="omni-icon">
(24x24 viewBox, fill none, 1.5px gold stroke, round caps - the same style as
the hub-card icons on the territory pages). site.css sizes them at 1em so each
icon takes the font-size the emoji had. Unmapped pictographs fail the build so
a newly pasted page cannot reintroduce one unnoticed.
"""
import re

# Characters that are plain text symbols, not emoji, and stay as they are:
# check mark, ballot x and multiplication x (table ticks and CSS bullets).
KEEP = {"✓", "✗", "✕"}

# Pictographs, with an optional emoji variation selector (U+FE0F) after them.
EMOJI_RE = re.compile(
    "([\U0001F000-\U0001FAFF☀-➿⌀-⏿⭐])️?"
)

ICONS = {
    "\U0001F4CD": ('pin', '<path d="M12 21s7-6.5 7-11.5A7 7 0 0 0 5 9.5C5 14.5 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>'),
    "⭐":     ('star', '<path d="M12 3l2.6 5.6 6 .8-4.4 4.2 1.1 6-5.3-2.9-5.3 2.9 1.1-6L3.4 9.4l6-.8z"/>'),
    "★":     ('star', '<path d="M12 3l2.6 5.6 6 .8-4.4 4.2 1.1 6-5.3-2.9-5.3 2.9 1.1-6L3.4 9.4l6-.8z"/>'),
    "\U0001F3C5": ('medal', '<circle cx="12" cy="9" r="5.5"/><path d="M9 13.5L7.5 21l4.5-2.5 4.5 2.5L15 13.5"/>'),
    "\U0001F30D": ('globe', '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c3 3 3 14 0 17M12 3.5c-3 3-3 14 0 17"/>'),
    "\U0001F4CA": ('bar-chart', '<path d="M4 20h16"/><rect x="6" y="11" width="3" height="7" rx=".5"/><rect x="11" y="6" width="3" height="12" rx=".5"/><rect x="16" y="9" width="3" height="9" rx=".5"/>'),
    "\U0001F4C9": ('trend-down', '<path d="M3 7l6 6 4-4 8 8"/><path d="M15 17h6v-6"/>'),
    "\U0001F4C8": ('trend-up', '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>'),
    "\U0001F5A5": ('monitor', '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>'),
    "\U0001F534": ('circle', '<circle cx="12" cy="12" r="6"/>'),
    "\U0001F3CB": ('dumbbell', '<path d="M3 12h2M19 12h2"/><rect x="5" y="8" width="3" height="8" rx="1"/><rect x="16" y="8" width="3" height="8" rx="1"/><path d="M8 12h8"/>'),
    "\U0001F3E0": ('home', '<path d="M4 11l8-7 8 7"/><path d="M6 10v10h12V10"/><path d="M10 20v-6h4v6"/>'),
    "\U0001F3E1": ('home-garden', '<path d="M3 11l7-6 7 6"/><path d="M5 10v10h10V10"/><path d="M8 20v-5h4v5"/><path d="M19 20v-4"/><circle cx="19" cy="13" r="2.5"/>'),
    "\U0001F527": ('wrench', '<path d="M14.5 4.5a4 4 0 0 0-4.8 5.2L4 15.4V20h4.6l5.7-5.7a4 4 0 0 0 5.2-4.8l-2.8 2.8-2.4-.6-.6-2.4z"/>'),
    "\U0001F3AF": ('target', '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>'),
    "\U0001F6E1": ('shield', '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/>'),
    "\U0001F9ED": ('compass', '<circle cx="12" cy="12" r="8.5"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>'),
    "\U0001FA91": ('chair', '<path d="M7 11V5a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v6"/><path d="M5 11h14v3H5z"/><path d="M7 14v6M17 14v6"/>'),
    "\U0001F4CB": ('clipboard', '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3h6v2H9z"/><path d="M8 11h8M8 15h6"/>'),
    "\U0001F4AA": ('strength', '<path d="M6 18L18 6"/><path d="M4 14l6 6M14 4l6 6"/><path d="M3 17l4 4M17 3l4 4"/>'),
    "\U0001F393": ('graduation', '<path d="M3 9l9-4 9 4-9 4z"/><path d="M7 11v4c0 1.5 2.5 3 5 3s5-1.5 5-3v-4"/><path d="M21 9v5"/>'),
    "\U0001F52C": ('microscope', '<path d="M9 3h4v7H9z"/><path d="M11 10v4"/><path d="M7 17a5 5 0 0 0 10 0"/><path d="M5 21h14"/><path d="M13 14a4 4 0 0 1 4 3"/>'),
    "⏱":     ('stopwatch', '<circle cx="12" cy="13" r="7.5"/><path d="M12 9v4l2.5 1.5"/><path d="M10 2h4M12 2v3.5"/><path d="M18.5 6.5L20 5"/>'),
    "\U0001F9E0": ('brain', '<path d="M9.5 4a3 3 0 0 0-3 3v1a3 3 0 0 0-1.5 5.5A3 3 0 0 0 7 19h2.5V4z"/><path d="M14.5 4a3 3 0 0 1 3 3v1a3 3 0 0 1 1.5 5.5A3 3 0 0 1 17 19h-2.5V4z"/>'),
    "✈":     ('plane', '<path d="M17.8 19.2L16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>'),
    "\U0001F512": ('lock', '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>'),
    "\U0001F510": ('lock-key', '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/><circle cx="12" cy="15.5" r="1.5"/><path d="M12 17v2"/>'),
    "\U0001FA7A": ('stethoscope', '<path d="M5 4v5a5 5 0 0 0 10 0V4"/><path d="M10 14v3a4 4 0 0 0 8 0v-2"/><circle cx="18" cy="12" r="2"/>'),
    "\U0001F3C4": ('wave', '<path d="M3 13c2-2 4-2 6 0s4 2 6 0 4-2 6 0"/><path d="M3 18c2-2 4-2 6 0s4 2 6 0 4-2 6 0"/><circle cx="7" cy="6" r="2.5"/>'),
    "⏸":     ('pause', '<rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/>'),
    "\U0001F4B3": ('card', '<rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 10h18"/><path d="M7 15h4"/>'),
    "\U0001F957": ('leaf', '<path d="M5 19C5 10 11 5 20 4c-1 9-6 15-15 15z"/><path d="M5 19c2-5 6-9 11-12"/>'),
    "⚖":     ('scales', '<path d="M12 4v16"/><path d="M8 20h8"/><path d="M4 8h16"/><path d="M6 8l-3 6a3 3 0 0 0 6 0z"/><path d="M18 8l-3 6a3 3 0 0 0 6 0z"/>'),
    "\U0001F4A7": ('droplet', '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>'),
    "⚡":     ('bolt', '<path d="M13 3L5 14h6l-1 7 8-11h-6z"/>'),
    "\U0001F4D0": ('ruler', '<path d="M4 20L20 4v16z"/><path d="M12 20v-3M16 20v-3M20 12h-3M20 16h-3"/>'),
    "\U0001F91D": ('handshake', '<path d="M12 11L9 8l-5 5 6 6 2-2"/><path d="M12 11l3-3 5 5-6 6-2-2"/><path d="M9 14l1.5 1.5M11 12l1.5 1.5"/>'),
    "\U0001F465": ('users', '<circle cx="9" cy="8" r="3.5"/><path d="M3 20a6 6 0 0 1 12 0"/><path d="M15.5 4.5a3.5 3.5 0 0 1 0 7"/><path d="M17 14a6 6 0 0 1 4 6"/>'),
    "\U0001F9D8": ('lotus', '<circle cx="12" cy="5" r="2.5"/><path d="M12 8v5"/><path d="M4 18c3-2 5-5 8-5s5 3 8 5"/><path d="M4 18c2 1.5 4 2 8 2s6-.5 8-2"/>'),
    "\U0001F550": ('clock', '<circle cx="12" cy="12" r="8.5"/><path d="M12 7v5l3 2"/>'),
    "⛳":     ('golf', '<path d="M8 21V4"/><path d="M8 4l9 3-9 3"/><path d="M4 21c0-1.5 2-2.5 4-2.5s4 1 4 2.5"/>'),
}


def svg(char):
    name, paths = ICONS[char]
    return f'<svg class="omni-icon omni-icon--{name}" viewBox="0 0 24 24" aria-hidden="true">{paths}</svg>'


def css_data_uri(char):
    """The same icon as a CSS url() for ::before/::after content."""
    _name, paths = ICONS[char]
    body = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%23c9a84c" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{paths}</svg>')
    body = body.replace('"', "'").replace("<", "%3C").replace(">", "%3E").replace("#", "%23")
    return f'url("data:image/svg+xml,{body}")'


class UnmappedEmoji(Exception):
    pass


def replace(text, where=""):
    """Swap every pictograph in an HTML fragment for its SVG.
    Returns (text, {char: count}). Raises on a pictograph with no icon."""
    counts = {}

    def sub(m):
        ch = m.group(1)
        if ch in KEEP:
            return m.group(0)
        if ch not in ICONS:
            raise UnmappedEmoji(f"{where}: no icon for U+{ord(ch):04X} {ch!r}")
        counts[ch] = counts.get(ch, 0) + 1
        return svg(ch)

    return EMOJI_RE.sub(sub, text), counts


def find(text):
    """Pictographs (excluding KEEP) still present in text."""
    return sorted({m.group(1) for m in EMOJI_RE.finditer(text) if m.group(1) not in KEEP})
