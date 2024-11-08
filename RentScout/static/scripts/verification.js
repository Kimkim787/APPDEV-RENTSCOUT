$(document).ready(function(){
    request_pending_verifications();

    function request_pending_verifications(page=null){
        const container = $('#verifications_container');
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
                        href: `building_info/${verification.buildingid}`,
                        class: 'building_name'
                    })

                    const building_owner = $('<a></a>', {
                        text: verification.building_owner_email,
                        href: `/user/user_profile_admin_access/${verification.building_owner_id}`,
                        class: 'owner_name'
                    })

                    const description = $('<p></p>', {
                        text: verification.building_description,
                        class: 'building_description',
                    })

                    const view_profile = $('<button></button>', {
                        class: 'view_user_profile_btn',
                        text: "View User Profile",
                        value: verification.building_owner_id
                    })

                    const view_building = $('<button></button>', {
                        class: 'view_building',
                        text: "View Building",
                        value: verification.buildingid
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

                    button_div.append(view_building);
                    button_div.append(view_profile);
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
});