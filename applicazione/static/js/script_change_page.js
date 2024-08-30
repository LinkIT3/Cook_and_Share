$(document).ready(function() {
    $(".nav-item").on('click', function() {
        var page_id = $(this).attr("id");
        $(".page").filter(":visible").hide();
        $(".page"+ "#" + page_id).show();
    });
});