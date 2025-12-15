document.addEventListener('DOMContentLoaded', function() {
    // === NAME EDIT LOGIC ===
    const btnEditName = document.getElementById('btnEditName');
    const userNameDisplay = document.getElementById('userNameDisplay');
    const userInputContainer = document.getElementById('userInputContainer');
    const userNameInput = document.getElementById('userNameInput');
    let isEditingName = false;

    if (btnEditName) {
        btnEditName.addEventListener('click', function() {
            if (!isEditingName) {
                // Switch to Edit Mode
                userNameDisplay.style.display = 'none';
                userInputContainer.style.display = 'block';
                userNameInput.focus();
                this.innerHTML = '<i class="bi bi-save"></i>';
                this.classList.remove('btn-outline-secondary');
                this.classList.add('btn-success', 'text-white');
                isEditingName = true;
            } else {
                // Save Changes
                const newName = userNameInput.value.trim();
                if (!newName) {
                    showToast('El nombre no puede estar vacío', 'warning');
                    return;
                }
                
                // AJAX call to save
                fetch('/Panel/Info/UpdateName', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ nombre: newName })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.status === 'success') {
                        userNameDisplay.textContent = newName;
                        // Switch back to View Mode
                        userNameDisplay.style.display = 'block';
                        userInputContainer.style.display = 'none';
                        btnEditName.innerHTML = '<i class="bi bi-pencil-fill"></i>';
                        btnEditName.classList.remove('btn-success', 'text-white');
                        btnEditName.classList.add('btn-outline-secondary');
                        isEditingName = false;
                        showToast('Nombre actualizado correctamente', 'success');
                    } else {
                        showToast('Error: ' + data.message, 'error');
                    }
                })
                .catch(err => {
                    console.error(err);
                    showToast('Error de conexión', 'error');
                });
            }
        });
    }
});
