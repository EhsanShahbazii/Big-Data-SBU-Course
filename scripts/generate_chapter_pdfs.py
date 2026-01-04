#!/usr/bin/env python3
"""
generate_chapter_pdfs.py
Extracts chapter-by-chapter standalone PDFs from BigData-Notes/main.pdf,
attaching the cover page (page 1) to each chapter and setting author metadata.
Also exports all PDFs to pdf/ and docs/pdfs/ for GitHub Pages.
"""

import os
import shutil
import fitz  # PyMuPDF

SOURCE_PDF = "BigData-Notes/main.pdf"
PDF_DIR = "pdf"
PDF_CHAPTERS_DIR = os.path.join(PDF_DIR, "chapters")
PDF_FULL_DIR = os.path.join(PDF_DIR, "full")
DOCS_PDF_DIR = "docs/pdfs"

CHAPTERS = [
    {
        "id": "00",
        "filename": "Chapter00_Preface.pdf",
        "title_fa": "پیش‌گفتار: کلان‌داده و مبانی محاسبات مقیاس‌پذیر",
        "title_en": "Preface: Big Data & Scalable Computing Fundamentals",
        "pages": (2, 4)
    },
    {
        "id": "01",
        "filename": "Chapter01_DataMining_HighDimensional.pdf",
        "title_fa": "فصل اول: داده‌کاوی و فضاهای با بعد بالا",
        "title_en": "Chapter 01: Data Mining & High-Dimensional Spaces",
        "pages": (10, 14)
    },
    {
        "id": "02",
        "filename": "Chapter02_MapReduce_HDFS.pdf",
        "title_fa": "فصل دوم: نگاشت-کاهش و پشته نرم‌افزاری پردازش توزیع‌شده",
        "title_en": "Chapter 02: MapReduce & Distributed Computing Stack",
        "pages": (15, 19)
    },
    {
        "id": "03",
        "filename": "Chapter03_Finding_Similar_Items_LSH.pdf",
        "title_fa": "فصل سوم: یافتن آیتم‌های مشابه و درهم‌سازی حساس به مکان (LSH)",
        "title_en": "Chapter 03: Finding Similar Items & Locality-Sensitive Hashing",
        "pages": (20, 26)
    },
    {
        "id": "04",
        "filename": "Chapter04_Mining_Data_Streams.pdf",
        "title_fa": "فصل چهارم: کاوش جریان‌های داده (Mining Data Streams)",
        "title_en": "Chapter 04: Mining Data Streams & Real-Time Analytics",
        "pages": (28, 35)
    },
    {
        "id": "05",
        "filename": "Chapter05_LinkAnalysis_PageRank.pdf",
        "title_fa": "فصل پنجم: تحلیل پیوندها و رتبه‌بندی وب (Link Analysis & PageRank)",
        "title_en": "Chapter 05: Link Analysis & Web PageRank",
        "pages": (36, 41)
    },
    {
        "id": "06",
        "filename": "Chapter06_Frequent_Itemsets.pdf",
        "title_fa": "فصل ششم: مجموعه‌آیتم‌های پرتکرار و قوانین انجمنی",
        "title_en": "Chapter 06: Frequent Itemsets & Association Rules",
        "pages": (42, 46)
    },
    {
        "id": "07",
        "filename": "Chapter07_Clustering_Massive_Data.pdf",
        "title_fa": "فصل هفتم: خوشه‌بندی در فضاهای با بعد بالا (BFR & CURE)",
        "title_en": "Chapter 07: High-Dimensional Clustering (BFR & CURE)",
        "pages": (48, 52)
    },
    {
        "id": "08",
        "filename": "Chapter08_Online_Advertising.pdf",
        "title_fa": "فصل هشتم: تبلیغات برخط در وب (Online Advertising & AdWords)",
        "title_en": "Chapter 08: Online Advertising & Google AdWords",
        "pages": (53, 56)
    },
    {
        "id": "09",
        "filename": "Chapter09_Recommender_Systems.pdf",
        "title_fa": "فصل نهم: سامانه‌های توصیه‌گر (Recommender Systems)",
        "title_en": "Chapter 09: Recommender Systems & Matrix Factorization",
        "pages": (57, 60)
    },
    {
        "id": "10",
        "filename": "Chapter10_Social_Network_Graphs.pdf",
        "title_fa": "فصل دهم: کاوش گراف‌های شبکه‌های اجتماعی (Social Networks)",
        "title_en": "Chapter 10: Mining Social-Network Graphs",
        "pages": (62, 65)
    },
    {
        "id": "11",
        "filename": "Chapter11_Dimensionality_Reduction.pdf",
        "title_fa": "فصل یازدهم: روش‌های کاهش بعد (SVD, PCA & CUR)",
        "title_en": "Chapter 11: Dimensionality Reduction (SVD, PCA & CUR)",
        "pages": (66, 70)
    },
    {
        "id": "12",
        "filename": "Chapter12_LargeScale_MachineLearning.pdf",
        "title_fa": "فصل دوازدهم: یادگیری ماشین در مقیاس بزرگ (SVM & SGD)",
        "title_en": "Chapter 12: Large-Scale Machine Learning (SVM & SGD)",
        "pages": (72, 75)
    },
    {
        "id": "13",
        "filename": "Chapter13_NeuralNetworks_DeepLearning.pdf",
        "title_fa": "فصل سیزدهم: شبکه‌های عصبی و یادگیری عمیق (Deep Learning)",
        "title_en": "Chapter 13: Neural Networks & Deep Learning",
        "pages": (76, 80)
    }
]

