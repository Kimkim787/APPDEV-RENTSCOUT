$(document).ready(function(){
    request_bookmarks();
    $('#buildings').on('click', '.heart_sign', function(){
        remove_bookmark($(this));
    });

    function request_bookmarks(){
        const section = $('section');
        $.ajax({
            url: '/user/bookmark/request/',
            type: 'GET',
            data: {
                'page': 1,
                'filter': ''
            },
            success: function(response_data){
                console.log(response_data);
                $.each(response_data.bookmarks, function(index, bookmark){
                    let box = $('<div></div>', {
                        class: 'buildingbox'
                    })
                    let anchor_tag = $('<a></a>', {
                        href: `/building_info/${bookmark.building_id}/`,
                    })
                    let image = $('<img>', {
                        src: bookmark.building_image,
                        alt: `Image of ${bookmark.building_name}`
                    })
                    let div = $('<div></div>', {
                        class: 'building_address_container'
                    })
                    let anchor_tag2 = $('<a></a>', {
                        text: bookmark.building_address,
                        href: `/building_info/${bookmark.building_id}/`,
                    })

                    let building_name = $('<h5></h5>', {
                        text: bookmark.building_name,
                    })

                    let name_heart_box = $('<div></div>', { class: 'name_heart_box' });
                    
                    let heart_sign = $('<div></div>', {
                        class: 'heart_sign',
                        value: bookmark.building_id
                    })

                    div.append(anchor_tag2);
                    name_heart_box.append(building_name);
                    name_heart_box.append(heart_sign);
                    anchor_tag.append(image);
                    box.append(name_heart_box);
                    box.append(anchor_tag);
                    box.append(div);
                    
                    
                    $('#buildings').append(box);
                    
                })
            }, 
            error: function(xhr) {
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    SoloMessageFlow(xhr.responseJSON.error, "error");
                } else {
                    SoloMessageFlow('An unexpected error occurred', "error");
                }
            }
        })
    }

    function remove_bookmark(btn){
        console.log(btn);
        building_id = $(btn).attr('value');
        $.ajax({
            url: '/user/bookmark/delete/',
            type: 'POST',
            data: {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'building_id': building_id
            },
            success: function (){
                $(btn).removeClass('heart-active')
                SoloMessageFlow("Removed from Bookmark", "success");

                $(btn).closest('.buildingbox').remove();
            },
            error: function(xhr, status, error) {
                let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
                SoloMessageFlow(`${errorMessage}`, 'error');
              }
        })
    }

}) // ready function