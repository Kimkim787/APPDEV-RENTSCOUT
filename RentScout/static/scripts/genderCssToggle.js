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

    $('#back_button').on('click', function(){
        $('#first_form').removeClass('hidden');
        $('#second_form').addClass('hidden');
        
    })

    // CONFIRM EMAIL BUTTON
    $('#get_otp').on('click', function(){
        const email = $(this).closest('div').find('input[name="email"]').val();
        send_otp(email);
    })

    // RESEND CODE BUTTON
    $('#resend_otp').on('click', function(){
        const email = $(this).closest('div').find('input[name="email"]').val();
        send_otp(email);
    })

    // CONFIRM CODE BUTTON
    $('#confirm_otp').on('click', function(){
        validate_otp($(this));
    })

    function send_otp(email){
        console.log(email);
        $.ajax({
            url: '/signup/get_otp/',
            type: 'GET',
            success: function(response){
                const public_key = response.mail_keys.public_key;
                const template_key = response.mail_keys.template_key;
                localStorage.setItem('otp', response.otp);

                setTimeout(function() {
                    localStorage.removeItem('otp');
                }, 600000);  // 10 minutes

                // SEND OTP TO EMAIL
                emailjs.send(public_key, template_key, {
                    to_email: email,
                    otp: response.otp,
                  }).then(
                    function(response) {
                        $('#user_email').text(email);
                        $('#otp_confirmation_form').removeClass('hidden');
                    //   SoloMessageFlow(`OTP was sent to ${email}`, 'success')
                    },
                    function(error) {
                      console.error("Failed to send email.", error);
                    //   SoloMessageFlow('Failed to send email. Something\'s wrong with the server.', 'error')
                    }
                    ); 
            }, 
            error: function(xhr, status, error) {
                let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
                SoloMessageFlow(`${errorMessage}`, 'error');
            }

        })
    }

    function validate_otp(btn){
        console.log("validating otp");
        const saved_otp = localStorage.getItem('otp');
        const inputted_otp = $(btn).closest('#otp_confirmation_form').find('input[name="OTP"]').val();
        console.log(saved_otp);
        console.log(inputted_otp);
        if(!(saved_otp === inputted_otp)){
            console.log('otp did not match');
            return;
        } else { 
            console.log('otp valid');
            const password1 = $('input[name="password1"]');
            const password2 = $('input[name="password2"]');
            const role = $('select[name="role"]');
            const create_btn = $('#create_account_btn');

            $(password1).removeAttr('disabled');
            $(password2).removeAttr('disabled');
            $(role).removeAttr('disabled');
            $(create_btn).removeAttr('disabled');

            $(password1).removeAttr('tabindex');
            $(password2).removeAttr('tabindex');
            $(role).removeAttr('tabindex');

            $('#otp_confirmation_form').addClass('hidden');

            $('#get_otp').addClass('hidden');
            $('#verified_email').removeClass('hidden');
        }
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