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
});
