(function () {
    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
    if (reduce.matches) {
        document.querySelectorAll(".reveal").forEach(function (el) {
            el.classList.add("reveal--visible");
        });
    } else {
        var nodes = document.querySelectorAll(".reveal");
        if (!nodes.length || !("IntersectionObserver" in window)) {
            nodes.forEach(function (el) {
                el.classList.add("reveal--visible");
            });
        } else {
            var io = new IntersectionObserver(
                function (entries) {
                    entries.forEach(function (entry) {
                        if (entry.isIntersecting) {
                            entry.target.classList.add("reveal--visible");
                            io.unobserve(entry.target);
                        }
                    });
                },
                { root: null, threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
            );
            nodes.forEach(function (el) {
                io.observe(el);
            });
        }
    }
})();

(function () {
    var STORAGE_COLLAPSE = "pinvoices.sidebarCollapsed";
    var MQ_DESKTOP = window.matchMedia("(min-width: 881px)");

    function $(id) {
        return document.getElementById(id);
    }

    function isDesktop() {
        return MQ_DESKTOP.matches;
    }

    function setCollapsed(on) {
        document.body.classList.toggle("sidebar--collapsed", !!on);
        var btn = $("app-sidebar-collapse");
        if (btn) {
            btn.setAttribute("aria-pressed", on ? "true" : "false");
            btn.setAttribute("title", on ? "Agrandir le menu" : "Réduire le menu");
        }
        try {
            localStorage.setItem(STORAGE_COLLAPSE, on ? "1" : "0");
        } catch (e) {
            /* ignore */
        }
    }

    function loadCollapsed() {
        try {
            return localStorage.getItem(STORAGE_COLLAPSE) === "1";
        } catch (e) {
            return false;
        }
    }

    function setDrawer(open) {
        document.body.classList.toggle("sidebar--drawer-open", !!open);
        var menuBtn = $("app-menu-toggle");
        var side = $("app-sidebar");
        if (menuBtn) {
            if (isDesktop()) {
                menuBtn.setAttribute("aria-expanded", "false");
            } else {
                menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
            }
        }
        if (side) {
            if (isDesktop()) {
                side.removeAttribute("aria-hidden");
            } else {
                side.setAttribute("aria-hidden", open ? "false" : "true");
            }
        }
    }

    function closeDrawer() {
        setDrawer(false);
    }

    function initSidebar() {
        var shell = document.querySelector(".app-shell");
        if (!shell) {
            return;
        }

        var collapseBtn = $("app-sidebar-collapse");
        var menuBtn = $("app-menu-toggle");
        var backdrop = $("app-sidebar-backdrop");

        if (isDesktop()) {
            setCollapsed(loadCollapsed());
        } else {
            document.body.classList.remove("sidebar--collapsed");
        }

        if (collapseBtn) {
            collapseBtn.addEventListener("click", function () {
                if (!isDesktop()) {
                    return;
                }
                setCollapsed(!document.body.classList.contains("sidebar--collapsed"));
            });
        }

        if (menuBtn) {
            menuBtn.addEventListener("click", function () {
                if (isDesktop()) {
                    return;
                }
                var open = !document.body.classList.contains("sidebar--drawer-open");
                setDrawer(open);
            });
        }

        if (backdrop) {
            backdrop.addEventListener("click", closeDrawer);
        }

        MQ_DESKTOP.addEventListener("change", function () {
            if (isDesktop()) {
                setDrawer(false);
                setCollapsed(loadCollapsed());
            } else {
                document.body.classList.remove("sidebar--collapsed");
                setDrawer(false);
            }
        });

        document.querySelectorAll(".app-sidebar__nav a").forEach(function (a) {
            a.addEventListener("click", function () {
                if (!isDesktop()) {
                    closeDrawer();
                }
            });
        });

        document.addEventListener("keydown", function (e) {
            if (e.key === "Escape" && document.body.classList.contains("sidebar--drawer-open")) {
                closeDrawer();
            }
        });

        setDrawer(false);
        var sideInit = $("app-sidebar");
        if (sideInit && isDesktop()) {
            sideInit.removeAttribute("aria-hidden");
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initSidebar);
    } else {
        initSidebar();
    }
})();
