$(document).ready(function() {


    var events = $('#events');
    var table = $('#example').DataTable( {
        dom: 'Bfrtip',
        select: {
            style: 'single'
        },
        lengthChange: false,
        //"language": {
        //    "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json"
        //},
         "language": {
            
    "sProcessing":     "Procesando...",
    "sLengthMenu":     "Mostrar _MENU_ Dispositivos",
    "sZeroRecords":    "No se encontraron Dispositivos",
    "sEmptyTable":     "Ningun dato disponible en esta tabla",
    "sInfo":           "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ Dispositivos",
    "sInfoEmpty":      "Mostrando Dispositivos del 0 al 0 de un total de 0 Dispositivos",
    "sInfoFiltered":   "(filtrado de un total de _MAX_ Dispositivos)",
    "sInfoPostFix":    "",
    "sSearch":         "Buscar Dispositivos:",
    "sUrl":            "",
    "sInfoThousands":  ",",
    "sLoadingRecords": "Cargando...",
    "oPaginate": {
        "sFirst":    "Primero",
        "sLast":     "Ultimo",
        "sNext":     "Siguiente",
        "sPrevious": "Anterior"
    },
    "oAria": {
        "sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
        "sSortDescending": ": Activar para ordenar la columna de manera descendente"
    }

        },
        buttons: [
                    {extend:    'pdfHtml5',
                    text: '<i class="glyphicon glyphicon-plus btn btn-success">Nuevo</i>', titleAttr: 'Nuevo Device',
                    action: function () {

                    //bootbox.alert('Datos Seleccionados:'+data);                   
                    //alert( 'Datos Seleccionados:'+data ) ;
                    bootbox.dialog({
                    title: 'Ingresar Datos del Dispositivo ',
                    message: $('#addForm'),
                    show: true // We will show it manually later
                                  })
                                    .on('shown.bs.modal', function() {
                                        $('#addForm').show();// Show the login form
                                        $('input[name="id"]').val('');
                                        $('input[name="username"]').val('');
                                        $('input[name="mail"]').val('');
                                      })
                                       .on('hide.bs.modal', function(e) {
                    // Bootbox will remove the modal (including the body which contains the login form)
                    // after hiding the modal
                    // Therefor, we need to backup the form
                                        $('#addForm').hide().appendTo('body'); 
                                        table.ajax.reload();



                                          })
                                          .modal('show');


                                         

                    
                            }
                    },
                
                    {extend:    'pdfHtml5',
                    text: '<i class="glyphicon glyphicon-remove btn btn-danger">Eliminar</i>', titleAttr: 'Eliminar',
                    action: function () {

                         /*
                         table.on( 'select', function ( e, dt, type, indexes ) {
                                         var rowData = table.rows( indexes ).data().toArray();
                                        alert('selected:'+rowData);
                              } ).on( 'deselect', function ( e, dt, type, indexes ) {
            var rowData = table.rows( indexes ).data().toArray();
            alert('deselect'+ '<div><b>'+type+' <i>de</i>selection</b> - '+JSON.stringify( rowData )+'</div>')
        } );*/
                    if( table.rows( { selected: true } ).count()>0){
                      
                    bootbox.confirm("Esta Seguro que desea eliminar el Dispositivo?", function(result){ 
                                        
                                     
                                        var data = table.row( { selected: true } ).data();
                                        var selectedrow=table.row( { selected: true } );
                                        console.log(selectedrow);
                                        var id = {id:data[0]}
                                        var url = "{{ url_for('eliminar') }}"; // send the form data here.
                                        console.log('This was logged in the callback: ' + result); 
                                        if(result==true){

                                               $.ajax({
                                                    type: 'POST',
                                                    url: url,
                                                    data: JSON.stringify(id),
                                                    dataType: 'json',
                                                    contentType: 'application/json; charset=utf-8'
                                                }).done(function(data) {
                                                     table.ajax.reload();
                                                    bootbox.alert(data.data);
                                                });



                                        }


                                    
                                          

                                    });

                            }
                            else{
                                bootbox.alert('Debe seleccionar un Dispositivo')
                            }

                        }


                    },
                
                    {extend:    'pdfHtml5',
                    text: '<i class="glyphicon glyphicon-edit btn btn-primary">Editar</i>', titleAttr: 'Editar',
                    action: function () {

                    if( table.rows( { selected: true } ).count()>0){
                    var data = table.row( { selected: true } ).data();
                    var index = table.row( { selected: true } ).index();
                    console.log(index);
                    //bootbox.alert('Datos Seleccionados:'+data);                   
                    //alert( 'Datos Seleccionados:'+data ) ;
                    var box = bootbox.dialog({
                    title: 'Modificar Datos del Dispositivo ',
                    message: $('#userForm'),
                    show: false // We will show it manually later
                                  })
                                    box.on('shown.bs.modal', function() {
                                        $('#userForm')                                          
                                                                    .show();// Show the login form
                                        $('input[name="id"]').val(data['0']);
                                        $('input[name="username"]').val(data['1']);
                                        $('input[name="mail"]').val(data['2']);
                                        console.log(data['1'])
                                      })
                                        .on('hide.bs.modal', function(e) {
                    // Bootbox will remove the modal (including the body which contains the login form)
                    // after hiding the modal
                    // Therefor, we need to backup the form
                                        $('#userForm').hide().appendTo('body');
                                        table.ajax.reload();

                                           })
                                            
                                          

                                           

                                            .modal('show');

                                            }
                                            else{
                                            bootbox.alert('Debe seleccionar un Dispositivo')

                                            }
                                         }       

                    },

                    {extend:    'pdfHtml5',
                    text: '<i class="glyphicon glyphicon-cog btn btn-success">Config</i>',titleAttr: 'Configurar',
                    action: function (  ) {
                    window.location = "/config"; 
                                    }
                    }

                ],


        //"sDom": "<'row-fluid'<'span6 toolbar'><'span6'>r>t<'row-fluid'<'span6'f><'span6'p>>",
        "bProcessing": true,
        "bjQueryUI": true,
        "sAjaxSource": "{{ url_for('_server_data') }}",
        
       });





} ); 
