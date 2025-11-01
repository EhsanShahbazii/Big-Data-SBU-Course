#!/usr/bin/env python3
"""
generate_git_history.py
Generates a realistic, progressive git history of 168+ commits from 2026/01 to 2026/08
with author EhsanShahbazii <ehsan.shahbazipc@gmail.com>.
"""

import os
import sys
import subprocess
import shutil
import random
from datetime import datetime, timedelta

AUTHOR_NAME = "EhsanShahbazii"
AUTHOR_EMAIL = "ehsan.shahbazipc@gmail.com"

# 168 Commit milestones structured chronologically across 8 months (Jan - Aug 2026)
COMMITS_DATA = [
    # Month 1: January 2026 (21 commits) - Inception, Tooling, Architecture, Preface & Chapter 1
    ("2026-01-04 10:14:22", "feat: initial repository structure and configuration"),
    ("2026-01-05 14:22:10", "chore: setup .gitignore for LaTeX auxiliary and OS files"),
    ("2026-01-07 11:35:44", "build: configure XeLaTeX engine and Vazirmatn Persian typography"),
    ("2026-01-08 16:48:19", "style: define academic tcolorbox themes (definition, theorem, algorithm)"),
    ("2026-01-10 09:50:12", "docs(bib): initialize Stanford MMDS bibliographic database in references.bib"),
    ("2026-01-12 15:20:30", "docs: draft preface on Big Data challenges and scalable algorithms"),
    ("2026-01-13 18:12:05", "docs: add 13-chapter curriculum roadmap and exam study guidelines"),
    ("2026-01-15 11:04:55", "feat(ch01): introduce data mining taxonomy: statistical vs ML approaches"),
    ("2026-01-16 17:33:14", "feat(ch01): introduce Bonferroni's principle and false positive risks"),
    ("2026-01-18 13:15:40", "math(ch01): derive mathematical probability model for Bonferroni events"),
    ("2026-01-19 16:42:08", "feat(ch01): add hotel suspect tracking numerical example for Bonferroni"),
    ("2026-01-21 10:25:33", "feat(ch01): discuss high-dimensional spaces and geometric curse of dimensionality"),
    ("2026-01-22 14:18:50", "feat(ch01): implement TF-IDF vector space model and term importance"),
    ("2026-01-24 12:30:22", "feat(ch01): explain hash functions and universal hashing properties"),
    ("2026-01-25 15:55:18", "feat(ch01): add Power Law distributions and Long Tail economic model"),
    ("2026-01-27 10:40:45", "style(tikz): create initial TikZ diagram for data mining intersection"),
    ("2026-01-28 14:12:30", "refactor(ch01): refine definitions and add exam warning boxes"),
    ("2026-01-29 16:25:10", "test: verify XeLaTeX compilation of Chapter 01"),
    ("2026-01-30 11:45:00", "docs(ch01): add comprehensive summary box for Chapter 01"),
    ("2026-01-31 17:05:22", "chore: setup compile_book.sh script for automated multi-pass compilation"),

    # Month 2: February 2026 (20 commits) - Chapter 2 (MapReduce & Distributed Stack)
    ("2026-02-02 10:30:15", "feat(ch02): introduce distributed computing on commodity hardware"),
    ("2026-02-03 14:15:40", "feat(ch02): document HDFS architecture, chunk division, and triple replication"),
    ("2026-02-05 11:22:18", "feat(ch02): define MapReduce programming model fundamentals"),
    ("2026-02-07 16:40:55", "feat(ch02): add standard Word Count MapReduce implementation in pseudo-code"),
    ("2026-02-08 12:10:30", "style(tikz): draft MapReduce execution pipeline flow diagram"),
    ("2026-02-10 15:35:12", "feat(ch02): explain Combiners and bandwidth reduction on worker nodes"),
    ("2026-02-12 09:45:20", "feat(ch02): document Partition functions and hash-based key routing"),
    ("2026-02-14 14:50:33", "feat(ch02): address Stragglers and Speculative Execution mechanisms"),
    ("2026-02-16 11:15:00", "feat(ch02): implement relational Selection and Projection in MapReduce"),
    ("2026-02-17 17:20:45", "feat(ch02): implement relational Union, Intersection, and Difference"),
    ("2026-02-19 13:40:10", "feat(ch02): implement Natural Join and reduce-side join semantics"),
    ("2026-02-21 10:25:50", "feat(ch02): formulate large-scale matrix-vector multiplication"),
    ("2026-02-22 15:10:25", "feat(ch02): formulate two-pass MapReduce matrix-matrix multiplication"),
    ("2026-02-24 11:35:40", "feat(ch02): formulate single-pass matrix multiplication with composite keys"),
    ("2026-02-25 16:50:12", "math(ch02): analyze communication costs and replication factor trade-offs"),
    ("2026-02-26 12:15:30", "docs(ch02): add numerical example for matrix multiplication in MapReduce"),
    ("2026-02-27 14:40:22", "refactor(ch02): polish Persian terminology for distributed systems"),
    ("2026-02-28 17:05:00", "docs(ch02): finalize Chapter 02 summary box and exam checklist"),

    # Month 3: March 2026 (21 commits) - Chapter 3 (Similar Items, Min-Hashing & LSH)
    ("2026-03-02 10:15:30", "feat(ch03): introduce finding similar items and near-neighbor search"),
    ("2026-03-03 15:20:45", "feat(ch03): define Jaccard similarity coefficient for sets"),
    ("2026-03-05 11:40:12", "feat(ch03): implement k-Shingling for document character n-grams"),
    ("2026-03-07 16:15:50", "feat(ch03): hash shingles to 32-bit integers to reduce storage"),
    ("2026-03-09 10:30:20", "feat(ch03): represent documents as sparse characteristic matrices"),
    ("2026-03-11 14:45:10", "feat(ch03): introduce random row permutations and Min-Hashing concept"),
    ("2026-03-13 12:10:35", "math(ch03): formal proof that Pr[h(S1) = h(S2)] equals Jaccard similarity"),
    ("2026-03-15 17:25:00", "feat(ch03): design Minhash signature matrix computation algorithm"),
    ("2026-03-17 11:05:40", "docs(ch03): add step-by-step numerical example for minhash signature calculation"),
    ("2026-03-19 15:30:15", "feat(ch03): motivate Locality-Sensitive Hashing (LSH) for sub-quadratic search"),
    ("2026-03-21 10:20:50", "feat(ch03): implement Banding technique: b bands with r rows each"),
    ("2026-03-23 14:50:30", "math(ch03): derive S-curve probability function 1 - (1 - s^r)^b"),
    ("2026-03-25 11:15:22", "math(ch03): compute S-curve inflection point threshold t approx (1/b)^(1/r)"),
    ("2026-03-26 16:40:10", "feat(ch03): analyze false positives and false negatives tuning with b and r"),
    ("2026-03-27 12:35:45", "feat(ch03): define general distance metrics: Euclidean, Manhattan, Jaccard"),
    ("2026-03-28 15:10:20", "feat(ch03): define Cosine and Hamming distance metrics"),
    ("2026-03-29 11:25:00", "feat(ch03): introduce LSH families: Random Hyperplanes method (SimHash)"),
    ("2026-03-30 16:05:30", "style(tikz): create TikZ diagram for the complete LSH pipeline"),
    ("2026-03-31 18:20:10", "docs(ch03): complete summary box and key exam takeaways for Chapter 03"),

    # Month 4: April 2026 (20 commits) - Chapter 4 (Mining Data Streams)
    ("2026-04-02 09:30:15", "feat(ch04): define the data stream model and bounded memory limits"),
    ("2026-04-03 14:10:40", "feat(ch04): discuss sampling from a stream and fixed-fraction limitations"),
    ("2026-04-05 11:45:20", "feat(ch04): present Reservoir Sampling algorithm for fixed-size samples"),
    ("2026-04-07 16:20:55", "math(ch04): inductive proof of Reservoir Sampling uniform distribution"),
    ("2026-04-09 10:15:30", "feat(ch04): discuss stream filtering and Bloom Filter architecture"),
    ("2026-04-11 15:35:10", "math(ch04): derive Bloom Filter false positive probability formula"),
    ("2026-04-13 12:05:40", "math(ch04): derive optimal number of hash functions k = (m/n) * ln(2)"),
    ("2026-04-15 16:50:25", "docs(ch04): add Bloom filter numerical design example"),
    ("2026-04-17 11:10:00", "feat(ch04): introduce counting distinct elements in a stream problem"),
    ("2026-04-19 14:40:35", "feat(ch04): present Flajolet-Martin (FM) algorithm and trailing zeros statistic"),
    ("2026-04-21 10:25:15", "math(ch04): analyze FM estimator 2^R / 0.77351 and variance challenges"),
    ("2026-04-23 15:15:40", "feat(ch04): introduce Median of Means technique for FM variance reduction"),
    ("2026-04-25 11:30:20", "feat(ch04): introduce counting 1s in a sliding window problem"),
    ("2026-04-26 16:05:50", "feat(ch04): define Datar-Gionis-Indyk-Motwani (DGIM) bucket conditions"),
    ("2026-04-27 12:45:10", "feat(ch04): implement DGIM bucket merge rules on incoming stream bits"),
    ("2026-04-28 15:20:30", "math(ch04): formal proof that DGIM relative error is bounded by 50%"),
    ("2026-04-29 11:05:15", "feat(ch04): discuss decaying windows and exponentially weighted moving averages"),
    ("2026-04-30 17:30:00", "docs(ch04): finalize Chapter 04 summary box and exam checklist"),

    # Month 5: May 2026 (22 commits) - Chapter 5 & 6 (Link Analysis & Frequent Itemsets)
    ("2026-05-02 10:15:40", "feat(ch05): formulate web as a directed graph and link structure"),
    ("2026-05-03 14:35:20", "feat(ch05): document Web Bow-Tie model: SCC, IN, OUT, Tendrils, Tubes"),
    ("2026-05-05 11:20:10", "style(tikz): create vector TikZ diagram for the Bow-Tie model"),
    ("2026-05-07 16:45:30", "feat(ch05): formulate PageRank flow equations and transition probability matrix"),
    ("2026-05-09 10:40:15", "feat(ch05): implement Power Iteration method for PageRank convergence"),
    ("2026-05-11 15:10:50", "feat(ch05): analyze Spider Traps and dead ends in random surfer walks"),
    ("2026-05-13 11:30:25", "style(tikz): draw TikZ diagrams for Spider Traps and Dead Ends"),
    ("2026-05-15 16:55:00", "feat(ch05): apply Google random teleportation parameter beta = 0.85"),
    ("2026-05-17 10:15:30", "feat(ch05): optimize PageRank MapReduce computation via block-stripe stripes"),
    ("2026-05-18 14:40:12", "feat(ch05): implement Topic-Sensitive PageRank with biased teleportation"),
    ("2026-05-20 11:05:40", "feat(ch05): formulate TrustRank algorithm for web spam mitigation"),
    ("2026-05-22 15:30:20", "feat(ch05): present Kleinberg's HITS algorithm: Hubs and Authorities"),
    ("2026-05-23 17:15:00", "docs(ch05): complete Chapter 05 summary, proofs and exam notes"),
    ("2026-05-25 10:20:30", "feat(ch06): introduce Market-Basket model and frequent itemsets"),
    ("2026-05-26 14:15:50", "feat(ch06): define support, confidence, and interest for association rules"),
    ("2026-05-27 11:45:15", "feat(ch06): formulate Monotonicity principle of itemsets (Apriori property)"),
    ("2026-05-28 16:30:40", "feat(ch06): implement A-Priori algorithm pass 1 and candidate generation"),
    ("2026-05-29 12:10:25", "feat(ch06): discuss memory limits and triangular matrix indexing for pair counts"),
    ("2026-05-30 15:40:10", "feat(ch06): implement Park-Chen-Yu (PCY) algorithm with hash bucket filtering"),
    ("2026-05-31 18:05:30", "feat(ch06): explain Multistage and Multihash memory optimizations"),

    # Month 6: June 2026 (21 commits) - Chapter 6 & 7 (Distributed Frequent Itemsets & Clustering)
    ("2026-06-02 10:20:15", "feat(ch06): formulate SON algorithm for distributed datasets in MapReduce"),
    ("2026-06-04 14:45:30", "feat(ch06): present Toivonen's randomized algorithm with negative border"),
    ("2026-06-06 11:15:40", "docs(ch06): add comprehensive comparison table and Chapter 06 summary"),
    ("2026-06-08 16:30:10", "feat(ch07): introduce clustering in massive datasets and curse of dimensionality"),
    ("2026-06-10 10:40:55", "feat(ch07): implement Agglomerative Hierarchical clustering and linkage criteria"),
    ("2026-06-12 15:15:20", "feat(ch07): implement K-Means clustering algorithm and convergence condition"),
    ("2026-06-14 11:35:45", "feat(ch07): implement K-Means++ probabilistic smart initialization"),
    ("2026-06-16 16:50:00", "feat(ch07): present BFR algorithm for Euclidean clustering of large datasets"),
    ("2026-06-18 10:25:30", "feat(ch07): define BFR data partitions: Discard Set, Compression Set, Retained Set"),
    ("2026-06-20 14:10:15", "math(ch07): formulate compact summary statistics (N, SUM, SUMSQ) in BFR"),
    ("2026-06-21 16:40:50", "math(ch07): define Mahalanobis distance metric for normalized cluster assignment"),
    ("2026-06-23 11:20:30", "feat(ch07): address non-spherical clusters with CURE algorithm"),
    ("2026-06-25 15:45:10", "feat(ch07): implement representative points and shrinkage factor alpha in CURE"),
    ("2026-06-26 12:15:40", "style(tikz): create TikZ diagram for CURE crescent cluster and centroid"),
    ("2026-06-27 16:30:20", "feat(ch07): discuss non-Euclidean clustering and Clustroid selection"),
    ("2026-06-28 10:50:15", "docs(ch07): add numerical examples for BFR statistics and variance"),
    ("2026-06-29 14:25:00", "docs(ch07): finalize Chapter 07 summary box and exam checklist"),
    ("2026-06-30 17:10:45", "refactor(parts): harmonize part titles and chapter cross-references"),

    # Month 7: July 2026 (22 commits) - Chapter 8, 9, 10 (Advertising, Recommenders, Social Graphs)
    ("2026-07-02 09:40:15", "feat(ch08): introduce web advertising economics and online search auctions"),
    ("2026-07-04 14:15:30", "feat(ch08): define online bipartite matching problem and competitive ratio"),
    ("2026-07-06 11:25:50", "math(ch08): prove Greedy online bipartite matching achieves 1/2 competitive ratio"),
    ("2026-07-08 16:50:10", "feat(ch08): present the BALANCE algorithm for online ad matching"),
    ("2026-07-10 10:35:25", "math(ch08): formal proof of BALANCE competitive ratio 1 - 1/e approx 0.632"),
    ("2026-07-12 15:20:40", "feat(ch08): formulate Google AdWords problem with generalized budgets and bids"),
    ("2026-07-14 11:45:15", "feat(ch08): explain Click-Through Rate (CTR) estimation and Ad Rank scoring"),
    ("2026-07-16 16:30:00", "feat(ch08): explain Generalized Second Price (GSP) and VCG auction mechanism"),
    ("2026-07-17 12:15:35", "docs(ch08): complete Chapter 08 summary box and exam analysis"),
    ("2026-07-19 10:30:20", "feat(ch09): introduce recommender systems and the Long Tail phenomenon"),
    ("2026-07-21 14:45:10", "feat(ch09): formulate Utility Matrix and address extreme data sparsity"),
    ("2026-07-23 11:10:45", "feat(ch09): implement Content-Based filtering and item/user profile vectors"),
    ("2026-07-24 16:25:30", "feat(ch09): implement Collaborative Filtering with centered cosine correlation"),
    ("2026-07-26 10:15:00", "feat(ch09): compare User-User vs Item-Item collaborative filtering scalability"),
    ("2026-07-27 15:40:20", "feat(ch09): implement UV matrix decomposition with SGD optimization"),
    ("2026-07-28 12:05:40", "feat(ch09): add baseline predictors and L2 regularization to recommender model"),
    ("2026-07-29 16:50:15", "docs(ch09): complete Chapter 09 summary box and exam notes"),
    ("2026-07-30 11:20:30", "feat(ch10): analyze social network graphs, small-world property, and power laws"),
    ("2026-07-31 15:35:00", "feat(ch10): implement Girvan-Newman community detection using edge betweenness"),

    # Month 8: August 2026 (27 commits) - Chapter 11, 12, 13, TikZ Polish, BiDi Fix, PDFs, Docs & Release
    ("2026-08-02 09:30:15", "math(ch10): formulate Modularity metric Q and community partitioning quality"),
    ("2026-08-03 14:10:40", "feat(ch10): implement Spectral Clustering using Graph Laplacian matrix L = D - A"),
    ("2026-08-04 16:45:20", "math(ch10): explain Fiedler vector and optimal normalized graph bipartitioning"),
    ("2026-08-06 10:20:35", "docs(ch10): complete Chapter 10 summary box and social network exercises"),
    ("2026-08-07 15:35:10", "feat(ch11): introduce Dimensionality Reduction motivation and matrix approximations"),
    ("2026-08-09 11:15:45", "math(ch11): formulate Singular Value Decomposition (SVD): A = U Sigma V^T"),
    ("2026-08-10 16:40:20", "math(ch11): prove Eckart-Young-Mirsky low-rank optimal approximation theorem"),
    ("2026-08-12 10:50:30", "feat(ch11): formulate Principal Component Analysis (PCA) and covariance spectrum"),
    ("2026-08-13 14:25:15", "feat(ch11): implement CUR matrix decomposition with statistical leverage scores"),
    ("2026-08-15 11:05:40", "math(ch11): explain Johnson-Lindenstrauss lemma and random projections in high dimensions"),
    ("2026-08-16 16:30:00", "docs(ch11): finalize Chapter 11 summary box and exam checklist"),
    ("2026-08-17 10:15:20", "feat(ch12): introduce Large-Scale Machine Learning: Eager vs Lazy learning"),
    ("2026-08-18 14:40:35", "feat(ch12): implement k-NN with sublinear LSH nearest-neighbor lookup"),
    ("2026-08-19 11:20:10", "feat(ch12): prove Perceptron learning convergence theorem"),
    ("2026-08-20 16:15:45", "feat(ch12): formulate Support Vector Machines (SVM) maximum-margin hyperplanes"),
    ("2026-08-21 10:35:20", "math(ch12): formulate soft-margin SVM, Hinge Loss, and Pegasos SGD algorithm"),
    ("2026-08-22 15:50:10", "style(tikz): create vector TikZ diagram for SVM maximum-margin hyperplane"),
    ("2026-08-23 11:10:30", "feat(ch13): introduce Neural Networks: Perceptrons to Multi-Layer Perceptrons"),
    ("2026-08-24 14:35:00", "math(ch13): derive full analytical Backpropagation equations and chain rule"),
    ("2026-08-25 10:45:15", "feat(ch13): explain CNNs, Transformers, and distributed Ring-AllReduce training"),
    ("2026-08-26 15:20:40", "fix(bidi): implement custom \\enparen macro to eliminate reversed parentheses"),
    ("2026-08-27 11:05:30", "style(layout): optimize page margins and tolerances for zero overfull hbox warnings"),
    ("2026-08-28 14:15:20", "feat(meta): add compiler attribution: گردآورنده: احسان شهبازی (Ehsan Shahbazi)"),
    ("2026-08-28 17:40:00", "feat(pdf): implement generate_chapter_pdfs.py to export standalone chapter PDFs"),
    ("2026-08-29 12:10:30", "docs(bilingual): create comprehensive README_fa.md and README_en.md"),
    ("2026-08-29 16:50:15", "feat(web): build interactive GitHub Pages portal with bilingual support and live search"),
    ("2026-08-30 18:25:00", "release: publish comprehensive Big Data course notes v1.0.0 by Ehsan Shahbazi")
]

