const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
}

// Upload Image Future Implementation
// const photoInput = document.querySelector("#avatar");
// const photoPreview = document.querySelector("#preview-avatar");
// if (photoInput)
//   photoInput.onchange = () => {
//     const [file] = photoInput.files;
//     if (file) {
//       photoPreview.src = URL.createObjectURL(file);
//     }
//   };


