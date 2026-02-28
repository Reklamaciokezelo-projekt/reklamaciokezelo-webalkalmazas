/**
 * Tom Select inicializáló
 * @param {string} elementId - A HTML select elem ID-ja
 * @param {string} placeholderText - A megjelenítendő segédszöveg
 * @param {boolean} shouldClear - Igaz esetén törli az alapértelmezett kijelölést (pl. regisztrációnál)
 */
function initDynamicSelect(elementId, placeholderText, shouldClear) {

    // --- HTML elem keresése ID alapján ---
    const el = document.getElementById(elementId);
    if (!el) return;

    // --- TomSelect példány létrehozása ---
    return new TomSelect("#" + elementId, {
        
        // --- Új elem létrehozásakor 'NEW_' prefix hozzáadása ---
        create: function(input) {
            return {
                value: 'NEW_' + input, 
                text: input
            };
        },

        allowEmptyOption: true,
        placeholder: placeholderText,

        // --- Törli az alapértelmezett értéket a mezőből ---
        onInitialize: function() { 
            if (shouldClear) {
                this.clear(); 
            }
        },
        
        // --- Új (NEW_ prefixű) elem hozzáadásakor visszajelző toast megjelenítése ---
        onOptionAdd: function(value) {

            if (String(value).startsWith('NEW_')) {
                const actualValue = String(value).substring(4);

                // --- Toast meghívása új elem esetén ---
                const toastEl = document.getElementById('localSuccessToast');
                const toastMsg = document.getElementById('localToastMessage');
                if (toastEl && toastMsg) {
                    toastMsg.innerHTML = `Az új elem (<strong>${actualValue}</strong>) rögzítésre került a mentési sorba.`;
                    new bootstrap.Toast(toastEl, { delay: 3000 }).show();
                }
            }
        },
        // --- Egyedi megjelenítés a keresési listában ---
        render: {
            // --- Új elem hozzáadásának formázása ---
            option_create: (data, escape) => `<div class="create" style="padding: 8px;"><strong style="color: #0d6efd;">+</strong> Hozzáadás: <strong>${escape(data.input)}</strong></div>`,
            // --- Üres találat esetén megjelenő szöveg ---
            no_results: (data, escape) => `<div class="no-results" style="padding: 8px;">Nincs találat: "${escape(data.input)}"</div>`
        }
    });
}