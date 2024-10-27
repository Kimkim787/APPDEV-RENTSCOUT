$(document).ready(function(){
    // "SEE PHOTOS" BUTTON CLICKED
    $('#rooms_container').on('click', '.photo_btn', function(){
        $('.form_item').addClass('hidden');
        show_room_photos($(this))
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
    $('#policies_container').on('click', '.pol_edit_btn', function(){
        let li = $(this).closest('li');
        let policy_id_holder = li.find('input');
        let old_policy = li.find('p[class="policy"]').text();
        
        // empty element li
        li.empty();

        let textarea = $('<textarea></textarea>', {
            class: 'edit_policy_text',
            // id: `edit_policy_${policy_id_holder.val()}`,
            text: old_policy
        })

        let submit_btn = $('<button></button>', {
            text: 'Save',
            class: 'save_update_policy',
            value: policy_id_holder.val()
        })

        // li.append(policy_id_holder);
        li.append(textarea);
        li.append(submit_btn);

        // add new element to list
    })

    // POLICY SAVE EDIT BTN
    $('#policies_container').on('click', '.save_update_policy', function(){
        update_policy($(this));
    })
        // TOGGLE FORMS
    $('.edit_btn').on('click', function() {
        // hide forms (third column)
        $('.form_item').addClass('hidden');
        // get building id
        let buildingId = $(this).closest('ul').find('.building_id').val();
        
            // EDIT BUILDING
        if($(this).val() == 'Edit Building'){
            $('#building_form').removeClass('hidden');
            // set building id to form
            $('#building_id_holder').val(buildingId);
            console.log(buildingId)
            request_bldg_instance(buildingId);
            
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
            console.log('rooms');
            request_rooms($(this));

            // UPLOAD PHOTO BTN
        } else if ($(this).val() == 'upload_room_photo'){
            $('#upload_room_photo').removeClass('hidden');
        }

    }) // edit_btn on click

    // middle bar back btn
    $('.backbtn').on('click', function(){
        $('#photo_view').toggleClass('hidden');
        $('#room_view').toggleClass('hidden');
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
                alert("success");
            },
            error: function(){
                alert('error');
            }
        })
    }

    // REQUEST ROOMS FOR MIDDLE BAR
    function request_rooms(btn){
        $('#photo_container').empty();
        $('#rooms_container').empty();
        let query = $(btn).closest('ul').find('.building_id').val();
            // REQUEST ROOMS FOR ROOM_VIEW
        $.ajax({
            url: '/room/get_rooms/',
            data: {
                'building_id': query,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(data){
                // console.log("datas: ");
                console.log(data);
                if (data.room_data.length >= 1){
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

                        let p = $('<p></p>', {
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
                        
                        // console.log(input);
                        // console.log(p);

                        room_div.append(input);
                        btn_div.append(photo_btn);
                        btn_div.append(update_btn);
                        room_div.append(p);
                        room_div.append(btn_div);

                        // console.log("room div is:");
                        // console.log(room_div);
                        $('#rooms_container').append(room_div);

                        $('.mid_item').addClass('hidden'); 
                        $('#room_view').removeClass('hidden'); 
                    });
                } else {
                    $('.mid_item').addClass('hidden');
                    $('#no_room_message').removeClass('hidden');
                }
            },
            error: function(xhr, status, error) {
                console.log(xhr.responseText);
                alert(error, status);
            }

        })

    }

    // SHOW ROOM PHOTOS TO MIDDLE BAR
    function show_room_photos(btn = null, room_id = null){
        // initalize = empty
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

                $.each(data.image_list, function( index, photo){
                    let li = $("<li></li>");

                    let del_btn = $('<button></button>', {
                        class: 'del_photo_btn',
                        type: 'button',
                        text: 'delete',
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

    // UPLOAD PHOTO BTN CLICK
    $('#upload_room_photo_btn').on('click', function() {
        let query = $(this).closest('#upload_photo_container').find('#upload_room_holder').val();
        let formData = new FormData($('#file-upload-form')[0]);
        axios.post('/room_photo/upload/as_view', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        })
        .then(function(response) {
            alert('Upload successful!');
            show_room_photos(null, query);
            resetFileUpload();
        })
        .catch(function(error) {
            console.error(error);
            alert(`Error: ${error.response.data.error || 'Upload failed!'}`);
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
                    <label for="room_name">Room Name:</label>
                    <input type="text" name="room_name" value="${response_data.room_name}"> 
                    <label for="person_free">Person Available:</label>
                    <input type="text" name="person_free" value="${response_data.person_free}">
                    
                    <label for="current_male">Male resident:</label>
                    <input type="text" name="current_male" value="${response_data.current_male}">
                
                    <label for="current_female">Female resident:</label>
                    <input type="text" name="current_female" value="${response_data.current_female}">
                
                    <label for="price">Price:</label>
                    <input type="text" name="price" value="${response_data.price}">
                
                    <label for="room_size">Room Size:</label>
                    <input type="text" name="room_size" value="${response_data.room_size}">
                
                
                    <p><b>Additional Information:</b></p>
                
                    <label for="bed">Single bed:</label>
                    <input type="text" name="bed" value="${response_data.bed}">
                
                    <label for="double_deck">Double bed:</label>
                    <input type="text" name="double_deck" value="${response_data.double_deck}">
                
                    <input type="checkbox" name="shower" ${response_data.shower ? 'checked':''}>
                    <label for="shower">Shower</label>
                
                    <input type="checkbox" name="priv_bathroom" ${response_data.priv_bathroom ? 'checked':''}>
                    <label for="priv_bathroom">Private Bathroom</label>
                
                    <input type="checkbox" name="public_bathroom" ${response_data.public_bathroom ? 'checked':''}>
                    <label for="public_bathroom">Public Bathroom</label>
                
                    <input type="checkbox" name="AC" ${response_data.AC ? 'checked':''}>
                    <label for="AC">Air Conditioned</label>
                
                    <input type="checkbox" name="wardrobe" ${response_data.wardrobe ? 'checked':''}
                    <label for="wardrobe">Wardrobe</label>
                
                    <input type="checkbox" name="kitchen" ${response_data.kitchen ? 'checked':''}>
                    <label for="kitchen">Kitchen</label>
                
                    <input type="checkbox" name="free_wifi" ${response_data.free_wifi ? 'checked':''}>
                    <label for="free_wifi">Free Wifi</label>
                
                    <button id="edit_room_save" value="${response_data.roomid}" >Save<button>
                `);
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
        let textarea = $('<textarea></textarea>', {
            name: 'policy',
        });

        let cancel_btn = $('<button></button>', {
            id: 'new_pol_cancel_btn',
            text: 'Cancel'
        })

        let save_btn = $('<button></button>', {
            id: 'new_pol_save_btn',
            text: 'Save'
        });

        li.append(title);
        li.append(textarea);
        li.append(cancel_btn);
        li.append(save_btn);
        pol_container.prepend(li);  
        } // else
    }

    // GET ALL POLICIES OF BUILDING
    function request_bldg_policies(query){
        let pol_container = $('#policies_container');
        pol_container.empty();
        $.ajax({
            url: '/building/policies_request/',
            type: 'GET',
            data: {
                'building_id': query,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            },
            success: function(data){
                console.log(data)
                ul = $('#policies_container');

                $.each(data.policy_lists, function(index, policy){
                    let li = $('<li></li>')

                    let input = $('<input>', {
                        type: 'text',
                        class: 'policy_id_holder hidden',
                        value: policy.policy_id
                    });

                    let textarea = $('<p></p>', {
                        class: 'policy',
                        text: policy.policy
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

                    li.append(input);
                    li.append(textarea);
                    li.append(del_btn);
                    li.append(edit_btn);

                    ul.append(li);
                })
            },
            error: function(xhr, status, error){
                alert(`Error ${xhr.status}: ${error}`);
            }
        })
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
        pol_id = $(btn).closest('li').find('.policy_id_holder').val();
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

    function update_policy(btn){
        let policy_text = $(btn).closest('li')
            .find('textarea[class="edit_policy_text"]').val();

        let policy_id = $(btn).val();

        console.log(policy_text);
        console.log(policy_id);
        $.ajax({
            url: '/building/policy/update/',
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'policy_id': policy_id, 
                'policy': policy_text
            },
            success: function(){
                alert('success');
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
                            <input type="checkbox" name="free_wifi" id="free_wifi" ${data.free_wifi ? 'checked' : ''}/>
                            <label for="free_wifi">Free Wifi</label>

                            <input type="checkbox" name="shared_kitchen" id="shared_kitchen" ${data.shared_kitchen ? 'checked' : ''}/>
                            <label for="shared_kitchen">Shared Kitchen</label>

                            <input type="checkbox" name="smoke_free" id="smoke_free" ${data.smoke_free ? 'checked' : ''}/>
                            <label for="smoke_free">Smoke Free</label>

                            <input type="checkbox" name="janitor" id="janitor" ${data.janitor ? 'checked' : ''}/>
                            <label for="janitor">Janitor</label>

                            <input type="checkbox" name="guard" id="guard" ${data.guard ? 'checked' : ''}/>
                            <label for="guard">Guard</label>

                            <input type="checkbox" name="waterbill" id="waterbill" ${data.waterbill ? 'checked' : ''}/>
                            <label for="waterbill">Water Bill Included</label>

                            <input type="checkbox" name="electricbill" id="electricbill" ${data.electricbill ? 'checked' : ''}/>
                            <label for="electricbill">Electric Bill Included</label>

                            <input type="checkbox" name="food" id="food" ${data.food ? 'checked' : ''}/>
                            <label for="food">Food</label>

                            <button id="update_amenity_btn" value="${bldg_id}">Update</button>
                    `)
                    amenity_container.removeClass('hidden');
                } else { // If no amenities was found
                    $('#amenity_update_form').empty();
                    $('#create_amenity_btn').val(bldg_id);
                    $('#amenities_create_form').removeClass('hidden');
                    $('#amenities_create_form').html(`
                        <input type="checkbox" name="free_wifi"/>
                        <label for="free_wifi">Free Wifi</label>

                        <input type="checkbox" name="shared_kitchen"/>
                        <label for="shared_kitchen">Shared Kitchen</label>

                        <input type="checkbox" name="smoke_free"/>
                        <label for="smoke_free">Smoke Free</label>

                        <input type="checkbox" name="janitor"/>
                        <label for="janitor">Janitor</label>

                        <input type="checkbox" name="guard"/>
                        <label for="guard">Guard</label>

                        <input type="checkbox" name="waterbill"/>
                        <label for="waterbill">Water Bill Included</label>

                        <input type="checkbox" name="electricbill"/>
                        <label for="electricbill">Electric Bill Included</label>

                        <input type="checkbox" name="food"/>
                        <label for="food">Food</label>

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

