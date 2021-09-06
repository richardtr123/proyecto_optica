
$(document).ready(function() {  
  $('#stockTable').DataTable({
  //para cambiar el lenguaje a español
      "language": {
              "lengthMenu": "Mostrar _MENU_ registros",
              "zeroRecords": "No se encontraron resultados",
              "info": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
              "infoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
              "infoFiltered": "(filtrado de un total de _MAX_ registros)",
              "sSearch": "Buscar:",
              "oPaginate": {
                  "sFirst": "Primero",
                  "sLast":"Último",
                  "sNext":"Siguiente",
                  "sPrevious": "Anterior"
         },
         "sProcessing":"Procesando...",
          }
  });  
    
});


function ResaltarFila(id_tabla){
  
  if (id_tabla == undefined)      // si no se le pasa parametro
      // recupera todas las filas de todas las tablas
      
      var filas = document.getElementsByTagName("tr");
  else{
      // recupera todas las filas de la tabla indicada en el parametro
      var tabla = document.getElementById(id_tabla);
      var filas = tabla.getElementsByTagName("tr");
  }
  // recorre cada una de las filas
  for(var i in filas) {
    // si el puntero esta encima de la fila asigna la regla css: resaltar
      filas[i].onmouseover = function() {
          this.className = "resaltar";
      }
      // si el puntero salga de la fila asigna ninguna regla
      filas[i].onmouseout = function() {
          this.className = null;
      }
  }
}
