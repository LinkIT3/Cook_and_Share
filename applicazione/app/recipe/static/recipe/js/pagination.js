class Pagination {
    constructor(results, hasNext, hasPrevious, currentPage, totalPages, nextPageNumber, previousPageNumber, name_container) {
        this.results = results;
        this.hasNext = hasNext;
        this.hasPrevious = hasPrevious;
        this.currentPage = currentPage;
        this.totalPages = totalPages;
        this.nextPageNumber = nextPageNumber;
        this.previousPageNumber = previousPageNumber;
        this.name_container = name_container;
    }
    
    async renderResults(resultsContainer, url) {
        resultsContainer.empty();

        try{
            const requests = this.results.map(result => {
                return $.ajax({
                    url: url,
                    type: 'post',
                    data: JSON.stringify({id: result.id}),
                    contentType: "application/json",
                    headers: {
                        "X-CSRFToken": getCookie('csrftoken')
                    },
                }).then(data => {
                    return data;
                }).catch(error => {
                    console.error('Errore nella richiesta:', error);
                    return null;
                });
            });
            
            const responses = await Promise.all(requests);

            if (Array.isArray(responses)) {
                const validResponses = responses.filter(response => response !== null);

                validResponses.forEach(data => {
                    if (data && data.html) {
                        resultsContainer.append(data.html);
                    } else {
                        console.error("Data not valid:", data);
                    }
                });
            } else {
                console.error('The response is not an array:', responses);
            }
        } catch (error) {
            console.error('Errore nella gestione delle richieste:', error);
        }
    }

    renderResultsRecipes(){
        const resultsContainer = $('.container-recipes-' + this.name_container);
        const url = 'load-recipe-card/';
        this.renderResults(resultsContainer, url);
    }

    renderResultsUsers(){
        const resultsContainer = $('.container-' + this.name_container);
        const url = 'load-user-card/';
        this.renderResults(resultsContainer, url);
    }
    
    renderPagination() {
        const paginationContainer = $('#pagination-container-' +  this.name_container);
        paginationContainer.empty();
        
        if(this.currentPage == 1){
            paginationContainer.append(`<a href="#" class="page-link" data-page="0"><i class="fa-solid fa-angles-left"></i></a>`);
            paginationContainer.append(`<a href="#" class="page-link" data-page="0"><i class="fa-solid fa-chevron-left"></i></a>`);
        }
        else{
            paginationContainer.append(`<a href="#" class="page-link" data-page="1"><i class="fa-solid fa-angles-left"></i></a>`);
            paginationContainer.append(`<a href="#" class="page-link" data-page="${this.previousPageNumber}"><i class="fa-solid fa-chevron-left"></i></a>`);
        }

        paginationContainer.append(`<span>${this.currentPage} of ${this.totalPages}</span>`);

        if(this.currentPage == this.totalPages){
            paginationContainer.append(`<a href="#" class="page-link" data-page="0"><i class="fa-solid fa-chevron-right"></i></a>`);
            paginationContainer.append(`<a href="#" class="page-link" data-page="0"><i class="fa-solid fa-angles-right"></i></a>`);
        }
        else{
            paginationContainer.append(`<a href="#" class="page-link" data-page="${this.nextPageNumber}"><i class="fa-solid fa-chevron-right"></i></a>`);
            paginationContainer.append(`<a href="#" class="page-link" data-page="${this.totalPages}"><i class="fa-solid fa-angles-right"></i></a>`);
        }
    }
    
    renderRecipes() {
        this.renderResultsRecipes();
        this.renderPagination();
    }

    renderProfiles(){
        this.renderResultsUsers();
        this.renderPagination();
    }
}

function loadPage(page, name, name_container, user_id=null, search_string=null) {
    var pag = new Pagination();

    data = {page: page, type: name};

    if (user_id != null) {
        data['user_id'] = user_id;
    }

    if (search_string != null) {
        data['search_string'] = search_string;
    }

    $.ajax({
        url: 'get-recipes/',
        type: 'post',
        data: JSON.stringify(data),
        contentType: "application/json", 
        headers: {
            "X-CSRFToken": getCookie('csrftoken')
        },
        
        success: function (data) {
            const pagination = new Pagination(
                data.results,
                data.has_next,
                data.has_previous,
                data.current_page,
                data.total_pages,
                data.next_page_number,
                data.previous_page_number,
                name_container
            );
            
            if(name == "search-users")
                pagination.renderProfiles();
            else
                pagination.renderRecipes();
        }
    });
}

// document.addEventListener("DOMContentLoaded", function() {
//     loadPage(1);
// });

$(document).on('click', '.page-link', function (e) {
    e.preventDefault();
    let page = $(this).data('page');

    if (page != 0) {
        loadPage(page);
    }
});