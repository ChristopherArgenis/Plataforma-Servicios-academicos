function openTab(tabId) {
  const buttons = document.querySelectorAll("#crudTabs .nav-link");
  const contents = document.querySelectorAll(".tab-content");

  buttons.forEach((btn) => {
    // Now, all buttons are tab toggles, so remove active class from all.
    btn.classList.remove("active");
  });
  contents.forEach((content) => (content.style.display = "none"));

  const clickedButton = document.querySelector(
    `[onclick="openTab('${tabId}')"]`
  );
  if (clickedButton) {
    clickedButton.classList.add("active");
    document.getElementById(tabId).style.display = "block";
  }
}

// On page load, ensure the first administration tab is displayed.
window.onload = function () {
  openTab("view"); // Now displays the 'Ver' tab by default on load
};