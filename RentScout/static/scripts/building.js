emailjs.init("Q_A-eXEwrvvQsFMYs");
$(document).ready(function() {
  request_bookmark_status();
  display_verification_status();

  $('#heart_container').on('click', '#heart_sign', function(){
  //   console.log('clicked');
  //   $(this).toggleClass('heart-active');
    $('#heart_container').empty();
    if($(this).hasClass('heart-active')){
      remove_bookmark($(this));
    } else {
      add_bookmark($(this));
    }
    
  });

  //  VIEW ROOM INFORMATION
  $('.view_photo_btn').on('click', function() {
    
    $('#photo_container').empty();
    let query = $(this).attr('id');

    $.ajax({
      url: '/room_photo/request/',
      data: {
        'roomid': query,
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
      },
      success: function(data) {
        let firstImageSrc = '';
        console.log(data);
        $.each(data.image_list, function(index, image){
          let li = $("<li></li>");
          let img = $("<img>", {
            class: 'view_room_imgs',
            alt: "Photo of room " + image.photo_id,
            src: image.photo_url,
          });

          if (firstImageSrc === '') {
            firstImageSrc = img.attr('src');
          }

          li.append(img);
          $('#photo_container').append(li);
        });

        $('.view_room_imgs').first().css('opacity', '0.5');
        if (firstImageSrc) {
          $('.selectedpicbox').html(`<img src="${firstImageSrc}" alt="Selected room image" class="selected_image" style="opacity: 1;">`);
        } else {
          $('.selectedpicbox').html(`<img src="${noImagePath}" alt="Selected room image" class="selected_image" style="opacity: 1;">`);
          
        }

        view_photo_modal.removeClass('hidden');

        $('.view_room_imgs').on('click', function() {
          $('.view_room_imgs').css('opacity', '1');
          $(this).css('opacity', '0.5');
          let selectedSrc = $(this).attr('src');
          $('.selectedpicbox').html(`<img src="${selectedSrc}" alt="Selected room image" class="selected_image" style="opacity: 1;">`);
        });
      },
      error: function(xhr, status, error) {
        let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
        SoloMessageFlow(`${errorMessage}`, 'error');
      }
    });

    // SET REQUIRED INFO FOR ONLINE TRANSACTION/RESERVATION
    $('#roomid').val(query);
    get_reservation_status();
    
  });

  // INITIALIZE FIRST ROOM INFORMATION
  $('.view_photo_btn').first().trigger('click');

  // NOT IMPLEMENTED
  $('#view_photo_close').on('click', function() {
    $('#photo_container').empty();
    changeViewStatus();
  });

  // FEEDBACK EDIT BUTTON
  $('.feedback_edit_btn').on('click', function(){
    let parent = $(this).closest('.feedbackdisplay');
    parent.addClass('hidden');
    parent.next('.edit_comment_container').removeClass('hidden');
  });

  // FEEDBACK CANCEL EDIT BUTTON
  $('.feedback_cancel_edit').on('click', function(){
    let parent = $(this).closest('.edit_comment_container');
    parent.addClass('hidden');
    parent.prev('.feedbackdisplay').removeClass('hidden');  
  });

  // REPORT BUTTON
  $(document).on('click', '#report_button', function(){
    console.log($(this).closest('div').find('input[name="buildingid"]').val());
    $.ajax({
      url: '/building/create_report/',
      type: 'POST',
      data: {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        'buildingid': $(this).closest('div').find('input[name="buildingid"]').val(),
        'reason': $('textarea[name="reason"]').val(),
      },
      success: function(response){
        // SoloMessageFlow("Thank you for your report. Our team will review the issue and take appropriate action", 'success')
        SoloMessageFlow(response.success);
        closereport();
    
      },
      error: function(xhr, status, error) {
        let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
        SoloMessageFlow(`${errorMessage}`, 'error');
        $('textarea[name="reason"]').focus();
      }
    })
  });

  // CREATE VERIFICATION CLICK
  $('#verification_status_box').on('click', '#verify_btn', function(){
    create_verification();
  })

  // REMOVE VERIFICATION CLICK
  $('#verification_status_box').on('click', '#pending_verification', function(){
    delete_verification();
  })

  // REPORT BUTTON CLICK
  $('img[alt="report_image"]').on('click', function(){
    $('#report_modal').removeClass("hidden");
  })

  // CLOSE REPORT BUTTON
  $('#close_report').on("click", closereport )

  // CANCEL REPORT BUTTON
  $('#cancel_report_button').on('click', closereport )

  // RESERVATION BUTTON
  $('#request_reservation').on('click', function(){
    // FOR TRANSITION PURPOSES
    $('#waiting').removeClass('hidden');
    $('#request_reservation').addClass('hidden');
    request_reserve($(this));
  } )

  // CANCEL RESERVATION
  $('#cancel_request_reservation').on('click', function(){
    // $('#waiting').removeClass('hidden');
    // $('#request_reservation').addClass('hidden');

    $.ajax({
      url: '/reservations/delete/',
      type: 'POST',
      data: {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        'roomid': $('#roomid').val()
      },
      success: function(response){
        SoloMessageFlow(`${response.success}`);
        get_reservation_status();
      },
      error: function(xhr, status, error) {
        let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
        SoloMessageFlow(`${errorMessage}`, 'error');
      }
    })
  })

  // POP UP MESSAGE
  $('#send_message').on('click', function(){
    // console.log($('#buildingid').val());
    $.ajax({
      url: '/messages/building/get_owner_id/',
      type: 'GET',
      data: {
        'buildingid': $('#buildingid').val(),
      },
      success: function(response){
        console.log(response);
        $('#convo_head').find('h4').text(response.receiver_name);
        $('#receiverid').val(response.success);
        $('#user_image').attr('src', `${response.profile_image}`);
        get_message(response.success);

      }, 
      error: function(xhr, status, error) {
        let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
        SoloMessageFlow(`${errorMessage}`, 'error');
      }
    })
  });

  // DISPLAY QRCODE FOR DOWNPAYMENT
  $('#generate_qr').on('click', function(){
    $('#qr_modal').removeClass('hidden');
  })

  // DISPLAY PAYMENT FORM
  $('#send_payment_receipt').on('click', function(){
    $('#send_payment').removeClass('hidden');
  })

  // CLOSE QRCODE FOR PAYMENT
  $('#qr_close_btn').on('click', function(){
    $('#qr_modal').addClass('hidden');
  })

  // PRELOAD PAYMENT IMAGE
  $('#payment_img').on('change', function(event) {
    const previewDiv = $('#receipt_preview');
    const file = event.target.files[0];

    if (file && file.type.startsWith('image/')) {
      console.log('IMage File');
        const reader = new FileReader();

        reader.onload = function(e) {
            previewDiv.html(`<img src="${e.target.result}" alt="Preview Image">`);
        };

        reader.readAsDataURL(file);
    } else {
        previewDiv.html('<span>Invalid image file</span>');
    }
});

  // SSEND PAYMENT FORM
  $('#send_payment_btn').on('click', function(){
    $('#send_payment').addClass('hidden');
    const formData = new FormData();
    const image = $('#payment_img')[0].files[0];
    const referal = $('#referralid').val();
    const roomid = $('#roomid').val();
    const token = $('input[name="csrfmiddlewaretoken"]').val();

    formData.append('csrfmiddlewaretoken', token)
    formData.append('payment_img', image);
    formData.append('referralid', referal);
    formData.append('roomid_holder', roomid);

    $.ajax({
      url: '/payment/send/',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function(){
        SoloMessageFlow('Payment Sent');
      },
      error: function(xhr, status, error) {
        // let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
        SoloMessageFlow("Error Sending Payment", 'error');
      }
    })
  })

  // CANCEL PAYMENT FORM
  $('#cancel_payment_btn').on('click', function(){
    $('#send_payment').addClass('hidden');
  })

  // UPDATE BUILDING ANCHOR TAG
  $('#update_building_link').on('click', function(e){
    e.preventDefault();
    console.log($('#buildingid').val());
    sessionStorage.setItem('fn_name', 'request_bldg_instance');
    sessionStorage.setItem('buildingid', $('#buildingid').val());
    window.location.href = $(this).attr('href');
  })

  $('#add_new_room_btn').on('click', function(e){
    e.preventDefault();
    console.log('new room clicked');
    sessionStorage.setItem('fn_name', 'add_new_room');
    sessionStorage.setItem('buildingid', $('#buildingid').val());

    window.location.href = $(this).attr('href');
  })

  function closereport(){
    const report_modal = $("#report_modal");
    $(report_modal).addClass('hidden');
    $(report_modal).find('textarea[name="reason"]').val("");
  }

  function request_bookmark_status(return_status = false){
    console.log("Requesting bookamr status");

    let building_id = $('#heart_container').attr('value');
    $.ajax({
      url: '/user/bookmark/building/page/',
      type: 'GET',
      data: {
        'buildingid': building_id
      },
      success: function(response, status, xhr){
        console.log(response.success);
        let heart_container = $('#heart_container');
        let heart = '';
        if (response.success === 'Already Bookmarked'){
            heart = $('<div></div>', {
            id: 'heart_sign',
            class: 'heart heart-active',
            value: response.buildingid
          })
        } else if(response.success === 'Not Bookmarked') {
            heart = $('<div></div>', {
            id: 'heart_sign',
            class: 'heart',
            value: response.buildingid
          })
        }

        heart_container.append(heart);
      },
      error: function(xhr, status, error) {
        let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
        SoloMessageFlow("Error on bookmark status", 'error');
      }
    })
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
        console.log('Success');
        SoloMessageFlow("Successfully Bookmarked")
        request_bookmark_status();
      },
      error: function(xhr, status, error) {
        let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
        SoloMessageFlow(`${errorMessage}`, 'error');
        request_bookmark_status();
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
      success: function (response){
        SoloMessageFlow(response.success, 'success');
        request_bookmark_status();
      },
      error: function(xhr, status, error) {
        let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
        SoloMessageFlow(`${errorMessage}`, 'error');
      }
    })
  }

  function display_verification_status(){
    let box = $('#verification_status_box');
    box.empty();
    $.ajax({
      url: '/building/request/verification_status/',
      type: 'GET',
      data: {
        'buildingid': box.attr('value')
      },
      success: function(response){
        console.log(response.verification_status)
        if(response.verification_status === 'Not Verified'){
          let button = $('<button></button>', {
            text: 'Not Verified',
            id: 'verify_btn'
          })
          box.append(button);

        } else if (response.verification_status === 'Pending'){
          let p = $('<p></p>', {
            text: 'Pending',
            id: 'pending_verification'
          })
          box.append(p);

        } else if (response.verification_status === 'Verified'){
          let img = $('<img/>', {
            src: '/static/imgs/building/verified-icon-removebg-preview.png',
            alt: 'Verification Badge',
            id:  'verified'
          })
          console.log(img);
          box.append(img);
          $('#online_transaction_container').removeClass("hidden");
        
          get_reservation_status();
        }

      }, 
      error: function(xhr) {
        if (xhr.responseJSON && xhr.responseJSON.error) {
            alert(xhr.responseJSON.error); 
        } else {
            alert('An unexpected error occurred.');
        }
    }
    })
  }

  function create_verification(){
    const box = $('#verification_status_box');
    $.ajax({
      url: '/building/create_verification/',
      type: 'POST',
      data: {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        'buildingid': box.attr('value')
      },
      success: function(response){

        display_verification_status();
        SoloMessageFlow(`${response.success}`, "success");
      },
      error: function(xhr, status, error) {
        let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
        SoloMessageFlow(`${errorMessage}`, 'error');
      }  
  })
  }

  function delete_verification(){
    const box = $('#verification_status_box');
    $.ajax({
      url: '/building/remove_verification/',
      type: 'POST',
      data: {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        'buildingid': box.attr('value')
      },
      success: function(response){
        // alert('Verification request removed.');

        display_verification_status();
        SoloMessageFlow(`${response.success}`, "success");
      },
      error: function(xhr, status, error) {
        let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
        SoloMessageFlow(`${errorMessage}`, 'error');
      } 
    });
  }

  // SEND NOTIFICATION TO LANDLORD GMAIL
  function request_reserve(btn){
    const roomid = $('#roomid').attr('value');
    $.ajax({
      url: '/reservations/send_notification/',
      type: 'GET',
      data: {
        'roomid': roomid,
      },
      success: function(response_data){
        // IF AJAX SUCCESS SEND GMAIL TO LANDLORD
        console.log(`Good day! ${response_data.boarder_name} requested a slot for room ${response_data.room_name}.`);
        emailjs.send(response_data.public_key, response_data.template_key, {
          receiver_email: response_data.landlord_email,
          to_name: response_data.to_name,
          anchor_tag: "http://127.0.0.1:8000/reservations/",
          message: `Good day! ${response_data.boarder_name} requested a slot for room ${response_data.room_name}.`
        }).then(
          function(response) {
            create_reservation(btn);
            
          },
          function(error) {
            console.error("Failed to send email.", error);
            SoloMessageFlow('Failed to send email. Something\'s wrong with the server.', 'error')
          }
          );      
        },
      error: function(xhr, status, error) {
        let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
        SoloMessageFlow(`${errorMessage}`, 'error');
        $('#waiting').addClass('hidden');
        $('#request_reservation').removeClass('hidden');
  } 
    })

  }

  // CREATE RESERVATION IN DATABASE
  function create_reservation(){
    console.log($('#roomid').attr('value'));
    $.ajax({
      url: '/reservations/create_reservation/',
      type: 'POST',
      data: {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        'roomid': $('#roomid').attr('value')
      },
      success: function(){
        SoloMessageFlow("The owner has been notified. " +
        "We\'ll send you a mail once the owner has accepted your request", 'success')
        get_reservation_status();
      },
      error: function(xhr, status, error) {
        let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
        SoloMessageFlow(`${errorMessage}`, 'error');
      } 
    })
  }

  function get_reservation_status(){
    console.log($('#roomid').val());

    // PREVENT RESERVATION STATUS IF NO ROOMS
    if($('#roombox_item_container').children().length === 0){
      return;
    }

    $.ajax({
      url: '/reservations/get/reservation_status/',
      type: 'GET',
      data: {
        'roomid': $('#roomid').attr('value')
      },
      success: function(response){
        console.log('reservation request');
        console.log(response);
        //  
        if(response.success == true && response.status == 'Pending'){
          console.log('Pending');
          $('#waiting').addClass('hidden');
          $('#request_reservation').addClass('hidden');
          $('#qr_container').addClass('hidden');
          $('#cancel_request_reservation').removeClass('hidden');
          $('#qr_container').addClass('hidden');
        // 
        } else if (response.success == true && response.status == 'Accepted') {
          console.log('accepted');
          $('#waiting').addClass('hidden');
          $('#request_reservation').addClass('hidden');
          $('#cancel_request_reservation').addClass('hidden');
          $('#qr_container').removeClass('hidden');
        
        } else {
          console.log('none');
          $('#waiting').addClass('hidden');
          $('#request_reservation').removeClass('hidden');
          $('#qr_container').addClass('hidden');
          $('#cancel_request_reservation').addClass('hidden');
        }
      },
      error: function(xhr, status, error) {
        // let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
        // SoloMessageFlow(`${errorMessage}`, 'error');
        console.log(errorMessage)
        return;
      } 
    })
  }

}); // Ready Function

