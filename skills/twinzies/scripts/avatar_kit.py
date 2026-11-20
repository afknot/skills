#!/usr/bin/env python3
"""Contour-line portrait kit for Twinzies twins (v3).

One-weight line portraits, no props or accessories, over abstract colour shapes.
Avatars are visual archetypes, not likenesses or evidence.

  python avatar_kit.py spec.json out.svg
  python avatar_kit.py --library <twinzies-library>    # avatars/specs.json -> avatars/<id>.svg

Spec: {"label": str, "pose": profile|three_quarter|front|down, "flip": bool,
       "hair": crop|long|curls|fringe|wisp|waves, "age": adult|older,
       "bg": 1-6, "palette": [c1,c2,c3]}   colours: terracotta sage sand blush lavender slate mustard plum
"""
import json, sys, os, math
PAPER = "#f4efe9"; INK = "#2a2623"
C = {"terracotta": "#c98a6e", "sage": "#8f9e8b", "sand": "#dccfb6", "blush": "#e9c8c3", "lavender": "#d9d1e6",
     "slate": "#a7b6bd", "mustard": "#d8b86f", "plum": "#b79aa8"}

def bg(n, p):
    a, b, c = [C[x] for x in p]
    if n == 1: return (f'<circle cx="170" cy="170" r="120" fill="{a}" opacity=".6"/><circle cx="262" cy="238" r="84" fill="{b}" opacity=".85"/>'
                       f'<rect x="318" y="40" width="14" height="150" rx="7" fill="{c}"/><rect x="342" y="70" width="14" height="150" rx="7" fill="{c}" opacity=".6"/>')
    if n == 2: return (f'<path d="M70 400 V170 C70 60 250 60 250 170 V400Z" fill="{a}" opacity=".6"/><circle cx="296" cy="120" r="58" fill="{b}" opacity=".9"/>'
                       f'<path d="M250 400 C250 330 360 330 360 400Z" fill="{c}" opacity=".8"/>')
    if n == 3: return (f'<ellipse cx="140" cy="190" rx="70" ry="150" fill="{a}" opacity=".6" transform="rotate(18 140 190)"/><ellipse cx="260" cy="210" rx="64" ry="140" fill="{b}" opacity=".7" transform="rotate(-14 260 210)"/>'
                       f'<path d="M0 330 C80 290 140 370 220 330 S340 300 400 330 V400 H0Z" fill="{c}" opacity=".7"/>')
    if n == 4: return (f'<path d="M-20 300 L300 -20 L420 100 L100 420Z" fill="{a}" opacity=".55"/><path d="M200 400 A140 140 0 0 1 400 260 V400Z" fill="{b}" opacity=".85"/>'
                       f'<circle cx="92" cy="96" r="34" fill="{c}"/>')
    if n == 5: return (f'<circle cx="200" cy="190" r="150" fill="none" stroke="{a}" stroke-width="26" opacity=".7" stroke-dasharray="520 420" transform="rotate(-30 200 190)"/>'
                       f'<path d="M270 60 C340 50 372 120 340 170 C310 210 250 190 244 140 C240 100 250 64 270 60Z" fill="{b}" opacity=".85"/><circle cx="84" cy="318" r="46" fill="{c}" opacity=".8"/>')
    return (f'<path d="M0 0 H190 A190 190 0 0 1 0 190Z" fill="{a}" opacity=".7"/><rect x="230" y="190" width="130" height="130" rx="30" fill="{b}" opacity=".8" transform="rotate(12 295 255)"/>'
            f'<rect x="196" y="230" width="100" height="100" rx="24" fill="{c}" opacity=".6" transform="rotate(-10 246 280)"/>')

def curls(cx, cy, rx, ry, n=9):
    pts = [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a))) for a in [172 + 196.0 * i / n for i in range(n + 1)]]
    d = f"M{pts[0][0]:.0f} {pts[0][1]:.0f}"
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        r = math.hypot(x1 - x0, y1 - y0) * 0.62
        d += f" A{r:.0f} {r:.0f} 0 0 1 {x1:.0f} {y1:.0f}"
    return d

