
function add_select2(val){
    $('.ingredient-select_' + val).select2({
        tags: true,
        placeholder: "Select Ingredient",
        allowClear: true,
    });
}

$(document).ready(function() {
    var val = 0;
    
    $('#ingredient-list').append(
        $(`<div id="div_id_ingredients" class="mb-3">
                <label for="id_ingredient_field" class="form-label requiredField">
                    Ingredients
                    <span class="asteriskField">*</span>
                </label>
            </div>`
    ));

    $('#div_id_ingredients').append(new_ingedient_selector(val));
    add_select2(val);
    val ++;
    
    const newIngredientField = $('#div_id_ingredients');

    $('#add-ingredient').on('click', function() {
        newIngredientField.append(new_ingedient_selector(val));
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
});