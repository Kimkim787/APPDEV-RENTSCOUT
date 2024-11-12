$(document).ready(function(){
    let building_container = $('#buildings_container');
    let number_pages = $('#number_pages');
    let filter = null;
    let current_page = 1;  // Added global variable to track the current page

    if ($('#filter_value').val()) {
        filter = $('#filter_value').val();
    }

    $('#filter_btn').on('click', function () {
        filter = $('#filter_value').val();
        current_page = 1;  // Reset to page 1 when a new filter is applied
        request_buildings();
    });

    // FILTER SEARCH ON ENTER
    $('#filter_value').on('keydown', function (event) {
        if (event.which == 13) {
            filter = $(this).val();
            current_page = 1;  // Reset to page 1 when a new filter is applied
            request_buildings();
        }
    });

    // PAGE SELECTED CLICK
    $('#number_pages').on('click', '.page_numbers', function () {
        filter = $('#filter_value').val();
        current_page = parseInt($(this).attr('value'));  // Update current page based on clicked button
        request_buildings(current_page);
    });

    // HEART ICON CLICK (BOOKMARK)
    building_container.on('click', '.heart_sign', function(){
        console.log($(this));
        if($(this).hasClass('heart-active')){
            remove_bookmark($(this));
        } else {
            add_bookmark($(this));
        }
        
    }) 


    // PREVIOUS BUTTON CLICK
    $('#number_pages').on('click', '#prev_btn', function () {
        if (current_page > 1) {
            current_page--;  // Decrease current page
            request_buildings(current_page);
        }
    });

    // NEXT BUTTON CLICK
    $('#number_pages').on('click', '#next_btn', function () {
        current_page++;  // Increase current page
        request_buildings(current_page);
    });

    request_buildings();

    function request_buildings(page_val) {
        building_container.empty();
        number_pages.empty();
        let page = page_val || 1;

        $.ajax({
            url: '/home_page/request/buildings/',
            type: 'GET',
            data: {
                'page': page,
                'filter': filter,
            },
            success: function (response) {
                console.log(response);

                // Display buildings
                $.each(response.building_datas, function (index, building) {
                    let box = $('<div></div>', { class: 'buildingbox' });
                    let anchor_tag = $('<a></a>', { href: `building_info/${building.building_id}/` });
                    let image = $('<img>', {
                        src: building.building_image,
                        alt: `Image of ${building.building_name}`
                    });
                    let div = $('<div></div>', { class: 'building_address_container' });
                    let anchor_tag2 = $('<a></a>', {
                        text: building.building_address,
                        href: `building_info/${building.building_id}/`,
                    });

                    let name_heart_box = $('<div></div>', { class: 'name_heart_box' });
                    let building_name = $('<h5></h5>', { text: building.building_name });
                    let heart_sign = $('<div></div>', {
                        class: 'heart_sign',
                        value: building.building_id
                    });

                    if (building.bookmark_status) {
                        heart_sign.addClass('heart-active')
                    }

                    div.append(anchor_tag2);
                    name_heart_box.append(building_name);
                    name_heart_box.append(heart_sign);
                    box.append(name_heart_box);
                    anchor_tag.append(image);

                    box.append(anchor_tag);
                    box.append(div);

                    building_container.append(box);
                });

                if (response.total_pages <= 1) {
                    return;
                }

                // Display pages
                let paginator_container = $('<div></div>', { id: 'paginator_container' });

                // PREVIOUS BUTTON
                if (response.has_previous) {
                    let previous_btn = $('<button></button>', {
                        id: 'prev_btn',
                        text: '<'
                    });
                    paginator_container.append(previous_btn);
                }

                // PAGES BUTTONS
                for (let i = 1; i <= response.total_pages; i++) {
                    let page_number = $('<button></button>', {
                        class: 'page_numbers' + (response.current_page === i ? ' active_page' : ''),
                        text: i,
                        value: i
                    });
                    paginator_container.append(page_number);
                }

                // NEXT BUTTON
                if (response.has_next) {
                    let next_btn = $('<button></button>', {
                        id: 'next_btn',
                        text: '>'
                    });
                    paginator_container.append(next_btn);
                }

                number_pages.append(paginator_container);
            },
            error: function () {
                console.log("Error loading buildings");
            }
        });
    }

    function add_bookmark(btn){
        building_id = $(btn).attr('value');
        console.log(building_id);
        $.ajax({
          url: '/user/bookmark/add/',
          type: 'POST',
          data: {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'buildingid': building_id
          },
          success: function(){
            $(btn).toggleClass('heart-active');
          },
          error: function(xhr, status, error){
            console.log(error);
            alert(`Error: ${xhr.responseText.error || error}`);
          }
        });
      }

    function remove_bookmark(btn){
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
            },
            error: function(xhr, status, error){
            console.log(error);
            alert(`Error: ${xhr.responseText.error || error}`);
            }
        })
    }

})