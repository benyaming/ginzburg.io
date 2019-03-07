$('#like').click(function(){
    var catid;
    var csrf;
    catid = $(this).attr("data-catid");
    csrf = $('input[name=csrfmiddlewaretoken]').attr('value')
    $.ajax(
    {
        type:"POST",
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
        },

     })
});

$('#unlike').click(function(){
     var catid;
    var csrf;
    catid = $(this).attr("data-catid");
    csrf = $('input[name=csrfmiddlewaretoken]').attr('value')
    $.ajax(
    {
        type:"DELETE",
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
        },

     })
});