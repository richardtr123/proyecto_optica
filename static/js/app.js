//no tocar
let sidebar = document.querySelector(".sidebar");
let sidebarBtn = document.querySelector(".bx-menu");
cargarStorage();

let arrow = document.querySelectorAll(".arrow");
for (var i = 0; i < arrow.length; i++) {
  arrow[i].addEventListener("click", (e) => {
    let arrowParent = e.target.parentElement.parentElement;
    arrowParent.classList.toggle("showMenu");
  });
}
let lag;
console.log(sidebarBtn);
sidebarBtn.addEventListener("click", () => {
  lag = sidebar.classList.toggle("close");
  localStorage.setItem("llave", lag);
});

function cargarStorage() {
  let candado = localStorage.getItem("llave") === "true";
  // para el sidebar este apegado o extendido
  if (candado) {
    sidebar.classList.toggle("close");
  }
}

let valorcito = "hola";

const list = document.querySelectorAll(".list");
function activeLink() {
  list.forEach((item) => item.classList.remove("active"));
  this.classList.add("active");
}
list.forEach((item) => item.addEventListener("click", activeLink));
