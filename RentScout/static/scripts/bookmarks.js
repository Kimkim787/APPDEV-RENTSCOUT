$(document).ready(function(){
    request_bookmarks();
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

                    let building_name = $('<h3></h3>', {
                        text: bookmark.building_name,
                    })
                    
                    let heart_sign = $('<div></div>', {
                        class: 'heart_sign',
                        value: bookmark.building_id
                    })

                    div.append(anchor_tag2);
                    anchor_tag.append(building_name);
                    anchor_tag.append(image);
                    
                    box.append(anchor_tag);
                    box.append(div);
                    box.append(heart_sign);
                    
                    $('section').append(box);
                })
            }, 
            error: function(){

            }
        })
    }
}) // ready function