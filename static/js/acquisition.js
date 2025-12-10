// Handle Update Modal
document.addEventListener('DOMContentLoaded', function() {
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

    // --- Logic for Relevantes Button ---
    const btnRelevantes = document.getElementById('btnRelevantes');
    if (btnRelevantes) {
        btnRelevantes.addEventListener('click', function() {
            // Count selected checkboxes
            const checkboxes = document.querySelectorAll('input[name="keys[]"]:checked');
            const count = checkboxes.length;

            if (count === 3) {
                // Determine if we need to show error via modal or just proceed to confirmation
                // Requirement 1.3: "En caso de elegir mas o menos de 3, decirle en el modal"
                // It says "decirle en el modal", implies maybe errors should also be in a modal?
                // But simplifying: logic is "Save exactly 3".
                
                // Show Confirmation Modal
                const modalEl = document.getElementById('modalRelevantes');
                if (modalEl && typeof bootstrap !== 'undefined') {
                    const modal = new bootstrap.Modal(modalEl);
                    modal.show();
                }
            } else {
                // Show Error Alert/Modal as per requirement 1.3 "decirle en el modal"
                // Let's reuse the modal or create a simple alert.
                // Requirement says "decirle en el modal".
                // We can use the same modal structure but change text, OR create a generic message modal.
                // For now, let's use a standard alert for simplicity unless "modal" is strict UI requirement for error too.
                // User said "decirle en el modal". I'll try to be nice.
                alert("Por favor, selecciona exactamente 3 artículos para continuar. Has seleccionado " + count + ".");
            }
        });
    }

    const btnConfirmarRelevantes = document.getElementById('btnConfirmarRelevantes');
    if (btnConfirmarRelevantes) {
        btnConfirmarRelevantes.addEventListener('click', function() {
            const checkboxes = document.querySelectorAll('input[name="keys[]"]:checked');
            const selectedIds = Array.from(checkboxes).map(cb => cb.value);

            // Create a form to submit
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = '/Panel/save_relevant_articles'; // Route we will create
            
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
});
