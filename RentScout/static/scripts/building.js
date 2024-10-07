$(document).ready(function() {
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

        for (let key in data) {
          let li = $("<li></li>");
          let img = $("<img>", {
            class: 'view_room_imgs',
            alt: "Photo of room " + key,
            src: '/media/' + data[key],
          });

          if (firstImageSrc === '') {
            firstImageSrc = img.attr('src');
          }

          li.append(img);
          $('#photo_container').append(li);
        }

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
      photoContainer.scrollLeft += 68;
  });

  prevBtn.addEventListener('click', () => {
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
