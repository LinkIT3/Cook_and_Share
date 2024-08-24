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
    $('#id_username').on('input', function() {
        var username = $(this).val();
        
        if (username.length > 0) {
            $.ajax({
                type: 'POST',
                url: "{% url 'check_username' %}",
                
                data: {
                    'username': username,
                    'csrfmiddlewaretoken': csrftoken
                },
                
                dataType: 'json',
                
                success: function(data) {
                    if (data.is_taken) {
                        $('#username-feedback').text('Username already used');
                        $('#submit-btn').prop('disabled', true);
                    } 
                    else {
                        $('#username-feedback').text('');
                        $('#submit-btn').prop('disabled', false);
                    }
                }
            });
        } 
        else {
            $('#username-feedback').text('');
            $('#submit-btn').prop('disabled', false);
        }
    });
    
    // Controllo Email in tempo reale
    $('#id_email').on('input', function() {
        var email = $(this).val();
        
        if (email.length > 0) {
            $.ajax({
                type: 'POST',
                url: "{% url 'check_email' %}",
                
                data: {
                    'email': email,
                    'csrfmiddlewaretoken': csrftoken
                },
                
                dataType: 'json',
                
                success: function(data) {
                    if (data.is_taken) {
                        $('#email-feedback').text('Email already used');
                        $('#submit-btn').prop('disabled', true);
                    } 
                    else {
                        $('#email-feedback').text('');
                        $('#submit-btn').prop('disabled', false);
                    }
                }
            });
        } 
        else {
            $('#email-feedback').text('');
            $('#submit-btn').prop('disabled', false);
        }
    });
    
    // Controllo Password in tempo reale
    $('#id_password1, #id_password2').on('input', function() {
        var password = $('#id_password1').val();
        var passwordConfirm = $('#id_password2').val();
        
        if (password !== passwordConfirm) {
            $('#password-feedback').text('The password are different');
            $('#submit-btn').prop('disabled', true);
        } 
        else {
            $('#password-feedback').text('');
            $('#submit-btn').prop('disabled', false);
        }
    });
});