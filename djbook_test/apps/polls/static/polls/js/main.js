$(document).ready(function (){

    var csrf = $('input[name=csrfmiddlewaretoken]').val();

    $('.btn').click(function (response){
        $.ajax({
            url: '',
            type: 'get',
            data: {
                button_text: $('.input_class').text(response.text)
            },
            success: function(response) {
                $('.btn').text(response.text)
                $('#seconds').append('<li>' + response.text + '</li>')
            }

        })
    });

    $('#seconds').on('click', 'li', function() {
        $.ajax({
            url: '',
            type: 'post',
            data: {
                text: $(this).text(),
                csrfmiddlewaretoken: csrf
            },
            success: function(response) {
                $('#right').append('<li>' + response.data + '</li>')
            }
        })
    })

});