// ==============================================================================
// Big Data Course Portal JavaScript - Interactive UI & Modal Logic
// Compiler: Ehsan Shahbazi (احسان شهبازی)
// ==============================================================================

document.addEventListener('DOMContentLoaded', () => {
    // 1. Theme Toggle
    const themeToggleBtn = document.getElementById('theme-toggle');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const savedTheme = localStorage.getItem('theme') || (prefersDark ? 'dark' : 'light');
    
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        });
    }

    function updateThemeIcon(theme) {
        if (!themeToggleBtn) return;
        const iconSpan = themeToggleBtn.querySelector('.theme-icon');
        if (iconSpan) {
            iconSpan.textContent = theme === 'dark' ? '☀️' : '🌙';
        }
    }

    // 2. Filter & Live Search
    const searchInput = document.getElementById('search-input');
    const filterPills = document.querySelectorAll('.pill-btn');
    const chapterCards = document.querySelectorAll('.chapter-card');

    let currentPart = 'all';
    let searchQuery = '';

    function filterCards() {
        chapterCards.forEach(card => {
            const cardPart = card.getAttribute('data-part');
            const textContent = (card.textContent || '').toLowerCase();

            const matchesPart = (currentPart === 'all' || cardPart === currentPart);
            const matchesSearch = textContent.includes(searchQuery.toLowerCase());

            if (matchesPart && matchesSearch) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });
    }

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            searchQuery = e.target.value.trim();
            filterCards();
        });
    }

    filterPills.forEach(pill => {
        pill.addEventListener('click', () => {
            filterPills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            currentPart = pill.getAttribute('data-part');
            filterCards();
        });
    });

    // 3. PDF Preview Modal
    const modalOverlay = document.getElementById('pdf-modal');
    const modalIframe = document.getElementById('modal-iframe');
    const modalTitle = document.getElementById('modal-title');
    const modalCloseBtn = document.getElementById('modal-close');
    const previewButtons = document.querySelectorAll('.btn-preview');

    previewButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const pdfUrl = btn.getAttribute('data-pdf');
            const title = btn.getAttribute('data-title');

            if (modalIframe && modalTitle && modalOverlay) {
                modalIframe.src = pdfUrl;
                modalTitle.textContent = title || 'پیش‌نمایش سند PDF';
                modalOverlay.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        });
    });

    function closeModal() {
        if (modalOverlay) {
            modalOverlay.classList.remove('active');
            if (modalIframe) modalIframe.src = '';
            document.body.style.overflow = '';
        }
    }

    if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeModal);
    if (modalOverlay) {
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) closeModal();
        });
    }

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeModal();
    });

    // 4. BibTeX Copy to Clipboard
    const copyBibtexBtn = document.getElementById('copy-bibtex-btn');
    const bibtexCode = document.getElementById('bibtex-code');

    if (copyBibtexBtn && bibtexCode) {
        copyBibtexBtn.addEventListener('click', () => {
            navigator.clipboard.writeText(bibtexCode.textContent.trim()).then(() => {
                const originalText = copyBibtexBtn.innerHTML;
                copyBibtexBtn.innerHTML = '✓ کپی شد!';
                setTimeout(() => {
                    copyBibtexBtn.innerHTML = originalText;
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy: ', err);
            });
        });
    }
});
