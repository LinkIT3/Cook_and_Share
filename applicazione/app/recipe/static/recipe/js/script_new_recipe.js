
function add_select2(val){
    $('.ingredient-select_' + val).select2({
        tags: true,
        placeholder: "Select Ingredient",
        allowClear: true,
    });
}

$(document).ready(function() {
    var val = 0;
    var ingredients_list;

    $.ajax({
        url: 'get_ingredients/',
        type: 'post',
        data: JSON.stringify(),
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
        
        $('#div_id_ingredients').append(new_ingredient_selector(val));
        add_select2(val);
        val ++;
    });

    function new_ingredient_selector(val){
        let html = `<div class="ingredient-field mb-3" id="id_ingredient_field_` + val + `">
                        <select name="ingredients_` + val + `" class="ingredient-select_` + val + ` form-select" aria-label="Ingredient selector" required="True">
                            <option value="">Select Ingredient</option>`;
    
        for(const ingredient of ingredients_list){
            html += '<option value="' + ingredient + '">' + ingredient + '</option>';
        }
    
        html += `</select>
                <input type="text" class="form-control quantity-input" name="quantities_` + val + `" placeholder="Quantity" required="True" />
                </div>`
                
        return $(html);
    }

    const newIngredientField = $('#div_id_ingredients');
    
    $('#add-ingredient').on('click', function() {
        newIngredientField.append(new_ingredient_selector(val));
        add_select2(val);
        val ++;
    });
    
    $('#remove-ingredient').on('click', function() {
        if (val > 1){
            val --;
            $('#id_ingredient_field_'+ val).remove()
        }
    })
    
    $(document).on('change', '.ingredient-select', function() {
        let value = $(this).val();
        if (value && value.indexOf('new') !== -1) {
            let newIngredient = value.split('new:')[1].trim();
            $(this).append(new Option(newIngredient, newIngredient, true, true));
            $(this).val(newIngredient).trigger('change');
        }
    });

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
});