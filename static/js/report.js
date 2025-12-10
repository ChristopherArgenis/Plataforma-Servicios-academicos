document.addEventListener('DOMContentLoaded', function() {
    const reportContainer = document.getElementById('Report');
    if (reportContainer) {
        // Event Delegation for Report container
        reportContainer.addEventListener('click', function(event) {
            // Add Book Button
            const btnAddBook = event.target.closest('#btnAddBook');
            if (btnAddBook) {
                const librosContainer = document.getElementById('librosContainer');
                if (librosContainer) {
                    const rows = librosContainer.getElementsByClassName('dynamic-book-row');
                    if (rows.length > 0) {
                        const lastRow = rows[rows.length - 1];
                        const newRow = lastRow.cloneNode(true);
                        
                        // Clear inputs in the new row
                        const inputs = newRow.querySelectorAll('input');
                        inputs.forEach(input => {
                            input.value = '';
                        });

                        librosContainer.appendChild(newRow);
                    }
                }
            }

            // Open Save Books Modal
            const btnOpenSaveBooksModal = event.target.closest('#btnOpenSaveBooksModal');
            if (btnOpenSaveBooksModal) {
                console.log('Opening modal...'); // Debug
                const form = document.getElementById('formularioCientifico');
                const librosInputs = form.querySelectorAll('input[name="librosCientificos[]"]');
                const capitulosInputs = form.querySelectorAll('input[name="capitulosLibro[]"]');
                
                let countBooks = 0;
                let countChapters = 0;

                librosInputs.forEach(input => {
                    if (input.value.trim() !== '') countBooks++;
                });

                capitulosInputs.forEach(input => {
                    if (input.value.trim() !== '') countChapters++;
                });

                console.log('Books:', countBooks, 'Chapters:', countChapters); // Debug

                document.getElementById('countBooks').textContent = countBooks;
                document.getElementById('countChapters').textContent = countChapters;

                const modalEl = document.getElementById('confirmSaveBooksModal');
                if (modalEl && typeof bootstrap !== 'undefined') {
                    const modal = new bootstrap.Modal(modalEl);
                    modal.show();
                    
                    // Add event listener to confirm button when modal opens
                    setupConfirmButton();
                } else {
                    console.error('Modal element or Bootstrap not found');
                }
            }
        });
    } else {
        console.error('Report container not found');
    }
    
    // Setup confirm button handler (called when modal opens)
    function setupConfirmButton() {
        const btnConfirmSaveBooks = document.getElementById('btnConfirmSaveBooks');
        if (btnConfirmSaveBooks) {
            // Remove any existing listeners to avoid duplicates
            const newBtn = btnConfirmSaveBooks.cloneNode(true);
            btnConfirmSaveBooks.parentNode.replaceChild(newBtn, btnConfirmSaveBooks);
            
            // Add fresh event listener
            newBtn.addEventListener('click', function() {
                console.log('Confirm button clicked!'); // Debug
                const form = document.getElementById('formularioCientifico');
                const formData = new FormData(form);

                console.log('Sending data to server...'); // Debug
                fetch('/save_books', {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    console.log('Response received:', response); // Debug
                    return response.json();
                })
                .then(data => {
                    console.log('Data:', data); // Debug
                    if (data.status === 'success') {
                        console.log('Success! Clearing form and closing modal...'); // Debug
                        
                        // Close modal FIRST
                        const modalEl = document.getElementById('confirmSaveBooksModal');
                        if (modalEl) {
                            const modal = bootstrap.Modal.getInstance(modalEl);
                            if (modal) {
                                modal.hide();
                                console.log('Modal hidden'); // Debug
                            }
                        }
                        
                        // Wait a bit for modal to close, then clear form
                        setTimeout(() => {
                            // Clear form
                            const form = document.getElementById('formularioCientifico');
                            if (form) {
                                form.reset();
                                console.log('Form reset'); // Debug
                            }
                            
                            // Remove extra rows, keep only one
                            const librosContainer = document.getElementById('librosContainer');
                            if (librosContainer) {
                                const rows = librosContainer.getElementsByClassName('dynamic-book-row');
                                while (rows.length > 1) {
                                    librosContainer.removeChild(rows[rows.length - 1]);
                                }
                                console.log('Extra rows removed, rows remaining:', rows.length); // Debug
                            }
                            
                            console.log('All cleanup completed!'); // Debug
                        }, 300);
                    }
                })
                .catch(error => console.error('Error:', error));
            });
            
            console.log('Confirm button listener attached'); // Debug
        } else {
            console.error('Confirm button not found');
        }
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

    // === COMITES Y JURADO LOGIC ===
    const tipoParticipacionRadios = document.querySelectorAll('input[name="tipoParticipacion"]');
    
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
        
        // Common fields are shown for Comite and Jurado, hidden for Estudiantes (based on my assumption in plan)
        if (commonFields) {
            if (value === 'estudiantes') {
                commonFields.style.display = 'none';
            } else {
                commonFields.style.display = 'block'; // using block? or flex? default is block usually for div
                // or restore previous display style? block is safe for div
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

    // Listener
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
                    
                    // Clear input in the new row
                    const input = newRow.querySelector('input');
                    if (input) input.value = '';

                    estudiantesContainer.appendChild(newRow);
                }
            }
        });
    }
});
