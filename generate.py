import os
import zipfile
from PIL import Image, ImageDraw, ImageFont

RATIOS = {
    "2x3_ratio": (7200, 10800),
    "3x4_ratio": (5400, 7200),
    "4x5_ratio": (4800, 6000),
    "ISO_paper": (7016, 9933),
    "11x14_ratio": (3300, 4200)
}

BG_COLOR = "#F4F1EA"
TEXT_COLOR = "#1A1A1A"
SUBTEXT_COLOR = "#666666"

def build_single_pack(title_text, subtitle_text, output_dir="dist"):
    os.makedirs(output_dir, exist_ok=True)
    temp_files = []

    for ratio_name, (width, height) in RATIOS.items():
        img = Image.new("RGB", (width, height), color=BG_COLOR)
        draw = ImageDraw.Draw(img)

        font_size = int(width * 0.075)
        sub_font_size = int(width * 0.022)

        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        try:
            main_font = ImageFont.truetype(font_path, font_size)
            sub_font = ImageFont.truetype(font_path, sub_font_size)
        except Exception:
            main_font = ImageFont.load_default()
            sub_font = ImageFont.load_default()

        bbox_main = draw.textbbox((0, 0), title_text, font=main_font)
        text_w = bbox_main[2] - bbox_main[0]
        text_h = bbox_main[3] - bbox_main[1]

        main_x = (width - text_w) / 2
        main_y = (height - text_h) / 2 - (sub_font_size * 2)
        draw.text((main_x, main_y), title_text, fill=TEXT_COLOR, font=main_font)

        if subtitle_text:
            bbox_sub = draw.textbbox((0, 0), subtitle_text, font=sub_font)
            sub_w = bbox_sub[2] - bbox_sub[0]
            sub_x = (width - sub_w) / 2
            sub_y = main_y + text_h + int(sub_font_size * 1.5)
            draw.text((sub_x, sub_y), subtitle_text, fill=SUBTEXT_COLOR, font=sub_font)

        file_name = f"{ratio_name}.jpg"
        img.save(file_name, "JPEG", quality=95, dpi=(300, 300))
        temp_files.append(file_name)

    safe_title = "".join(c for c in title_text if c.isalnum() or c in (' ', '_')).rstrip().replace(' ', '_')
    zip_path = os.path.join(output_dir, f"{safe_title}_Pack.zip")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for f in temp_files:
            zipf.write(f, f)
            os.remove(f)

    print(f"[Done] Generated: {zip_path}")

def run():
    if not os.path.exists("quotes.txt"):
        print("[!] quotes.txt not found")
        return

    with open("quotes.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    for line in lines:
        parts = line.split("|")
        title = parts[0].strip()
        sub = parts[1].strip() if len(parts) > 1 else ""
        build_single_pack(title, sub)

if __name__ == "__main__":
    run()
