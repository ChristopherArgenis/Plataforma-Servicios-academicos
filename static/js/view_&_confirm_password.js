document.addEventListener('DOMContentLoaded', () => {
  // Tab Switching Logic
  const loginTab = document.getElementById("loginTab");
  const registerTab = document.getElementById("registerTab");
  const loginForm = document.getElementById("loginForm");
  const registerForm = document.getElementById("registerForm");

  if (loginTab && registerTab && loginForm && registerForm) {
    loginTab.addEventListener("click", () => {
      loginTab.classList.add("active");
      registerTab.classList.remove("active");
      loginForm.style.display = "block";
      registerForm.style.display = "none";
    });

    registerTab.addEventListener("click", () => {
      registerTab.classList.add("active");
      loginTab.classList.remove("active");
      loginForm.style.display = "none";
      registerForm.style.display = "block";
    });
  }

  // Password Toggle Logic
  function togglePassword(inputId, buttonId) {
    const input = document.getElementById(inputId);
    const button = document.getElementById(buttonId);
    const icon = button.querySelector("i");

    if (input && button && icon) {
      button.addEventListener("click", () => {
        const type = input.getAttribute("type") === "password" ? "text" : "password";
        input.setAttribute("type", type);
        icon.classList.toggle("bi-eye");
        icon.classList.toggle("bi-eye-slash");
      });
    }
  }

  // Initialize Toggles
  togglePassword("loginPassword", "toggleLoginPassword");
  togglePassword("loginConfirmPassword", "toggleLoginConfirmPassword");
  togglePassword("registerPassword", "toggleRegisterPassword");
  togglePassword("registerConfirmPassword", "toggleRegisterConfirmPassword");

  // Password Matching Logic
  function checkPasswords(passId, confirmId, buttonId, warningId) {
    const pass = document.getElementById(passId);
    const confirm = document.getElementById(confirmId);
    const button = document.getElementById(buttonId);
    const warning = document.getElementById(warningId);

    if (pass && confirm && button && warning) {
      const validate = () => {
        if (pass.value && confirm.value && pass.value === confirm.value) {
          button.classList.remove("disabled-btn");
          warning.classList.add("d-none");
        } else {
          button.classList.add("disabled-btn");
          if (confirm.value) {
             warning.classList.remove("d-none");
          } else {
             warning.classList.add("d-none");
          }
        }
      };

      pass.addEventListener("input", validate);
      confirm.addEventListener("input", validate);
    }
  }

  // Initialize Validation
  checkPasswords("registerPassword", "registerConfirmPassword", "registerButton", "registerMismatch");
  checkPasswords("loginPassword", "loginConfirmPassword", "loginButton", "loginMismatch");
});