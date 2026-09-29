#!/usr/bin/env python3
"""
generate_banner.py
Generates a stunning 16:9 landscape banner inspired by the MMDS book cover,
featuring the iconic miner character lifting the giant glowing golden rock of data,
ambient graph network nodes, elegant typography, and compiler attribution to Ehsan Shahbazi.
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import arabic_reshaper
from bidi.algorithm import get_display

FONT_VAZIR = "/Users/ehsan/Library/Fonts/Vazirmatn-Bold.ttf"
FONT_LATIN = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_LATIN_REG = "/System/Library/Fonts/HelveticaNeue.ttc"

OUTPUT_BANNER_HD = "docs/assets/banner.png"
OUTPUT_BANNER_MD = "docs/assets/banner_social.png"
OUTPUT_BANNER_ROOT = "docs/assets/banner.jpg"

def reshape_fa(text):
    return get_display(arabic_reshaper.reshape(text))

def main():
    W, H = 1920, 1080
    print(f"Generating 16:9 landscape banner ({W}x{H})...")

    # 1. Base Gradient Canvas (Rich Purple / Lavender / Deep Midnight Violet)
    canvas = np.zeros((H, W, 3), dtype=np.float32)
    Y, X = np.ogrid[:H, :W]

    # Epicenter of the golden glow around (460, 420)
    glow_x, glow_y = 460, 420
    dist = np.sqrt(((X - glow_x)/1.3)**2 + (Y - glow_y)**2)
    norm_dist = np.clip(dist / 1100.0, 0, 1.0)

    # Color palette
    c_glow = np.array([232, 208, 246], dtype=np.float32)  # Radiant light lavender
    c_mid = np.array([125, 78, 148], dtype=np.float32)    # Cover classic violet/purple
    c_dark = np.array([20, 13, 36], dtype=np.float32)     # Deep dark indigo/navy

    for i in range(3):
        stage1 = c_glow[i] * (1 - norm_dist*1.6) + c_mid[i] * (norm_dist*1.6)
        stage2 = c_mid[i] * (1 - (norm_dist - 0.45)*2) + c_dark[i] * ((norm_dist - 0.45)*2)
        canvas[:, :, i] = np.where(norm_dist < 0.45, stage1, stage2)

    canvas = np.clip(canvas, 0, 255).astype(np.uint8)
    img = Image.fromarray(canvas)

    # 2. Add Ambient Digital Network Graphs & Nodes (Big Data theme)
    draw = ImageDraw.Draw(img, "RGBA")
    np.random.seed(42)

    node_points = []
    for _ in range(60):
        nx = int(np.random.uniform(40, W - 40))
        ny = int(np.random.uniform(40, H - 40))
        node_points.append((nx, ny))

    # Connect nearby nodes with subtle glowing lines
    for i in range(len(node_points)):
        for j in range(i + 1, len(node_points)):
            p1 = node_points[i]
            p2 = node_points[j]
            d = np.hypot(p1[0] - p2[0], p1[1] - p2[1])
            if d < 230:
                alpha = int(45 * (1.0 - d / 230.0))
                draw.line([p1, p2], fill=(215, 190, 255, alpha), width=1)

    # Draw nodes
    for nx, ny in node_points:
        radius = np.random.choice([2, 3, 4])
        alpha = np.random.randint(70, 170)
        draw.ellipse([nx - radius, ny - radius, nx + radius, ny + radius], fill=(245, 230, 255, alpha))

    # 3. Golden Volumetric Aura Behind the Golden Rock
    aura_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    aura_draw = ImageDraw.Draw(aura_layer)
    for r in range(420, 30, -20):
        alpha = int(60 * (1.0 - r / 420.0)**1.5)
        aura_draw.ellipse([glow_x - r, glow_y - r, glow_x + r, glow_y + r], fill=(255, 210, 50, alpha))
    aura_layer = aura_layer.filter(ImageFilter.GaussianBlur(35))
    img.paste(aura_layer, (0, 0), aura_layer)

    # 4. Paste the Miner Character & Golden Rock
    miner_rgba = Image.open("scratch/miner_perfect.png").convert("RGBA")
    orig_w, orig_h = miner_rgba.size
    target_h = 880
    target_w = int(orig_w * (target_h / orig_h))
    miner_resized = miner_rgba.resize((target_w, target_h), Image.Resampling.LANCZOS)

    miner_x = 70
    miner_y = 110

    # Soft drop shadow for character
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow_mask = miner_resized.split()[3]
    shadow_draw = ImageDraw.Draw(shadow)
    shadow.paste((10, 5, 20, 160), (miner_x + 18, miner_y + 24), mask=shadow_mask)
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    img.paste(shadow, (0, 0), shadow)

    # Paste character
    img.paste(miner_resized, (miner_x, miner_y), miner_resized)

    # Golden light sparkles over the rock
    sparkle_draw = ImageDraw.Draw(img, "RGBA")
    sparkles = [
        (420, 220, 8), (490, 280, 12), (380, 310, 6), (530, 210, 7), (450, 160, 10)
    ]
    for sx, sy, sr in sparkles:
        sparkle_draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 255, 240, 230))
        sparkle_draw.ellipse([sx - sr*2, sy - sr*2, sx + sr*2, sy + sr*2], fill=(255, 220, 100, 70))

    # 5. Right-Hand Information & Typography
    draw = ImageDraw.Draw(img, "RGBA")
    start_x = 760

    # Pill Badge: Reference & University
    badge_bg = (255, 255, 255, 25)
    badge_border = (255, 255, 255, 60)
    badge_x, badge_y = start_x, 150
    badge_w, badge_h = 600, 44
    draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=22, fill=badge_bg, outline=badge_border, width=1)
    
    font_badge = ImageFont.truetype(FONT_LATIN, 16)
    draw.text((badge_x + 24, badge_y + 12), "STANFORD CS246 REFERENCE  •  SBU COURSE NOTES", fill=(245, 235, 255), font=font_badge)

    # English Main Title
    font_en_title = ImageFont.truetype(FONT_LATIN, 56)
    draw.text((start_x + 2, 222), "MINING OF MASSIVE DATASETS", fill=(10, 5, 20, 180), font=font_en_title)
    draw.text((start_x, 220), "MINING OF MASSIVE DATASETS", fill=(255, 255, 255), font=font_en_title)

    # Persian Main Title
    font_fa_title = ImageFont.truetype(FONT_VAZIR, 52)
    fa_title_text = reshape_fa("مبانی و الگوریتم‌های کلان‌داده")
    draw.text((start_x + 2, 307), fa_title_text, fill=(10, 5, 20, 180), font=font_fa_title)
    draw.text((start_x, 305), fa_title_text, fill=(255, 215, 64), font=font_fa_title)

    # Subtitle Dual Language
    font_sub_en = ImageFont.truetype(FONT_LATIN_REG, 22)
    draw.text((start_x, 395), "Foundations, Scalable Algorithms & Distributed Architectures", fill=(225, 215, 245), font=font_sub_en)

    font_sub_fa = ImageFont.truetype(FONT_VAZIR, 22)
    fa_sub_text = reshape_fa("درسنامه جامع دانشگاهی، تحلیل الگوریتم‌ها و محاسبات مقیاس‌پذیر")
    draw.text((start_x, 435), fa_sub_text, fill=(205, 195, 230), font=font_sub_fa)

    # Divider Line
    draw.line([(start_x, 495), (start_x + 950, 495)], fill=(255, 255, 255, 45), width=2)

    # Compiler Attribution Glassmorphic Box
    box_x, box_y = start_x, 530
    box_w, box_h = 960, 200
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=18, fill=(255, 255, 255, 20), outline=(255, 255, 255, 40), width=1)

    # Author Avatar circle
    avatar_x, avatar_y = box_x + 35, box_y + 40
    draw.ellipse([avatar_x, avatar_y, avatar_x + 80, avatar_y + 80], fill=(255, 200, 50, 230), outline=(255, 255, 255, 150), width=2)
    font_avatar = ImageFont.truetype(FONT_LATIN, 34)
    draw.text((avatar_x + 18, avatar_y + 20), "ES", fill=(25, 15, 45), font=font_avatar)

    # Author details
    font_author_fa = ImageFont.truetype(FONT_VAZIR, 28)
    font_author_en = ImageFont.truetype(FONT_LATIN, 20)
    font_author_sub = ImageFont.truetype(FONT_VAZIR, 18)

    fa_author = reshape_fa("گردآورنده و پژوهشگر: احسان شهبازی")
    draw.text((box_x + 140, box_y + 35), fa_author, fill=(255, 255, 255), font=font_author_fa)
    draw.text((box_x + 140, box_y + 80), "Ehsan Shahbazi  •  ehsan.shahbazipc@gmail.com", fill=(225, 215, 245), font=font_author_en)
    
    fa_inst = reshape_fa("دانشکده مهندسی و علوم کامپیوتر • دانشگاه شهید بهشتی (SBU) • پاییز و زمستان ۱۴۰۴")
    draw.text((box_x + 140, box_y + 115), fa_inst, fill=(190, 180, 215), font=font_author_sub)

    # Clean text link
    github_link = "GitHub: github.com/EhsanShahbazii/Big-Data-SBU-Course"
    draw.text((box_x + 140, box_y + 150), github_link, fill=(255, 220, 100), font=font_author_en)

    # 6. Bottom Topic Tags
    tags = [
        "MapReduce & HDFS",
        "LSH & Min-Hashing",
        "Data Streams & DGIM",
        "PageRank & Web Graph",
        "Frequent Itemsets",
        "BFR & CURE Clustering",
        "Dimensionality Reduction",
        "Large-Scale ML & SVM",
        "Deep Learning"
    ]
    font_tag = ImageFont.truetype(FONT_LATIN, 14)
    tag_x = start_x
    tag_y = 780

    for tag in tags:
        bbox = font_tag.getbbox(tag)
        tw = bbox[2] - bbox[0]
        pw = tw + 24
        ph = 36

        if tag_x + pw > start_x + 980:
            tag_x = start_x
            tag_y += 46

        draw.rounded_rectangle([tag_x, tag_y, tag_x + pw, tag_y + ph], radius=18, fill=(255, 255, 255, 18), outline=(255, 255, 255, 40), width=1)
        draw.text((tag_x + 12, tag_y + 10), tag, fill=(240, 235, 255), font=font_tag)
        tag_x += pw + 12

    # Stanford Authors Credit
    font_credit = ImageFont.truetype(FONT_LATIN_REG, 15)
    credit_text = "Based on Mining of Massive Datasets by Jure Leskovec, Anand Rajaraman, Jeffrey D. Ullman (Stanford University)"
    draw.text((start_x, 950), credit_text, fill=(185, 175, 210, 200), font=font_credit)

    # 7. Save High-Definition Outputs
    os.makedirs("docs/assets", exist_ok=True)
    img.save(OUTPUT_BANNER_HD, "PNG", quality=95)
    print(f"[OK] HD Banner saved to {OUTPUT_BANNER_HD}")

    img_social = img.resize((1280, 720), Image.Resampling.LANCZOS)
    img_social.save(OUTPUT_BANNER_MD, "PNG", quality=90)
    print(f"[OK] Social Banner saved to {OUTPUT_BANNER_MD}")

    img.convert("RGB").save(OUTPUT_BANNER_ROOT, "JPEG", quality=92)
    print(f"[OK] JPEG Banner saved to {OUTPUT_BANNER_ROOT}")

if __name__ == "__main__":
    main()
