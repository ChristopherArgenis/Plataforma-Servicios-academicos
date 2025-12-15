document.addEventListener('DOMContentLoaded', function() {
    const reportContainer = document.getElementById('Report');
    if (!reportContainer) return;

    const getClienteId = () => reportContainer.dataset.clienteId;

    // Estado local para participantes de Financiación
    let participantesFinanciacion = [];

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
            showNotification('Error: Cliente ID no encontrado', 'error');
            return;
        }

        // Ensure cliente_id is in FormData
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
    // DYNAMIC ROWS LOGIC
    // ========================================
    function setupDynamicList(btnAddId, containerId, rowClass) {
        const btnAdd = document.getElementById(btnAddId);
        if (btnAdd) {
            btnAdd.addEventListener('click', function() {
                const container = document.getElementById(containerId);
                if (container) {
                    const rows = container.getElementsByClassName(rowClass);
                    if (rows.length > 0) {
                        const templateRow = rows[0]; 
                        const newRow = templateRow.cloneNode(true);
                        
                        // Clear inputs
                        newRow.querySelectorAll('input, select, textarea').forEach(input => {
                            // Don't clear radio buttons/checkboxes 'checked' status here immediately or set default?
                            // For text/select:
                            if (input.type !== 'hidden' && input.type !== 'radio' && input.type !== 'checkbox') {
                                input.value = '';
                            }
                        });

                        // Fix Radio Button IDs to be unique
                        const timestamp = new Date().getTime();
                        newRow.querySelectorAll('input[type="radio"]').forEach((radio, idx) => {
                            const oldId = radio.id;
                            const newId = oldId + '_' + timestamp + '_' + idx;
                            radio.id = newId;
                            
                            // Find corresponding label
                            const label = newRow.querySelector(`label[for="${oldId}"]`);
                            if (label) {
                                label.setAttribute('for', newId);
                            }
                            
                            // Reset selection to default (e.g. Comite) if needed
                            if (radio.value === 'comite') radio.checked = true;
                            else radio.checked = false;
                        });

                        // Show delete button
                        const deleteBtn = newRow.querySelector('.delete-row-btn');
                        if (deleteBtn) {
                            deleteBtn.style.display = 'block';
                            deleteBtn.onclick = () => newRow.remove();
                        }
                        
                        container.appendChild(newRow);
                    }
                }
            });
        }
    }

    // Initialize all dynamic sections
    const sections = [
        { btn: 'btnAddTesis', container: 'tesisContainer', row: 'dynamic-tesis-row' },
        { btn: 'btnAddCurso', container: 'cursosContainer', row: 'dynamic-course-row' },
        
        // Difusion
        { btn: 'btnAddCongreso', container: 'congresoContainer', row: 'dynamic-congreso-row' },
        { btn: 'btnAddEvento', container: 'eventoContainer', row: 'dynamic-evento-row' },
        
        // Comites (Unificado)
        { btn: 'btnAddComite', container: 'comitesContainer', row: 'dynamic-comite-row' },
        // Jurados removed (handled by Comites)
        
        { btn: 'btnAddEstudiante', container: 'estudiantesContainer', row: 'dynamic-estudiante-row' },
        
        { btn: 'btnAddDivulgacion', container: 'divulgacionContainer', row: 'dynamic-divulgacion-row' },
        { btn: 'btnAddEstancia', container: 'estanciaContainer', row: 'dynamic-estancia-row' }
    ];

    sections.forEach(config => setupDynamicList(config.btn, config.container, config.row));

    // Libros Special Case
    const btnAddBook = document.getElementById('btnAddBook');
    if (btnAddBook) {
        btnAddBook.addEventListener('click', function() {
            const container = document.getElementById('librosContainer');
            if (container) {
                const rows = container.getElementsByClassName('dynamic-book-row');
                if (rows.length > 0) {
                    const newRow = rows[0].cloneNode(true);
                    newRow.querySelectorAll('input').forEach(i => i.value = '');
                     const deleteBtn = newRow.querySelector('.delete-row-btn');
                    if (deleteBtn) {
                        deleteBtn.style.display = 'block';
                        deleteBtn.onclick = () => newRow.remove();
                    }
                    container.appendChild(newRow);
                }
            }
        });
    }

    // ========================================
    // FORM SUBMISSIONS
    // ========================================
    const forms = [
        { id: 'formularioCientifico', url: '/Panel/Reporte/libros/guardar', msg: 'Libros guardados' },
        { id: 'formularioGeneral3', url: '/Panel/Reporte/articulos/guardar', msg: 'Tesis guardadas' },
        { id: 'formularioCursos4', url: '/Panel/Reporte/cursos/guardar', msg: 'Cursos guardados' },
        
        // Comites (Unificado)
        { id: 'formComites', url: '/Panel/Reporte/comite/guardar', msg: 'Comités y Jurados guardados' },
        { id: 'formEstudiantes', url: '/Panel/Reporte/estudiantes/guardar', msg: 'Estudiantes guardados' },
        
        { id: 'formCongresos', url: '/Panel/Reporte/congresos/guardar', msg: 'Congresos guardados' },
        { id: 'formEventos', url: '/Panel/Reporte/eventos/guardar', msg: 'Eventos guardados' },
        
        { id: 'formularioDivulgacion', url: '/Panel/Reporte/divulgacion/guardar', msg: 'Divulgación guardada' },
        { id: 'formularioEstancia', url: '/Panel/Reporte/estancias/guardar', msg: 'Estancias guardadas' },
        
        // Simples
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
    // FINANCIAMIENTO LOGIC
    // ========================================
    
    function renderParticipantes() {
        const container = document.getElementById('participantesFinList');
        if (!container) return;
        
        container.innerHTML = '';
        participantesFinanciacion.forEach((p, index) => {
            const badge = document.createElement('div');
            badge.className = 'd-flex justify-content-between align-items-center bg-white border p-2 mb-1 rounded';
            badge.innerHTML = `
                <small><strong>${p.nombre}</strong> (${p.tipo}) - ${p.institucion}</small>
                <button type="button" class="btn btn-sm text-danger remove-part-btn" data-index="${index}">&times;</button>
            `;
            container.appendChild(badge);
        });

        // Add listeners to remove buttons
        container.querySelectorAll('.remove-part-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const idx = parseInt(this.dataset.index);
                participantesFinanciacion.splice(idx, 1);
                renderParticipantes();
            });
        });
    }

    const btnAddPartFin = document.getElementById('btnAddPartFin');
    if (btnAddPartFin) {
        btnAddPartFin.addEventListener('click', function() {
            const nameInput = document.getElementById('partFinName');
            const instInput = document.getElementById('partFinInst');
            
            // Get selected radio
            const tipoRadio = document.querySelector('input[name="tipoPartFin"]:checked');
            const tipo = tipoRadio ? tipoRadio.value : 'N/A';

            if (nameInput && nameInput.value.trim() !== '') {
                participantesFinanciacion.push({
                    nombre: nameInput.value.trim(),
                    tipo: tipo,
                    institucion: instInput ? instInput.value.trim() : ''
                });
                
                nameInput.value = '';
                if (instInput) instInput.value = '';
                renderParticipantes();
            }
        });
    }

    // Financiación Submit
    const formFinanciacion = document.getElementById('formularioFinanciacion');
    if (formFinanciacion) {
        formFinanciacion.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            // Append attributes as JSON string
            formData.append('participantesLista', JSON.stringify(participantesFinanciacion));
            sendFormData('/Panel/Reporte/financiacion/guardar', formData, 'Proyecto de Financiación guardado');
        });
    }

    // Load Financiados Data
    const loadFinanciacion = () => {
        const clienteId = getClienteId();
        if (!clienteId) return;

        fetch(`/Panel/Reporte/financiacion/obtener?cliente_id=${clienteId}`)
        .then(res => res.json())
        .then(resp => {
            if (resp.status === 'success' && resp.data) {
                const d = resp.data;
                // Fill fields
                const inputs = {
                    'tituloFinanciacion': d.tituloFinanciacion,
                    'fuenteFinanciamiento': d.fuenteFinanciamiento,
                    'clasificacionFinanciacion': d.clasificacionFinanciacion,
                    'indoleFinanciacion': d.indoleFinanciacion
                };
                
                for (const [name, val] of Object.entries(inputs)) {
                    const el = formFinanciacion.querySelector(`[name="${name}"]`);
                    if (el && val) el.value = val;
                }

                // Fill list
                // Aseguramos que sea array. Si es string (fallback), parseamos?
                // Backend ya lo envía parseado en 'participantesLista' (ver ReportService.obtener)
                if (d.participantesLista && Array.isArray(d.participantesLista)) {
                    participantesFinanciacion = d.participantesLista;
                    renderParticipantes();
                } else if (typeof d.participantesLista === 'string') {
                     // Fallback raro
                     try {
                        participantesFinanciacion = JSON.parse(d.participantesLista);
                        renderParticipantes();
                     } catch(e) {}
                }
            }
        })
        .catch(console.error);
    };

    // Load on init if form exists
    if (formFinanciacion) {
        loadFinanciacion();
    }

});
