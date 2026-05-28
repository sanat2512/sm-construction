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