def main():
    if not os.path.exists(SOURCE_PDF):
        print(f"Error: {SOURCE_PDF} not found!")
        return

    os.makedirs(PDF_CHAPTERS_DIR, exist_ok=True)
    os.makedirs(PDF_FULL_DIR, exist_ok=True)
    os.makedirs(DOCS_PDF_DIR, exist_ok=True)

    # 1. Copy Full PDF
    full_pdf_dest = os.path.join(PDF_FULL_DIR, "BigData_Course_Notes_Full.pdf")
    docs_full_dest = os.path.join(DOCS_PDF_DIR, "BigData_Course_Notes_Full.pdf")
    shutil.copyfile(SOURCE_PDF, full_pdf_dest)
    shutil.copyfile(SOURCE_PDF, docs_full_dest)
    print(f"[OK] Full PDF saved to {full_pdf_dest} and {docs_full_dest}")

    # 2. Extract Each Chapter
    src_doc = fitz.open(SOURCE_PDF)

    for ch in CHAPTERS:
        out_doc = fitz.open()

        # Page 1 is the cover (0-indexed: 0)
        out_doc.insert_pdf(src_doc, from_page=0, to_page=0)

        # Chapter pages (1-indexed converted to 0-indexed)
        start_p = ch["pages"][0] - 1
        end_p = ch["pages"][1] - 1
        out_doc.insert_pdf(src_doc, from_page=start_p, to_page=end_p)

        # Metadata
        out_doc.set_metadata({
            "title": f"{ch['title_fa']} - {ch['title_en']}",
            "author": "گردآورنده: احسان شهبازی (Ehsan Shahbazi)",
            "subject": "Mining of Massive Datasets (MMDS) Big Data Notes",
            "creator": "XeLaTeX / xepersian / PyMuPDF",
            "keywords": "Big Data, MMDS, MapReduce, LSH, PageRank, Clustering, Deep Learning, احسان شهبازی"
        })

        out_path1 = os.path.join(PDF_CHAPTERS_DIR, ch["filename"])
        out_path2 = os.path.join(DOCS_PDF_DIR, ch["filename"])

        out_doc.save(out_path1, deflate=True)
        out_doc.save(out_path2, deflate=True)
        out_doc.close()

        page_count = (end_p - start_p + 1) + 1  # cover + chapter pages
        size_kb = os.path.getsize(out_path1) // 1024
        print(f"[OK] {ch['filename']} ({page_count} pages, {size_kb} KB): {ch['title_fa']}")

    src_doc.close()
    print("\n=== All chapter PDFs generated successfully! ===")

if __name__ == "__main__":
    main()
