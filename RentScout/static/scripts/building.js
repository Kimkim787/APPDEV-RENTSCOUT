$(document).ready(function(){
  $('.view_photo_btn').on('click', function(){
    $('#photo_container').empty();
    console.log("view photo");
    let query = $(this).attr('id');
    console.log(query);
    $.ajax({
      url: '/room_photo/request/',
      // type: 'POST', 
      data: {
          'roomid': query, 
          'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
      },

      success: function(data){
        console.log(data);

        for(let key in data){
          console.log();
          let li = $("<li></li>");
          let img = $("<img >", {
            class: 'view_room_imgs',
            alt: "Photo of room " + key,
            src: '/media/' + data[key] ,
        });
        console.log(img);
        li.append(img)

        // append to photo container
        $('#photo_container').append(li)
        }

        view_photo_modal.removeClass('hidden');
        
      },
      error: function(xhr, status, error) {
          console.log(xhr.responseText);
          alert(error, status);
      }
    });
  });

  $('#view_photo_close').on('click', function(){
    $('#photo_container').empty();
    changeViewStatus();
  })
});

let view_photo_modal = $('#view_photo_modal');

function changeViewStatus(){
  console.log(view_photo_modal);
  if (view_photo_modal.hasClass('hidden')){
    view_photo_modal.removeClass('hidden');
  } else {
    view_photo_modal.addClass('hidden');
  }
}