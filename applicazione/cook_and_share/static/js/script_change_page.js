$(document).ready(function() {
    var hash = window.location.hash.replace('#', '');
    
    if (!hash) {
        window.location.href = "/#home";
        hash = "home";
    }
    
    change_page(hash);
    
    $(".nav-item").on('click', function() {
        change_page(this.id);
    });
});

function change_page(item){
    window.location.href = "/#" + item;
    
    $(".page").filter(":visible").hide();
    $(".page"+ "#" + item + '-page').show();
}