/* =========================
   SM CONSTRUCTION MAIN JS
========================= */

document.addEventListener("DOMContentLoaded", () => {

// SEO + performance fixes
document.querySelectorAll("img").forEach(img => {
    img.setAttribute("loading", "lazy");

    if (!img.alt || img.alt.trim() === "") {
        img.alt = "SM Construction Project Image";
    }
});

    /* =========================
       ELEMENTS
    ========================= */
    const navLinks = document.querySelector(".nav-links");
    const hamburgerIcon = document.querySelector(".hamburger i");
    const header = document.querySelector(".header");
    const heroTitle = document.querySelector(".hero-content h1");

    /* =========================
       MOBILE MENU
    ========================= */
    window.toggleMenu = function () {

        if (!navLinks || !hamburgerIcon) return;

        navLinks.classList.toggle("active");

        if (navLinks.classList.contains("active")) {

            hamburgerIcon.classList.remove("fa-bars");
            hamburgerIcon.classList.add("fa-times");

        } else {

            hamburgerIcon.classList.remove("fa-times");
            hamburgerIcon.classList.add("fa-bars");
        }
    };

    /* =========================
       CLOSE MENU ON LINK CLICK
    ========================= */
    document.querySelectorAll(".nav-links a").forEach(link => {

        link.addEventListener("click", () => {

            if (!navLinks || !hamburgerIcon) return;

            navLinks.classList.remove("active");

            hamburgerIcon.classList.remove("fa-times");
            hamburgerIcon.classList.add("fa-bars");
        });

    });

    /* =========================
       STICKY HEADER
    ========================= */
    window.addEventListener("scroll", () => {

        if (!header) return;

        if (window.scrollY > 50) {

            header.classList.add("sticky");

        } else {

            header.classList.remove("sticky");
        }
    });

    /* =========================
       TYPEWRITER HERO
    ========================= */
    if (heroTitle) {

        const text = "We Build Your Dream";
        let i = 0;

        heroTitle.innerHTML = "";

        function typeWriter() {

            if (i < text.length) {

                heroTitle.innerHTML += text.charAt(i);

                i++;

                setTimeout(typeWriter, 70);
            }
        }

        typeWriter();
    }

    /* =========================
       SCROLL ANIMATION
    ========================= */
    const cards = document.querySelectorAll(
        ".project-card, .card, .box"
    );

    if (cards.length > 0) {

        const observer = new IntersectionObserver((entries) => {

            entries.forEach(entry => {

                if (entry.isIntersecting) {

                    entry.target.style.opacity = "1";

                    entry.target.style.transform = "translateY(0)";
                }
            });

        }, {
            threshold: 0.15
        });

        cards.forEach(card => {

            card.style.opacity = "0";

            card.style.transform = "translateY(40px)";

            card.style.transition = "0.6s ease";

            observer.observe(card);
        });
    }

    /* =========================
       AUTO FOOTER YEAR
    ========================= */
    const footerText = document.querySelector("footer p");

    if (footerText) {

        footerText.innerHTML =
            `© ${new Date().getFullYear()} SM Construction | Built with Quality & Trust`;
    }

    /* =========================
       BUTTON RIPPLE EFFECT
    ========================= */
    document.querySelectorAll(
        ".btn, .btn-primary, .btn-secondary, .edit, .delete"
    ).forEach(button => {

        button.addEventListener("click", function (e) {

            const ripple = document.createElement("span");

            ripple.classList.add("ripple");

            const rect = button.getBoundingClientRect();

            ripple.style.left =
                `${e.clientX - rect.left}px`;

            ripple.style.top =
                `${e.clientY - rect.top}px`;

            button.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);
        });

    });

    /* =========================
       IMAGE HOVER ZOOM
    ========================= */
    document.querySelectorAll(".box img").forEach(img => {

        img.style.transition = "0.4s";

        img.addEventListener("mouseenter", () => {

            img.style.transform = "scale(1.05)";
        });

        img.addEventListener("mouseleave", () => {

            img.style.transform = "scale(1)";
        });

    });

    /* =========================
       SWIPER SLIDER
    ========================= */
    if (typeof Swiper !== "undefined") {

        new Swiper(".mySwiper", {

            loop: true,

            speed: 1000,

            autoplay: {
                delay: 3000,
                disableOnInteraction: false,
            },

            pagination: {
                el: ".swiper-pagination",
                clickable: true,
            },

            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev",
            },

            slidesPerView: 1,

            spaceBetween: 20
        });

    } else {

        console.log("Swiper library not loaded");
    }

    /* =========================
       SMOOTH SCROLL
    ========================= */
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {

        anchor.addEventListener("click", function (e) {

            const target = document.querySelector(
                this.getAttribute("href")
            );

            if (target) {

                e.preventDefault();

                target.scrollIntoView({
                    behavior: "smooth"
                });
            }
        });

    });

    /* =========================
       DELETE CONFIRMATION
    ========================= */
    document.querySelectorAll(".delete").forEach(button => {

        button.addEventListener("click", function (e) {

            const confirmDelete = confirm(
                "Are you sure you want to delete this item?"
            );

            if (!confirmDelete) {

                e.preventDefault();
            }
        });

    });

    /* =========================
       PROJECT SEARCH
    ========================= */
    window.searchProjects = function () {

        const input = document.getElementById("searchInput");

        if (!input) return;

        const filter = input.value.toLowerCase();

        const boxes =
            document.querySelectorAll(".project-grid .box, .grid .box");

        boxes.forEach(box => {

            const text = box.innerText.toLowerCase();

            if (text.includes(filter)) {

                box.style.display = "block";

            } else {

                box.style.display = "none";
            }

        });

    };

    /* =========================
       GALLERY LIGHTBOX
    ========================= */
    const galleryImages =
        document.querySelectorAll(".gallery-image");

    const lightbox =
        document.getElementById("lightbox");

    const lightboxImg =
        document.getElementById("lightboxImg");

    const closeLightbox =
        document.getElementById("closeLightbox");

    if (galleryImages.length > 0 &&
        lightbox &&
        lightboxImg) {

        galleryImages.forEach(img => {

            img.addEventListener("click", () => {

                lightbox.style.display = "flex";

                lightboxImg.src = img.src;
            });

        });

    }

    if (closeLightbox && lightbox) {

        closeLightbox.addEventListener("click", () => {

            lightbox.style.display = "none";

        });

    }

    if (lightbox && lightboxImg) {

        lightbox.addEventListener("click", (e) => {

            if (e.target !== lightboxImg) {

                lightbox.style.display = "none";
            }

        });

    }
/* =========================
   MOBILE MENU IMPROVEMENT (ADD ONLY)
========================= */

(function () {

    const navLinks = document.querySelector(".nav-links");
    const hamburger = document.querySelector(".hamburger");
    const hamburgerIcon = document.querySelector(".hamburger i");

    if (!navLinks || !hamburger) return;

    // Close when clicking outside menu
    document.addEventListener("click", (e) => {

        const isClickInsideMenu = navLinks.contains(e.target);
        const isClickHamburger = hamburger.contains(e.target);

        if (!isClickInsideMenu && !isClickHamburger && navLinks.classList.contains("active")) {

            navLinks.classList.remove("active");

            if (hamburgerIcon) {
                hamburgerIcon.classList.remove("fa-times");
                hamburgerIcon.classList.add("fa-bars");
            }
        }

    });

    // Close on scroll (IMPORTANT for your issue)
    window.addEventListener("scroll", () => {

        if (navLinks.classList.contains("active")) {

            navLinks.classList.remove("active");

            if (hamburgerIcon) {
                hamburgerIcon.classList.remove("fa-times");
                hamburgerIcon.classList.add("fa-bars");
            }
        }

    });

})();
});