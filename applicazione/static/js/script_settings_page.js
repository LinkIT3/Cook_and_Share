$(document).ready(function() {
    $('#id_password_new_1, #id_password_new_2').on('input', function() {
        var password = $('#id_password_new_1').val();
        var passwordConfirm = $('#id_password_new_2').val();
        $('#password-feedback').show();
        
        if (password.length > 0){
            $('#id_password_new_1').removeClass('is-invalid');
            
            if (passwordConfirm.length > 0) {
                if (password !== passwordConfirm) {
                    $('#password-feedback').text('The password are different');
                    $('#id_password_new_2').addClass('is-invalid');
                    $('#id_password_new_1').removeClass('is-valid');
                    $('#id_password_new_2').removeClass('is-valid');
                    $('#submit-btn-paswd').prop('disabled', true);
                } 
                else {
                    $('#password-feedback').text('');
                    $('#id_password_new_2').removeClass('is-invalid');
                    $('#id_password_new_1').addClass('is-valid');
                    $('#id_password_new_2').addClass('is-valid');
                    $('#submit-btn-paswd').prop('disabled', false);
                }
            }
            else{
                $('#id_password_new_2').addClass('is-invalid');
                $('#password-feedback').text('The password are different');
                $('#submit-btn-paswd').prop('disabled', true);
            }
        }
        else {
            if (password.length == 0)
                $('#id_password_new_1').addClass('is-invalid');
            
            if (passwordConfirm.length == 0)
                $('#id_password_new_2').addClass('is-invalid');
            
            $('#password-feedback').text('The password cannot be empty');
            $('#id_password1_new_').removeClass('is-valid');
            $('#id_password_new_2').removeClass('is-valid');
            $('#submit-btn-paswd').prop('disabled', true);
        }
    });
});