let view_photo_modal = $('#view_photo_modal');

function changeViewStatus() {
  if (view_photo_modal.hasClass('hidden')) {
    view_photo_modal.removeClass('hidden');
  } else {
    view_photo_modal.addClass('hidden');
  }
}

document.addEventListener("DOMContentLoaded", function() {
  const photoContainer = document.getElementById('photo_container');
  const nextBtn = document.getElementById('next_btn');
  const prevBtn = document.getElementById('prev_btn');
  
  nextBtn.addEventListener('click', () => {
      console.log("next");
      photoContainer.scrollLeft += 68;
  });

  prevBtn.addEventListener('click', () => {
    console.log("prev");
    photoContainer.scrollLeft -= 68;
  });
});

// Display room info based on the room ID
const roomIdDisplay = document.getElementById('room_id_display');
const roomRows = document.querySelectorAll('div[data-roomid]');

function filterRoomsById(roomId) {
    roomRows.forEach(row => {
        if (row.getAttribute('data-roomid') === roomId) {
            row.style.display = '';  // Show row
        } else {
            row.style.display = 'none';  // Hide row
        }
    });
}

const initialRoomId = roomIdDisplay.textContent.replace('Room ID: ', '').trim();
filterRoomsById(initialRoomId);

const viewPhotoButtons = document.querySelectorAll('.view_photo_btn');

viewPhotoButtons.forEach(button => {
    button.addEventListener('click', function () {
        const roomId = this.id; // Get the room ID from the button's ID
        roomIdDisplay.textContent = 'Room ID: ' + roomId; // Update room ID display
        filterRoomsById(roomId);  // Filter room rows
        changeViewStatus(); // Toggle modal visibility
    });
});
