// on('action', 'button id or class')
$(document).on('click', '#submit', function (e){
    e.preventDefault();
    $.ajax({
        // type of form
        type: 'POST',
        // url: django url path
        url: 'ajax_check/',
        data: {
            // input fields by id or class
            name: $('#name').val(),
            email: $('#email').val(),
            bio: $('#bio').val(),
            // csrf token from hidden html input
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        dataType: 'json',
        // if django view returned true / if the request succeeds
        success: function (data){
            $('span.name').html(data);
        },
        error: function (data){
            $('span.email').html('error')
        }
    })
})
