const selectAllCheckbox = document.getElementById('select_all');

// Escuchar cambios
selectAllCheckbox.addEventListener('change', function() {
    // Obtener todos los checkboxes hijos
    const checkboxes = document.querySelectorAll('.all');
    checkboxes.forEach(cb => {
        cb.checked = selectAllCheckbox.checked;
    });
});