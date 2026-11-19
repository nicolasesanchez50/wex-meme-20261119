"""Generate the WEX "only 4 Visa cards" meme as original artwork.

Brand-neutral on purpose: no WEX or Visa wordmark, logo, swoosh or corporate
colourway is reproduced, so the result cannot be mistaken for a real ad or
announcement. The joke lives in the caption, which names the company.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 900
BG = (18, 22, 30)
PANEL = (28, 34, 45)
INK = (240, 244, 250)
MUTED = (150, 163, 180)
ACCENT = (255, 196, 92)
CARD_EDGE = (90, 104, 124)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def center(draw, text, y, f, fill):
    w = draw.textbbox((0, 0), text, font=f)[2]
    draw.text(((W - w) / 2, y), text, font=f, fill=fill)


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# --- top: setup line -------------------------------------------------------
center(d, "WEX SHOWED US THEIR ENTIRE", 58, font(BOLD, 40), MUTED)
center(d, "PAYMENT CARD PORTFOLIO", 108, font(BOLD, 46), INK)

# --- wallet body -----------------------------------------------------------
wallet_x, wallet_y, wallet_w, wallet_h = 150, 215, 900, 380
d.rounded_rectangle(
    [wallet_x, wallet_y, wallet_x + wallet_w, wallet_y + wallet_h],
    radius=28, fill=PANEL, outline=CARD_EDGE, width=3,
)
# wallet stitching
d.rounded_rectangle(
    [wallet_x + 16, wallet_y + 16, wallet_x + wallet_w - 16, wallet_y + wallet_h - 16],
    radius=20, outline=(52, 62, 78), width=2,
)
d.text((wallet_x + 36, wallet_y + 30), "CARD SLOTS", font=font(MONO, 22), fill=MUTED)

# --- four cards, fanned slightly ------------------------------------------
card_w, card_h = 150, 210
base_y = wallet_y + 130
for i in range(4):
    x = wallet_x + 90 + i * 175
    y = base_y - i * 12
    shadow = [x + 8, y + 10, x + card_w + 8, y + card_h + 10]
    d.rounded_rectangle(shadow, radius=14, fill=(12, 16, 22))
    d.rounded_rectangle([x, y, x + card_w, y + card_h], radius=14,
                        fill=(238, 240, 244), outline=(180, 186, 196), width=2)
    # chip
    d.rounded_rectangle([x + 20, y + 34, x + 58, y + 62], radius=6, fill=(196, 162, 92))
    # stripe
    d.rectangle([x, y + 96, x + card_w, y + 112], fill=(206, 210, 218))
    # neutral card number dots
    for k in range(4):
        d.ellipse([x + 20 + k * 22, y + 140, x + 34 + k * 22, y + 154], fill=(150, 158, 170))
    d.text((x + 20, y + 172), f"CARD {i + 1}", font=font(MONO, 18), fill=(120, 128, 140))

# --- empty slots hint ------------------------------------------------------
d.text((wallet_x + 90, wallet_y + wallet_h - 46),
       "  ".join(["---- empty ----"] * 3),
       font=font(MONO, 20), fill=(74, 86, 104))

# --- punchline -------------------------------------------------------------
center(d, "That's it. That's the portfolio.", 640, font(BOLD, 52), ACCENT)
center(d, "Four. Not five. Definitely not a sixth hiding behind the gym membership.",
       712, font(REG, 30), INK)

# --- footer ----------------------------------------------------------------
center(d, "good-natured industry humour · not a factual claim · no real people depicted",
       822, font(REG, 22), MUTED)

img.save("/home/nicolas/.context/taskmarket/TSK-18R29K9F/wex-4-visa-cards.png", optimize=True)
print("saved", img.size)
