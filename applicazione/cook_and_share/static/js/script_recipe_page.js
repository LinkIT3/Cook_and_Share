class Pagination {
    constructor(results, hasNext, hasPrevious, currentPage, totalPages, nextPageNumber, previousPageNumber) {
        this.results = results;
        this.hasNext = hasNext;
        this.hasPrevious = hasPrevious;
        this.currentPage = currentPage;
        this.totalPages = totalPages;
        this.nextPageNumber = nextPageNumber;
        this.previousPageNumber = previousPageNumber;
    }
    
    renderResults() {
        const resultsContainer = $('.container-recipes');
        resultsContainer.empty();

        this.results.forEach(result => {
            $.ajax({
                url: 'load-recipe-card/',
                type: 'post',
                data: JSON.stringify({id: result.id}),
                contentType: "application/json",
                headers: {
                    "X-CSRFToken": getCookie('csrftoken')
                },

                success: function (data) {
                    resultsContainer.append(data.html);
                }
            });
            
        });  
    }

    getCookie(name) {
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
    
    renderPagination() {
        const paginationContainer = $('#pagination-container');
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
    
    renderAll() {
        this.renderResults();
        this.renderPagination();
    }
}

function loadPage(page) {
    let pag = new Pagination()
    $.ajax({
        url: 'recipes-page/',
        type: 'post',
        data: JSON.stringify({page: page}),
        contentType: "application/json", 
        headers: {
            "X-CSRFToken": pag.getCookie('csrftoken')
        },
        
        success: function (data) {
            const pagination = new Pagination(
                data.results,
                data.has_next,
                data.has_previous,
                data.current_page,
                data.total_pages,
                data.next_page_number,
                data.previous_page_number
            );
            pagination.renderAll();
        }
    });
}

$(document).ready(function () {
    loadPage(1);
});

$(document).on('click', '.page-link', function (e) {
    e.preventDefault();
    let page = $(this).data('page');

    if (page != 0) {
        loadPage(page);
    }
});