# ---- poses: (lines, hair-anchor) drawn in a 400 box; flip mirrors ----
def pose_profile(age, hair):
    s = ('M246 112 C262 128 262 150 258 168 C256 176 262 184 270 196 C278 208 282 214 280 220 C276 226 270 226 266 228 '
         'C268 236 270 240 268 244 C266 248 270 250 268 254 C266 260 262 262 262 264 C266 270 266 278 258 286 C250 296 238 298 228 292 '
         'C206 296 186 280 180 252 M246 112 C200 92 150 124 150 190 C150 214 160 236 172 248 '
         'M240 196 q9 -8 18 0 q-9 5 -18 0 M236 182 q12 -7 24 -2 M184 204 c-9 -2 -11 16 -2 24 c6 4 11 0 11 -7 '
         'M228 292 C230 320 230 340 232 366 M172 248 C172 292 164 332 152 376 M70 400 C92 362 138 348 170 346 M232 360 C272 362 318 376 334 400 M260 258 q6 3 10 0')
    if age == "older": s += ' M252 202 q4 6 2 12 M244 224 q-4 6 -2 14'
    return s

def pose_three_quarter(age):
    s = ('M200 118 C170 130 160 170 166 206 C172 244 192 270 216 280 C242 278 258 248 260 208 C262 164 244 122 200 118 '
         'M178 198 q12 -9 26 0 M222 198 q10 -7 22 0 M176 182 q16 -9 32 -2 M222 180 q12 -6 24 0 '
         'M216 204 C212 224 205 232 211 238 C217 243 225 239 222 234 '
         'M196 258 C204 254 212 256 214 256 C220 256 228 254 234 260 C224 270 204 268 196 258 M198 259 C208 261 224 261 233 260 '
         'M166 208 c-8 0 -8 16 0 22 M196 276 C194 300 190 316 178 330 M236 274 C238 300 244 318 258 332 M70 400 C90 356 140 336 178 330 M258 332 C300 340 340 364 350 400')
    if age == "older": s += ' M170 194 q-6 4 -7 10 M250 196 q5 4 6 10 M182 232 q-2 8 3 14 M242 230 q2 8 -3 14 M176 160 q26 -7 56 0'
    return s

def pose_front(age):
    s = ('M168 128 C150 150 148 190 154 218 C162 252 182 276 202 282 C226 278 246 254 252 220 C258 188 254 152 236 128 '
         'M176 202 q12 -10 26 0 q-13 7 -26 0 M214 202 q12 -10 26 0 q-13 7 -26 0 '
         'M172 186 q16 -10 32 -2 M216 184 q16 -8 32 2 '
         'M208 206 C205 226 198 234 205 240 C212 244 220 240 217 236 '
         'M188 256 C198 252 207 255 210 255 C213 255 222 252 232 256 C226 270 194 270 188 256 M190 257 C200 261 220 261 231 257 '
         'M178 282 C176 300 170 314 158 326 M230 284 C232 302 240 316 254 328 M60 400 C80 360 128 338 158 326 M254 328 C296 338 340 362 352 400 '
         'M186 202 a3 3 0 1 0 6 0 a3 3 0 1 0 -6 0 M224 202 a3 3 0 1 0 6 0 a3 3 0 1 0 -6 0 M154 206 c-8 0 -8 16 0 22 M252 206 c8 0 8 16 0 22')
    return s

def pose_down(age):
    s = ('M176 126 C152 146 148 190 156 224 C166 258 184 280 206 286 C230 282 248 256 252 222 C258 186 252 150 232 126 '
         'M176 206 q12 8 26 0 M214 206 q12 8 26 0 M172 190 q16 -8 32 0 M216 190 q16 -8 32 0 '
         'M210 210 C208 228 202 238 208 243 C214 247 222 243 220 239 '
         'M192 262 C200 258 208 261 211 261 C214 261 222 258 230 262 C222 272 200 272 192 262 M193 263 C204 265 218 265 229 263 '
         'M182 288 C180 306 174 318 162 330 M230 290 C232 306 240 320 254 330 M64 400 C84 362 130 342 162 330 M254 330 C296 340 340 364 352 400')
    if age == "older": s += ' M168 200 q-6 4 -7 10 M250 200 q5 4 6 10 M180 240 q-2 8 3 14 M240 240 q2 8 -3 14'
    return s

