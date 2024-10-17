$('.card').ready(function() {
    $('.page').on('click', '.like-button', function() {
        toggleLike($(this));
    });

    $('.page').on('click', '.bookmark-button', function() {
        toggleSave($(this));
    });

    $('.page').on('click', '.share-button', function() {
        copyLink($(this));
    });
});

function toggleLike(item){
$.ajax({
        url: 'toggle_liked/',
        type: 'post',
        data: JSON.stringify({id: item.closest('.card').attr('id')}),
        contentType: "application/json",
        headers: {
            "X-CSRFToken": getCookie('csrftoken')
        },

        success: function () {
            item.find('#michelinLogoFiller').toggle();
        },

        error: function(error) {
            console.error("Errore:", error);
            $('body').append($(`
                <div class="messages">
                    <div id="alert" class="alert alert-danger alert-dismissible fade show" role="alert">
                        Unable to update like!
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                </div>
            `));
        }
    })
}

function toggleSave(item){
    $.ajax({
        url: 'toggle_saved/',
        type: 'post',
        data: JSON.stringify({id: item.closest('.card').attr('id')}),
        contentType: "application/json",
        headers: {
            "X-CSRFToken": getCookie('csrftoken')
        },

        success: function () {
            item.find('#bookmarkFiller').toggle();
        },

        error: function(error) {
            console.error("Errore:", error);
            $('body').append($(`
                <div class="messages">
                    <div id="alert" class="alert alert-danger alert-dismissible fade show" role="alert">
                        Unable to update saves!
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                </div>
            `));
        }
    })
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function copyLink(item){
    navigator.clipboard.writeText(item.attr('link'));
    $('body').append($(`
        <div class="messages">
            <div id="alert" class="alert alert-success alert-dismissible fade show" role="alert">
                Link copied to clipboard!
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        </div>
    `));
}