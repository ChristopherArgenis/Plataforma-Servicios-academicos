document.addEventListener('DOMContentLoaded', function() {
    const reportContainer = document.getElementById('Report');
    if (!reportContainer) {
        console.error('Report container not found');
        return;
    }

    // ========================================
    // LIBROS SECTION - Clean Implementation
    // ========================================
    
    const btnAddBook = document.getElementById('btnAddBook');
    const btnSaveLibros = document.getElementById('btnSaveLibros');
    const librosContainer = document.getElementById('librosContainer');
    const formLibros = document.getElementById('formularioCientifico');
    
    // Add new book row
    if (btnAddBook) {
        btnAddBook.addEventListener('click', function() {
            if (!librosContainer) return;
            
            const rows = librosContainer.querySelectorAll('.dynamic-book-row');
            if (rows.length === 0) return;
            
            // Clone last row
            const lastRow = rows[rows.length - 1];
            const newRow = lastRow.cloneNode(true);
            
            // Clear all inputs
            newRow.querySelectorAll('input').forEach(input => {
                input.value = '';
            });
            
            // Append new row
            librosContainer.appendChild(newRow);
        });
    }
    
    // Save Libros
    if (btnSaveLibros) {
        btnSaveLibros.addEventListener('click', function() {
            if (!formLibros) return;
            
            // Get cliente_id
            const clienteId = reportContainer.dataset.clienteId;
            if (!clienteId) {
                showToast('Error: Cliente ID no encontrado', 'error');
                return;
            }
            
            // Collect data from form
            const formData = new FormData(formLibros);
            
            // Get all books and chapters (arrays)
            const libros = formData.getAll('librosCientificos[]').filter(v => v.trim() !== '');
            const capitulos = formData.getAll('capitulosLibro[]').filter(v => v.trim() !== '');
            
            // Validate at least one entry
            if (libros.length === 0 && capitulos.length === 0) {
                showToast('Debe agregar al menos un libro o capítulo', 'warning');
                return;
            }
            
            // Prepare payload
            const payload = {
                cliente_id: clienteId,
                data: {
                    libros_cientificos: libros,
                    capitulos_libro: capitulos
                }
            };
            
            // Send to server
            fetch('/Panel/Reporte/libros/guardar', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    showToast('Libros guardados correctamente', 'success');
                    
                    // Clear form
                    formLibros.reset();
                    
                    // Remove extra rows, keep only first
                    const rows = librosContainer.querySelectorAll('.dynamic-book-row');
                    for (let i = rows.length - 1; i > 0; i--) {
                        rows[i].remove();
                    }
                } else {
                    showToast('Error: ' + data.message, 'error');
                }
            })
            .catch(err => {
                console.error('Error saving libros:', err);
                showToast('Error de conexión al guardar', 'error');
            });
        });
    }

    // === DIFUSION LOGIC ===
    
    // Toggle between Congreso and Evento fields
    const tipoDifusionRadios = document.querySelectorAll('input[name="tipoDifusion"]');
    tipoDifusionRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            const congresoFields = document.getElementById('congresoFields');
            const eventoFields = document.getElementById('eventoFields');
            
            if (this.value === 'congreso') {
                if (congresoFields) congresoFields.style.display = 'block';
                if (eventoFields) eventoFields.style.display = 'none';
            } else if (this.value === 'evento') {
                if (congresoFields) congresoFields.style.display = 'none';
                if (eventoFields) eventoFields.style.display = 'block';
            }
        });
    });

    // === COMITES LOGIC ===
    const subapartadoComiteRadios = document.querySelectorAll('input[name="subapartadoComite"]');
    subapartadoComiteRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            const comiteTesisInputs = document.getElementById('comiteTesisInputs');
            if (this.value === 'tesis') {
                if (comiteTesisInputs) comiteTesisInputs.style.display = 'block';
            } else {
                if (comiteTesisInputs) comiteTesisInputs.style.display = 'none';
            }
        });
    });

    // Function to handle visibility
    function toggleParticipacionFields(value) {
        const comiteFields = document.getElementById('comiteFields');
        const juradoFields = document.getElementById('juradoFields');
        const commonFields = document.getElementById('commonFields');
        const estudiantesFields = document.getElementById('estudiantesFields');
        
        // Hide all first
        if (comiteFields) comiteFields.style.display = 'none';
        if (juradoFields) juradoFields.style.display = 'none';
        if (estudiantesFields) estudiantesFields.style.display = 'none';
        
        if (commonFields) {
            if (value === 'estudiantes') {
                commonFields.style.display = 'none';
            } else {
                commonFields.style.display = 'block'; 
            }
        }

        if (value === 'comite') {
            if (comiteFields) comiteFields.style.display = 'block';
        } else if (value === 'jurado') {
            if (juradoFields) juradoFields.style.display = 'block';
        } else if (value === 'estudiantes') {
            if (estudiantesFields) estudiantesFields.style.display = 'block';
        }
    }

    // Initial check
    const checkedParticipacion = document.querySelector('input[name="tipoParticipacion"]:checked');
    if (checkedParticipacion) {
        toggleParticipacionFields(checkedParticipacion.value);
    }

    const tipoParticipacionRadios = document.querySelectorAll('input[name="tipoParticipacion"]');
    tipoParticipacionRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            toggleParticipacionFields(this.value);
        });
    });

    // === ESTUDIANTES SUB-LOGIC ===
    const tipoEstudianteRadios = document.querySelectorAll('input[name="tipoEstudiante"]');
    tipoEstudianteRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            const proyectoFields = document.getElementById('proyectoFields');
            const servicioFields = document.getElementById('servicioFields');
            
            if (this.value === 'proyecto') {
                if (proyectoFields) proyectoFields.style.display = 'block';
                if (servicioFields) servicioFields.style.display = 'none';
            } else if (this.value === 'servicio') {
                if (proyectoFields) proyectoFields.style.display = 'none';
                if (servicioFields) servicioFields.style.display = 'block';
            }
        });
    });

    // Add students dynamically
    const btnAddStudent = document.getElementById('btnAddStudent');
    if (btnAddStudent) {
        btnAddStudent.addEventListener('click', function() {
            const estudiantesContainer = document.getElementById('estudiantesContainer');
            if (estudiantesContainer) {
                const rows = estudiantesContainer.getElementsByClassName('dynamic-student-row');
                if (rows.length > 0) {
                    const lastRow = rows[rows.length - 1];
                    const newRow = lastRow.cloneNode(true);
                    const input = newRow.querySelector('input');
                    if (input) input.value = '';
                    estudiantesContainer.appendChild(newRow);
                }
            }
        });
    }

    // === FINANCIADOS PARTICIPANTS LOGIC ===
    let participantesFinanciacion = [];
    const btnAddPartFin = document.getElementById('btnAddPartFin');
    
    // Render Function
    function renderParticipantesFin() {
        const container = document.getElementById('participantesFinList');
        if (!container) return;
        container.innerHTML = '';
        
        participantesFinanciacion.forEach((p, index) => {
            const item = document.createElement('div');
            item.className = 'd-flex justify-content-between align-items-center bg-white p-2 mb-2 rounded border shadow-sm';
            item.innerHTML = `
                <div>
                    <span class="fw-bold text-primary">${p.nombre}</span>
                    <small class="text-muted mx-2">|</small>
                    <span class="text-secondary small">${p.tipo}</span>
                    <small class="text-muted mx-2">|</small>
                    <span class="text-dark small">${p.institucion}</span>
                </div>
                <button type="button" class="btn btn-outline-danger btn-sm border-0" onclick="removeParticipanteFin(${index})">
                    <i class="bi bi-trash"></i>
                </button>
            `;
            container.appendChild(item);
        });
    }
    
    // Expose remove function globally
    window.removeParticipanteFin = function(index) {
        participantesFinanciacion.splice(index, 1);
        renderParticipantesFin();
    };

    if (btnAddPartFin) {
        btnAddPartFin.addEventListener('click', function() {
           const nameInput = document.getElementById('partFinName');
           const instInput = document.getElementById('partFinInst');
           const typeInput = document.querySelector('input[name="tipoPartFin"]:checked');
           
           if (!nameInput.value.trim()) {
               alert('El nombre es requerido');
               return;
           }
           if (!typeInput) {
               alert('Seleccione un tipo (Académico/Estudiante)');
               return;
           }
           
           const participante = {
               nombre: nameInput.value.trim(),
               tipo: typeInput.value, // Academico or Estudiante
               institucion: instInput.value.trim() || 'N/A'
           };
           
           participantesFinanciacion.push(participante);
           renderParticipantesFin();
           
           // Clear inputs
           nameInput.value = '';
           instInput.value = '';
           // Don't clear radio? better UX to keep it or reset? Resetting is safer.
           typeInput.checked = false; 
        });
    }

    // === DYNAMIC LISTS LOGIC (Generic) ===
    function setupDynamicList(btnAddId, containerId, rowClass) {
        const btnAdd = document.getElementById(btnAddId);
        if (btnAdd) {
            btnAdd.addEventListener('click', function() {
                const container = document.getElementById(containerId);
                if (container) {
                    const rows = container.getElementsByClassName(rowClass);
                    if (rows.length > 0) {
                        const lastRow = rows[rows.length - 1];
                        const newRow = lastRow.cloneNode(true);
                        
                        // Clear inputs
                        const inputs = newRow.querySelectorAll('input, select');
                        inputs.forEach(input => input.value = '');

                        // Show delete button for new row
                        const deleteBtn = newRow.querySelector('.delete-row-btn');
                        if (deleteBtn) {
                            deleteBtn.style.display = 'block';
                            // Add listener to new delete button
                            deleteBtn.addEventListener('click', function() {
                                newRow.remove();
                            });
                        }

                        container.appendChild(newRow);
                        
                        // Ensure first row also has delete button if there are > 1 rows?
                        // Or just show delete button for ANY row if count > 1?
                        // Simple approach: Always show delete on cloned rows.
                        // Ideally, if we have > 1 row, all should be deletable? 
                        // Let's keep it simple: Clone adds a row with a working delete button.
                        // First row delete button is initially hidden. We can enable it if count > 1.
                        updateDeleteButtons(container, rowClass);
                    }
                }
            });
        }
    }

    function updateDeleteButtons(container, rowClass) {
        const rows = container.getElementsByClassName(rowClass);
        Array.from(rows).forEach((row, index) => {
            const deleteBtn = row.querySelector('.delete-row-btn');
            if (deleteBtn) {
                // If only 1 row, hide delete. Else show.
                deleteBtn.style.display = rows.length > 1 ? 'block' : 'none';
                // Ensure listener is attached (might duplicate if not careful, but cloneNode doesn't copy dynamic listeners)
                // Better: rely on event delegation or attach only on creation.
                // Since this runs on "Add", we can just set display.
                // The cleaner way:
                deleteBtn.onclick = function() {
                   if (container.getElementsByClassName(rowClass).length > 1) {
                       row.remove();
                       updateDeleteButtons(container, rowClass);
                   }
                };
            }
        });
    }

    setupDynamicList('btnAddTesis', 'tesisContainer', 'dynamic-tesis-row');
    setupDynamicList('btnAddCurso', 'cursosContainer', 'dynamic-course-row');
    
    // Difusión section
    setupDynamicList('btnAddCongreso', 'congresoContainer', 'dynamic-congreso-row');
    setupDynamicList('btnAddEvento', 'eventoContainer', 'dynamic-evento-row');
    
    // Comités section
    setupDynamicList('btnAddComite', 'comitesContainer', 'dynamic-comite-row');
    setupDynamicList('btnAddEstudiante', 'estudiantesContainer', 'dynamic-estudiante-row');
    
    // Divulgación section
    setupDynamicList('btnAddDivulgacion', 'divulgacionContainer', 'dynamic-divulgacion-row');
    
    // Estancias section
    setupDynamicList('btnAddEstancia', 'estanciaContainer', 'dynamic-estancia-row');


    // === GLOBAL FORM SUBMISSION HANDLERS ===
    
    // 1. SAVE LIBROS (Existing) - Logic in setupConfirmButton

    // 2. SAVE TESIS/DOCENCIA (Step 2 - "Articulos") -> Now Multiple
    const formTesis = document.getElementById('formularioGeneral3');
    if (formTesis) {
        formTesis.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            // Collect arrays
            const titulos = formData.getAll('tituloTesis3[]');
            const grados = formData.getAll('grado3[]');
            const estudiantes = formData.getAll('estudiante3[]');
            const instituciones = formData.getAll('institucion3[]');
            const estatus = formData.getAll('estatus3[]');

            // Construct JSON payload
            // We'll send arrays. The backend should handle converting to JSON string if needed.
            const data = {
                titulo: titulos,
                nivel: grados, 
                nombre_estudiante: estudiantes,
                institucion: instituciones,
                estatus: estatus
            };
            // Note: If fields are empty, arrays might have empty strings.
             sendReportData('/Panel/Reporte/articulos/guardar', data, 'Tesis guardada');
        });
    }

    // 3. SAVE CURSOS (Step 3)
    const formCursos = document.getElementById('formularioCursos4'); 
    if (formCursos) {
        formCursos.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const data = {
                materia: formData.getAll('materia4[]'),
                nivel: formData.getAll('nivel4[]'),
                periodo: formData.getAll('periodo4[]'),
                institucion: formData.getAll('institucion4[]'),
                programas: formData.getAll('programas4[]')
            };
            sendReportData('/Panel/Reporte/cursos/guardar', data, 'Cursos guardados');
        });
    }

    // 4. SAVE COMITES (Step 4)
    const formComites = document.getElementById('formularioComites');
    if (formComites) {
        formComites.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const tipo = formData.get('tipoParticipacion');
            
            let data = {
                tipo_participacion: tipo,
                nivel_academico: formData.get('nivelAcademico'),
                programa_posgrado: formData.get('programaPosgrado')
            };

            if (tipo === 'comite') {
                const sub = formData.get('subapartadoComite');
                data.participacion = `Comité - ${sub || 'General'}`;
                data.titulo_tesis = formData.get('tituloTesisComite');
                data.nombre_estudiante = formData.get('estudianteComite');
            } else if (tipo === 'jurado') {
                data.participacion = 'Jurado - Examen de Grado';
                data.titulo_tesis = formData.get('tituloTesisJurado');
                data.nombre_estudiante = formData.get('estudianteJurado');
            } else if (tipo === 'estudiantes') {
                 const subTipo = formData.get('tipoEstudiante');
                 const estData = {
                     nombre: formData.get('nombreEstudianteParticipacion'), 
                     actividad: subTipo, 
                     titulo_proyecto: formData.get('tituloProyectoEstudiante'),
                     procedencia: formData.get('procedenciaServicio') // Ensure this field exists if used
                 };
                 
                 if(subTipo === 'proyecto') {
                     estData.actividad = `Proyecto: ${formData.get('nivelProyecto')}`;
                     estData.titulo_proyecto = formData.get('tituloProyectoEstudiante');
                 } else {
                     estData.actividad = 'Servicio Social';
                     estData.procedencia = formData.get('procedenciaServicio');
                 }
                 
                 sendReportData('/Panel/Reporte/estudiantes/guardar', estData, 'Estudiante guardado');
                 return; 
            }
            
            sendReportData('/Panel/Reporte/comite/guardar', data, 'Participación guardada');
        });
    }

    // 5. SAVE FINANCIADOS
    const formFinanciacion = document.getElementById('formularioFinanciacion');
    if (formFinanciacion) {
        formFinanciacion.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const data = {
                tituloFinanciacion: formData.get('tituloFinanciacion'),
                fuenteFinanciamiento: formData.get('fuenteFinanciamiento'),
                clasificacionFinanciacion: formData.get('clasificacionFinanciacion'),
                indoleFinanciacion: formData.get('indoleFinanciacion'),
                participantesLista: participantesFinanciacion
            };
            sendReportData('/Panel/Reporte/financiacion/guardar', data, 'Financiación guardada');
        });
    }

    // === SIMPLE SECTIONS SAVE LOGIC ===
    
    // 6. SAVE PATENTE (Step 7)
    const formPatente = document.getElementById('formularioPatente');
    if (formPatente) {
        formPatente.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const data = {
                descripcion: formData.get('descripcion')
            };
            sendReportData('/Panel/Reporte/patentes/guardar', data, 'Patente guardada');
        });
    }

    // 7. SAVE COMISIONES (Step 10)
    const formComisiones = document.getElementById('formularioComisiones');
    if (formComisiones) {
        formComisiones.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const data = {
                descripcion: formData.get('descripcion')
            };
            sendReportData('/Panel/Reporte/comisiones/guardar', data, 'Comisión guardada');
        });
    }

    // 8. SAVE VINCULACION (Step 11)
    const formVinculacion = document.getElementById('formularioVinculacion');
    if (formVinculacion) {
        formVinculacion.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const data = {
                descripcion: formData.get('descripcion')
            };
            sendReportData('/Panel/Reporte/vinculacion/guardar', data, 'Vinculación guardada');
        });
    }

    // 9. SAVE DISTINCIONES (Step 12)
    const formDistinciones = document.getElementById('formularioDistinciones');
    if (formDistinciones) {
        formDistinciones.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const data = {
                descripcion: formData.get('descripcion')
            };
            sendReportData('/Panel/Reporte/distinciones/guardar', data, 'Distinción guardada');
        });
    }

    // 10. SAVE LOGROS (Step 13)
    const formLogros = document.getElementById('formularioLogros');
    if (formLogros) {
        formLogros.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const data = {
                descripcion: formData.get('descripcion')
            };
            sendReportData('/Panel/Reporte/logros/guardar', data, 'Logro guardado');
        });
    }

    // === helper functions
    function sendReportData(url, dataObject, successMessage) {
        const clienteId = document.getElementById('Report')?.dataset.clienteId;
        if (!clienteId) {
            showToast('Error: Cliente ID no encontrado', 'error');
            return;
        }

        const payload = {
            cliente_id: clienteId,
            data: dataObject
        };

        fetch(url, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                showToast(successMessage || 'Guardado correctamente', 'success');
            } else {
                showToast('Error al guardar: ' + data.message, 'error');
            }
        })
        .catch(err => {
            console.error(err);
            showToast('Error de red al guardar', 'error');
        });
    }
});
