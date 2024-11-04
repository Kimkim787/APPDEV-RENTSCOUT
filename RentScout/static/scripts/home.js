$(document).ready(function(){
    let building_container = $('#buildings_container');
    let filter = null;
    if($('#filter_value').val()){
        filter = $('#filter_value').val();
    }

    $('#filter_btn').on('click', function(){
        filter = $('#filter_value').val();
        request_buildings();
    });
    // FILTER SEARCH ON ENTER
    $('#filter_value').on('keydown', function(event){
        if(event.which == 13){
            filter = $(this).val();
            request_buildings();
        }
    });
    // PAGE SELECTED CLICK
    $('#buildings_container').on('click', '.page_numbers', function(){
        filter = $('#filter_value').val();
        console.log($(this).attr('value'));
        request_buildings($(this).attr('value'));

    });

    // PREVIOUS BUTTON CLICK
    $('#buildings_container').on('click', '#prev_btn', function(){
        filter = $('#filter_value').val();
        let current_page = $('#buildings_container').find('.active_page').attr('value');
        console.log(current_page);
        request_buildings(parseInt(current_page - 1));
    })

    // NEXT BUTTON CLICK
    $('#buildings_container').on('click', '#next_btn', function(){
        filter = $('#filter_value').val();
        let current_page = $('#buildings_container').find('.active_page').attr('value');
        console.log(current_page);
        request_buildings(parseInt(current_page + 1));
    })

    request_buildings();
    
    function request_buildings(page_val){
        building_container.empty();
        let page = 1;
        
        if(page_val != null){
            page = page_val;
        }

        console.log("Btn: " + page_val);
        console.log('page: ' + page);
        $.ajax({
            url: '/home_page/request/buildings/',
            type: 'GET',
            data: {
                'page': page,
                'filter': filter,
            },
            success: function(response){
                console.log(response);
                $.each(response.building_datas, function(index, building){
                    
                    // FOR DISPLAYING BUILDINGS
                    let box = $('<div></div>', {
                        class: 'buildingbox'
                    })
                    let anchor_tag = $('<a></a>', {
                        href: `building_info/${building.building_id}/`,
                    })
                    let image = $('<img>', {
                        src: building.building_image,
                        alt: `Image of ${building.building_name}`
                    })
                    let div = $('<div></div>', {
                        class: 'building_address_container'
                    })
                    let h6 = $('<h6></h6>', {
                        text: building.building_address
                    })

                    let building_name = $('<h3></h3>', {
                        text: building.building_name,
                    })

                    div.append(h6);
                    anchor_tag.append(image);
                    anchor_tag.append(div);

                    box.append(building_name);
                    box.append(anchor_tag);

                    building_container.append(box);
                    // END FOR DISPLAYING BUILDINGS
                })

                if(response.total_pages <=1 ){
                    return;
                }
                // FOR DISPLAYING PAGES
                
                let paginator_container = $('<div></div>', {
                    id: 'paginator_container'
                });

                    // PREVIOUS BUTTON]
                if(response.has_previous == true){
                    let previous_btn = $('<button></button>', {
                        id: 'prev_btn',
                        text: '<'
                    });
                    paginator_container.append(previous_btn);
                }
                    // PAGES BUTTONS
                for(let i=1; i<=response.total_pages;i++){
                    let page_number = $('<button></button>', {
                        class: 'page_numbers' + (response.current_page === i ? ' active_page': ''),
                        text: i,
                        value: i
                    })
                    paginator_container.append(page_number);
                }

                    // NEXT BUTTON
                if(response.has_next == true){
                    let next_btn = $('<button></button>', {
                        id: 'next_btn',
                        text: '>'
                    });
                    paginator_container.append(next_btn);
                }

                building_container.append(paginator_container);
            },
            error: function(){

            }
        })
    }
})