document.addEventListener("DOMContentLoaded", function() {
    const tabs = document.querySelectorAll('[data-mdb-toggle="pill"]');
    tabs.forEach(tab => {
      tab.addEventListener("click", function() {
        const target = document.querySelector(this.getAttribute("href"));
        if (target) {
          document.querySelectorAll(".tab-pane").forEach(tabPane => {
            tabPane.classList.remove("show", "active");
          });
          document.querySelectorAll('[data-mdb-toggle="pill"]').forEach(tabLink => {
            tabLink.classList.remove("active");
          });
          this.classList.add("active");
          target.classList.add("show", "active");
        }
      });
    });
  });
  