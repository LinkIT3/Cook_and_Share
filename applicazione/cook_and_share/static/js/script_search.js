$(document).ready(function() {
    $("#form-search").submit(function(event){
        event.preventDefault();

        loadPage(1, 'search-recipes', "search-recipes", null, $('#input-search').val());
        loadPage(1, 'search-users', "search-users", null, $('#input-search').val());
    });

    $(document).on('click', '.set-search-recipes', function() {
        $(this).addClass('active');
        $('.set-search-users').removeClass('active');
        $('.results-recipes').show();
        $('.results-profiles').hide();
    });

    $(document).on('click', '.set-search-users', function() {
        $(this).addClass('active');
        $('.set-search-recipes').removeClass('active');
        $('.results-profiles').show();
        $('.results-recipes').hide();
    });

    $(document).on('click', 'button.follow-card', function() {
        const button = $(this);
        const id = button.attr('id');

        $.ajax({
            url: 'toggle_follow/',
            type: 'post',
            data: JSON.stringify({ user: id }),
            contentType: "application/json", 
            headers: {
                "X-CSRFToken": getCookie('csrftoken')
            },

            success: function(data){
                if(button.text().includes("Follow")){
                    button.text("Unfollow");
                }
                else{
                    button.text("Follow");
                }
            }
        });
    })
});