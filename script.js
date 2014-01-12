$(function(){
    $.ajax({
        url: '/get-html',
        type: 'GET',
        data: {
            id: 1,
        },
        dataType: 'html'
    })
    .done(function( data ) {
        $("#container").html(data);
    })
    .fail(function( data ) {
        alert("FAILED");
    })
    .always(function( data ) {
    });
});