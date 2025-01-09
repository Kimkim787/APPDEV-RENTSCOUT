emailjs.init("Q_A-eXEwrvvQsFMYs");
$(document).ready(function(){
    $('#next_form').on('click', function(event){
        const container = $(this).closest('#first_form');
        let valid = true;
        $.each($(container.find('input')), function(index, element){
            // validate here
            element.setCustomValidity('');
            if(!element.checkValidity()){
                console.log($(element).attr('name') + " is invalid");
                element.setCustomValidity(`This field is required`);
                element.reportValidity();
                valid = false;
                return false;
            }
        })
        if(!valid){
            event.preventDefault();
        }
        // else {
        //     // DIRI E SHOW ANG NEXT FORM
        // }
    })

    $('#create_account_btn').on('click', function(e){
        e.preventDefault();
        console.log('Create account clicked');

        if(validate_text_input($('input[name="firstname"]'))){
            if(validate_text_input($('input[name="lastname"]'))){
                if(validate_text_input($('input[name="middlename"]'))){
                    if(validate_date_input($('input[name="birthdate"]'))){
                        if(validate_email_input($('input[name="email"]'))){
                            if(validate_password_input($('input[name="password1"]'))){
                                console.log('password 1 and 2 valid')
                                if( validate_role_input() ){
                                    console.log('valid input');
                                    $('#signup_form').submit();
                                }
                            }
                        }
                    }
                }
            }
        }
    });

    $('#back_button').on('click', function(){
        $('#first_form').removeClass('hidden');
        $('#second_form').addClass('hidden');
        
    })


    function validate_text_input(element){
        const inputField = $(element).val(); 
        const for_err = $(element).attr('for_err');
        const specialCharPattern = /[,@$()_*&^#!:;{}|?<>+=-]/;     // Regex for special characters except "."
        const numbers = /[\d]/; // REGEX FOR NUMBERS
        
        // Check for empty input
        if (inputField.trim() === '') {
            SoloMessageFlow(`Please input ${for_err}`, 'error');
            $(element).focus();
            return false;
        }

        // Check for special characters
        if (specialCharPattern.test(inputField)) {
            SoloMessageFlow(`${for_err} should not include special characters`, 'error');
            $(element).focus();
            return false;
        }

        if (numbers.test(inputField)){
            SoloMessageFlow(`${for_err} should not include numerical values`, 'error');
            $(element).focus();
            return false;
        }
        return true;
    }

    function validate_date_input(element){
        const dateInput = $(element).val();
        console.log(dateInput);
        const datePattern = /^\d{4}\-\d{2}\-\d{2}$/; // REGEX FOR DATE FORMAT yyyy/mm/
        const alphabetPattern = /[a-zA-Z]/;
        
        if (dateInput.trim() === '') {
            SoloMessageFlow('Date of Birth cannot be empty', 'error');
            $(element).focus();
            return false;
        }

        // Validate yyyy/mm/dd format
        if (!datePattern.test(dateInput) || alphabetPattern.test(dateInput)) {
            SoloMessageFlow('Please follow this format for birthdate: [YYYY-MM-DD]', 'error');
            $(element).focus();
            return false;
        }

        const parts = dateInput.split('-');
        const year = parseInt(parts[0], 10);
        const month = parseInt(parts[1], 10) - 1; 
        const day = parseInt(parts[2], 10);
        const date = new Date(year, month, day);

        if (date.getFullYear() !== year || date.getMonth() !== month || date.getDate() !== day) {
            SoloMessageFlow('Invalid date. Please enter a real date.', 'error');
            $(element).focus();
            return false;
        }
        return true;


    }

    function validate_password_input(element){
        const password = $(element).val();
        const password2 = $('input[name="password2"]').val();
        console.log(password);
        console.log(password2);
        if (password.trim() === '') {
            SoloMessageFlow('Password cannot be empty', 'error');
            $(element).focus();
            $(password).val("");
            $(password2).val("");
            return false;
        }
    
        // Check if password is at least 8 characters
        if (password.length < 8) {
            SoloMessageFlow('Password must be at least 8 characters long', 'error');
            $(element).focus();
            $(password).val("");
            $(password2).val("");
            return false;
        }

        if (password != password2){
            $(element).focus();
            $(password).val("");
            $(password2).val("");
            SoloMessageFlow('Password did not match', 'error');
            return false;
        }

        return true;
    }

    function validate_role_input(){
        const role = $('#role').val();

        if (role === '' || role === '-------') {
            SoloMessageFlow('Please select a valid role (Boarder or Landlord)', 'error');
            $(role).focus();
            return false;
        }
        return true;
    }

    function validate_email_input(email) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const email_txt = $(email).val();
        if (email_txt.trim() === '') {
            SoloMessageFlow('Email cannot be empty', 'error');
            $(email).focus();
            return false;
        }

        if (!emailPattern.test(email_txt)) {
            SoloMessageFlow('Invalid email address', 'error');
            $(email).focus();
            return false;
        }
        return true;
    }
    
})// ready function

const selectElement = document.getElementById('gender');
                    let isOptionsOpen = false;
                
                    selectElement.addEventListener('mousedown', function(e) {
                        if (!isOptionsOpen) {
                            selectElement.style.borderBottomLeftRadius = '0';
                            selectElement.style.borderBottomRightRadius = '0';
                            isOptionsOpen = true;
                        } else {
                            selectElement.style.borderBottomLeftRadius = '';
                            selectElement.style.borderBottomRightRadius = '';
                            isOptionsOpen = false;
                        }
                    });
                
                    selectElement.addEventListener('blur', function() {
                        selectElement.style.borderBottomLeftRadius = '';
                        selectElement.style.borderBottomRightRadius = '';
                        isOptionsOpen = false;
                    });