$(document).ready(function(){
    // "SEE PHOTOS" BUTTON CLICKED
    $('#rooms_container').on('click', '.photo_btn', function(){
        show_room_photos($(this))
    });

    // TOGGLE FORMS
    $('.edit_btn').on('click', function() {
        $('.form_item').addClass('hidden');
        if($(this).val() == 'Edit Building'){
            $('#building_form').removeClass('hidden');

        } else if( $(this).val() == 'Amenities'){
            $('#amenities_form').removeClass('hidden');

        } else if( $(this).val() == 'Policies'){
            $('#policies_form').removeClass('hidden');
        } else if ($(this).val() == 'Rooms') {
            // REQUEST PHOTOS FOR MIDDLE BAR
            req_rooms($(this));
        } else if ($(this).val() == 'upload_room_photo'){
            $('#upload_room_photo').removeClass('hidden');
        }

    }) // edit_btn on click

    // middle bar back btn
    $('.backbtn').on('click', function(){
        $('.mid_item').toggleClass('hidden');
    });    

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
            // Optionally update the DOM here
            console.log("After uploading: query is " + query);
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

    // REQUEST ROOMS FOR MIDDLE BAR
    function req_rooms(btn){
        $('#photo_container').empty();
        $('#rooms_container').empty();
        let query = $(btn).closest('ul').find('#building_id').val();
            // REQUEST ROOMS FOR ROOM_VIEW
        $.ajax({
            url: '/room/get_rooms/',
            data: {
                'building_id': query,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(data){
                // console.log("datas: ");
                // console.log(data);
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
                        class: 'update_btn',
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

                    $('#photo_view').addClass('hidden'); 
                    $('#room_view').removeClass('hidden'); 
                });

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
        } else{
            query = room_id;
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

}); // ready function