HAIR = {
 ("profile","crop"):  'M152 190 C144 140 186 100 236 108 M162 150 C188 124 226 116 262 138 M178 132 q14 -10 30 -12 M200 126 q14 -8 30 -6',
 ("profile","fringe"):'M150 214 C140 130 192 92 238 106 C262 114 270 132 266 160 M170 130 C200 140 236 130 262 150 M190 118 C210 130 236 126 256 134',
 ("three_quarter","long"): 'M200 112 C148 110 124 172 132 242 C138 302 126 342 110 384 M200 112 C252 108 286 160 280 230 C276 280 292 330 302 378 M170 128 C150 190 152 250 140 304 M232 120 C264 160 264 220 272 272 M200 112 C186 128 176 144 170 160',
 ("three_quarter","wisp"): 'M168 170 C160 130 180 106 208 104 C234 102 252 122 256 150 M180 116 q10 -10 24 -12 M222 106 q16 0 26 12',
 ("front","curls"): None,
 ("front","waves"):'M200 106 C150 104 128 160 134 220 C138 268 126 300 116 336 M200 106 C250 104 274 160 268 220 C264 268 276 300 288 336 M200 106 C182 124 170 142 160 160 M200 106 C220 124 236 140 246 160',
 ("front","crop"): 'M156 190 C142 124 180 92 210 92 C246 92 266 126 250 190 M158 144 C188 124 226 126 250 146 M170 118 q14 -8 30 -8 M214 110 q14 0 26 8 M176 134 l4 -6 M194 128 l4 -6 M214 128 l4 -6 M232 132 l4 -6',
 ("down","crop"): 'M154 196 C142 128 182 94 212 94 C248 94 268 128 252 192 M156 150 C186 130 226 130 252 150 M172 120 q14 -8 30 -8 M214 112 q14 0 26 8',
 ("down","waves"): 'M206 108 C152 106 130 166 136 226 C140 268 130 298 120 336 M206 108 C254 106 276 166 270 226 C266 266 276 296 286 336 M206 108 C186 128 172 148 162 168',
}

def build(spec):
    pose = spec.get("pose", "front"); hair = spec.get("hair", "crop"); age = spec.get("age", "adult")
    pal = spec.get("palette", ["sand", "terracotta", "sage"])
    body = {"profile": lambda: pose_profile(age, hair), "three_quarter": lambda: pose_three_quarter(age),
            "front": lambda: pose_front(age), "down": lambda: pose_down(age)}[pose]()
    h = HAIR.get((pose, hair))
    if hair == "curls": h = curls(200, 170, 80, 78) + ' M190 110 q-8 -16 6 -22 M214 108 q10 -14 22 -8 M168 134 q-6 -14 6 -22'
    g = f'<g fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    g += f'<path d="{body}"/>' + (f'<path d="{h}"/>' if h else '') + '</g>'
    if spec.get("flip"): g = f'<g transform="translate(400 0) scale(-1 1)">{g}</g>'
    g = f'<g transform="translate(-30 -34) scale(1.16)">{g}</g>'
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" role="img" aria-label="' + spec.get("label", "Illustrated twin portrait") + '">'
            f'<rect width="400" height="400" fill="{PAPER}"/>' + bg(spec.get("bg", 1), pal) + g + '</svg>')

if __name__ == "__main__":
    if sys.argv[1] == "--library":
        lib = sys.argv[2]; specs = json.load(open(os.path.join(lib, "avatars", "specs.json")))
        for k, v in specs.items():
            open(os.path.join(lib, "avatars", k + ".svg"), "w").write(build(v)); print("wrote", k)
    else:
        open(sys.argv[2], "w").write(build(json.load(open(sys.argv[1]))))
