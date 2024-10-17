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
                url: '/load-recipe-template/' + result.id + '/',  // URL che corrisponde alla tua vista
                type: 'get',
                success: function (data) {
                    resultsContainer.append(data.html);
                }
            });
            
        });
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
    $.ajax({
        url: 'recipes-page/?page=' + page,
        type: 'get',
        dataType: 'json',
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