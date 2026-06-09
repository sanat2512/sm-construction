
/* =========================
   ADMIN SEARCH
========================= */

document.addEventListener("DOMContentLoaded", () => {

    const searchInput =
        document.getElementById("searchInput");

    if (searchInput) {

        searchInput.addEventListener("keyup", function () {

            let value =
                this.value.toLowerCase();

            let items =
                document.querySelectorAll(".grid .box");

            items.forEach(item => {

                item.style.display =
                    item.innerText
                        .toLowerCase()
                        .includes(value)
                        ? ""
                        : "none";
            });

        });

    }

});


/* =========================
   SIDEBAR AUTO HIDE ON SCROLL (MOBILE)
========================= */

document.addEventListener("DOMContentLoaded", () => {

    const sidebar =
        document.querySelector(".sidebar");

    if (!sidebar) return;

    let lastScrollTop = 0;

    window.addEventListener("scroll", function () {

        let scrollTop =
            window.pageYOffset || document.documentElement.scrollTop;

        if (scrollTop > lastScrollTop) {

            // scrolling down → hide sidebar
            sidebar.classList.add("hide");

        } else {

            // scrolling up → show sidebar
            sidebar.classList.remove("hide");
        }

        lastScrollTop =
            scrollTop <= 0 ? 0 : scrollTop;

    });

});