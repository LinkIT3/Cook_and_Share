
function add_select2(val){
    $('.ingredient-select_' + val).select2({
        tags: true,
        placeholder: "Select Ingredient",
        allowClear: true,
    });
}

$(document).ready(function() {
    let val = 0;
    let ingredients_list;
    
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
    
    $.ajax({
        url: 'get_ingredients/',
        type: 'post',
        data: JSON.stringify({id: 0}),
        contentType: "application/json",
        headers: {
            "X-CSRFToken": getCookie('csrftoken')
        },
        
        error: function(error) {
            console.error("Errore:", error);
            $('body').append($(`
                <div class="messages">
                    <div id="alert" class="alert alert-danger alert-dismissible fade show" role="alert">
                        Unable to get ingredients!
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                </div>
            `));
            
            $('#submit-id-new-recipe-form').prop("disabled", true);
            
            return null;
        }
    }).done(function(data) {
        ingredients_list = data;
        
        $('#ingredient-list').append(
            $(`<div id="div_id_ingredients" class="mb-3">
                    <label for="id_ingredient_field" class="form-label requiredField">
                        Ingredients
                        <span class="asteriskField">*</span>
                    </label>
                </div>`
        ));
        
        new_ingredient_selector();
        original_ingredients()
    });
    
    function new_ingredient_selector(){
        let html = `<div class="ingredient-field mb-3" id="id_ingredient_field_` + val + `">
                        <select name="ingredients_` + val + `" class="ingredient-select_` + val + ` form-select" aria-label="Ingredient selector" required="True">
                            <option value="">Select Ingredient</option>`;
        
        for(const ingredient of ingredients_list){
            html += '<option value="' + ingredient + '">' + ingredient + '</option>';
        }
        
        html += `   </select>
                        <input type="text" class="form-control quantity-input ingredient-quantity_` + val + `" name="quantities_` + val + `" placeholder="Quantity" required="True" />
                </div>`
                
        $('#div_id_ingredients').append(html);
        add_select2(val);
        val++
    }

    function remove_ingredient_selector(){
        if (val > 1){
            val --;
            $('#id_ingredient_field_'+ val).remove()
        }
    }
    
    const newIngredientField = $('#div_id_ingredients');
    
    $('#add-ingredient').on('click', function() {
        new_ingredient_selector();
    });
    
    $('#remove-ingredient').on('click', function() {
        remove_ingredient_selector();
    })
    
    $(document).on('change', '.ingredient-select', function() {
        let value = $(this).val();
        if (value && value.indexOf('new') !== -1) {
            let newIngredient = value.split('new:')[1].trim();
            $(this).append(new Option(newIngredient, newIngredient, true, true));
            $(this).val(newIngredient).trigger('change');
        }
    });
    
    function original_ingredients(){
        if($('.cancel-edit-remix').length > 0){
            $.ajax({
                url: 'get_ingredients/',
                type: 'post',
                data: JSON.stringify({id: $('.cancel-edit-remix').attr('id')}),
                contentType: "application/json",
                headers: {
                    "X-CSRFToken": getCookie('csrftoken')
                },
                
                success: function(data) {
                    let data_len = Object.keys(data).length;
                    
                    for(let [ingredient, quantity] of Object.entries(data)){
                        $('.ingredient-select_' + (val - 1)).val(ingredient).trigger('change');
                        $('.ingredient-quantity_' + (val - 1)).val(quantity);
                        
                        if(val != data_len){
                            new_ingredient_selector();
                        }
                    }
                },

                error: function(error) {
                    console.error("Errore:", error);
                    $('body').append($(`
                        <div class="messages">
                            <div id="alert" class="alert alert-danger alert-dismissible fade show" role="alert">
                                Unable to obtain the original ingredients!
                                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                            </div>
                        </div>
                    `));
                    
                    $('#submit-id-new-recipe-form').prop("disabled", true);
                    
                    return null;
                }
            });
        }
    }
});