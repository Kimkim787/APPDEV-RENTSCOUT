$(document).ready(function(){
    $('#add_building_btn').on('click', function(){
        $('.form_item').addClass("hidden");
        $('#new_building_form').removeClass('hidden');
        $('.bar_room').addClass('hidden');
    })

    // "SEE PHOTOS" BUTTON CLICKED
    $('#rooms_container').on('click', '.photo_btn', function(){
        let room_id = $(this).closest('.room_item').find('input[class="roomid_holder"]').val();
        $('.form_item').addClass('hidden');
        $('#add_room_btn').addClass('hidden');
        $('#edit_room_form').addClass('hidden');
        show_room_photos($(this));
        $('#upload_room_photo').removeClass('hidden');
        $('#upload_roomid_holder').val(room_id);
    });

    // Image clicked
    $('#photo_container').on('click', '.room_photos', function(){
        $('.form_item').addClass('hidden');
        $('#large_image_view').removeClass('hidden');
        // assign background-img to Large image View
        $('#large_image_view').css('background-image', `url('${$(this).attr('src')}')`);
    })

    // REQUEST ROOM BTN
    $('#rooms_container').on('click', '.room_update_btn', function(){
        $('.form_item').addClass('hidden');
        $('#edit_room_form').removeClass('hidden');
        request_room_data($(this));
    });

    // ADD ROOM BTN ON MIDDLE BAR
    $('#add_room_btn').on('click', function(){
        $('#room_id_holder').attr('value', $(this).attr('value'));
        $('.form_item').addClass('hidden');
        $('#new_room_form').removeClass('hidden');
        
    })

    $('#addroomsave').on('click', function(){
        create_new_room($(this));
    })

    // UPDATE ROOM BTN
    $('#edit_room_form').on('click', '#edit_room_save', function(){
        update_room($(this));
    })
    
    $('#building_update_form').on('submit', function(event){
        event.preventDefault();
        update_building();
    });

    $('#add_policy_btn').on('click', function(event){
        event.preventDefault();
        show_newpolicy_form();
    });

    // CERTIFICATE BUTTON
    $('#add_certificate_btn').on('click', function(){
        $('#upload_certificate').removeClass('hidden');
    });

    // AMENITIES CREATION BUTTON
    $('#amenities_create_form').on('click', '#create_amenity_btn', function(event){
        console.log('create amentiy butn');
        create_amenity($(this));
    })

    // AMENITIES UPDATE BUTTON
    $('#amenity_update_form').on('click', '#update_amenity_btn', function(e){
        update_amenity($(this));
    })

    // CANCEL POLICY CREATION FORM
    $('#policies_container').on('click', '#new_pol_cancel_btn', function(e){
        $('#new_pol_form').remove();
    });

    // POLICY CREATION BUTTON
    $('#policies_container').on('click', '#new_pol_save_btn', function(e){
        save_new_policy($(this));
    });

    $('#policies_container').on('click', '.pol_del_btn', function(){
        if(confirm("Are you sure you want to delete this policy?")){
            delete_policy($(this));

        };
    })

    // POLICY EDIT BTN
    $('#policies_container').on('click', '.pol_edit_btn', function() {
        let li = $(this).closest('li');
        let old_policy = li.find('p[class="policy"]').text();
        let policy_id = li.find('input').val();
    
        // Clear the content of `li` but keep the ID in the button
        li.empty();
    
        let textarea = $('<textarea></textarea>', {
            class: 'edit_policy_text',
            text: old_policy
        });
    
        let submit_btn = $('<button></button>', {
            text: 'Save',
            class: 'save_update_policy',
            'data-policy-id': policy_id // Store policy_id here
        });
        
    
        li.append(textarea);
        li.append(submit_btn);
    });
    

    // POLICY SAVE EDIT BTN
    $('#policies_container').on('click', '.save_update_policy', function(){
        update_policy($(this));
    })

    // TOGGLE FORMS
    $('.edit_btn').on('click', function() {
        // hide forms (third column)
        $('.form_item').addClass('hidden');

        // Hide Middle Bar
        $('#room_bar').addClass('hidden');

        // HIDE Certificate Things
        $('#certificate_bar').addClass('hidden');
        $('#upload_certificate').addClass('hidden');

        // get building id
        let buildingId = $(this).closest('ul').find('.building_id').val();
        
            // EDIT BUILDING
        if($(this).val() == 'Edit Building'){
            $('#building_form').removeClass('hidden');
            // set building id to form
            $('#building_id_holder').val(buildingId);
            console.log(buildingId)
            request_bldg_instance(buildingId);

            // CERTIFICATES
        } else if ( $(this).val() == 'Certificates'){
            let building_id = $(this).closest('ul').find('input[class="building_id"]').val();
            console.log(building_id);
            $('#certificate_bar').removeClass('hidden');
            $('#upload_certificate').removeClass('hidden');
            $('#upload_buildingid_holder').val(building_id);
            request_certificates($(this));

            // AMENITIES
        } else if( $(this).val() == 'Amenities'){
            $('#amenities_section').removeClass('hidden');
            request_amenity($(this));
            // POLICIES
        } else if( $(this).val() == 'Policies'){
            $('#policies_form').removeClass('hidden');

                // ADD VALUE TO ADD_POLICY_BTN FOR QUERY
            $('#add_policy_btn').val(buildingId);
            request_bldg_policies(buildingId)
            
            // ROOMS
        } else if ($(this).val() == 'Rooms') {
            // REQUEST PHOTOS FOR MIDDLE BAR
            console.log('clicked rrom');
            $('#room_bar').removeClass('hidden');
            request_rooms(btn_elem=$(this));
            $('#add_room_btn').removeClass('hidden');

            // UPLOAD PHOTO BTN
        } else if ($(this).attr('value') == 'upload_room_photo'){
            console.log('UPload Phto BTN')
            let room_id = $(this).closest('div').find('#roomid_holder').val();
            $('#room_bar').removeClass('hidden');
            $('#upload_room_photo').removeClass('hidden');
            $('#upload_room_holder').val(room_id);
        }

    }) // edit_btn on click

    // middle bar back btn
    $('.backbtn').on('click', function(){
        $('#photo_view').toggleClass('hidden');
        $('#room_view').toggleClass('hidden');
        $('#add_room_btn').toggleClass('hidden');
        $('#upload_room_photo').addClass('hidden');
        $('#large_image_view').addClass('hidden');
    });    

    // UPDATE BILDING GET FUNCTION
    function request_bldg_instance(bldg_id){
        $.ajax({
            url: '/building/update_view/',
            type: 'GET',
            data: {
                'bldg_id': bldg_id,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(data){
                $('#bldg_name').val(data.building_name);
                $('#bldg_price').val(data.price);
                $('#bldg_vacant').val(data.rooms_vacant);
                $('#bldg_zipcode').val(data.zip_code);
                $('#bldg_street').val(data.street);
                $('#bldg_city').val(data.city);
                $('#bldg_province').val(data.province);
                $('#bldg_country').val(data.country);
                $('#bldg_desc').val(data.details);
                $('#bldg_coords').val(data.coordinates);
            },
            error: function(xhr, status, error){
                console.log(`${status}: ${error}`);
            }
        });
    }

    // UPDATE BUILDING POST FUNCTION
    function update_building(){
        form_data = {
            'bldg_id': $('#building_id_holder').val(),
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'building_name': $('#bldg_name').val(),
            'price': $('#bldg_price').val(),
            'rooms_vacant': $('#bldg_vacant').val(),
            'zip_code': $('#bldg_zipcode').val(),
            'street': $('#bldg_street').val(),
            'city': $('#bldg_city').val(),
            'province': $('#bldg_province').val(),
            'country': $('#bldg_country').val(),
            'details': $('#bldg_desc').val(),
            'coordinates': $('#bldg_coords').val(),
        }
        console.log(form_data);
        $.ajax({
            url: "/building/update_view/",
            type: 'POST',
            data: form_data,
            success: function(){
                SoloMessageFlow("Successfully saved.");
            },
            error: function(xhr) {
                console.error("Error:", xhr.responseJSON.error);
            }
        })
    }

    function create_new_room(btn){
        const buildingid = $(btn).closest('#room_form').find('input[id="room_id_holder"]').val();
        form_data = {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'buildingid': buildingid,
            'room_name': $('#room_form').find('input[name="room_name"]').val(),
            'person_free': $('#room_form').find('input[name="person_free"]').val(),
            'current_male': $('#room_form').find('input[name="current_male"]').val(),
            'current_female': $('#room_form').find('input[name="current_female"]').val(),
            'price': $('#room_form').find('input[name="price"]').val(),
            'room_size': $('#room_form').find('input[name="room_size"]').val(),
            'bed': $('#room_form').find('input[name="bed"]').val(),
            'double_deck': $('#room_form').find('input[name="double_deck"]').val(),
        
            'shower': $('#room_form').find('input[name="shower"]').is(':checked'),
            'priv_bathroom': $('#room_form').find('input[name="priv_bathroom"]').is(':checked'),
            'public_bathroom': $('#room_form').find('input[name="public_bathroom"]').is(':checked'),
            'AC': $('#room_form').find('input[name="AC"]').is(':checked'),
            'wardrobe': $('#room_form').find('input[name="wardrobe"]').is(':checked'),
            'kitchen': $('#room_form').find('input[name="kitchen"]').is(':checked'),
            'free_wifi': $('#room_form').find('input[name="free_wifi"]').is(':checked')
        }
        $.ajax({
            url: '/room/create_view/',
            type: 'POST',
            data: form_data,
            success: function(){
                alert('Successfully created new Room');
                console.log(buildingid);
                request_rooms(null, buildingid);
            },
            error: function(xhr) {
                console.error("Error:", xhr.responseJSON.error);
            }
        })
    }

    // REQUEST ROOMS FOR MIDDLE BAR
    function request_rooms(btn_elem=null, btn_id=null ) {
        $('#photo_container').empty();
        $('#rooms_container').empty();
        let query = null;
        if(btn_elem != null){
            query = $(btn_elem).closest('ul').find('.building_id').val();
        } else {
            query = btn_id;
        }
        console.log("Room Query is: " + query);
        // assign building id to add room btn
        $('#add_room_btn').attr('value', query);
    
        $.ajax({
            url: '/room/get_rooms/',
            data: {
                'building_id': query,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(data) {
                console.log(data);
                if (data.room_data.length >= 1) {
                    $.each(data.room_data, function(index, room) {
                        let room_div = $("<div></div>", {
                            class: 'room_item'
                        });
    
                        let input = $('<input>', {
                            type: 'hidden',
                            class: 'roomid_holder'
                        }).val(room.roomid);
    
                        let btn_div = $('<div></div>', {
                            class: 'btn_div'
                        });
    
                        let p = $('<h2></h2>', {
                            id: 'room_name'
                        }).text(room.room_name);
    
                        let photo_btn = $('<button></button>', {
                            text: "See Photos",
                            class: "photo_btn",
                        });
    
                        let update_btn = $('<button></button>', {
                            text: "Update Room",
                            class: 'room_update_btn',
                        });
    
                        room_div.append(input);
                        btn_div.append(photo_btn);
                        btn_div.append(update_btn);
                        room_div.append(p);
                        room_div.append(btn_div);
    
                        $('#rooms_container').append(room_div);
    
                        $('.mid_item').addClass('hidden');
                        $('#room_view').removeClass('hidden');
                    });
                } else {
                    $('.mid_item').addClass('hidden');
                    $('#no_room_message').removeClass('hidden');
                }
            },
            error: function(xhr) {
                console.error("Error:", xhr.responseJSON.error);
            }
        });
    }

    // SHOW ROOM PHOTOS TO MIDDLE BAR
    function show_room_photos(btn = null, room_id = null){
        // initalize = empty
        console.log("show room photos")
        $('#photo_container').empty();

        // get roomid from hidden input
        query = null;
        if(btn){
            query = $(btn).closest('.room_item').find('.roomid_holder').val();
        } else if(room_id){
            query = room_id;
        } else{
            return;
        }
        
        // roomid_holder on middle section
        $('#roomid_holder').val(query);
        // roomid_holder on upload upload form
        $('#upload_room_holder').val(query);

        $.ajax({
            url: '/room_photo/request/',
            data: {
                'roomid': query,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(data) {
                // set ROOM NAME
                $('#photo_name').text(data.room_name);
                console.log(data.image_list);
                $.each(data.image_list, function( index, photo){
                    let li = $("<li></li>");

                    let del_btn = $('<img>', {
                        src: deleteIconUrl,  // Assuming deleteIconUrl is already defined in the template
                        alt: 'Delete',
                        class: 'delete-icon',
                        title: 'Delete',  // Tooltip for accessibility
                        click: function() {
                            if (confirm('Are you sure you want to delete this photo?')) {
                                fn_delete_room_photo($(this));
                            }
                        }
                    });
                    
                    
                    let id_holder = $('<input>', {
                        type: 'hidden',
                        name: 'img_id',
                        value: photo.photo_id,
                    })

                    let img = $("<img>", {
                        class: 'room_photos',
                        alt: "image " + photo.photo_id,
                        src: photo.photo_url,
                    });
                    
                    li.append(del_btn);
                    li.append(id_holder);
                    li.append(img);

                    $('#photo_container').append(li);
                })

                $('#room_view').addClass('hidden');
                $('#photo_view').removeClass('hidden'); 
            },
            error: function(xhr, status, error) {
                console.log(xhr.responseText);
                alert(`${xhr}: ${status}`);
            }


        }); // ajax
    }

    $('#upload_certificate_btn').on('click', function () {
        // Retrieve building ID from hidden input
        const buildingId = $('#upload_buildingid_holder').val();
        console.log('Building ID:', buildingId);
    
        // Get file input element
        const fileInput = document.getElementById('certificate-upload');
        if (!fileInput.files || fileInput.files.length === 0) {
          alert('Please select a file');
          return;
        }
    
        // Create FormData from the form
        const formData = new FormData($('#certificate-upload-form')[0]);
        for (const [key, value] of formData.entries()) {
            console.log(key + ": " + value);
        }
        // Submit form data using Axios
        axios
          .post('/certificate/upload/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          })
          .then(function (response) {
            alert('Upload successful!');
            resetFileUpload2();
          })
          .catch(function (error) {
            console.error(error);
            alert(
              `Error: ${
                error.response?.data?.error || 'Upload failed!'
              }`
            );
        });
    });

    $('#upload_room_photo_btn').on('click', function () {
        // Retrieve room ID from hidden input
        const roomId = $('#upload_roomid_holder').val();
        console.log('Room ID:', roomId);

        // Get file input element
        const fileInput = document.getElementById('room-photo-upload');
        if (!fileInput.files || fileInput.files.length === 0) {
        alert('Please select a file');
        return;
        }

        // Create FormData from the form
        const formData = new FormData($('#room-photo-upload-form')[0]);

        // Submit form data using Axios
        axios
        .post('/room_photo/upload/as_view/', formData, {
            headers: {
            'Content-Type': 'multipart/form-data',
            },
        })
        .then(function (response) {
            alert('Room photo upload successful!');
            show_room_photos(null, roomId);
            resetFileUploadRoomPhoto();

        })
        .catch(function (error) {
            console.error(error);
            alert(
            `Error: ${
                error.response?.data?.error || 'Room photo upload failed!'
            }`
            );
        });
    });

    // DELETE PHOTO_VIEW
    function fn_delete_room_photo(button){
        let query = $(button).siblings('input[name="img_id"]').val();
        console.log(query);
        $.ajax({
            url: '/room_photo/delete/view/',
            type: 'POST',
            data: {
                'photo_id': query,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response, status, message){
                button.closest('li').remove(); // Remove the <li> from the DOM
                alert("Successfully deleted image")
            },
            error: function(xhr, status, error){
                console.log(error);
                alert(`Error: ${xhr.responseText.error || error}`);
            }
        })
    }

    // REQUEST ROOM DATA FOR RIGHT-MOST CONTAINER
    function request_room_data(btn){
        let room_id = $(btn).closest('.room_item')
            .find('input[class="roomid_holder"]').val();
        
        let form_container = $('#edit_room_form_container');
        $.ajax({
            url: '/room/request/',
            type: 'GET',
            data: {
                'primary_key': room_id,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },

            success: function(response_data){
                console.log(response_data);
                form_container.html(`
                    <div class="editroombox">
                        <div class="editroombox2">
                            <div class="lblinptdiv">
                                <label for="room_name">Room Name:</label>
                                <input type="text" name="room_name" value="${response_data.room_name}">
                            </div>
                            <div class="lblinptdiv">
                                <label for="person_free">Person Available:</label>
                                <input type="text" name="person_free" value="${response_data.person_free}">
                            </div>
                            <div class="lblinptdiv">
                                <label for="current_male">Male resident:</label>
                                <input type="text" name="current_male" value="${response_data.current_male}">
                            </div>
                            <div class="lblinptdiv">
                                <label for="current_female">Female resident:</label>
                                <input type="text" name="current_female" value="${response_data.current_female}">
                            </div>
                            
                            <div class="lblinptdiv">
                                <label for="room_size">Room Size:</label>
                                <input type="text" name="room_size" value="${response_data.room_size}">
                            </div>
                        </div>

                        <p><b>Additional Information:</b></p>
                    
                        <div class="lblinptdiv">
                            <label for="bed">Single bed:</label>
                            <input type="text" name="bed" value="${response_data.bed}">
                        </div>
                        <div class="lblinptdiv">
                            <label for="double_deck">Double bed:</label>
                            <input type="text" name="double_deck" value="${response_data.double_deck}">
                        </div>
                        
                        <div class="additionalinfobox">
                            <div class="checkboxsdiv">
                                <input type="checkbox" name="shower" ${response_data.shower ? 'checked' : ''}>
                                <label for="shower">Shower</label>
                            </div>
                            <div class="checkboxsdiv">
                                <input type="checkbox" name="priv_bathroom" ${response_data.priv_bathroom ? 'checked' : ''}>
                                <label for="priv_bathroom">Private Bathroom</label>
                            </div>
                            <div class="checkboxsdiv">
                                <input type="checkbox" name="public_bathroom" ${response_data.public_bathroom ? 'checked' : ''}>
                                <label for="public_bathroom">Public Bathroom</label>
                            </div>
                            <div class="checkboxsdiv">
                                <input type="checkbox" name="AC" ${response_data.AC ? 'checked' : ''}>
                                <label for="AC">Air Conditioned</label>
                            </div>
                            <div class="checkboxsdiv">
                                <input type="checkbox" name="wardrobe" ${response_data.wardrobe ? 'checked' : ''}>
                                <label for="wardrobe">Wardrobe</label>
                            </div>
                            <div class="checkboxsdiv">
                                <input type="checkbox" name="kitchen" ${response_data.kitchen ? 'checked' : ''}>
                                <label for="kitchen">Kitchen</label>
                            </div>
                            <div class="checkboxsdiv">
                                <input type="checkbox" name="free_wifi" ${response_data.free_wifi ? 'checked' : ''}>
                                <label for="free_wifi">Free Wifi</label>
                            </div>
                        </div>
                    </div>
                    <button id="edit_room_save" value="${response_data.roomid}">Save</button>
                `);
                // <div class="lblinptdiv">
                            //     <label for="price">Price:</label>
                            //     <input type="text" name="price" value="${response_data.price}">
                            // </div>                
            },
            error: function(xhr, status, error){
                console.log(error);
                alert(`Error: ${xhr.responseText.error || error}`);
            }
        })

    }
    
    function update_room(btn){
        let room_id = $(btn).val();
        let form = $('#edit_room_form_container');

        let form_data = {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),

            'room_id': $('#edit_room_save').val(),
            'room_name': $('input[name="room_name"]').val(),
            'person_free': $('input[name="person_free"]').val(),
            'current_male': $('input[name="current_male"]').val(),
            'current_female': $('input[name="current_female"]').val(),
            'price': $('input[name="price"]').val(),
            'room_size': $('input[name="room_size"]').val(),
            'bed': $('input[name="bed"]').val(),
            'double_deck': $('input[name="double_deck"]').val(),
        
            'shower': $('input[name="shower"]').is(':checked'),
            'priv_bathroom': $('input[name="priv_bathroom"]').is(':checked'),
            'public_bathroom': $('input[name="public_bathroom"]').is(':checked'),
            'AC': $('input[name="AC"]').is(':checked'),
            'wardrobe': $('input[name="wardrobe"]').is(':checked'),
            'kitchen': $('input[name="kitchen"]').is(':checked'),
            'free_wifi': $('input[name="free_wifi"]').is(':checked')
        };

        $.ajax({
            url: '/room_update_view/',
            type: 'POST',
            data: form_data,
            success: function(){
                alert('success');
            },
            error: function(xhr, status, error){
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    alert(`Error ${xhr.status}: ${xhr.responseJSON.error}`);
                } else {
                    alert(`Error ${xhr.status}: ${error}`);
                }
            }
        });
        $('#edit_room_form').addClass('hidden');
    }

    function request_certificates(btn){
        const buildingid = $(btn).closest('ul').find('input[class="building_id"]').val();
        $.ajax({
            url: '/certificates/get/',
            type: 'GET',
            data: {
                'buildingid': buildingid
            }, 
            success: function(response){
                console.log(response.certificates);
            }, 
            error: function(xhr, status, error) {
                let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
                SoloMessageFlow(`${errorMessage}`, 'error');
            }
        })
    }

    function show_newpolicy_form(){
        if($('#new_pol_form').length){
            console.log("Form is already shown")
            return;
        } else{
        let pol_container = $('#policies_container');
        let li = $('<li></li>', {
            id: 'new_pol_form'
        })

        let title = $('<h3></h3>', {
            id: 'new_pol_form_title',
            text: 'New Policy Form'
        })

        let addbox = $('<div></div>', {
            class: 'addbox'
        });

        let textarea = $('<textarea></textarea>', {
            name: 'policy',
            placeholder: 'Add new policy here'
        });

        let cancel_btn = $('<button></button>', {
            id: 'new_pol_cancel_btn',
            text: 'Cancel'
        })

        let save_btn = $('<button></button>', {
            id: 'new_pol_save_btn',
            text: 'Save'
        });

        addbox.append(cancel_btn);
        addbox.append(save_btn);

        // li.append(title);
        li.append(textarea);
        li.append(addbox);
        pol_container.prepend(li);  
        } // else
    }

    // GET ALL POLICIES OF BUILDING
    function request_bldg_policies(query) {
        let pol_container = $('#policies_container');
        pol_container.empty();
        $.ajax({
            url: '/building/policies_request/',
            type: 'GET',
            data: {
                'building_id': query,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            },
            success: function(data) {
                console.log(data);
                let ul = $('#policies_container');
    
                $.each(data.policy_lists, function(index, policy) {
                    let li = $('<li></li>');
                    let textarea = $('<p></p>', {
                        class: 'policy',
                        text: policy.policy
                    });
                
                    // Add hidden input to store policy_id
                    let policyIdInput = $('<input>', {
                        type: 'hidden',
                        value: policy.policy_id // Set the policy ID here
                    });
                
                    let buttonbox = $('<div></div>', {
                        class: 'buttonbox'
                    });
                
                    let del_btn = $('<button></button>', {
                        class: 'pol_del_btn',
                        text: 'Delete',
                        value: policy.policy_id
                    });
                
                    let edit_btn = $('<button></button>', {
                        class: 'pol_edit_btn',
                        text: 'Edit'
                    });
                
                    buttonbox.append(del_btn);
                    buttonbox.append(edit_btn);
                
                    // Append the hidden input and other elements to li
                    li.append(policyIdInput);
                    li.append(textarea);
                    li.append(buttonbox);
                
                    ul.append(li);
                });                
            },
            error: function(xhr, status, error) {
                alert(`Error ${xhr.status}: ${error}`);
            }
        });
    }
    

    function save_new_policy(btn){
        let bldg_id = $('#add_policy_btn').val()
        let text_element = $(btn).closest('li').find('textarea').val();
        form_inputs = {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'buildingid': bldg_id,
            'policy': text_element
        }
        $.ajax({
            url: '/building/policy/add_new/' ,
            type: 'POST',
            data: form_inputs,
            success: function() {
                refresh_policy_display();
            },
            error: function(xhr, status, error){
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    alert(`Error ${xhr.status}: ${xhr.responseJSON.error}`);
                } else {
                    alert(`Error ${xhr.status}: ${error}`);
                }
            }
        })
    }

    function delete_policy(btn){
        pol_id = $(btn).val();
        console.log(pol_id);
        $.ajax({
            url: '/building/policy/delete/',
            type: 'POST',
            data: {
                'policy_id': pol_id,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            },
            success: function(){
                refresh_policy_display();
            },
            error: function(xhr, status, error){
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    alert(`Error ${xhr.status}: ${xhr.responseJSON.error}`);
                } else {
                    alert(`Error ${xhr.status}: ${error}`);
                }
            }
        })
    }
    // REFRESH POLICY DISPLAY
    function refresh_policy_display(){
        let bldg_id = $('#add_policy_btn').val();
        let pol_container = $('#policies_container');
        request_bldg_policies(bldg_id)
    }

    function update_policy(btn) {
        let li = $(btn).closest('li');
        let policy_text = li.find('textarea.edit_policy_text').val();
        let policy_id = $(btn).data('policy-id'); // Retrieve policy_id here
    
        console.log("Policy Text:", policy_text);
        console.log("Policy ID:", policy_id); // Verify if policy_id is retrieved correctly
    
        if (!policy_id) {
            alert("Policy ID not found");
            return;
        }
    
        $.ajax({
            url: '/building/policy/update/',
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'policy_id': policy_id,
                'policy': policy_text
            },
            success: function() {
                alert('Success');
                refresh_policy_display();
            },
            error: function(xhr, status, error) {
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    alert(`Error ${xhr.status}: ${xhr.responseJSON.error}`);
                } else {
                    alert(`Error ${xhr.status}: ${error}`);
                }
            }
        });
    }
    
    


    function create_amenity(btn){
        let building_id = $(btn).val();
        let form = $(btn).closest('#amenities_create_form');
        let free_wifi = form.find('input[name="free_wifi"]').is(':checked');
        let shared_kitchen = form.find('input[name="shared_kitchen"]').is(':checked');
        let smoke_free = form.find('input[name="smoke_free"]').is(':checked');
        let janitor = form.find('input[name="janitor"]').is(':checked');
        let guard = form.find('input[name="guard"]').is(':checked');
        let waterbill = form.find('input[name="waterbill"]').is(':checked');
        let electricbill = form.find('input[name="electricbill"]').is(':checked');
        let food = form.find('input[name="food"]').is(':checked');

        form_data = {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'building_id': building_id,
            'free_wifi': free_wifi,
            'shared_kitchen': shared_kitchen,
            'smoke_free': smoke_free,
            'janitor': janitor,
            'guard': guard,
            'waterbill': waterbill,
            'electricbill': electricbill,
            'food': food,
        }

        $.ajax({
            url: '/building/amenity/create_new/',
            type: 'POST',
            data: form_data,
            success: function(){
                alert('Successfuly created Amenities');
                request_amenity(null, building_id);
            },
            error: function(xhr, status, error){
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    alert(`Error ${xhr.status}: ${xhr.responseJSON.error}`);
                } else {
                    alert(`Error ${xhr.status}: ${error}`);
                }
            }
        })
    }

    function request_amenity(btn=null, query=null){
        $('.amenity_form_items').addClass('hidden');
        bldg_id = ""
        if(btn){
            bldg_id = $(btn).closest('ul').find('.building_id').val();
        } else {
            bldg_id = query;
        }
        console.log(bldg_id);
        $.ajax({
            url: '/building/amenity_request/',
            type: 'GET',
            data: {
                'building_id': bldg_id,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            },
            success: function(data){
                // If Amenities was found
                if (data.status === 200){
                    console.log("success");
                    $('#amenities_create_form').empty();
                    amenity_container = $('#amenity_update_form');
                    amenity_container.empty();
                    
                    amenity_container.html(`
                        <div class="all_checkboxes_container">
                            <div class="checkbox_div2">
                                <label for="free_wifi">Free Wifi</label>
                                <input type="checkbox" name="free_wifi" id="free_wifi" ${data.free_wifi ? 'checked' : ''}/>
                            </div>
                            <div class="checkbox_div2">
                                <label for="shared_kitchen">Shared Kitchen</label>
                                <input type="checkbox" name="shared_kitchen" id="shared_kitchen" ${data.shared_kitchen ? 'checked' : ''}/>
                                
                            </div>
                            <div class="checkbox_div2">
                                <label for="smoke_free">Smoke Free</label>
                                <input type="checkbox" name="smoke_free" id="smoke_free" ${data.smoke_free ? 'checked' : ''}/>
                                
                            </div>
                            <div class="checkbox_div2">
                                <label for="janitor">Janitor</label>
                                <input type="checkbox" name="janitor" id="janitor" ${data.janitor ? 'checked' : ''}/>
                                
                            </div>
                            <div class="checkbox_div2">
                                <label for="guard">Guard</label>
                                <input type="checkbox" name="guard" id="guard" ${data.guard ? 'checked' : ''}/>
                                
                            </div>
                            <div class="checkbox_div2">
                                <label for="waterbill">Water Bill Included</label>
                                <input type="checkbox" name="waterbill" id="waterbill" ${data.waterbill ? 'checked' : ''}/>
                                
                            </div>
                            <div class="checkbox_div2">
                                <label for="electricbill">Electric Bill Included</label>
                                <input type="checkbox" name="electricbill" id="electricbill" ${data.electricbill ? 'checked' : ''}/>
                                
                            </div>
                            <div class="checkbox_div2">
                                <label for="food">Food</label>
                                <input type="checkbox" name="food" id="food" ${data.food ? 'checked' : ''}/>
                                
                            </div>
                        </div>
                            <button id="update_amenity_btn" value="${bldg_id}">Update</button>
                    `)
                    amenity_container.removeClass('hidden');
                } else { // If no amenities was found
                    $('#amenity_update_form').empty();
                    $('#create_amenity_btn').val(bldg_id);
                    $('#amenities_create_form').removeClass('hidden');
                    $('#amenities_create_form').html(`
                        <div class="all_checkboxes_container">
                            <div class="checkbox_div2">
                                <label for="free_wifi">Free Wifi</label>
                                <input type="checkbox" name="free_wifi"/>
                            </div>
                            <div class="checkbox_div2">
                                <label for="shared_kitchen">Shared Kitchen</label>
                                <input type="checkbox" name="shared_kitchen"/>
                            </div>
                            <div class="checkbox_div2">
                                <label for="smoke_free">Smoke Free</label>
                                <input type="checkbox" name="smoke_free"/>
                            </div>
                            <div class="checkbox_div2">
                                <label for="janitor">Janitor</label>
                                <input type="checkbox" name="janitor"/>
                            </div>
                            <div class="checkbox_div2">
                                <label for="guard">Guard</label>
                                <input type="checkbox" name="guard"/>
                            </div>
                            <div class="checkbox_div2">
                                <label for="waterbill">Water Bill Included</label>
                                <input type="checkbox" name="waterbill"/>
                            </div>
                            <div class="checkbox_div2">
                                <label for="electricbill">Electric Bill Included</label>
                                <input type="checkbox" name="electricbill"/>
                            </div>
                            <div class="checkbox_div2">
                                <label for="food">Food</label>
                                <input type="checkbox" name="food"/>
                            </div>
                        </div>
                        <button id="create_amenity_btn" value="${bldg_id}">Create</button>
                    `);
                }
            },
            error: function(xhr, status, error){
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    if (status === 404) {
                        console.log("status is 404");
                    } else{
                    alert(`Error ${xhr.status}: ${xhr.responseJSON.error}`);
                    }
                } else {
                    alert('Other errors');
                }
            }
        })
    }

    function update_amenity(btn){
        let building_id = $(btn).val();
        let form = $(btn).closest('#amenity_update_form');
        let free_wifi = form.find('input[name="free_wifi"]').is(':checked');
        let shared_kitchen = form.find('input[name="shared_kitchen"]').is(':checked');
        let smoke_free = form.find('input[name="smoke_free"]').is(':checked');
        let janitor = form.find('input[name="janitor"]').is(':checked');
        let guard = form.find('input[name="guard"]').is(':checked');
        let waterbill = form.find('input[name="waterbill"]').is(':checked');
        let electricbill = form.find('input[name="electricbill"]').is(':checked');
        let food = form.find('input[name="food"]').is(':checked');

        form_data = {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'building_id': building_id,
            'free_wifi': free_wifi,
            'shared_kitchen': shared_kitchen,
            'smoke_free': smoke_free,
            'janitor': janitor,
            'guard': guard,
            'waterbill': waterbill,
            'electricbill': electricbill,
            'food': food,
        }
        console.log(form_data);
        $.ajax({
            url: '/building/amenity/update/',
            type: 'POST',
            data: form_data,
            success: function(){
                alert('success');
                request_amenity(null, building_id);
            },
            error: function(xhr, status, error){
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    if (status === 404) {
                        console.log("status is 404");
                    } else{
                    alert(`Error ${xhr.status}: ${xhr.responseJSON.error}`);
                    }
                } else {
                    alert('Other errors');
                }
            }
        });
    }
}); // ready function



// -------- new added js code ---------

document.querySelectorAll(".buildingname").forEach((buildingName, index) => {
    buildingName.addEventListener("click", function () {
        const hiddenBtns = document.querySelectorAll(".hiddenbtns")[index];
        const isVisible = hiddenBtns.classList.contains("show");

        // Hide all button lists, reset rotation, and reset borders for all items
        document.querySelectorAll(".hiddenbtns").forEach((btnList, i) => {
            btnList.classList.remove("show");
            document.querySelectorAll(".buildingname")[i].classList.remove("active", "no-border");
        });

        // Toggle visibility, border removal, and rounded border for the clicked item
        if (!isVisible) {
            hiddenBtns.classList.add("show");
            buildingName.classList.add("active", "no-border");
        }
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const firstAdivAnchor = document.querySelector(".adiv .buildingname");
    if (firstAdivAnchor) {
        firstAdivAnchor.style.borderTopLeftRadius = "5px";
        firstAdivAnchor.style.borderTopRightRadius = "5px";
    }
});

