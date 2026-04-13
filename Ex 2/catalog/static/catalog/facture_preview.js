(function () {
    var STORAGE_KEY = "pinvoices.invPreviewAccent";

    function eur(n) {
        var v = Math.round(Number(n) * 100) / 100;
        if (Number.isNaN(v)) {
            return "—";
        }
        return v.toFixed(2).replace(".", ",") + "\u00a0€";
    }

    function parseJsonScript(id) {
        var el = document.getElementById(id);
        if (!el || !el.textContent) {
            return null;
        }
        try {
            return JSON.parse(el.textContent);
        } catch (e) {
            return null;
        }
    }

    function produitMap(list) {
        var m = {};
        if (!list) {
            return m;
        }
        list.forEach(function (p) {
            m[String(p.id)] = p;
        });
        return m;
    }

    function val(el) {
        return el && "value" in el ? el.value : "";
    }

    function escapeHtml(s) {
        return String(s)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;");
    }

    function nl2br(s) {
        return s.replace(/\n/g, "<br>");
    }

    var MOIS = [
        "janvier",
        "février",
        "mars",
        "avril",
        "mai",
        "juin",
        "juillet",
        "août",
        "septembre",
        "octobre",
        "novembre",
        "décembre",
    ];

    function dateFactureFr() {
        var d = new Date();
        return d.getDate() + " " + MOIS[d.getMonth()] + " " + d.getFullYear();
    }

    function getAccent() {
        var input = document.getElementById("inv-preview-accent");
        if (input && input.value) {
            return input.value;
        }
        return "#1a73e8";
    }

    function syncHiddenFromAccent() {
        var h = document.getElementById("facture-theme-couleur");
        var accent = getAccent();
        if (h && /^#[0-9A-Fa-f]{6}$/.test(accent)) {
            h.value = accent;
        }
    }

    function applyAccentToDoc() {
        var root = document.getElementById("inv-preview-root");
        if (!root) {
            return;
        }
        var doc = root.querySelector(".inv-doc");
        if (doc) {
            doc.style.setProperty("--inv-accent", getAccent());
        }
    }

    function render(form) {
        var produits = produitMap(parseJsonScript("produits-preview-data"));
        var statutLabels = parseJsonScript("statut-labels-data") || {};

        var ref = val(form.querySelector('[name="reference"]'));
        var statut = val(form.querySelector('[name="statut"]'));
        var client = val(form.querySelector('[name="client_nom"]'));
        var email = val(form.querySelector('[name="client_email"]'));
        var tel = val(form.querySelector('[name="client_telephone"]'));
        var adr = val(form.querySelector('[name="adresse_facturation"]'));
        var devise = val(form.querySelector('[name="devise"]')) || "EUR";
        var notes = val(form.querySelector('[name="notes_internes"]'));

        var totalFormsEl = form.querySelector('[name="form-TOTAL_FORMS"]');
        var total = totalFormsEl ? parseInt(totalFormsEl.value, 10) || 0 : 0;
        var rows = [];
        var sumHt = 0;
        var sumTva = 0;
        var sumTtc = 0;
        var hasProductRow = false;

        for (var i = 0; i < total; i++) {
            var sel = form.querySelector('[name="form-' + i + '-produit"]');
            var qEl = form.querySelector('[name="form-' + i + '-quantite"]');
            var rEl = form.querySelector('[name="form-' + i + '-remise_pourcent"]');
            var libEl = form.querySelector('[name="form-' + i + '-libelle_override"]');

            var pid = val(sel);
            var qty = parseInt(val(qEl), 10);
            var rem = parseFloat((val(rEl) || "0").replace(",", "."));
            var lib = val(libEl);

            if (!pid) {
                continue;
            }
            var p = produits[pid];
            if (!p) {
                continue;
            }
            hasProductRow = true;
            if (!qty || qty < 1) {
                qty = 0;
            }

            var prix = parseFloat(String(p.prix).replace(",", "."));
            var taux = parseFloat(String(p.taux_tva).replace(",", "."));
            var remF = Number.isFinite(rem) ? rem : 0;
            var ht = prix * qty * (1 - remF / 100);
            var tva = ht * (taux / 100);
            var ttc = ht + tva;

            if (qty > 0) {
                sumHt += ht;
                sumTva += tva;
                sumTtc += ttc;
            }

            var label = lib ? lib : p.nom;
            rows.push({
                label: label,
                pu: prix,
                qty: qty,
                rem: remF,
                ht: ht,
                tva: tva,
                ttc: ttc,
                taux: taux,
            });
        }

        var accent = escapeHtml(getAccent());
        var statutLabel = statutLabels[statut] ? escapeHtml(statutLabels[statut]) : "—";

        var html = "";
        html += '<article class="inv-doc" style="--inv-accent:' + accent + '">';
        html += '<div class="inv-doc__sheet">';
        html += '<header class="inv-doc__masthead">';
        html += '<div class="inv-doc__brand">';
        html += '<span class="inv-doc__logo">PInvoices</span>';
        html += '<span class="inv-doc__tagline">Piwebi × Trustia</span>';
        html += "</div>";
        html += '<div class="inv-doc__masthead-right">';
        html += '<span class="inv-doc__kind">Facture</span>';
        html += '<div class="inv-doc__refline">';
        html += '<span class="inv-doc__ref-label">Réf.</span> ';
        html += "<strong>" + (ref ? escapeHtml(ref) : "—") + "</strong>";
        html += "</div>";
        html += '<p class="inv-doc__date">Date&nbsp;: ' + dateFactureFr() + "</p>";
        html += '<p class="inv-doc__statut"><span class="inv-doc__pill">' + statutLabel + "</span></p>";
        html += "</div>";
        html += "</header>";

        html += '<div class="inv-doc__parties">';
        html += '<div class="inv-doc__party inv-doc__party--from">';
        html += '<h3 class="inv-doc__party-title">Émetteur</h3>';
        html += '<p class="inv-doc__party-text"><strong>PInvoices</strong><br />Démonstration produit<br />France</p>';
        html += "</div>";
        html += '<div class="inv-doc__party inv-doc__party--to">';
        html += '<h3 class="inv-doc__party-title">Facturer à</h3>';
        if (client || email || tel || adr) {
            html += '<div class="inv-doc__party-text">';
            if (client) {
                html += "<strong>" + escapeHtml(client) + "</strong>";
            } else {
                html += "<span class=\"inv-doc__placeholder\">Nom du client</span>";
            }
            if (email) {
                html += "<br />" + escapeHtml(email);
            }
            if (tel) {
                html += "<br />" + escapeHtml(tel);
            }
            if (adr) {
                html += "<br />" + nl2br(escapeHtml(adr));
            }
            html += "</div>";
        } else {
            html += '<p class="inv-doc__placeholder">Coordonnées client…</p>';
        }
        html += "</div>";
        html += "</div>";

        html += '<p class="inv-doc__devise">Devise&nbsp;: <strong>' + escapeHtml(devise) + "</strong></p>";

        if (!hasProductRow) {
            html += '<div class="inv-doc__empty">';
            html += "<p>Ajoutez au moins une ligne avec un <strong>produit</strong> et une <strong>quantité</strong> pour voir le tableau et les totaux.</p>";
            html += "</div>";
        } else {
            html += '<div class="inv-doc__table-wrap">';
            html += '<table class="inv-doc__table">';
            html += "<thead><tr>";
            html += "<th>Description</th>";
            html += '<th class="inv-doc__num">PU HT</th>';
            html += '<th class="inv-doc__num">Qté</th>';
            html += '<th class="inv-doc__num">Rem.</th>';
            html += '<th class="inv-doc__num">TVA</th>';
            html += '<th class="inv-doc__num">HT</th>';
            html += '<th class="inv-doc__num">TTC</th>';
            html += "</tr></thead><tbody>";
            for (var r = 0; r < rows.length; r++) {
                var row = rows[r];
                html += "<tr>";
                html += "<td>" + escapeHtml(row.label) + "</td>";
                html += '<td class="inv-doc__num">' + eur(row.pu) + "</td>";
                html += '<td class="inv-doc__num">' + (row.qty > 0 ? String(row.qty) : "—") + "</td>";
                html += '<td class="inv-doc__num">' + (row.rem ? row.rem.toFixed(2).replace(".", ",") + "\u00a0%" : "—") + "</td>";
                html += '<td class="inv-doc__num">' + row.taux.toFixed(2).replace(".", ",") + "\u00a0%</td>";
                html += '<td class="inv-doc__num">' + eur(row.ht) + "</td>";
                html += '<td class="inv-doc__num inv-doc__num--strong">' + eur(row.ttc) + "</td>";
                html += "</tr>";
            }
            html += "</tbody></table>";
            html += "</div>";

            if (sumTtc > 0) {
                html += '<div class="inv-doc__totals">';
                html += '<dl class="inv-doc__totals-dl">';
                html += "<div><dt>Total HT</dt><dd>" + eur(sumHt) + "</dd></div>";
                html += "<div><dt>Total TVA</dt><dd>" + eur(sumTva) + "</dd></div>";
                html += '<div class="inv-doc__totals-ttc"><dt>Total TTC</dt><dd>' + eur(sumTtc) + "</dd></div>";
                html += "</dl>";
                html += "</div>";
            }
        }

        if (notes) {
            html += '<div class="inv-doc__notes">';
            html += '<h4 class="inv-doc__notes-title">Notes</h4>';
            html += '<p class="inv-doc__notes-body">' + nl2br(escapeHtml(notes)) + "</p>";
            html += "</div>";
        }

        html += "</div></article>";

        var mount = document.getElementById("inv-preview-root");
        if (mount) {
            mount.innerHTML = html;
        }
        applyAccentToDoc();
        syncHiddenFromAccent();
    }

    function loadStoredAccent() {
        try {
            var s = localStorage.getItem(STORAGE_KEY);
            var input = document.getElementById("inv-preview-accent");
            if (s && /^#[0-9A-Fa-f]{6}$/.test(s) && input) {
                input.value = s;
            }
        } catch (e) {
            /* ignore */
        }
        syncHiddenFromAccent();
    }

    function saveAccent(hex) {
        try {
            localStorage.setItem(STORAGE_KEY, hex);
        } catch (e) {
            /* ignore */
        }
    }

    function bindToolbar(form) {
        var input = document.getElementById("inv-preview-accent");
        var presets = document.querySelectorAll(".inv-preview-preset");

        function onAccentChange() {
            if (input) {
                saveAccent(input.value);
            }
            applyAccentToDoc();
            syncHiddenFromAccent();
        }

        if (input) {
            input.addEventListener("input", onAccentChange);
            input.addEventListener("change", onAccentChange);
        }

        for (var i = 0; i < presets.length; i++) {
            presets[i].addEventListener("click", function () {
                var c = this.getAttribute("data-color");
                if (c && input) {
                    input.value = c;
                    saveAccent(c);
                    applyAccentToDoc();
                    syncHiddenFromAccent();
                }
            });
        }
    }

    function init() {
        var form = document.getElementById("facture-create-form");
        if (!form) {
            return;
        }
        loadStoredAccent();
        bindToolbar(form);

        var run = function () {
            render(form);
        };
        form.addEventListener("input", run);
        form.addEventListener("change", run);
        form.addEventListener("submit", function () {
            syncHiddenFromAccent();
        });
        run();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
