(function () {
    function init() {
        var form = document.getElementById("facture-detail-theme");
        if (!form) {
            return;
        }
        var input = form.querySelector('input[type="color"].inv-preview-color');
        var presets = form.querySelectorAll(".inv-preview-preset");
        for (var i = 0; i < presets.length; i++) {
            presets[i].addEventListener("click", function () {
                var c = this.getAttribute("data-color");
                if (c && input) {
                    input.value = c;
                }
            });
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
