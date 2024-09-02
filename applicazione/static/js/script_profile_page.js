function updateClassBasedOnOrientation() {
    if (window.matchMedia("(orientation: portrait)").matches) {
        $('.btn.btn-primary.logout').addClass('btn-sm');
        $('.fa-solid.fa-gear.fa-xl').removeClass('fa-xl').addClass('fa-lg');
    } 
    else {
        $('.btn.btn-primary.logout').removeClass('btn-sm');
        $('.fa-solid.fa-gear.fa-sm').removeClass('fa-lg').addClass('fa-xl');
    }
}


$(document).ready(function() {
    updateClassBasedOnOrientation();
    $(window).on('resize', updateClassBasedOnOrientation);
});