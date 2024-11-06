$(document).ready(function() {
    if(authenticated) {
        $(document).on('click', '.like-button', function() {
            toggleLike($(this));
        });

        $(document).on('click', '.bookmark-button', function() {
            toggleSave($(this));
        });

        $(document).on('click', '.remix-edit-button', function() {
            remix_editRecipe($(this));
        });
    }

    $(document).on('click', '.share-button', function() {
        copyLink($(this));
    });

    $(document).on('click', '.download-button', function() {
        downloadRecipe($(this));
    });
});

function toggleLike(item){
    $.ajax({
        url: 'toggle_liked/',
        type: 'post',
        data: JSON.stringify({id: item.closest('.recipe').attr('id')}),
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
        data: JSON.stringify({id: item.closest('.recipe').attr('id')}),
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

async function copyLink(item){
    try{
        await navigator.clipboard.writeText(item.attr('link'));
        $('body').append($(`
            <div class="messages">
                <div id="alert" class="alert alert-success alert-dismissible fade show" role="alert">
                    Link copied to clipboard!
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            </div>
        `));
    }
    catch(error){
        console.error("Error while coping in clipboard:", error);
    }
}

function remix_editRecipe(item){
    const url = window.location.origin + '/remix_edit_recipe/' + item.closest('.recipe').attr('id') +'/';
    
    window.location.href = url;
}

function downloadRecipe(item){
    const regex = /\/recipe\/\d+\/(.*)$/;
    filename = item.attr("pdf-name");

    $.ajax({
        url: 'recipe/' + item.closest('.recipe').attr('id') + '/',
        type: 'post',
        data: JSON.stringify({id: item.closest('.recipe').attr('id')}),
        contentType: "application/json",
        headers: {
            "X-CSRFToken": getCookie('csrftoken')
        },

        success: function (data) {
            var opt = {
                margin:       0.5,
                filename:     filename,
                image:        { type: 'jpeg', quality: 0.98 },
                html2canvas:  { scale: 3, useCORS: true},
                jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
            };

            html2pdf().from(data.html).set(opt).save();
        }
    });
}