emailjs.init("Q_A-eXEwrvvQsFMYs");
$(document).ready(function(){
    $('#upload_btn').on('click', function(){
        $('input[name="profile_image"]').trigger('click');
    })

    $('#profile_pic_input').on('change', function(){
        previewImage(this, $('#profile_img'))
    })

    $('#get_otp').on('click', function(){
        const email = $('input[name="email"]').val();
        send_otp(email);
    })

    $('#resend_otp').on('click', function(){
        const email = $('input[name="email"]').val();
        send_otp(email);
    })
    
    // CONFIRM CODE BUTTON
    $('#confirm_otp').on('click', function(){
        validate_otp($(this));
    })

    $('#close_otp_modal').on('click', function(){
        $('#modal_body').addClass('hidden');
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
                      SoloMessageFlow(`OTP was sent to ${email}`, 'success');
                      $('#modal_body').removeClass('hidden');
                      $('#user_email').text(email);
                    },
                    function(error) {
                        console.log(error);
                        SoloMessageFlow("Failed to send email.", 'error');
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
        const inputted_otp = $('#OTP').val();
        console.log(saved_otp);
        console.log(inputted_otp);
        if(!(saved_otp === inputted_otp)){
            console.log('otp did not match');
            SoloMessageFlow('OTP did not match', 'error');
            return;
        } else { 
            $.ajax({
                url: '/signup/get_otp/',
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                },
                success: function(response){
                    SoloMessageFlow(response.success);
                    location.reload();
                }, 
                error: function(response){
                    SoloMessageFlow(response.error, 'error');
                    location.reload();
                }
            })
            SoloMessageFlow('Successfully Verified');
            $('#modal_body').removeClass('hidden');
        }
    }


    function previewImage(input, imgElement) {
        if (input.files && input.files[0]) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                $(imgElement).attr('src', e.target.result);
            }
            
            reader.readAsDataURL(input.files[0]);
        }
    }

});