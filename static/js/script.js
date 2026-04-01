/* ============================================================
   VILLAGE SATTAM — Main JavaScript
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

    // ============================================
    // MOBILE DRAWER TOGGLE
    // ============================================
    const mobileToggle = document.getElementById('mobileToggle');
    const mobileDrawer = document.getElementById('mobileDrawer');
    const drawerClose = document.getElementById('drawerClose');
    const drawerOverlay = document.getElementById('drawerOverlay');

    function openDrawer() {
        mobileDrawer.classList.add('open');
        drawerOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeDrawer() {
        mobileDrawer.classList.remove('open');
        drawerOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (mobileToggle) mobileToggle.addEventListener('click', openDrawer);
    if (drawerClose) drawerClose.addEventListener('click', closeDrawer);
    if (drawerOverlay) drawerOverlay.addEventListener('click', closeDrawer);

    // ============================================
    // FLASH MESSAGE AUTO-DISMISS
    // ============================================
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(function (flash) {
        setTimeout(function () {
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(100%)';
            flash.style.transition = 'all 0.4s ease';
            setTimeout(function () { flash.remove(); }, 400);
        }, 5000);
    });

    // ============================================
    // SCROLL ANIMATIONS — Service & Scheme Cards
    // ============================================
    const animateTargets = document.querySelectorAll('.service-card, .scheme-card, .scheme-card-full, .stat-widget');

    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    const delay = entry.target.dataset.delay || 0;
                    setTimeout(function () {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }, parseInt(delay));
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        animateTargets.forEach(function (el) {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            observer.observe(el);
        });
    }

    // ============================================
    // ADMIN: BAR CHART ANIMATION
    // ============================================
    const bars = document.querySelectorAll('.bar');
    if (bars.length > 0) {
        setTimeout(function () {
            bars.forEach(function (bar) {
                const targetWidth = bar.style.width;
                bar.style.width = '0%';
                requestAnimationFrame(function () {
                    setTimeout(function () {
                        bar.style.width = targetWidth || '0%';
                    }, 50);
                });
            });
        }, 300);
    }

    // ============================================
    // STAT COUNTER ANIMATION
    // ============================================
    const statNumbers = document.querySelectorAll('.stat-number');
    if ('IntersectionObserver' in window) {
        const counterObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    const target = parseInt(el.textContent.replace(/\D/g, ''), 10);
                    if (!isNaN(target) && target > 0) {
                        animateCounter(el, target);
                    }
                    counterObserver.unobserve(el);
                }
            });
        }, { threshold: 0.5 });

        statNumbers.forEach(function (el) { counterObserver.observe(el); });
    }

    function animateCounter(el, target) {
        let current = 0;
        const duration = 800;
        const steps = 40;
        const increment = target / steps;
        const interval = duration / steps;

        const timer = setInterval(function () {
            current += increment;
            if (current >= target) {
                el.textContent = target;
                clearInterval(timer);
            } else {
                el.textContent = Math.floor(current);
            }
        }, interval);
    }

    // ============================================
    // SMOOTH ACTIVE NAV HIGHLIGHT ON SCROLL
    // ============================================
    const sections = document.querySelectorAll('section[id]');
    if (sections.length > 0) {
        window.addEventListener('scroll', function () {
            let current = '';
            sections.forEach(function (section) {
                const sectionTop = section.offsetTop - 100;
                if (window.pageYOffset >= sectionTop) {
                    current = section.getAttribute('id');
                }
            });
        }, { passive: true });
    }

    // ============================================
    // TABLE SEARCH / FILTER (Admin Pages)
    // ============================================
    const tableSearch = document.getElementById('tableSearch');
    if (tableSearch) {
        tableSearch.addEventListener('input', function () {
            const query = this.value.toLowerCase();
            const rows = document.querySelectorAll('.data-table tbody tr');
            rows.forEach(function (row) {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(query) ? '' : 'none';
            });
        });
    }

    // ============================================
    // FORM VALIDATION ENHANCEMENT
    // ============================================
    const forms = document.querySelectorAll('form');
    forms.forEach(function (form) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (!submitBtn) return;

        form.addEventListener('submit', function () {
            submitBtn.disabled = true;
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';

            // Re-enable after 5 seconds as fallback
            setTimeout(function () {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }, 5000);
        });
    });

    // ============================================
    // TOOLTIP FOR STATUS BADGES
    // ============================================
    const statusBadges = document.querySelectorAll('.status-badge');
    statusBadges.forEach(function (badge) {
        const statusMessages = {
            'Pending': 'Your complaint is awaiting review',
            'In Progress': 'Your complaint is being addressed',
            'Resolved': 'Your complaint has been resolved',
            'Rejected': 'Your complaint could not be processed'
        };
        const text = badge.textContent.trim();
        if (statusMessages[text]) {
            badge.setAttribute('title', statusMessages[text]);
        }
    });

    // ============================================
    // BACK TO TOP BUTTON
    // ============================================
    const backToTopBtn = document.createElement('button');
    backToTopBtn.innerHTML = '<i class="fas fa-chevron-up"></i>';
    backToTopBtn.className = 'back-to-top';
    backToTopBtn.setAttribute('aria-label', 'Back to top');
    backToTopBtn.style.cssText = `
        position: fixed; bottom: 24px; right: 24px; z-index: 200;
        width: 42px; height: 42px; border-radius: 50%;
        background: #1E3A8A; color: white; border: none; cursor: pointer;
        font-size: 0.85rem; box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        opacity: 0; transform: translateY(10px);
        transition: all 0.3s ease; display: flex;
        align-items: center; justify-content: center;
    `;
    document.body.appendChild(backToTopBtn);

    window.addEventListener('scroll', function () {
        if (window.pageYOffset > 400) {
            backToTopBtn.style.opacity = '1';
            backToTopBtn.style.transform = 'translateY(0)';
        } else {
            backToTopBtn.style.opacity = '0';
            backToTopBtn.style.transform = 'translateY(10px)';
        }
    }, { passive: true });

    backToTopBtn.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // ============================================
    // HERO STAT COUNTER — page load
    // ============================================
    const heroStats = document.querySelectorAll('.stat-num');
    heroStats.forEach(function (el) {
        const text = el.textContent;
        const num = parseInt(text.replace(/\D/g, ''), 10);
        const suffix = text.replace(/[\d]/g, '');
        if (!isNaN(num) && num > 0) {
            let count = 0;
            const step = Math.ceil(num / 60);
            const timer = setInterval(function () {
                count += step;
                if (count >= num) {
                    el.textContent = num + suffix;
                    clearInterval(timer);
                } else {
                    el.textContent = count + suffix;
                }
            }, 25);
        }
    });

    // ============================================
    // ACTIVE NAV LINK HIGHLIGHT
    // ============================================
    const currentPath = window.location.pathname;
    document.querySelectorAll('.main-nav a, .drawer-nav a').forEach(function (link) {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // ============================================
    // MINI SELECT CHANGE CONFIRMATION (Admin Complaints)
    // ============================================
    document.querySelectorAll('.mini-select').forEach(function (select) {
        select.addEventListener('change', function () {
            if (this.value && !confirm('Update status to "' + this.value + '"?')) {
                this.value = '';
            }
        });
    });

});