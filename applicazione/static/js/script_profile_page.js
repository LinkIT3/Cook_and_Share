function updateClassBasedOnOrientation() {
    if (window.matchMedia("(orientation: portrait)").matches) {
        $('.btn.btn-primary.logout').addClass('btn-sm');
        $('.fa-solid.fa-gear').removeClass('fa-xl').addClass('fa-lg');
    } 
    else {
        $('.btn.btn-primary.logout').removeClass('btn-sm');
        $('.fa-solid.fa-gear').removeClass('fa-lg').addClass('fa-xl');
    }
}


$(document).ready(function() {
    updateClassBasedOnOrientation();
    $(window).on('resize', updateClassBasedOnOrientation);
    
    $('.settings-show').on('click', function(){
        if($('.settings-div').hasClass('show'))
            $('.settings-div').removeClass('show');
        else
            $('.settings-div').addClass('show');
    });

    $('.settings-hide').on('click', function(){
        $('.settings-div').removeClass('show');
    });
});
