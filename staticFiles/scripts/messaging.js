$(document).ready(function(){
    // setInterval(get_inbox_data, 5000);

    $('#bubble').on('click', function(){
        $('#inbox').toggleClass('hidden');
        $('#message_convo').addClass('hidden');
        get_inbox_data(page = 1);
    })

    $('#message_close_btn').on('click', function(){
        $('#inbox').toggleClass('hidden');
    })

    $('#message_back_btn').on('click', function(){
        $('#message_convo').toggleClass('hidden');
        $('#inbox').toggleClass('hidden');
        $('#convo_list').empty();
        get_inbox_data();
    })

    $('#label_holder').on('click', function(){
        $('#attach_input').trigger('click');
    })

    $('#inbox_container').on('click', '.inbox_item', function(){
        set_message_convo_head($(this).attr('value'));
        get_message($(this).attr('value'));
        $('#inbox').addClass('hidden');
    })
    // IMAGE PRELOAD
    // $('#attach_input').on('change', function(event) {
    //     console.log("File uploaded");
    //     const file = event.target.files[0];
    //     const previewContainer = $('#image_preview_container');
    
    //     if (file) {
    //         const reader = new FileReader();
            
    //         reader.onload = function(e) {
    //             box = $('<div></div>', {
    //                 class: 'attachment_container'
    //             })

    //             image = $('<img></img>', {
    //                 src: `${e.target.result}`,
    //                 alt: 'Selected image',
    //                 class: 'preview_img'
    //             })

    //             delete_btn = $('<img></img>', {
    //                 src: '/static/imgs/remove.png',
    //                 alt: '',
    //                 class: 'del_attachment'
    //             })

    //             box.append(image);
    //             box.append(delete_btn);
    //             previewContainer.append(box);
    //         };
            
    //         reader.readAsDataURL(file);  // Read the file as a data URL
    //     } // else {
    //     //     previewContainer.html('');  // Clear preview if no file is selected
    //     // }
    // });

    let selectedFiles = [];  // Store multiple selected files

    $('#attach_input').on('change', function(event) {
        const files = event.target.files;
        const previewContainer = $('#image_preview_container');

        Array.from(files).forEach(file => {
            selectedFiles.push(file);  // Store each selected file

            const reader = new FileReader();
            
            reader.onload = function(e) {
                const box = $('<div></div>', {
                    class: 'attachment_container'
                });

                const image = $('<img></img>', {
                    src: e.target.result,
                    alt: 'Selected image',
                    class: 'preview_img'
                });

                const delete_btn = $('<img></img>', {
                    src: '/static/imgs/remove.png',
                    alt: '',
                    class: 'del_attachment'
                });

                // Remove image on delete click
                delete_btn.on('click', function() {
                    box.remove();
                    selectedFiles = selectedFiles.filter(f => f !== file);  // Remove file from array
                });

                box.append(image).append(delete_btn);
                previewContainer.append(box);  // Append each new image preview
            };

            reader.readAsDataURL(file);  // Preview each image
        });
    });

    // AJAX Submission (Send Message and Multiple Images)
    $('#send_convo_btn').on('click', function(e) {
        e.preventDefault();

        const formData = new FormData();
        const message = $('#chat_message').val();
        const token = $('input[name="csrfmiddlewaretoken"]').val();
        const receiverid = $('#receiverid').val();
        console.log(`${message}, ${token}, ${receiverid}`);
        formData.append('message', message);
        formData.append('csrfmiddlewaretoken', token)
        formData.append('receiverid', receiverid);

        selectedFiles.forEach(file => {
            formData.append('images', file);  // Append all files to FormData
        });

        $.ajax({
            url: '/messages/send_message/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log(response);

                // DISPLAY MESSAGE
                $.each(response.message_list, function(index, message){
            
                    let profile_icon_src = '';
                    let profile_icon_class = '';
                    let convo_container_class = '';
                    let convo_text_class = '';
        
                    // CLASS ASSINGMENT
                    if(message.sender == 'Boarder'){
                        profile_icon_src = message.boarder_profile;
                        profile_icon_class = 'boarder_profile_icon',
                        convo_container_class = "boarder_message_container";
                        convo_text_class = 'boarder_message_text';
        
                    } else if (message.sender == 'Landlord'){
                        profile_icon_src = message.landlord_profile;
                        profile_icon_class = 'landlord_profile_icon',
                        convo_container_class = "landlord_message_container";
                        convo_text_class = 'landlord_message_text';
                    }
                    
                    profile_icon = $('<img></img>', {
                        src: `${profile_icon_src}`,
                        alt: 'profile_icon',
                        class: profile_icon_class
                    })
                    
                    if(!message.image){
                        li = $('<li></li>', {
                            class: 'convo_list_item'
                        })
        
                        div = $('<div></div>', {
                            class: convo_container_class
                        })
        
                        text = $('<p></p>', {
                            text: `${message.message}`,
                            class: convo_text_class
                        })
        
                        time = $('<p></p>', {
                            text: `${message.time_sent}`,
                            class: 'convo_time'
                        })
        
                        li.append(time);
                        div.append(profile_icon);
                        div.append(text);
                        li.append(div);
                        $('#convo_list').append(li);
                    } else if(message.image){
                        li = $('<li></li>', {
                            class: 'convo_list_item'
                        })
        
                        div = $('<div></div>', {
                            class: convo_container_class
                        })
        
                        image = $('<img></img>', {
                            src: `${message.image}`,
                            alt: 'image_upload',
                            class: 'convo_image'
                        })
        
                        time = $('<p></p>', {
                            text: `${message.time_sent}`,
                            class: 'convo_time'
                        })
        
                        li.append(time);
                        div.append(profile_icon);
                        div.append(image);
                        li.append(div);
                        $('#convo_list').append(li);
        
                    }
                })

                SoloMessageFlow(response.success);

                // AUTO SCROLL DOWN
                const convo_body = $('#convo_list').get(0);
                convo_body.scrollTo({ top: convo_body.scrollHeight, behavior: 'smooth' });
                
                $('#image_preview_container').html('');
                $('textarea[name="message"]').val('');
                selectedFiles = [];  // Clear files after successful upload
            },
            error: function(xhr) {
                SoloMessageFlow('Failed to send message', 'error');
            }
        });
    });

    // VIEW MORE MESSAGES
    $('#convo_list').on('click', '#load_previous_convo', function(){
        $('#load_previous_convo').remove();
        $.ajax({
            url: '/messages/request/',
            type: 'GET',
            data: {
                'receiverid': $('#receiverid').val(),
                'page': $(this).attr('value'),
            },
            success: function(response){
                $.each(response.message_list, function(index, message){
                    let profile_icon_src = '';
                    let profile_icon_class = '';
                    let convo_container_class = '';
                    let convo_text_class = '';
        
                    // CLASS ASSINGMENT
                    if(message.sender == 'Boarder'){
                        profile_icon_src = response.boarder_profile;
                        profile_icon_class = 'boarder_profile_icon',
                        convo_container_class = "boarder_message_container";
                        convo_text_class = 'boarder_message_text';
        
                    } else if (message.sender == 'Landlord'){
                        profile_icon_src = response.landlord_profile;
                        profile_icon_class = 'landlord_profile_icon',
                        convo_container_class = "landlord_message_container";
                        convo_text_class = 'landlord_message_text';
                    }
                    
                    profile_icon = $('<img></img>', {
                        src: `${profile_icon_src}`,
                        alt: 'profile_icon',
                        class: profile_icon_class
                    })
                    
                    if(!message.image){
                        li = $('<li></li>', {
                            class: 'convo_list_item'
                        })
        
                        div = $('<div></div>', {
                            class: convo_container_class
                        })
        
                        text = $('<p></p>', {
                            text: `${message.message}`,
                            class: convo_text_class
                        })
        
                        time = $('<p></p>', {
                            text: `${message.time_sent}`,
                            class: 'convo_time'
                        })
        
                        li.append(time);
                        div.append(profile_icon);
                        div.append(text);
                        li.append(div);
                        $('#convo_list').prepend(li);

                    // HANDLE IMAGE
                    } else if(message.image){
                        li = $('<li></li>', {
                            class: 'convo_list_item'
                        })
        
                        div = $('<div></div>', {
                            class: convo_container_class
                        })
        
                        image = $('<img></img>', {
                            src: `${message.image}`,
                            alt: 'image_upload',
                            class: 'convo_image'
                        })
        
                        time = $('<p></p>', {
                            text: `${message.time_sent}`,
                            class: 'convo_time'
                        })
        
                        li.append(time);
                        div.append(profile_icon);
                        div.append(image);
                        li.append(div);
                        $('#convo_list').prepend(li);
                        
                    }
        
                })
                // PAGE CONTROL
                if (response.has_next){
            
                    const more_message = $('<p></p>', {
                        text: 'View More Messages',
                        id: 'load_previous_convo',
                        value: response.next_page
                    });
                    
                    $('#convo_list').prepend(more_message);
                }
            },
            error: function(xhr, status, error) {
                let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
                SoloMessageFlow(`${errorMessage}`, 'error');
            } 
        })
    })

    function get_inbox_data(page = 1){
        const inbox_container = $('#inbox_container');
        inbox_container.empty();
        $.ajax({
            url: '/inbox/get_inbox/',
            type: 'GET',
            data: {
                'page': page
            },
            success: function(response){
                console.log(response);
                $.each(response.inbox_list, function(index, data){
                    li = $('<li></li>', {
                        class: 'inbox_item',
                        value: data.receiver_id
                    })

                    div = $('<div></div>', {
                        class: 'inbox_design_control'
                    })

                    profile = $('<img></img>', {
                        src: data.user_profile,
                        alt: 'profile_icon',
                        class: 'profile_icon'
                    });

                    user_name = $('<p></p>', {
                        text: data.receiver_name,
                        class: 'receiver_name'
                    })

                    message = '';
                    if(data.sender == data.me){
                        message = `You: ${data.last_message.length > 0 ? data.last_message: "Sent an attachment"}`;
                    } else {
                        message = `${data.receiver_name.split(' ')[0]}: ${data.last_message.length > 0 ? data.last_message : "Sent an attachment"}`;
                    }

                    
                    message = $('<p></p>', {
                        text: message,
                        class: 'last_message'
                    })

                    div.append(user_name);
                    div.append(message);
                    li.append(profile);
                    li.append(div);
                    inbox_container.append(li);
                }); // each
            },
            error: function(xhr, status, error) {
                let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
                SoloMessageFlow(`${errorMessage}`, 'error');
              } 
                })
    }

    function set_message_convo_head(receiver_id){
        $.ajax({
            url: '/messages/get_user/',
            type: 'GET',
            data: {
              'receiver_id': receiver_id,
            },
            success: function(response){
              console.log(response);
              $('#convo_head').find('h4').text(response.receiver_name);
              $('#receiverid').val(response.success);
              $('#user_image').attr('src', `${response.profile_image}`);      
            }, 
            error: function(xhr, status, error) {
              let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
              SoloMessageFlow(`${errorMessage}`, 'error');
            }
          })
      
    }
}); /// ready function

