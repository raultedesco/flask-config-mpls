    $(document).ready(function() {
        $('#addForm').submit(function (e) {
            var url = "{{ url_for('add') }}"; // send the form data here.
            $.ajax({
                type: "POST",
                url: url,
                data: $('#addForm').serialize(), // serializes the form's elements.
                success: function (data) {
                    console.log(data);  // display the returned data in the console.
                    //$('#userForm').modal('hide');
                    $('#addForm').parents('.bootbox').modal('hide');
                    bootbox.alert(data.data);


                }
            });
            e.preventDefault(); // block the traditional submission of the form.
        });
        // Inject our CSRF token into our AJAX request.
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}")
                }
            }
        })
    }); 
