$('#like').click(function(){
    var catid = $(this).attr("data-catid");
    var csrf = $('input[name=csrfmiddlewaretoken]').attr('value');
    var liked;
    var method;
    var btn_class;
    if ($(this).attr('class') == 'btn btn-outline-dark btn-sm'){
        liked = false;
        method = 'POST';
        btn_class = 'btn btn-dark btn-sm';
    } else {
        liked = true;
        method = 'DELETE';
        btn_class = 'btn btn-outline-dark btn-sm';
    }

    $.ajax(
    {
        type: method,
        url: "/ajax/posts/" + catid,
        headers: {
            'X-CSRFToken': csrf
        },
        data:{
            post_id: catid
        },
        success: function( data )
        {
            $( '#likes_count' ).text(data.likes);
            $('#like').attr('class', btn_class);


        },

     })
});
