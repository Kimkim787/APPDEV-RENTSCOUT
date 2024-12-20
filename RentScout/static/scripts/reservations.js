emailjs.init("Q_A-eXEwrvvQsFMYs");
$(document).ready(function(){
  request_reservations();
  
  $('.building_items').on('click', function(){
    console.log("b_item clicked");
    $('#res_pending').val($(this).attr('value'));
    $('#res_accepted').val($(this).attr('value'));
    $('#res_declined').val($(this).attr('value'));
    request_reservations(buildingid = $(this).attr('value'));
  })
  
  $('#res_pending').on('click', function(){
    request_reservations(buildingid = $(this).attr('value'), statusQ = 'Pending');
  });

  $('#res_accepted').on('click', function(){
    request_reservations(buildingid = $(this).attr('value'), statusQ = 'Accepted');
  })

  $('#res_declined').on('click', function(){
    request_reservations(buildingid = $(this).attr('value'), statusQ = 'Declined')
  })

  $('#reservation_lists').on('click', '.accept_btns', accept_reservation);


  function request_reservations(buildingid=null, statusQ = null){
    $('#select_notice').addClass('hidden');
    $('#empty_notice').addClass('hidden');
    $('#reservation_lists').addClass('hidden');
    $('#reservation_lists').empty();

    $.ajax({
      url: '/reservations/get/pending/reservations/',
      type: 'GET',
      data: {
        'buildingid': buildingid,
        'statusQ': statusQ
      },
      success: function (response){
        console.log(response);
        if(response.success == "Select Required"){
          $('#select_notice').removeClass('hidden');
        } else if(response.reservation_count == 0) {
          $('#empty_notice').removeClass('hidden');
        } else {
          $('#reservation_lists').removeClass('hidden');
          $.each(response.reservations, function(index, item){
            let li = $('<li></li>', {
              class: 'reservation_item',
            });

            let name = $('<h3></h3>', {
              class: 'name',
              text: `${item.boarder_name} (${item.boarder_email})`
            })

            let dateObj = new Date(item.created);
            let date_setting = { month: 'short', day: 'numeric', year:'numeric' };
            let formated_date = dateObj.toLocaleDateString('en-US', date_setting);
            let date_requested = $('<p></p>', {
              class: 'date_requested',
              text: `${formated_date}`
            })

            let room = $('<p></p>', {
              class: 'room_name',
              text: `${item.room_name}`
            })

            let accept_btn = $('<button></button>', {
              class: 'accept_btns',
              value: `${item.reservationid}`,
              text: 'Accept'
            })

            let decline_btn = $('<button></button>', {
              class: 'decline_btns',
              value: `${item.reservationid}`,
              text: 'Decline'
            })

            li.append(name);
            li.append(date_requested);
            li.append(room);
            li.append(accept_btn);
            li.append(decline_btn);

            $('#reservation_lists').append(li);

          })
          
        }
      },
      error: function(xhr, status, error) {
        let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
        SoloMessageFlow(`${errorMessage}`, 'error');
      }  

    })
  }

  function send_accept_message(id = null){
    let reservationid = null;
    if (!(id == null)){
      reservationid = id;
    } else {
      reservationid = $(this).attr('value');
    }

    console.log(reservationid);
    $.ajax({
      url: '/reservations/get/mailjs_keys/',
      type: 'GET',
      data: {
        'reservationid': reservationid
      }, 
      success: function(response){
        // const data = response_data.response_data;
        // IF AJAX SUCCESS SEND GMAIL TO LANDLORD
        console.log(response);

        emailjs.send(response.public_key, response.template_key, {
          to_name: response.to_name,
          receiver_email: 'alcantaraclement@gmail.com', //data.to_email
          sender_name: response.from_email,
          anchor_tag: `http://127.0.0.1:8000/building_info/${ response.buildingid }/`,
          message: response.message
          // `Good day! Your request to ${response.room_name} at ${response.boarder_name} has been accepted. 
          //           Please visit the site to get the QR code for gcash payment.`
        }).then(
          function() {
            console.log(response.roomid);
            // accept_reservation(response.roomid);
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
      }
    })

  }

  function accept_reservation(){
    let reservationid = $(this).attr('value');
    // if (!(id == null)){
    //   reservationid = id;
    // } else {
    // reservationid = $(this).attr('value');
    // }
    // console.log(id);
    console.log(reservationid);

    $.ajax({
      url: '/reservations/accept/',
      type: 'POST',
      data: {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        'reservationid': reservationid
      },
      success: function(response){
        SoloMessageFlow(`${response.success}`);
        $('#res_pending').trigger('click');
        send_accept_message(reservationid);
      },
      error: function(xhr, status, error) {
        let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
        SoloMessageFlow(`${errorMessage}`, 'error');
      }
    })
  }

  function delete_reservation(){
    $.ajax({
      url: '',
      type: 'POST',
      data: {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        'reservationid': $(this).attr('value')
      },
      success: function(response){

      },
      error: function(xhr, status, error) {
        let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
        SoloMessageFlow(`${errorMessage}`, 'error');
      }
    })
  }
  // function request_building_reservations(build)
})