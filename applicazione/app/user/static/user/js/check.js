$(document).ready(function() {
    
    // Aggiungi il token CSRF a tutte le richieste AJAX
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
    
    const csrftoken = getCookie('csrftoken');
    
    // Controllo Username in tempo reale    
    $('#id_nickname').on('input', function() {
        var username = $(this).val().toLowerCase();
        $(this).val(username); 

        $('#nickname-feedback').show();

        if (username.match(/^[0-9a-z._-]*$/)){
            if (username.length > 0) {
                $.ajax({
                    type: 'POST',
                    url: checkUsernameUrl,
                    
                    data: {
                        'nickname': username,
                        'csrfmiddlewaretoken': csrftoken
                    },
                    
                    dataType: 'json',
                    
                    success: function(data) {
                        if (data.is_taken) {
                            $('#nickname-feedback').text('Nickname already used');
                            $('#id_nickname').addClass('is-invalid');
                            $('#id_nickname').removeClass('is-valid');
                            $('#submit-btn').prop('disabled', true);
                        } 
                        else {
                            $('#nickname-feedback').text('');
                            $('#id_nickname').removeClass('is-invalid');
                            $('#id_nickname').addClass('is-valid');
                            $('#submit-btn').prop('disabled', false);
                        }
                    },
                    
                    error: function(xhr, status, error) {
                        console.log('Errore:', error);
                    },
                });
            } 
            else {
                $('#nickname-feedback').text('');
                $('#id_nickname').removeClass('is-invalid');
                $('#id_nickname').removeClass('is-valid');
                $('#submit-btn').prop('disabled', true);
            }
        }
        else {
            $('#nickname-feedback').text('Nickname is invalid, you can use only number, letters and . - _');
            $('#id_nickname').addClass('is-invalid');
            $('#id_nickname').removeClass('is-valid');
            $('#submit-btn').prop('disabled', true);
        }
    });
    
    // Controllo Email in tempo reale
    $('#id_email').on('input', function() {
        var email = $(this).val();
        $('#email-feedback').show();

        if (email.length > 0) {
            if (String(email).toLowerCase().match(/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/)){
                $.ajax({
                    type: 'POST',
                    url: checkEmailUrl,
                    
                    data: {
                        'email': email,
                        'csrfmiddlewaretoken': csrftoken
                    },
                    
                    dataType: 'json',
                    
                    success: function(data) {
                        if (data.is_taken) {
                            $('#email-feedback').text('Email already used');
                            $('#id_email').addClass('is-invalid');
                            $('#id_email').removeClass('is-valid');
                            $('#submit-btn').prop('disabled', true);
                        } 
                        else {
                            $('#email-feedback').text('');
                            $('#id_email').removeClass('is-invalid');
                            $('#id_email').addClass('is-valid');
                            $('#submit-btn').prop('disabled', false);
                        }
                    },
                    
                    error: function(xhr, status, error) {
                        console.log('Errore:', error);
                    },
                });
            }
            else {
                $('#email-feedback').text('Email is invalid');
                $('#id_email').addClass('is-invalid');
                $('#id_email').removeClass('is-valid');
                $('#submit-btn').prop('disabled', true);
            }    
        }
        else {
            $('#email-feedback').text('');
            $('#id_email').removeClass('is-valid');
            $('#id_email').removeClass('is-invalid');
            $('#submit-btn').prop('disabled', true);
        }
        
    });
    
    // Controllo Password in tempo reale
    $('#id_password1, #id_password2').on('input', function() {
        var password = $('#id_password1').val();
        var passwordConfirm = $('#id_password2').val();
        $('#password-feedback').show();
        
        if (password.length > 0){
            $('#id_password1').removeClass('is-invalid');
            
            if (passwordConfirm.length > 0) {
                if (password !== passwordConfirm) {
                    $('#password-feedback').text('The password are different');
                    $('#id_password2').addClass('is-invalid');
                    $('#id_password1').removeClass('is-valid');
                    $('#id_password2').removeClass('is-valid');
                    $('#submit-btn').prop('disabled', true);
                } 
                else {
                    $('#password-feedback').text('');
                    $('#id_password2').removeClass('is-invalid');
                    $('#id_password1').addClass('is-valid');
                    $('#id_password2').addClass('is-valid');
                    $('#submit-btn').prop('disabled', false);
                }
            }
            else{
                $('#id_password2').addClass('is-invalid');
                $('#password-feedback').text('The password are different');
                $('#submit-btn').prop('disabled', true);
            }
        }
        else {
            if (password.length == 0)
                $('#id_password1').addClass('is-invalid');

            if (passwordConfirm.length == 0)
                $('#id_password2').addClass('is-invalid');

            $('#password-feedback').text('The password cannot be empty');
            $('#id_password1').removeClass('is-valid');
            $('#id_password2').removeClass('is-valid');
            $('#submit-btn').prop('disabled', true);
        }
    });
});