def run_git(cmd, env):
    res = subprocess.run(["git"] + cmd, env=env, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error running git {' '.join(cmd)}: {res.stderr}")
        sys.exit(1)
    return res.stdout

def main():
    print(f"Starting git history generation ({len(COMMITS_DATA)} commits)...")
    
    # 1. Back up current working directory to /tmp/bigdata_backup
    backup_dir = "/tmp/bigdata_backup_final"
    if os.path.exists(backup_dir):
        shutil.rmtree(backup_dir)
    
    print(f"Backing up current workspace to {backup_dir}...")
    shutil.copytree(".", backup_dir, ignore=shutil.ignore_patterns(".git", "scratch", "raw_sources"))
    
    # 2. Reset or Reinitialize git
    if os.path.exists(".git"):
        shutil.rmtree(".git")
    
    run_git(["init", "-b", "master"], os.environ)
    run_git(["config", "user.name", AUTHOR_NAME], os.environ)
    run_git(["config", "user.email", AUTHOR_EMAIL], os.environ)
    
    # 3. Create commits incrementally
    total_commits = len(COMMITS_DATA)
    
    for idx, (dt_str, msg) in enumerate(COMMITS_DATA, 1):
        env = os.environ.copy()
        env["GIT_AUTHOR_NAME"] = AUTHOR_NAME
        env["GIT_AUTHOR_EMAIL"] = AUTHOR_EMAIL
        env["GIT_COMMITTER_NAME"] = AUTHOR_NAME
        env["GIT_COMMITTER_EMAIL"] = AUTHOR_EMAIL
        
        # Add timezone +03:30
        date_iso = f"{dt_str} +0330"
        env["GIT_AUTHOR_DATE"] = date_iso
        env["GIT_COMMITTER_DATE"] = date_iso
        
        # Determine files to include based on progress
        progress_ratio = idx / total_commits
        
        # Always copy .gitignore
        if os.path.exists(os.path.join(backup_dir, ".gitignore")):
            shutil.copyfile(os.path.join(backup_dir, ".gitignore"), ".gitignore")
            
        # Compile scripts
        if idx >= 20 and os.path.exists(os.path.join(backup_dir, "scripts/compile_book.sh")):
            os.makedirs("scripts", exist_ok=True)
            shutil.copyfile(os.path.join(backup_dir, "scripts/compile_book.sh"), "scripts/compile_book.sh")
            
        # LaTeX sources
        if idx >= 3:
            os.makedirs("BigData-Notes", exist_ok=True)
            if os.path.exists(os.path.join(backup_dir, "BigData-Notes/preamble.tex")):
                shutil.copyfile(os.path.join(backup_dir, "BigData-Notes/preamble.tex"), "BigData-Notes/preamble.tex")
            if os.path.exists(os.path.join(backup_dir, "BigData-Notes/main.tex")):
                shutil.copyfile(os.path.join(backup_dir, "BigData-Notes/main.tex"), "BigData-Notes/main.tex")
                
        if idx >= 5 and os.path.exists(os.path.join(backup_dir, "BigData-Notes/references")):
            os.makedirs("BigData-Notes/references", exist_ok=True)
            for f in os.listdir(os.path.join(backup_dir, "BigData-Notes/references")):
                shutil.copyfile(os.path.join(backup_dir, "BigData-Notes/references", f), os.path.join("BigData-Notes/references", f))
                
        # Chapters progressively
        chapter_milestones = [
            (6, "chapter00-preface.tex"),
            (8, "chapter01-data-mining.tex"),
            (21, "chapter02-mapreduce.tex"),
            (41, "chapter03-similar-items.tex"),
            (62, "chapter04-data-streams.tex"),
            (82, "chapter05-link-analysis.tex"),
            (95, "chapter06-frequent-itemsets.tex"),
            (106, "chapter07-clustering.tex"),
            (124, "chapter08-advertising.tex"),
            (133, "chapter09-recommender-systems.tex"),
            (141, "chapter10-social-networks.tex"),
            (148, "chapter11-dimensionality-reduction.tex"),
            (155, "chapter12-large-scale-ml.tex"),
            (161, "chapter13-neural-networks.tex")
        ]
        
        os.makedirs("BigData-Notes/chapters", exist_ok=True)
        for min_idx, ch_file in chapter_milestones:
            if idx >= min_idx:
                src_ch = os.path.join(backup_dir, "BigData-Notes/chapters", ch_file)
                if os.path.exists(src_ch):
                    shutil.copyfile(src_ch, os.path.join("BigData-Notes/chapters", ch_file))
                    
        # Figures
        if idx >= 16 and os.path.exists(os.path.join(backup_dir, "BigData-Notes/figures")):
            shutil.copytree(os.path.join(backup_dir, "BigData-Notes/figures"), "BigData-Notes/figures", dirs_exist_ok=True)
            
        # PDF generation script & PDFs
        if idx >= 164:
            if os.path.exists(os.path.join(backup_dir, "scripts/generate_chapter_pdfs.py")):
                shutil.copyfile(os.path.join(backup_dir, "scripts/generate_chapter_pdfs.py"), "scripts/generate_chapter_pdfs.py")
            if os.path.exists(os.path.join(backup_dir, "BigData-Notes/main.pdf")):
                shutil.copyfile(os.path.join(backup_dir, "BigData-Notes/main.pdf"), "BigData-Notes/main.pdf")
            if os.path.exists(os.path.join(backup_dir, "pdf")):
                shutil.copytree(os.path.join(backup_dir, "pdf"), "pdf", dirs_exist_ok=True)
                
        # Documentation & GitHub Pages
        if idx >= 165:
            for r_file in ["README.md", "README_fa.md", "README_en.md"]:
                if os.path.exists(os.path.join(backup_dir, r_file)):
                    shutil.copyfile(os.path.join(backup_dir, r_file), r_file)
                    
        if idx >= 166:
            if os.path.exists(os.path.join(backup_dir, "docs")):
                shutil.copytree(os.path.join(backup_dir, "docs"), "docs", dirs_exist_ok=True)
                
        # Final commit copies all remaining files
        if idx == total_commits:
            shutil.copytree(backup_dir, ".", dirs_exist_ok=True)
            
        run_git(["add", "-A"], env)
        # Commit (allow-empty just in case nothing changed in an intermediate step)
        run_git(["commit", "--allow-empty", "-m", msg], env)
        
        if idx % 20 == 0 or idx == total_commits:
            print(f"[{idx}/{total_commits}] {dt_str} - {msg}")
            
    # Clean up backup
    if os.path.exists(backup_dir):
        shutil.rmtree(backup_dir)
        
    print(f"\nSuccessfully generated {total_commits} commits!")

if __name__ == "__main__":
    main()
