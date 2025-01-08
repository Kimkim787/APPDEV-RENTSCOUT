$(document).ready(function(){
    $('#upload_btn').on('click', function(){
        $('input[name="profile_image"]').trigger('click');
    })

    $('#profile_pic_input').on('change', function(){
        previewImage(this, $('#profile_img'))
    })

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