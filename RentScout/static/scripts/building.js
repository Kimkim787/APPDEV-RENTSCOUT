$(document).ready(function() {
  request_bookmark_status();
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
        console.log(xhr.responseText);
        alert(error, status);
      }
    });
  });

  $('.view_photo_btn').first().trigger('click');

  $('#view_photo_close').on('click', function() {
    $('#photo_container').empty();
    changeViewStatus();
  });

  $('.feedback_edit_btn').on('click', function(){
    let parent = $(this).closest('.feedbackdisplay');
    parent.addClass('hidden');
    parent.next('.edit_comment_container').removeClass('hidden');
  });

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
      success: function(reponse){
        alert('successfuly reported');
      },
      error: function(xhr, status, error) {
        console.error("AJAX Error: " + status + ": " + error);
      }    
    })
  });


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
        request_bookmark_status();
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
        request_bookmark_status();
      },
      error: function(xhr, status, error){
        console.log(error);
        alert(`Error: ${xhr.responseText.error || error}`);
      }
    })
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
