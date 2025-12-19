// ========================================
// INFO MODULE - HTMX-AWARE INITIALIZATION
// ========================================
(function() {
    'use strict';

    function initializeInfo() {
        const btnEditName = document.getElementById('btnEditName');
        if (!btnEditName) {
            console.log('[Info] Edit button not found, skipping initialization');
            return;
        }

        // Check if already initialized
        if (btnEditName.dataset.initialized === 'true') {
            console.log('[Info] Already initialized, skipping...');
            return;
        }

        console.log('[Info] Initializing module...');
        btnEditName.dataset.initialized = 'true';

        const userNameDisplay = document.getElementById('userNameDisplay');
        const userInputContainer = document.getElementById('userInputContainer');
        const userNameInput = document.getElementById('userNameInput');
        let isEditingName = false;

        btnEditName.addEventListener('click', function() {
            if (!isEditingName) {
                userNameDisplay.style.display = 'none';
                userInputContainer.style.display = 'block';
                userNameInput.focus();
                this.innerHTML = '<i class="bi bi-save"></i>';
                this.classList.remove('btn-outline-secondary');
                this.classList.add('btn-success', 'text-white');
                isEditingName = true;
            } else {
                const newName = userNameInput.value.trim();
                if (!newName) {
                    if (typeof showToast === 'function') {
                        showToast('El nombre no puede estar vacío', 'warning');
                    }
                    return;
                }
                
                fetch('/Panel/Info/UpdateName', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ nombre: newName })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.status === 'success') {
                        userNameDisplay.textContent = newName;
                        userNameDisplay.style.display = 'block';
                        userInputContainer.style.display = 'none';
                        btnEditName.innerHTML = '<i class="bi bi-pencil-fill"></i>';
                        btnEditName.classList.remove('btn-success', 'text-white');
                        btnEditName.classList.add('btn-outline-secondary');
                        isEditingName = false;
                        if (typeof showToast === 'function') {
                            showToast('Nombre actualizado correctamente', 'success');
                        }
                    } else {
                        if (typeof showToast === 'function') {
                            showToast('Error: ' + data.message, 'error');
                        }
                    }
                })
                .catch(err => {
                    console.error(err);
                    if (typeof showToast === 'function') {
                        showToast('Error de conexión', 'error');
                    }
                });
            }
        });

        console.log('[Info] Initialization complete');
    }

    // ========================================
    // EVENT LISTENER: content:ready (from htmx-cleanup.js)
    // ========================================
    document.addEventListener('content:ready', function(evt) {
        const container = evt.detail.container;
        const btnEditName = container.querySelector('#btnEditName');
        
        if (btnEditName) {
            console.log('[Info] content:ready event received, initializing...');
            initializeInfo();
        }
    });

    // ========================================
    // FALLBACK: DOMContentLoaded for direct page loads
    // ========================================
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            const btnEditName = document.getElementById('btnEditName');
            if (btnEditName) {
                console.log('[Info] DOMContentLoaded, initializing...');
                initializeInfo();
            }
        });
    } else {
        // DOM already loaded
        const btnEditName = document.getElementById('btnEditName');
        if (btnEditName) {
            console.log('[Info] DOM already loaded, initializing...');
            initializeInfo();
        }
    }

    console.log('[Info] Module loaded and ready');

})();
