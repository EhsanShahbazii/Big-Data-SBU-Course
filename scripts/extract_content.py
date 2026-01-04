#!/usr/bin/env python3
"""
Helper script using PyMuPDF to inspect slide content, outlines, text, and extract images.
Usage:
    python3 scripts/extract_content.py --slide ch01-intro.pdf
    python3 scripts/extract_content.py --book ch1n.pdf
    python3 scripts/extract_content.py --summary 1
"""
import sys
import os
import argparse
import fitz  # PyMuPDF

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "raw_sources"))

def inspect_pdf(pdf_path, max_pages=None):
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return

    doc = fitz.open(pdf_path)
    print(f"=== {os.path.basename(pdf_path)}: {len(doc)} pages ===")

    # Table of contents if any
    toc = doc.get_toc()
    if toc:
        print("--- Table of Contents ---")
        for item in toc[:25]:
            indent = "  " * (item[0] - 1)
            print(f"{indent}- {item[1]} (page {item[2]})")
        print("-------------------------")

    n_pages = len(doc) if max_pages is None else min(len(doc), max_pages)
    for i in range(n_pages):
        page = doc[i]
        text = page.get_text().strip()
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        if lines:
            title = lines[0]
            print(f"[Page {i+1}] {title}")
            for l in lines[1:6]:
                print(f"    {l}")
            if len(lines) > 6:
                print(f"    ... ({len(lines)-6} more lines)")

def extract_slide_titles(pdf_path):
    doc = fitz.open(pdf_path)
    titles = []
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        if lines:
            titles.append((i + 1, lines[0]))
    return titles

def extract_images_from_page(pdf_path, page_num, out_dir):
    doc = fitz.open(pdf_path)
    if page_num > len(doc) or page_num < 1:
        print(f"Invalid page {page_num}")
        return
    page = doc[page_num - 1]
    image_list = page.get_images(full=True)
    os.makedirs(out_dir, exist_ok=True)
    print(f"Found {len(image_list)} images on page {page_num}")
    for img_idx, img in enumerate(image_list):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        image_filename = os.path.join(out_dir, f"page_{page_num}_img_{img_idx+1}.{image_ext}")
        with open(image_filename, "wb") as f:
            f.write(image_bytes)
        print(f"Saved: {image_filename}")

def main():
    parser = argparse.ArgumentParser(description="Extract slide and book content from MMDS PDFs")
    parser.add_argument("--slide", type=str, help="Filename of slide in raw_sources/slides")
    parser.add_argument("--book", type=str, help="Filename of book in raw_sources/book")
    parser.add_argument("--pages", type=int, default=15, help="Number of pages to inspect")
    parser.add_argument("--extract-img", nargs=3, metavar=("PDF_TYPE", "FILENAME", "PAGE"),
                        help="Extract images: [slide|book] [filename] [page_num]")
    args = parser.parse_args()

    if args.slide:
        pdf_path = os.path.join(BASE_DIR, "slides", args.slide)
        inspect_pdf(pdf_path, args.pages)
    elif args.book:
        pdf_path = os.path.join(BASE_DIR, "book", args.book)
        inspect_pdf(pdf_path, args.pages)
    elif args.extract_img:
        subfolder, fname, pnum = args.extract_img
        pdf_path = os.path.join(BASE_DIR, "slides" if subfolder == "slide" else "book", fname)
        out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "BigData-Notes", "figures", "extracted"))
        extract_images_from_page(pdf_path, int(pnum), out_dir)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
