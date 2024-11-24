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
      error: function(xhr, status, error){
        alert(`Error: ${xhr.responseText.error || error}`);
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
});

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
