function togglePassword(id) {
  const field = document.getElementById(id);
  field.type = field.type === "password" ? "text" : "password";
}

const loginTab = document.getElementById("loginTab");
const registerTab = document.getElementById("registerTab");
const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");

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

function checkPasswords(passId, confirmId, buttonId, warningId) {
  const pass = document.getElementById(passId);
  const confirm = document.getElementById(confirmId);
  const button = document.getElementById(buttonId);
  const warning = document.getElementById(warningId);

  if (pass.value && confirm.value && pass.value === confirm.value) {
    button.classList.remove("disabled-btn");
    warning.classList.add("d-none");
  } else {
    button.classList.add("disabled-btn");
    warning.classList.remove("d-none");
  }
}

document.getElementById("registerPassword").addEventListener("input", () => {
  checkPasswords(
    "registerPassword",
    "registerConfirmPassword",
    "registerButton",
    "registerMismatch"
  );
});

document
  .getElementById("registerConfirmPassword")
  .addEventListener("input", () => {
    checkPasswords(
      "registerPassword",
      "registerConfirmPassword",
      "registerButton",
      "registerMismatch"
    );
  });

document.getElementById("loginPassword").addEventListener("input", () => {
  checkPasswords(
    "loginPassword",
    "loginConfirmPassword",
    "loginButton",
    "loginMismatch"
  );
});

document
  .getElementById("loginConfirmPassword")
  .addEventListener("input", () => {
    checkPasswords(
      "loginPassword",
      "loginConfirmPassword",
      "loginButton",
      "loginMismatch"
    );
  });