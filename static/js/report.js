// ========================================
// REPORT MODULE - HTMX-AWARE INITIALIZATION
// ========================================
(function() {
    'use strict';

    // Store original templates before initialization
    const originalTemplates = {};

    // ========================================
    // INITIALIZATION FUNCTION
    // ========================================
    function initializeReport() {
        const reportContainer = document.getElementById('Report');
        if (!reportContainer) {
            console.log('[Report] Container not found, skipping initialization');
            return;
        }

        // Check if already initialized (container-based flag)
        if (reportContainer.dataset.initialized === 'true') {
            console.log('[Report] Already initialized, skipping...');
            return;
        }

        console.log('[Report] Initializing module...');
        reportContainer.dataset.initialized = 'true';

        const getClienteId = () => reportContainer.dataset.clienteId;

        // ========================================
        // NOTIFICATIONS
        // ========================================
        function showNotification(message, type = 'success') {
            if (typeof showToast === 'function') {
                showToast(message, type);
            } else {
                alert(message);
            }
        }

        // ========================================
        // API HELPERS
        // ========================================
        function sendFormData(url, formData, successMessage) {
            const clienteId = getClienteId();
            if (!clienteId) {
                showNotification('Error: Cliente ID no encontrado. Recarga la página.', 'error');
                return;
            }

            if (!formData.has('cliente_id')) {
                formData.append('cliente_id', clienteId);
            }

            fetch(url, {
                method: 'POST',
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    showNotification(successMessage || 'Guardado correctamente', 'success');
                } else {
                    showNotification('Error: ' + data.message, 'error');
                }
            })
            .catch(err => {
                console.error(err);
                showNotification('Error de conexión', 'error');
            });
        }

        // ========================================
        // ROW INITIALIZATION HELPERS
        // ========================================

        function initComiteRow(row) {
            if (row.dataset.comiteInitialized === 'true') {
                console.log('[Report] initComiteRow: Already initialized, skipping');
                return;
            }
            
            console.log('[Report] initComiteRow: Initializing row');
            row.dataset.comiteInitialized = 'true';

            const uniqueId = Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            const hiddenInput = row.querySelector('.tipo-participacion-hidden');
            const radioComite = row.querySelector('[data-radio-comite]');
            const radioJurado = row.querySelector('[data-radio-jurado]');
            const labelComite = row.querySelector('.comite-label');
            const labelJurado = row.querySelector('.jurado-label');

            // Defensive verification
            if (!hiddenInput) {
                console.warn('[Report] initComiteRow: Hidden input not found in row', row);
                return;
            }
            if (!radioComite || !radioJurado) {
                console.warn('[Report] initComiteRow: Radio buttons not found in row', row);
                return;
            }
            if (!labelComite || !labelJurado) {
                console.warn('[Report] initComiteRow: Labels not found in row', row);
                return;
            }

            // Generate unique IDs
            const comiteId = `tipoPartComite_${uniqueId}`;
            const juradoId = `tipoPartJurado_${uniqueId}`;
            const radioName = `participacion_radio_${uniqueId}`;

            // Set unique IDs and names
            radioComite.id = comiteId;
            radioComite.name = radioName;
            radioJurado.id = juradoId;
            radioJurado.name = radioName;

            // Link labels to inputs
            labelComite.setAttribute('for', comiteId);
            labelJurado.setAttribute('for', juradoId);

            // Sync with hidden input
            const syncHidden = () => {
                if (radioComite.checked) {
                    hiddenInput.value = 'comite';
                } else if (radioJurado.checked) {
                    hiddenInput.value = 'jurado';
                }
            };

            radioComite.addEventListener('change', syncHidden);
            radioJurado.addEventListener('change', syncHidden);

            // Initialize hidden input value
            syncHidden();
        }

        function initFinanceRow(row) {
            if (row.dataset.financeInitialized === 'true') return;
            row.dataset.financeInitialized = 'true';

            let participants = [];
            const hiddenInput = row.querySelector('.participantes-json');
            const listContainer = row.querySelector('.participantes-list');
            const btnAdd = row.querySelector('.btn-add-part');
            const inputName = row.querySelector('.part-name');
            const selectTipo = row.querySelector('.part-tipo');
            const inputInst = row.querySelector('.part-inst');

            if (!hiddenInput || !listContainer || !btnAdd) return;

            try {
                if (hiddenInput.value) {
                    participants = JSON.parse(hiddenInput.value);
                }
            } catch (e) {
                console.error("Error parsing participants JSON", e);
                participants = [];
            }

            const render = () => {
                listContainer.innerHTML = '';
                participants.forEach((p, index) => {
                    const badge = document.createElement('div');
                    badge.className = 'd-flex justify-content-between align-items-center bg-white border p-2 mb-1 rounded';
                    badge.innerHTML = `
                        <small><strong>${p.nombre}</strong> (${p.tipo}) - ${p.institucion}</small>
                        <button type="button" class="btn btn-sm text-danger remove-part-btn">&times;</button>
                    `;
                    
                    badge.querySelector('.remove-part-btn').addEventListener('click', () => {
                        participants.splice(index, 1);
                        update();
                    });
                    
                    listContainer.appendChild(badge);
                });
            };

            const update = () => {
                 hiddenInput.value = JSON.stringify(participants);
                 render();
            };

            btnAdd.addEventListener('click', () => {
                const nombre = inputName.value.trim();
                const tipo = selectTipo.value;
                const institucion = inputInst.value.trim();

                if (!nombre) return;

                participants.push({ nombre, tipo, institucion });
                inputName.value = '';
                inputInst.value = '';
                update();
            });

            render();
        }

        // ========================================
        // DYNAMIC ROWS ENGINE
        // ========================================
        function setupDynamicList(btnAddId, containerId, rowClass, onRowInit = null) {
            const container = document.getElementById(containerId);
            if (!container) return;

            const rows = container.getElementsByClassName(rowClass);
            
            // Store original template BEFORE any initialization
            if (rows.length > 0 && !originalTemplates[rowClass]) {
                originalTemplates[rowClass] = rows[0].cloneNode(true);
                console.log('[Report] Stored original template for:', rowClass);
            }

            // Initialize existing rows
            const existingRows = container.getElementsByClassName(rowClass);
            Array.from(existingRows).forEach((row, index) => {
                 const deleteBtn = row.querySelector('.delete-row-btn');
                 if (deleteBtn) {
                     // NEVER show delete on first row
                     deleteBtn.style.display = index === 0 ? 'none' : 'block';
                 }
                 
                 // Force initialization even if already initialized
                 if (onRowInit) {
                     // Clear flags to force re-init
                     delete row.dataset.comiteInitialized;
                     delete row.dataset.financeInitialized;
                     onRowInit(row);
                 }
            });

            // Note: Add button click is handled by global event delegation
        }

        // ========================================
        // INITIALIZATION
        // ========================================
        
        setupDynamicList('btnAddBook', 'librosContainer', 'dynamic-book-row');
        setupDynamicList('btnAddTesis', 'tesisContainer', 'dynamic-tesis-row');
        setupDynamicList('btnAddCurso', 'cursosContainer', 'dynamic-course-row');
        setupDynamicList('btnAddCongreso', 'congresoContainer', 'dynamic-congreso-row');
        setupDynamicList('btnAddEvento', 'eventoContainer', 'dynamic-evento-row');
        setupDynamicList('btnAddDivulgacion', 'divulgacionContainer', 'dynamic-divulgacion-row');
        setupDynamicList('btnAddEstancia', 'estanciaContainer', 'dynamic-estancia-row');
        setupDynamicList('btnAddComite', 'comitesContainer', 'dynamic-comite-row', initComiteRow);
        setupDynamicList('btnAddEstudiante', 'estudiantesContainer', 'dynamic-estudiante-row');
        setupDynamicList('btnAddFinance', 'financeContainer', 'dynamic-finance-row', initFinanceRow);

        // ========================================
        // FORM SUBMISSIONS
        // ========================================
        const forms = [
            { id: 'formularioCientifico', url: '/Panel/Reporte/libros/guardar', msg: 'Libros guardados' },
            { id: 'formularioGeneral3', url: '/Panel/Reporte/articulos/guardar', msg: 'Tesis guardadas' },
            { id: 'formularioCursos4', url: '/Panel/Reporte/cursos/guardar', msg: 'Cursos guardados' },
            { id: 'formComites', url: '/Panel/Reporte/comite/guardar', msg: 'Comités y Jurados guardados' },
            { id: 'formEstudiantes', url: '/Panel/Reporte/estudiantes/guardar', msg: 'Estudiantes guardados' },
            { id: 'formCongresos', url: '/Panel/Reporte/congresos/guardar', msg: 'Congresos guardados' },
            { id: 'formEventos', url: '/Panel/Reporte/eventos/guardar', msg: 'Eventos guardados' },
            { id: 'formularioDivulgacion', url: '/Panel/Reporte/divulgacion/guardar', msg: 'Divulgación guardada' },
            { id: 'formularioEstancia', url: '/Panel/Reporte/estancias/guardar', msg: 'Estancias guardadas' },
            { id: 'formularioFinanciacion', url: '/Panel/Reporte/financiacion/guardar', msg: 'Proyectos guardados' },
            { id: 'formularioPatente', url: '/Panel/Reporte/patentes/guardar', msg: 'Patentes guardadas' },
            { id: 'formularioComisiones', url: '/Panel/Reporte/comisiones/guardar', msg: 'Comisiones guardadas' },
            { id: 'formularioVinculacion', url: '/Panel/Reporte/vinculacion/guardar', msg: 'Vinculación guardada' },
            { id: 'formularioDistinciones', url: '/Panel/Reporte/distinciones/guardar', msg: 'Distinciones guardadas' },
            { id: 'formularioLogros', url: '/Panel/Reporte/logros/guardar', msg: 'Logros guardados' }
        ];

        forms.forEach(config => {
            const form = document.getElementById(config.id);
            if (form) {
                form.addEventListener('submit', function(e) {
                    e.preventDefault();
                    sendFormData(config.url, new FormData(this), config.msg);
                });
            }
        });

        // ========================================
        // LOAD FINANCIACION DATA
        // ========================================
        const loadFinanciacion = () => {
            const formFinanciacion = document.getElementById('formularioFinanciacion');
            if (!formFinanciacion) return;

            const container = document.getElementById('financeContainer');
            const clienteId = getClienteId();
            
            fetch(`/Panel/Reporte/financiacion/obtener?cliente_id=${clienteId}`)
            .then(res => res.json())
            .then(resp => {
                if (resp.status === 'success' && resp.data) {
                    const projects = Array.isArray(resp.data) ? resp.data : (resp.data ? [resp.data] : []);
                    const rows = container.getElementsByClassName('dynamic-finance-row');
                    if (rows.length === 0) return;
                    
                    const template = rows[0].cloneNode(true);
                    
                    if (projects.length > 0) {
                         projects.forEach((proj, idx) => {
                             let row;
                             if (idx === 0) {
                                 row = rows[0]; 
                             } else {
                                 row = template.cloneNode(true);
                                 container.appendChild(row);
                                 const delBtn = row.querySelector('.delete-row-btn');
                                 if (delBtn) delBtn.style.display = 'block';
                             }
                             
                             if (proj.tituloFinanciacion) row.querySelector('[name="tituloFinanciacion[]"]').value = proj.tituloFinanciacion;
                             if (proj.fuenteFinanciamiento) row.querySelector('[name="fuenteFinanciamiento[]"]').value = proj.fuenteFinanciamiento;
                             
                             const selClas = row.querySelector('[name="clasificacionFinanciacion[]"]');
                             if (selClas && proj.clasificacionFinanciacion) selClas.value = proj.clasificacionFinanciacion;
                             
                             const selIndole = row.querySelector('[name="indoleFinanciacion[]"]');
                             if (selIndole && proj.indoleFinanciacion) selIndole.value = proj.indoleFinanciacion;
                             
                             const hiddenJson = row.querySelector('.participantes-json');
                             let partList = [];
                             if (proj.participantesLista) {
                                 partList = Array.isArray(proj.participantesLista) ? proj.participantesLista : JSON.parse(proj.participantesLista || '[]');
                             }
                             hiddenJson.value = JSON.stringify(partList);
                             
                             initFinanceRow(row);
                         });
                    } else {
                        initFinanceRow(rows[0]);
                    }
                }
            })
            .catch(console.error);
        };

        loadFinanciacion();

        console.log('[Report] Initialization complete');
    }

    // ========================================
    // EVENT LISTENER: content:ready (from htmx-cleanup.js)
    // ========================================
    document.addEventListener('content:ready', function(evt) {
        const container = evt.detail.container;
        const reportContainer = container.querySelector('#Report');
        
        if (reportContainer) {
            console.log('[Report] content:ready event received, initializing...');
            initializeReport();
        }
    });

    // ========================================
    // FALLBACK: DOMContentLoaded for direct page loads
    // ========================================
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            const reportContainer = document.getElementById('Report');
            if (reportContainer) {
                console.log('[Report] DOMContentLoaded, initializing...');
                initializeReport();
            }
        });
    } else {
        // DOM already loaded
        const reportContainer = document.getElementById('Report');
        if (reportContainer) {
            console.log('[Report] DOM already loaded, initializing...');
            initializeReport();
        }
    }

    // ========================================
    // CENTRALIZED EVENT DELEGATION
    // ========================================
    document.addEventListener('click', function(e) {
        const target = e.target;
        
        // Handle add row buttons
        const addButtons = {
            'btnAddBook': { container: 'librosContainer', rowClass: 'dynamic-book-row' },
            'btnAddTesis': { container: 'tesisContainer', rowClass: 'dynamic-tesis-row' },
            'btnAddCurso': { container: 'cursosContainer', rowClass: 'dynamic-course-row' },
            'btnAddCongreso': { container: 'congresoContainer', rowClass: 'dynamic-congreso-row' },
            'btnAddEvento': { container: 'eventoContainer', rowClass: 'dynamic-evento-row' },
            'btnAddDivulgacion': { container: 'divulgacionContainer', rowClass: 'dynamic-divulgacion-row' },
            'btnAddEstancia': { container: 'estanciaContainer', rowClass: 'dynamic-estancia-row' },
            'btnAddComite': { container: 'comitesContainer', rowClass: 'dynamic-comite-row', init: 'comite' },
            'btnAddEstudiante': { container: 'estudiantesContainer', rowClass: 'dynamic-estudiante-row' },
            'btnAddFinance': { container: 'financeContainer', rowClass: 'dynamic-finance-row', init: 'finance' }
        };

        for (const [btnId, config] of Object.entries(addButtons)) {
            if (target.id === btnId || target.closest(`#${btnId}`)) {
                e.preventDefault();
                const container = document.getElementById(config.container);
                if (!container) continue;

                const rows = container.getElementsByClassName(config.rowClass);
                if (rows.length === 0) continue;

                // Use stored original template or fallback to first row
                const templateRow = originalTemplates[config.rowClass] || rows[0];
                const newRow = templateRow.cloneNode(true);
                
                // Clear initialization flags
                delete newRow.dataset.comiteInitialized;
                delete newRow.dataset.financeInitialized;
                
                // Clear inputs
                newRow.querySelectorAll('input, select, textarea').forEach(input => {
                    const type = input.type ? input.type.toLowerCase() : '';
                    if (type === 'radio' || type === 'checkbox') {
                        input.checked = input.defaultChecked || false;
                    } else if (type === 'hidden') {
                        if (input.classList.contains('participantes-json')) {
                            input.value = '[]';
                        } else if (input.classList.contains('tipo-participacion-hidden')) {
                            input.value = 'comite';
                        }
                    } else {
                        input.value = '';
                    }
                });

                // Clear visual lists
                newRow.querySelectorAll('.participantes-list').forEach(l => l.innerHTML = '');

                // Show delete button
                const deleteBtn = newRow.querySelector('.delete-row-btn');
                if (deleteBtn) {
                    deleteBtn.style.display = 'block';
                }
                
                container.appendChild(newRow);

                // Initialize row if needed
                if (config.init === 'comite') {
                    initComiteRow(newRow);
                } else if (config.init === 'finance') {
                    initFinanceRow(newRow);
                }

                return;
            }
        }

        // Handle delete row buttons
        if (target.matches('.delete-row-btn') || target.closest('.delete-row-btn')) {
            e.preventDefault();
            const row = target.closest('[class*="dynamic-"][class*="-row"]');
            if (row) row.remove();
            return;
        }
    });

    // ========================================
    // HTMX-AWARE INITIALIZATION
    // ========================================
    
    // Try immediate initialization (for direct page loads)
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeReport);
    } else {
        initializeReport();
    }

    console.log('[Report] Module loaded and ready');

})();
