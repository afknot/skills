#!/usr/bin/env python3
"""Static accessibility scan of an HTML file. Standard library only.

  python a11y_scan.py page.html [--out findings.json]

Finds a subset of WCAG 2.2 problems detectable from markup and simple CSS. It does NOT replace
keyboard, screen reader, zoom or user testing. Each finding says what the tool can and cannot know.
"""
import json, re, sys, os
from html.parser import HTMLParser
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contrast import ratio

INTERACTIVE = {"a", "button", "input", "select", "textarea", "summary"}
GENERIC_LINK = re.compile(r"^(click here|here|read more|more|link|learn more)$", re.I)

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.f = []; self.stack = []; self.ids = {}; self.labels_for = set(); self.headings = []
        self.has_main = False; self.html_lang = None; self.title = None; self.in_title = False
        self.inputs = []; self.css = []; self.in_style = False; self.has_th = {}; self.tables = []
        self.cur = None; self.line = 0; self.viewport = None; self.inline_styles = []

    def add(self, sc, level, sev, title, detail, fix, conf="observed", ln=None, el=""):
        self.f.append({"sc": sc, "level": level, "severity": sev, "title": title, "detail": detail, "fix": fix,
                       "confidence": conf, "line": ln or self.getpos()[0], "element": el[:140]})

    def handle_starttag(self, tag, attrs):
        a = dict(attrs); ln = self.getpos()[0]; raw = f"<{tag}" + "".join(f' {k}="{v}"' if v is not None else f" {k}" for k, v in attrs) + ">"
        if tag == "html": self.html_lang = a.get("lang")
        if tag == "title": self.in_title = True
        if tag == "style": self.in_style = True
        if tag == "main" or a.get("role") == "main": self.has_main = True
        if "id" in a:
            if a["id"] in self.ids: self.add("4.1.2", "A", "major", "Duplicate id", f'id="{a["id"]}" appears more than once; labels and ARIA references can break.', "Make ids unique.", el=raw)
            self.ids[a["id"]] = ln
        if tag == "label" and a.get("for"): self.labels_for.add(a["for"])
        if re.fullmatch(r"h[1-6]", tag): self.headings.append((int(tag[1]), ln)); self.cur = {"tag": tag, "text": "", "ln": ln, "attrs": a, "kind": "heading"}
        if tag == "img":
            if "alt" not in a: self.add("1.1.1", "A", "major", "Image without alt text", "The image has no alt attribute; screen readers may read the file name.", 'Add alt text describing purpose, or alt="" if decorative.', el=raw)
            elif a.get("alt") and re.search(r"\.(png|jpe?g|gif|svg|webp)$", a["alt"], re.I): self.add("1.1.1", "A", "minor", "Alt text looks like a file name", a["alt"], "Describe the image's purpose.", el=raw)
        if tag in ("input", "select", "textarea"):
            t = a.get("type", "text").lower()
            if t not in ("hidden", "submit", "button", "reset", "image"):
                self.inputs.append({"a": a, "ln": ln, "raw": raw, "wrapped": any(s["tag"] == "label" for s in self.stack)})
            if "autocomplete" not in a and t in ("email", "tel", "password", "text") and re.search(r"(name|email|phone|address|zip|postal)", (a.get("name", "") + a.get("id", "")), re.I):
                self.add("1.3.5", "AA", "minor", "Personal data field without autocomplete", "A field that collects personal information lacks an autocomplete token.", "Add a valid autocomplete value (for example email, given-name).", conf="inferred", el=raw)
        if tag in ("button", "a", "summary") or a.get("role") in ("button", "link"):
            self.cur = {"tag": tag, "text": "", "ln": ln, "attrs": a, "raw": raw, "kind": "control"}
            if tag == "a" and a.get("href") in ("#", "") or (tag == "a" and str(a.get("href", "")).startswith("javascript:")):
                self.add("4.1.2", "A", "minor", "Link used as a button", f'href="{a.get("href")}"', "Use a <button> for actions; use real URLs for navigation.", el=raw)
        if tag in ("div", "span", "li", "td") and ("onclick" in a) and "role" not in a:
            self.add("2.1.1", "A", "major", "Clickable element is not keyboard accessible", f"<{tag}> has onclick but no role and is not focusable by default.", "Use a <button> or <a>, or add role, tabindex=0 and key handlers.", el=raw)
        if "tabindex" in a and re.fullmatch(r"[1-9]\d*", a["tabindex"] or ""):
            self.add("2.4.3", "A", "major", "Positive tabindex", f'tabindex="{a["tabindex"]}" overrides natural order.', "Use tabindex=0 or -1 and fix DOM order.", el=raw)
        if a.get("aria-hidden") == "true" and (tag in INTERACTIVE or "tabindex" in a):
            self.add("4.1.2", "A", "major", "Focusable element hidden from assistive tech", "aria-hidden=true on a focusable element.", "Remove aria-hidden or make it non-focusable.", el=raw)
        if tag == "meta" and a.get("name", "").lower() == "viewport":
            c = a.get("content", "").lower(); self.viewport = c
            if "user-scalable=no" in c or "user-scalable=0" in c or re.search(r"maximum-scale=(1(\.0)?|0?\.\d+)\b", c):
                self.add("1.4.4", "AA", "major", "Zoom is disabled", c, "Remove user-scalable=no and low maximum-scale.", el=raw)
        if tag in ("video", "audio") and "autoplay" in a: self.add("1.4.2", "A", "major", "Media autoplays", "Autoplaying media can talk over a screen reader.", "Remove autoplay or provide a pause control and no sound by default.", el=raw)
        if tag in ("marquee", "blink"): self.add("2.2.2", "A", "major", "Moving or blinking content", f"<{tag}> is obsolete and cannot be paused.", "Remove it.", el=raw)
        if tag == "iframe" and not (a.get("title") or a.get("aria-label")): self.add("4.1.2", "A", "minor", "iframe without title", "Frame has no accessible name.", "Add a title.", el=raw)
        if tag == "table": self.tables.append({"ln": ln, "th": False, "raw": raw}); 
        if tag == "th" and self.tables: self.tables[-1]["th"] = True
        if "style" in a: self.inline_styles.append((ln, a["style"], raw))
        if re.search(r"outline\s*:\s*(none|0)\b", a.get("style", "")): self.add("2.4.7", "AA", "major", "Focus outline removed inline", a["style"], "Keep a visible focus style (:focus-visible).", el=raw)
        self.stack.append({"tag": tag, "a": a, "ln": ln})

    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
        if tag == "style": self.in_style = False
        if self.cur and (tag == self.cur["tag"]):
            c = self.cur; self.cur = None; a = c["attrs"]; txt = c["text"].strip()
            name = txt or a.get("aria-label") or a.get("aria-labelledby") or a.get("title")
            if c["kind"] == "control" and not name and not c.get("img_alt"):
                self.add("4.1.2", "A", "major", "Control without an accessible name", "A button or link has no text, aria-label or labelled image.", "Add visible text or an aria-label.", ln=c["ln"], el=c["raw"])
            if c["kind"] == "control" and tag == "a" and txt and GENERIC_LINK.match(txt): self.add("2.4.4", "A", "minor", "Vague link text", f'"{txt}" does not say where it goes out of context.', "Use descriptive link text.", ln=c["ln"], el=c["raw"])
            if c["kind"] == "heading" and not txt and not a.get("aria-label"): self.add("1.3.1", "A", "minor", "Empty heading", "Heading has no text.", "Remove or fill it.", ln=c["ln"])
        if self.stack and self.stack[-1]["tag"] == tag: self.stack.pop()
        elif any(s["tag"] == tag for s in self.stack):
            while self.stack and self.stack.pop()["tag"] != tag: pass

    def handle_data(self, d):
        if self.in_title: self.title = (self.title or "") + d
        if self.in_style: self.css.append((self.getpos()[0], d))
        if self.cur is not None: self.cur["text"] += d

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.cur and tag == "img" and self.cur.get("kind") == "control": pass
        if tag in ("img",) and self.cur and self.cur["kind"] == "control" and dict(attrs).get("alt"): self.cur["img_alt"] = True
        if tag in ("img", "input", "br", "meta", "link", "hr"):
            if self.stack and self.stack[-1]["tag"] == tag: self.stack.pop()

    def finish(self):
        if not self.html_lang: self.add("3.1.1", "A", "major", "Page language not set", "The <html> element has no lang attribute.", 'Add lang="en" (or the page language).', ln=1)
        if not (self.title or "").strip(): self.add("2.4.2", "A", "minor", "Page has no title", "No <title> text.", "Add a unique, descriptive title.", ln=1)
        if not self.has_main: self.add("1.3.1", "A", "minor", "No main landmark", "No <main> element.", "Wrap the primary content in <main>.", ln=1)
        h1 = [h for h in self.headings if h[0] == 1]
        if not h1: self.add("1.3.1", "A", "minor", "No level-1 heading", "Page has no <h1>.", "Add one h1 describing the page.", ln=1)
        if len(h1) > 1: self.add("1.3.1", "A", "minor", "Multiple level-1 headings", f"{len(h1)} h1 elements.", "Use one h1 and structure the rest.", ln=h1[1][1])
        prev = 0
        for lvl, ln in self.headings:
            if prev and lvl > prev + 1: self.add("1.3.1", "A", "minor", "Heading level skipped", f"h{prev} to h{lvl}.", "Use sequential levels.", ln=ln)
            prev = lvl
        for i in self.inputs:
            a = i["a"]; named = i["wrapped"] or a.get("aria-label") or a.get("aria-labelledby") or (a.get("id") in self.labels_for) or a.get("title")
            if not named:
                sev = "major"; extra = " A placeholder is not a label." if a.get("placeholder") else ""
                self.add("3.3.2", "A", sev, "Form field without a label", "No label, aria-label or aria-labelledby." + extra, "Add a visible <label for=...>.", ln=i["ln"], el=i["raw"])
        for t in self.tables:
            if not t["th"]: self.add("1.3.1", "A", "minor", "Table without header cells", "No <th> found.", "Use <th scope> for headers, or avoid a table for layout.", conf="inferred", ln=t["ln"], el=t["raw"])
        # CSS contrast and small targets from simple rules
        css = "\n".join(c for _, c in self.css)
        for m in re.finditer(r"([^{}]+)\{([^}]*)\}", css):
            sel, body = m.group(1).strip(), m.group(2)
            fg = re.search(r"(?<![-\w])color\s*:\s*(#[0-9a-fA-F]{3,6})\b", body); bgc = re.search(r"background(?:-color)?\s*:\s*(#[0-9a-fA-F]{3,6})\b", body)
            if re.search(r"outline\s*:\s*(none|0)\b", body) and "focus" in sel and not re.search(r"(box-shadow|border|outline-color)", body):
                self.add("2.4.7", "AA", "major", "Focus style removed", f"{sel} removes the outline with no replacement.", "Provide a visible focus indicator.", conf="inferred", ln=0, el=sel)
            if fg and bgc:
                try:
                    r = ratio(fg.group(1), bgc.group(1)); fs = re.search(r"font-size\s*:\s*(\d+(?:\.\d+)?)px", body); size = float(fs.group(1)) if fs else 16
                    need = 3.0 if size >= 24 else 4.5
                    if r < need: self.add("1.4.3", "AA", "major" if r < 3 else "minor", "Low text contrast", f"{sel}: {fg.group(1)} on {bgc.group(1)} is {r:.2f}:1 (needs {need}:1).", "Darken the text or change the background.", conf="observed", ln=0, el=sel)
                except ValueError: pass
        return self.f

def scan(path):
    p = P(); p.feed(open(path, encoding="utf-8", errors="replace").read()); return p.finish()

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(__doc__)
    fs = scan(sys.argv[1]); out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
    seen = set(); uniq = []
    for f in fs:
        k = (f["title"], f["detail"], f["element"])
        if k not in seen: seen.add(k); uniq.append(f)
    for i, f in enumerate(uniq, 1): f["id"] = f"A{i}"
    if out: json.dump({"scanner": "a11y_scan.py (static markup and simple CSS only)", "findings": uniq}, open(out, "w"), indent=1)
    for f in uniq: print(f'{f["id"]:>4} {f["severity"]:<6} WCAG {f["sc"]:<6} {f["title"]}  (line {f["line"]})')
    print(f"{len(uniq)} findings. Static scan only: keyboard, screen reader, zoom and user testing still needed.")
