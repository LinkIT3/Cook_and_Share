$(document).ready(function() {
    var hash = window.location.hash;
    
    change_page($(hash+"-page"));

    $(".nav-item").on('click', function() {
        change_page($(this));
    });
});

function change_page(item){
    var page_id = item.attr("id");

    $(".page").filter(":visible").hide();
    $(".page"+ "#" + page_id).show();
}