/**
 * Toast Notification Utility
 * Shows Bootstrap toast notifications instead of alerts
 */

function showToast(message, type = 'success') {
    const toastEl = document.getElementById('liveToast');
    const toastIcon = document.getElementById('toastIcon');
    const toastTitle = document.getElementById('toastTitle');
    const toastMessage = document.getElementById('toastMessage');
    const toastHeader = toastEl.querySelector('.toast-header');
    
    // Configure based on type
    const config = {
        success: {
            icon: 'bi-check-circle-fill text-success',
            title: 'Éxito',
            headerClass: 'bg-success text-white'
        },
        error: {
            icon: 'bi-x-circle-fill text-danger',
            title: 'Error',
            headerClass: 'bg-danger text-white'
        },
        warning: {
            icon: 'bi-exclamation-triangle-fill text-warning',
            title: 'Advertencia',
            headerClass: 'bg-warning text-dark'
        },
        info: {
            icon: 'bi-info-circle-fill text-info',
            title: 'Información',
            headerClass: 'bg-info text-white'
        }
    };
    
    const settings = config[type] || config.success;
    
    // Update toast content
    toastIcon.className = `bi me-2 ${settings.icon}`;
    toastTitle.textContent = settings.title;
    toastMessage.textContent = message;
    
    // Update header styling
    toastHeader.className = `toast-header ${settings.headerClass}`;
    
    // Show toast
    const toast = new bootstrap.Toast(toastEl, {
        autohide: true,
        delay: 3000
    });
    toast.show();
}

// Make it globally available
window.showToast = showToast;
