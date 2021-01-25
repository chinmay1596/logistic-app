document.getElementById("newproduct").addEventListener("click", function () {
  document.querySelector(".bg-modal").style.display = "flex";
});

document.querySelector(".cancel").addEventListener("click", function () {
  document.querySelector(".bg-modal").style.display = "none";
});

document.getElementById("emailEdit").addEventListener("click", function () {
  document.querySelector("#email").style.display = "block";
});
