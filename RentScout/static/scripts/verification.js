$(document).ready(function(){
    request_pending_verifications();

    // DENY VERIFICATION BUTTON CLICK
    $('#verifications_container').on('click', '.deny_btn', function(){
        deny_verification($(this));
    })

    // ACCEPT VERIFICATION BUTTON CLICK
    $('#verifications_container').on('click', '.accept_btn', function(){
        accept_verification($(this));
    })

    // DENY BUTTON ON DENY MODAL
    $('#verification_modal').on('click', '#save_deny', function(){
        console.log('final Deny');
        continue_deny_verification($(this));
    })

    // CANCEL BUTTON ON DENY MODAL
    $('#verification_modal').on('click', '#cancel_deny', function(){
        $('#building_name').text('');
        $('#building_owner').text('');
        $('#save_deny').removeAttr('value');
    })

    function request_pending_verifications(page=null){
        const container = $('#verifications_container');
        container.empty();
        get_page = page ? page != null : 1;
        $.ajax({
            url: '/building/request/verification_requests/',
            type: 'GET',
            data: {
                'page': get_page
            },
            success: function(response){
                console.log(response)

                $.each(response.verification_requests, function(index, verification){
                    const verification_item_box = $('<div></div>', {
                        class: 'verification_item'
                    })
    
                    const center_div = $('<div></div>', {
                        class: 'center_div'
                    })

                    const button_div = $('<div></div>', {
                        class: 'button_div',
                    })

                    const building_image = $('<img/>', {
                        class: 'building_image',
                        alt: 'image of ' + verification.building_name,
                        src: verification.building_image
                    })

                    const building_name = $('<a></a>', {
                        text: verification.building_name,
                        href: `/building_info/${verification.buildingid}`,
                        target: '_blank',
                        class: 'building_name'
                    })

                    const building_owner = $('<a></a>', {
                        text: verification.building_owner_email,
                        href: `/user/user_profile_admin_access/${verification.building_owner_id}`,
                        target: '_blank',
                        class: 'owner_name'
                    })

                    const description = $('<p></p>', {
                        text: verification.building_description,
                        class: 'building_description',
                    })

                    // DESIGN LIKE BUTTON
                    const view_profile = $('<a></a>', {
                        text: 'View Owner Profile',
                        href: `/user/user_profile_admin_access/${verification.building_owner_id}`,
                        target: '_blank',
                        class: 'view_user_profile_btn'
                    })

                    //DESIGN LIKE BUTTON
                    const view_building = $('<a></a>', {
                        text: 'View Building',
                        href: `/building_info/${verification.buildingid}`,
                        target: '_blank',
                        class: 'view_building_btn'
                    })

                    const building_map = $('<a></a>', {
                        text: 'View Map',
                        href: verification.building_coordinates,
                        target: '_blank',
                        class: 'view_map_btn'
                    })

                    const deny_btn = $('<button></button>', {
                        class: 'deny_btn',
                        text: "Deny",
                        value: verification.verificationid
                    })

                    const accept_btn = $('<button></button>', {
                        class: 'accept_btn',
                        text: "Accept Verification",
                        value: verification.verificationid
                    })
                    
                    center_div.append(building_name);
                    center_div.append(building_owner);
                    center_div.append(description);

                    button_div.append(view_profile);
                    button_div.append(view_building);
                    button_div.append(building_map);
                    button_div.append(deny_btn);
                    button_div.append(accept_btn);
                    
                    verification_item_box.append(building_image);
                    verification_item_box.append(center_div);
                    verification_item_box.append(button_div);

                    container.append(verification_item_box);
                }) // end each
                
            },
            error: function(xhr) {
                console.error("Error:", xhr.responseJSON.error);
            }
        })
    }

    // DENY VERIFICATION FORM
    function deny_verification(btn){
        const verificationid = $(btn).attr('value');
        console.log(verificationid)
        $.ajax({
            url: '/building/deny_verification/',
            type: 'GET',
            data: {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'verificationid': verificationid,
            },
            success: function(response){
                console.log(response);
                $('#building_name').text(response.building_name);
                $('#building_owner').text(response.building_owner);
                $('#save_deny').attr('value', verificationid);
            },
            error: function(xhr) {
                console.error("Error:", xhr.responseJSON.error);
            }

        })
    }

    // FINALIZE DENY VERIFICATION
    function continue_deny_verification(btn){
        const verificationid = $(btn).attr('value');
        console.log('continue deny')
        $.ajax({
            url: '/building/deny_verification/',
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'verificationid': verificationid,
            },
            success: function(response){
                alert(response.success);
                request_pending_verifications();
            },
            error: function(xhr) {
                console.error("Error:", xhr.responseJSON.error);
            }

        })
    }

    function accept_verification(btn){
        const verificationid = $(btn).attr('value');
        console.log('accept')
        $.ajax({
            url: '/building/accept_verification/',
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'verificationid': verificationid,
            },
            success: function(response){
                alert(response.success);
                request_pending_verifications();
            },
            error: function(xhr) {
                console.error("Error:", xhr.responseJSON.error);
            }

        })
    }
});