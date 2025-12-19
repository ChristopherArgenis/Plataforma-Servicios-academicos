// ========================================
// ACQUISITION MODULE - HTMX-AWARE INITIALIZATION
// ========================================
(function() {
    'use strict';

    function initializeAcquisition() {
        const acquisitionContainer = document.getElementById('Adquisicion');
        if (!acquisitionContainer) {
            console.log('[Acquisition] Container not found, skipping initialization');
            return;
        }

        if (acquisitionContainer.dataset.initialized === 'true') {
            console.log('[Acquisition] Already initialized, skipping...');
            return;
        }

        console.log('[Acquisition] Initializing module...');
        acquisitionContainer.dataset.initialized = 'true';

        // Modal handlers
        const btnOpenUpdateModal = document.getElementById('btnOpenUpdateModal');
        if (btnOpenUpdateModal) {
            btnOpenUpdateModal.addEventListener('click', function() {
                const modalEl = document.getElementById('confirmUpdateModal');
                if (modalEl && typeof bootstrap !== 'undefined') {
                    const modal = new bootstrap.Modal(modalEl);
                    modal.show();
                }
            });
        }

        const btnRelevantes = document.getElementById('btnRelevantes');
        if (btnRelevantes) {
            btnRelevantes.addEventListener('click', function() {
                const checkboxes = document.querySelectorAll('input[name="keys[]"]:checked');
                const count = checkboxes.length;

                if (count === 3) {
                    const modalEl = document.getElementById('modalRelevantes');
                    if (modalEl && typeof bootstrap !== 'undefined') {
                        const modal = new bootstrap.Modal(modalEl);
                        modal.show();
                    }
                } else {
                    alert("Por favor, selecciona exactamente 3 artículos para continuar. Has seleccionado " + count + ".");
                }
            });
        }

        const btnConfirmarRelevantes = document.getElementById('btnConfirmarRelevantes');
        if (btnConfirmarRelevantes) {
            btnConfirmarRelevantes.addEventListener('click', function() {
                const checkboxes = document.querySelectorAll('input[name="keys[]"]:checked');
                const selectedIds = Array.from(checkboxes).map(cb => cb.value);

                const form = document.createElement('form');
                form.method = 'POST';
                form.action = '/Panel/save_relevant_articles';
                
                selectedIds.forEach(id => {
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = 'relevant_keys[]';
                    input.value = id;
                    form.appendChild(input);
                });

                document.body.appendChild(form);
                form.submit();
            });
        }

        console.log('[Acquisition] Initialization complete');
    }

    // ========================================
    // HTMX-AWARE INITIALIZATION
    // ========================================
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeAcquisition);
    } else {
        initializeAcquisition();
    }

    document.body.addEventListener('htmx:load', function(e) {
        if (e.detail.elt.id === 'Adquisicion' || e.detail.elt.querySelector('#Adquisicion')) {
            initializeAcquisition();
        }
    });

    console.log('[Acquisition] Module loaded and ready');

})();
