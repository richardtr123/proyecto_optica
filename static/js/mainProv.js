$(document).ready(function(){
    tabla_proveedores = $("#tabla_proveedores").DataTable({
        /*"columnDefs":[{
         "targets": -1,
         "data":null,
         "defaultContent": "<div class='text-center'><div class='btn-group'><button class='btn btn-primary btnEditar'>Editar</button><button class='btn btn-danger btnBorrar'>Borrar</button></div></div>"  
        }],*/
         
         //Para cambiar el lenguaje a español
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


    $("#btnNuevo").click(function(){
        $("#formProveedores").trigger("reset");
        $(".modal-header").css("background-color", "#28a745");
        $(".modal-header").css("color", "white");
        $(".modal-title").text("Nuevo Proveedor");
        $("#modalCRUD").modal("show");
    });

    $(document).on("click",".btnEditar", function(){

        fila = $(this).closest("tr");
        idP = parseInt(fila.find('td:eq(0)').text());
        nombreP = fila.find('td:eq(1)').text();
        telefonoP = fila.find('td:eq(2)').text();
        correoP = fila.find('td:eq(3)').text();
        direccionP = fila.find('td:eq(4)').text();
        dnirucP = fila.find('td:eq(5)').text();
        empresaP = fila.find('td:eq(6)').text();
        
        $("#txtid").val(idP);
        $("#txtnombre").val(nombreP);
        $("#txtnumero").val(telefonoP);
        $("#txtemail").val(correoP);
        $("#txtdireccion").val(direccionP);
        $("#txtdniRuc").val(dnirucP);
        $("#txtempre").val(empresaP);

        $(".modal-header").css("background-color", "#007bff");
        $(".modal-header").css("color", "white");
        $(".modal-title").text("Editar Persona"); 
        $("#modalCRUDEdit").modal("show");           
    });
    
    $("#formProveedoresEdit").submit(function(e){
        $("#modalCRUDEdit").modal("hide");
    });

    $("#formProveedores").submit(function(e){
        $("#modalCRUD").modal("hide");
    });
});