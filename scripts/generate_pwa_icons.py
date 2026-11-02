"""Generate high-quality PWA icons for Top's Academy."""
from pathlib import Path
from PIL import Image, ImageDraw

PUBLIC_DIR = Path(__file__).resolve().parent.parent / "platform" / "public"
PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

# Brand Colors
BRAND_BLUE = (24, 101, 242)      # #1865f2
BRAND_BG = (250, 251, 252)        # #fafbfc
WHITE = (255, 255, 255)
DARK_BLUE = (15, 68, 168)         # #0f44a8

def draw_crest(draw: ImageDraw.ImageDraw, size: int, color, offset_y: float = 0, scale: float = 1.0):
    """Draw the 3-tier Top's Academy crest (viewBox 0 0 24 24 scaled)."""
    # 24x24 coordinate reference
    # Tier 1 (top): M12 2L2 7l10 5 10-5-10-5z
    # Tier 2 (middle): M2 12l10 5 10-5
    # Tier 3 (bottom): M2 17l10 5 10-5
    
    # We draw supersampled coordinates
    cx = size / 2
    cy = (size / 2) + (offset_y * size)
    
    unit = (size * 0.72 * scale) / 20.0
    
    # Top diamond/cap:
    # (12, 3) -> (21, 7.5) -> (12, 12) -> (3, 7.5)
    p_top = [
        (cx, cy - 5.5 * unit),
        (cx + 9.5 * unit, cy - 1.25 * unit),
        (cx, cy + 3.0 * unit),
        (cx - 9.5 * unit, cy - 1.25 * unit),
    ]
    draw.polygon(p_top, fill=color)
    
    # Middle chevron band:
    # (3, 11.5) -> (12, 16) -> (21, 11.5) -> (21, 13.5) -> (12, 18) -> (3, 13.5)
    p_mid = [
        (cx - 9.5 * unit, cy + 2.25 * unit),
        (cx, cy + 6.5 * unit),
        (cx + 9.5 * unit, cy + 2.25 * unit),
        (cx + 9.5 * unit, cy + 4.75 * unit),
        (cx, cy + 9.0 * unit),
        (cx - 9.5 * unit, cy + 4.75 * unit),
    ]
    draw.polygon(p_mid, fill=color)
    
    # Bottom chevron band:
    p_bot = [
        (cx - 9.5 * unit, cy + 6.75 * unit),
        (cx, cy + 11.0 * unit),
        (cx + 9.5 * unit, cy + 6.75 * unit),
        (cx + 9.5 * unit, cy + 9.25 * unit),
        (cx, cy + 13.5 * unit),
        (cx - 9.5 * unit, cy + 9.25 * unit),
    ]
    draw.polygon(p_bot, fill=color)

def generate_icon(size: int, maskable: bool = False, solid_bg: bool = False) -> Image.Image:
    # 4x Supersampling for clean anti-aliasing
    super_size = size * 4
    if solid_bg:
        img = Image.new("RGBA", (super_size, super_size), BRAND_BLUE + (255,))
        draw = ImageDraw.Draw(img)
        # Scale for safe margin: maskable needs ~65% safe zone, solid can use 70%
        scale = 0.65 if maskable else 0.72
        draw_crest(draw, super_size, WHITE, offset_y=-0.08, scale=scale)
    else:
        # Standard icon with rounded blue badge on transparent or subtle circle
        img = Image.new("RGBA", (super_size, super_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Rounded badge / squircle
        margin = super_size * 0.04
        radius = super_size * 0.22
        draw.rounded_rectangle(
            [margin, margin, super_size - margin, super_size - margin],
            radius=radius,
            fill=BRAND_BLUE + (255,),
        )
        draw_crest(draw, super_size, WHITE, offset_y=-0.08, scale=0.68)
        
    return img.resize((size, size), Image.Resampling.LANCZOS)

def main():
    print(f"Generating PWA icons in {PUBLIC_DIR}...")
    
    # 1. 192x192
    img_192 = generate_icon(192, maskable=False)
    img_192.save(PUBLIC_DIR / "pwa-192x192.png", "PNG")
    print("  -> pwa-192x192.png")
    
    # 2. 512x512
    img_512 = generate_icon(512, maskable=False)
    img_512.save(PUBLIC_DIR / "pwa-512x512.png", "PNG")
    print("  -> pwa-512x512.png")
    
    # 3. 512x512 maskable (with safe zone & solid background)
    img_maskable = generate_icon(512, maskable=True, solid_bg=True)
    img_maskable.save(PUBLIC_DIR / "pwa-maskable-512x512.png", "PNG")
    print("  -> pwa-maskable-512x512.png")
    
    # 4. Apple touch icon 180x180
    img_apple = generate_icon(180, maskable=False, solid_bg=True)
    img_apple.save(PUBLIC_DIR / "apple-touch-icon.png", "PNG")
    print("  -> apple-touch-icon.png")
    
    # 5. Favicon 64x64 / ICO
    img_fav = generate_icon(64, maskable=False)
    img_fav.save(PUBLIC_DIR / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print("  -> favicon.ico")
    
    # 6. Vector SVG
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" fill="none">
  <rect width="512" height="512" rx="112" fill="#1865f2"/>
  <path d="M256 96L64 192l192 96 192-96-192-96z" fill="#ffffff"/>
  <path d="M64 278l192 96 192-96v38l-192 96-192-96v-38z" fill="#ffffff"/>
  <path d="M64 364l192 96 192-96v38l-192 96-192-96v-38z" fill="#ffffff"/>
</svg>"""
    (PUBLIC_DIR / "icon.svg").write_text(svg_content, encoding="utf-8")
    print("  -> icon.svg")
    print("Done!")

if __name__ == "__main__":
    main()
