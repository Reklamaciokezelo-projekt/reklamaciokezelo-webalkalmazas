/**
 * Tom Select inicializáló
 * @param {string} elementId - A HTML select elem ID-ja
 * @param {string} placeholderText - A megjelenítendő segédszöveg
 * @param {boolean} shouldClear - Igaz esetén törli az alapértelmezett kijelölést (pl. regisztrációnál)
 */
function initDynamicSelect(elementId, placeholderText, shouldClear) {

    // -- HTML elem megkeresése ID alapján --
    const el = document.getElementById(elementId);
    if (!el) return;

    // -- TomSelect példány létrehozása --
    return new TomSelect("#" + elementId, {
        create: true,
        allowEmptyOption: true,
        placeholder: placeholderText,

        // -- Törli az alapértelmezett értéket a mezőből --
        onInitialize: function() { 
            if (shouldClear) {
                this.clear(); 
            }
        },
        
        onOptionAdd: function(value) {
            // -- Ha a bevitt érték nem szám, akkor új elem került rögzítésre --
            if (isNaN(value)) {
                // -- Toast meghívása új elem esetén --
                const toastEl = document.getElementById('localSuccessToast');
                const toastMsg = document.getElementById('localToastMessage');
                if (toastEl && toastMsg) {
                    toastMsg.innerHTML = `Az új elem (<strong>${value}</strong>) rögzítésre került a mentési sorba.`;
                    new bootstrap.Toast(toastEl, { delay: 3000 }).show();
                }
            }
        },
        // -- Egyedi megjelenítés a keresési listában --
        render: {
            // -- Új elem hozzáadásának formázása --
            option_create: (data, escape) => `<div class="create" style="padding: 8px;"><strong style="color: #0d6efd;">+</strong> Hozzáadás: <strong>${escape(data.input)}</strong></div>`,
            // -- Üres találat esetén megjelenő szöveg --
            no_results: (data, escape) => `<div class="no-results" style="padding: 8px;">Nincs találat: "${escape(data.input)}"</div>`
        }
    });
}