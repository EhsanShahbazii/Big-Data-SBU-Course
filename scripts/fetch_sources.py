#!/usr/bin/env python3
"""
Downloads all lecture slide PDFs and book chapters for MMDS Big Data course.
"""
import os
import urllib.request
import urllib.error

SOURCES = {
    "slides": [
        ("ch01-intro.pdf", "http://mmds.org/mmds/v2.1/ch01-intro.pdf"),
        ("ch02-mapreduce.pdf", "http://mmds.org/mmds/v2.1/ch02-mapreduce.pdf"),
        ("ch03-lsh.pdf", "http://mmds.org/mmds/v2.1/ch03-lsh.pdf"),
        ("ch04-streams1.pdf", "http://mmds.org/mmds/v2.1/ch04-streams1.pdf"),
        ("ch04-streams2.pdf", "http://mmds.org/mmds/v2.1/ch04-streams2.pdf"),
        ("ch05-linkanalysis1.pdf", "http://mmds.org/mmds/v2.1/ch05-linkanalysis1.pdf"),
        ("ch05-linkanalysis2.pdf", "http://mmds.org/mmds/v2.1/ch05-linkanalysis2.pdf"),
        ("ch06-assocrules.pdf", "http://mmds.org/mmds/v2.1/ch06-assocrules.pdf"),
        ("ch07-clustering.pdf", "http://mmds.org/mmds/v2.1/ch07-clustering.pdf"),
        ("ch08-advertising.pdf", "http://mmds.org/mmds/v2.1/ch08-advertising.pdf"),
        ("ch09-recsys1.pdf", "http://mmds.org/mmds/v2.1/ch09-recsys1.pdf"),
        ("ch09-recsys2.pdf", "http://mmds.org/mmds/v2.1/ch09-recsys2.pdf"),
        ("ch10-graphs1.pdf", "http://mmds.org/mmds/v2.1/ch10-graphs1.pdf"),
        ("ch10-graphs2.pdf", "http://mmds.org/mmds/v2.1/ch10-graphs2.pdf"),
        ("ch11-dimred.pdf", "http://mmds.org/mmds/v2.1/ch11-dimred.pdf"),
        ("ch12-ml1.pdf", "http://mmds.org/mmds/v2.1/ch12-ml1.pdf"),
        ("ch12-ml2.pdf", "http://mmds.org/mmds/v2.1/ch12-ml2.pdf"),
        ("ch13-nn.pdf", "http://mmds.org/mmds/v2.1/ch13-nn.pdf"),
        ("ch13-deeplearning.pdf", "http://mmds.org/mmds/v2.1/ch13-deeplearning.pdf"),
    ],
    "book": [
        ("preface.pdf", "http://infolab.stanford.edu/~ullman/mmds/preface.pdf"),
        ("ch1n.pdf", "http://infolab.stanford.edu/~ullman/mmds/ch1n.pdf"),
        ("ch2n.pdf", "http://infolab.stanford.edu/~ullman/mmds/ch2n.pdf"),
        ("ch3n.pdf", "http://infolab.stanford.edu/~ullman/mmds/ch3n.pdf"),
        ("ch4.pdf", "http://infolab.stanford.edu/~ullman/mmds/ch4.pdf"),
        ("ch5.pdf", "http://infolab.stanford.edu/~ullman/mmds/ch5.pdf"),
        ("ch6.pdf", "http://infolab.stanford.edu/~ullman/mmds/ch6.pdf"),
        ("ch7.pdf", "http://infolab.stanford.edu/~ullman/mmds/ch7.pdf"),
        ("ch8.pdf", "http://infolab.stanford.edu/~ullman/mmds/ch8.pdf"),
        ("ch9.pdf", "http://infolab.stanford.edu/~ullman/mmds/ch9.pdf"),
        ("ch10n.pdf", "http://infolab.stanford.edu/~ullman/mmds/ch10n.pdf"),
        ("ch11.pdf", "http://infolab.stanford.edu/~ullman/mmds/ch11.pdf"),
        ("ch12n.pdf", "http://infolab.stanford.edu/~ullman/mmds/ch12n.pdf"),
        ("ch13.pdf", "http://infolab.stanford.edu/~ullman/mmds/ch13.pdf"),
        ("indexn.pdf", "http://infolab.stanford.edu/~ullman/mmds/indexn.pdf"),
    ],
    "misc": [
        ("errata-v3.html", "http://infolab.stanford.edu/~ullman/mmds/errata-v3.html")
    ]
}

def download_file(url, target_path):
    if os.path.exists(target_path) and os.path.getsize(target_path) > 1000:
        print(f"[EXISTS] {target_path}")
        return True
    print(f"[DOWNLOADING] {url} -> {target_path}")
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        )
        with urllib.request.urlopen(req, timeout=30) as response, open(target_path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print(f"[OK] Downloaded {target_path} ({len(data)} bytes)")
        return True
    except urllib.error.HTTPError as e:
        print(f"[HTTP ERROR {e.code}] {url}")
        return False
    except Exception as e:
        print(f"[ERROR] {url}: {e}")
        return False

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "raw_sources"))
    slides_dir = os.path.join(base_dir, "slides")
    book_dir = os.path.join(base_dir, "book")
    os.makedirs(slides_dir, exist_ok=True)
    os.makedirs(book_dir, exist_ok=True)

    print("=== Downloading Slides ===")
    for fname, url in SOURCES["slides"]:
        download_file(url, os.path.join(slides_dir, fname))

    print("\n=== Downloading Book Chapters ===")
    for fname, url in SOURCES["book"]:
        download_file(url, os.path.join(book_dir, fname))

    print("\n=== Downloading Misc ===")
    for fname, url in SOURCES["misc"]:
        download_file(url, os.path.join(base_dir, fname))

if __name__ == "__main__":
    main()
