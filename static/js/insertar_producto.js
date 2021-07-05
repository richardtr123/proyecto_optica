function init() {
  var inputFile = document.getElementById("file-imagen");
  inputFile.addEventListener("change", mostrarImagen, false);
}

function mostrarImagen(event) {
  var file = event.target.files[0];
  var reader = new FileReader();
  reader.onload = function (event) {
    var img = document.getElementById("previsualizacion");
    img.src = event.target.result;
  };
  reader.readAsDataURL(file);
}

window.addEventListener("load", init, false);