function get_message(receiverid, page = null){
    console.log(receiverid);
    $('#message_convo').removeClass('hidden');
    $.ajax({
      url: '/messages/request/',
      type: 'GET',
      data: {
        'receiverid': receiverid, 
        'page': page
      },
      success: function(response){
        console.log(response);

        $.each(response.message_list, function(index, message){
            
            let profile_icon_src = '';
            let profile_icon_class = '';
            let convo_container_class = '';
            let convo_text_class = '';

            // CLASS ASSINGMENT
            if(message.sender == 'Boarder'){
                profile_icon_src = response.boarder_profile;
                profile_icon_class = 'boarder_profile_icon',
                convo_container_class = "boarder_message_container";
                convo_text_class = 'boarder_message_text';

            } else if (message.sender == 'Landlord'){
                profile_icon_src = response.landlord_profile;
                profile_icon_class = 'landlord_profile_icon',
                convo_container_class = "landlord_message_container";
                convo_text_class = 'landlord_message_text';
            }
            
            profile_icon = $('<img></img>', {
                src: `${profile_icon_src}`,
                alt: 'profile_icon',
                class: profile_icon_class
            })
            
            if(!message.image){
                li = $('<li></li>', {
                    class: 'convo_list_item'
                })

                div = $('<div></div>', {
                    class: convo_container_class
                })

                text = $('<p></p>', {
                    text: `${message.message}`,
                    class: convo_text_class
                })

                time = $('<p></p>', {
                    text: `${message.time_sent}`,
                    class: 'convo_time'
                })

                li.append(time);
                div.append(profile_icon);
                div.append(text);
                li.append(div);
                $('#convo_list').prepend(li);

            } else if(message.image){
                li = $('<li></li>', {
                    class: 'convo_list_item'
                })

                div = $('<div></div>', {
                    class: convo_container_class
                })

                image = $('<img></img>', {
                    src: `${message.image}`,
                    alt: 'image_upload',
                    class: 'convo_image'
                })

                time = $('<p></p>', {
                    text: `${message.time_sent}`,
                    class: 'convo_time'
                })

                li.append(time);
                div.append(profile_icon);
                div.append(image);
                li.append(div);
                $('#convo_list').prepend(li);

            }
        })

        // PAGE CONTROL
        if (response.has_next){
    
            const more_message = $('<p></p>', {
                text: 'View More Messages',
                id: 'load_previous_convo',
                value: response.next_page
            });
            
            $('#convo_list').prepend(more_message);
        }

        // AUTO SCROLL DOWN
        const convo_body = $('#convo_list').get(0);
        convo_body.scrollTo({ top: convo_body.scrollHeight, behavior: 'smooth' });

      }, 
      error: function(xhr, status, error) {
        let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
        SoloMessageFlow(`${errorMessage}`, 'error');
      } 
    })
  }

