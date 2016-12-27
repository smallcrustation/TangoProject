$('#likes').click(function () {
    var catid;
    catid = $(this).attr("data-catid");
    $.get('/netchan/like/', {category_id : catid}, function (data) {
        $('#like_count').html(data);
        $('#likes').hide();
    })
})
$('#suggestion').keyup(function () {
    var query;
    query = $(this).val();
    $.get('/netchan/suggest', { suggestion: query }, function (data) {
        $('#cats').html(data);
    });
})

$(document).ready(function () {
    $(document).on('click', '#auto-add', function () {
        var cat_id;
        var page_title;
        var page_url;
        cat_id = $(this).attr("cat-id");
        page_title = $(this).attr("page-title");
        page_url = $(this).attr("page-url");
        $.get('/netchan/auto_add_page/', { cat_id: cat_id, title: page_title, url: page_url }, function (data) {
            $('#data-cat-list').html(data);
            $(this).hide(); // not working
        });
    });
});
