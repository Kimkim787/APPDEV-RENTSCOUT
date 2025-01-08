emailjs.init("Q_A-eXEwrvvQsFMYs");
$(document).ready(function(){
  request_reservations();
  
  $('.building_items').on('click', function(){
    console.log("b_item clicked");  

    $('#res_pending').attr('value', $(this).attr('value'));
    $('#res_accepted').attr('value', $(this).attr('value'));
    $('#res_declined').attr('value', $(this).attr('value'));

    $('#pay_pending').attr('value', $(this).attr('value'));
    $('#pay_accepted').attr('value', $(this).attr('value'));
    $('#pay_declined').attr('value', $(this).attr('value'));

    request_reservations(buildingid = $(this).attr('value'));
  })
  
  $('#res_pending').on('click', function(){
    $('#res_filter').attr('value', "Pending");
    request_reservations(buildingid = $(this).attr('value'), statusQ = 'Pending');
  });

  $('#res_accepted').on('click', function(){
    $('#res_filter').attr('value', "Accepted");
    request_reservations(buildingid = $(this).attr('value'), statusQ = 'Accepted');
  })

  $('#res_declined').on('click', function(){
    $('#res_filter').attr('value', "Declined");
    request_reservations(buildingid = $(this).attr('value'), statusQ = 'Declined')
  })

  $('#reservation_lists').on('click', '.accept_btns', accept_reservation);

  $('#reservation_lists').on('click', '.decline_btns', decline_reservation);

  $('#reservation_lists').on('click', '.delete_btns', delete_reservation_byid);

  // PAYMENT FILTER BUTTONS
  $('#pay_pending').on('click', function(){
    $('#pay_filter').attr('value', 'Pending');
    $('.colbox').addClass('hidden');
    $('.paymentbox').removeClass('hidden');
    payment_filter($(this).val(), 'Pending');
    
  });

  $('#pay_accepted').on('click', function(){
    $('#pay_filter').attr('value', 'Accepted');
    payment_filter($(this).val(), 'Accepted');
  });

  $('#pay_declined').on('click', function(){
    $('#pay_filter').attr('value', 'Declined');
    payment_filter($(this).val(), 'Declined');
  });

  $('#reservation_lists').on('click', '.accept_payment', function(){
    $.ajax({
      url: '/payment/accept/',
      type: 'POST',
      data: {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        'paymentid': $(this).attr('value')
      },
      success: function(response){
        SoloMessageFlow(response.success);
        payment_filter($('#pay_pending').attr('value'), $('#pay_filter').attr('value'));
      },
      error: function(xhr, status, error) {
        let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
        SoloMessageFlow(`${errorMessage}`, 'error');
      }

    })
  });

  $('#reservation_lists').on('click', '.decline_payment', function(){
    $.ajax({
      url: '/payment/decline/',
      type: 'POST',
      data: {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        'paymentid': $(this).attr('value')
      },
      success: function(response){
        SoloMessageFlow(response.success);
        payment_filter($('#pay_pending').attr('value'), $('#pay_filter').attr('value'));
      },
      error: function(xhr, status, error) {
        let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
        SoloMessageFlow(`${errorMessage}`, 'error');
      }
    })
  });

  $('#reservation_lists').on('click', '.hide_payment', function(){
    $.ajax({
      url: '/payment/hide/',
      type: 'POST',
      data: {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        'paymentid': $(this).attr('value')
      },
      success: function(response){
        SoloMessageFlow(response.success);
        payment_filter($('#pay_pending').attr('value'), $('#pay_filter').attr('value'));
      },
      error: function(xhr, status, error) {
        let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
        SoloMessageFlow(`${errorMessage}`, 'error');
      }
    });
  });

  $('#reservation_lists').on('click', '.receipt_img', function(){
    openFullScreen($(this).attr('src'));
  });

  $('#fullscreen-overlay').on('click', closeFullScreen);
  
  function request_reservations(buildingid=null, statusQ = 'Pending'){
    $('#select_notice').addClass('hidden');
    $('#empty_notice').addClass('hidden');
    $('#reservation_lists').addClass('hidden');
    $('#reservation_lists').empty();

    if (buildingid != null){

      $('#pay_pending').attr('value', buildingid);
      $('#pay_accepted').attr('value', buildingid);
      $('#pay_declined').attr('value', buildingid);

    } else {
      let value = $('#buildings_container .building_items').first().attr('value');

      console.log(value);
      $('#pay_pending').attr('value', value);
      $('#pay_accepted').attr('value', value);
      $('#pay_declined').attr('value', value);
    }

    $.ajax({
      url: '/reservations/get/pending/reservations/',
      type: 'GET',
      data: {
        'buildingid': buildingid,
        'statusQ': statusQ
      },
      success: function (response){
        console.log(response);
        if(response.success == "Select Required"){ // building owned is more than 1
          $('#select_notice').removeClass('hidden');
        } else if(response.reservation_count == 0) { // no reservation found
          $('#empty_notice').removeClass('hidden');
        } else {                                      
          $('#reservation_lists').removeClass('hidden');
          $.each(response.reservations, function(index, item){
            let li = $('<li></li>', {
              class: 'reservation_item',
            });

            let div1 = $('<div></div>', {
              class: 'div1',
            });

            let div2 = $('<div></div>', {
              class: 'div2',
            });

            let div3 = $('<div></div>', {
              class: 'div3',
            });

            let div4 = $('<div></div>', {
              class: 'div4',
            });

            let div5 = $('<div></div>', {
              class: 'div5',
            });

            let name = $('<h5></h5>', {
              class: 'name',
              text: `${item.boarder_name}`
            })
            let email = $('<h5></h5>', {
              class: 'email',
              text: `${item.boarder_email}`
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

            if(statusQ == 'Pending' || statusQ == 'Declined'){
              left_btn = $('<button></button>', {
                class: 'accept_btns',
                value: `${item.reservationid}`,
                text: 'Accept'
              })

            }
            
            if(statusQ == 'Accepted' || statusQ == 'Pending'){
              right_btn = $('<button></button>', {
                class: 'decline_btns',
                value: `${item.reservationid}`,
                text: 'Decline'
              })
            } else if(statusQ == 'Declined') {
              right_btn = $('<button></button>', {
                class: 'delete_btns',
                value: `${item.reservationid}`,
                text: 'Delete'
              })
            }

            div1.append(name);
            div2.append(email);
            div3.append(room);
            div4.append(date_requested);
            // statusQ == 'Accepted' && li.append(accept_btn);
            if(statusQ == 'Pending' || statusQ == 'Declined'){
              div5.append(left_btn);
            }
            div5.append(right_btn);
            li.append(div1);
            li.append(div2);
            li.append(div3);
            li.append(div4);
            li.append(div5);
            
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

  function  accept_reservation(){
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

  // function decline_reservation(){
  //   $.ajax({
  //     url: '/reservations/decline/',
  //     type: 'POST',
  //     data: {
  //       'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
  //       'reservationid': $(this).attr('value')
  //     },
  //     success: function(response){
  //       SoloMessageFlow(response.success);
  //     },
  //     error: function(xhr, status, error) {
  //       let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
  //       SoloMessageFlow(`${errorMessage}`, 'error');
  //     }
  //   })
  // }

  function decline_reservation(){
    $.ajax({
      url: '/reservations/decline/',
      type: 'POST',
      data: {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        'reservationid': $(this).attr('value')
      },
      success: function(response){
        $('#res_pending').trigger('click');
        SoloMessageFlow(response.success);
      },
      error: function(xhr, status, error) {
        let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
        SoloMessageFlow(`${errorMessage}`, 'error');
      }
    })
  }

  function delete_reservation_byid(){
    $.ajax({
      url: '/reservations/delete_byid/',
      type: 'POST',
      data: {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        'reservationid': $(this).attr('value')
      },
      success: function(response){
        SoloMessageFlow(response.success);
      },
      error: function(xhr, status, error) {
        let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
        SoloMessageFlow(`${errorMessage}`, 'error');
      }
    })
  }

  // FILTER BY RESERVATION STATUS
  function payment_filter(buildingid, Q){
    console.log('payment filter')
    const reserve_div = $('#reservation_lists');

    reserve_div.empty();
    $.ajax({
      url: '/payment/filter/',
      type: 'GET',
      data: {
        'buildingid': buildingid,
        'statusQ': Q
      },
      success: function(response){
        console.log(response);
        $.each(response.payments_list, function(index, data){
          li = $('<li></li>', {
            class: 'reservation_item'
          })

          let paydiv1 = $('<div></div>', {
            class: 'paydiv1',
          });

          let paydiv2 = $('<div></div>', {
            class: 'paydiv2',
          });

          let paydiv3 = $('<div></div>', {
            class: 'paydiv3',
          });

          let paydiv4 = $('<div></div>', {
            class: 'paydiv4',
          });

          let paydiv5 = $('<div></div>', {
            class: 'paydiv5',
          });

          user_name = $('<p></p>', {
            class: 'boarder_name',
            text: data.boarder
          })

          date = $('<p></p>', {
            class: 'date',
            text: data.date
          })

          image = $('<img></img>', {
            class: 'receipt_img',
            src: data.payment_img,
            alt: 'Receipt Img'
          })

          referal_code = $('<p></p>', {
            class: 'referal_code',
            text: `${data.referal_code}`
          })

            left_btn = $('<button></button>', {
              class: 'accept_payment',
              text: 'Accept',
              value: data.paymentid
            })
            
            right_btn = $('<button></button>', {
              class: 'decline_payment',
              text: 'Decline',
              value: data.paymentid
            })

            left_btn = $('<button></button>', {
              class: 'hide_payment',
              text: 'Hide',
              value: data.paymentid
            })
          
          if( Q == 'Pending' ){
            left_btn = $('<button></button>', {
              class: 'accept_payment',
              text: 'Accept',
              value: data.paymentid
            })

            right_btn = $('<button></button>', {
              class: 'decline_payment',
              text: 'Decline',
              value: data.paymentid
            })
          } else if ( Q == "Accepted"){
            left_btn = $('<button></button>', {
              class: 'hide_payment',
              text: 'Hide',
              value: data.paymentid
            })

          } else if ( Q == "Declined"){
            left_btn = $('<button></button>', {
              class: 'accept_payment',
              text: 'Accept',
              value: data.paymentid
            })

            right_btn = $('<button></button>', {
              class: 'hide_payment',
              text: 'Hide',
              value: data.paymentid
            })
          }

          paydiv1.append(user_name);
          paydiv2.append(date);
          
          paydiv3.append(referal_code);
          paydiv4.append(left_btn);
          if(Q == 'Pending' || Q == 'Declined'){
            paydiv4.append(right_btn);
          }
          paydiv5.append(image);

          li.append(paydiv1);
          li.append(paydiv2);
          li.append(paydiv3);
          li.append(paydiv4);
          li.append(paydiv5);
          reserve_div.append(li);
          $('#empty_notice').addClass('hidden');
          $('#select_notice').addClass('hidden');
          reserve_div.removeClass('hidden');
        })

      },
      error: function(xhr, status, error) {
        let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : error;
        SoloMessageFlow(`${errorMessage}`, 'error');
      }
    })
  }
  
  // FULL SCREEN THING
  function openFullScreen(img) {
    console.log(img);
    const fullImage = $('#fullscreen-image');
    const overlay = $('#fullscreen-overlay');
    
    fullImage.attr('src', img);
    overlay.css('display', 'flex');
}

  function closeFullScreen() {
    console.log("Close Fullscreen");
      $('#fullscreen-overlay').css('display', 'none');
  }

})