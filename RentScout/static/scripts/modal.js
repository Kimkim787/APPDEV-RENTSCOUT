$(document).ready(function(){
    $('#update_room').on('click', function(){
        let room_id = $(this).closest('.additionaldatabox').attr('data-roomid');
        console.log(room_id)
        $('#update_modal').removeClass('hidden');
        $('#update_modal').find('#room_id').val(room_id);
    })

    // $('#update_modal').on('click', function(){
    //     console.log('Queried');
    //     let query = $(this).attr('id');
    //     $.ajax({
    //         url: '/room_update/',  
    //         // type: 'POST', 
    //         data: {
    //             'primary_key': query, 
    //             'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
    //         },
    //         success: function(data){
    //             console.log(data);

    //             let modal_container = $('#update_modal');
    //             let room_id = modal_container.find('#room_id');
    //             let room_name = modal_container.find("input[name='room_name']");
    //             let person_free = modal_container.find("input[name='person_free']");
    //             let current_male = modal_container.find("input[name='current_male']");
    //             let current_female = modal_container.find("input[name='current_female']");
    //             let price = modal_container.find("input[name='price']");
    //             let room_size = modal_container.find("input[name='room_size']");
    //             let bed = modal_container.find("input[name='bed']");
    //             let double_deck = modal_container.find("input[name='double_deck']");
    //             let shower = modal_container.find("input[name='shower']");
    //             let priv_bathroom = modal_container.find("input[name='priv_bathroom']");
    //             let public_bathroom = modal_container.find("input[name='public_bathroom']");
    //             let AC = modal_container.find("input[name='AC']");
    //             let wardrobe = modal_container.find("input[name='wardrobe']");
    //             let kitchen = modal_container.find("input[name='kitchen']");
    //             let free_wifi = modal_container.find("input[name='free_wifi']");
                
    //             room_id.val(data.roomid);
    //             room_name.val(data.room_name);
    //             person_free.val(data.person_free);
    //             current_male.val(data.current_male);
    //             current_female.val(data.current_female);
    //             price.val(data.price);
    //             room_size.val(data.room_size);
    //             bed.val(data.bed);
    //             double_deck.val(data.double_deck);

    //             shower.prop('checked', data.shower);
    //             priv_bathroom.prop('checked', data.priv_bathroom);
    //             public_bathroom.prop('checked', data.public_bathroom);
    //             AC.prop('checked', data.AC);
    //             wardrobe.prop('checked', data.wardrobe);
    //             kitchen.prop('checked', data.kitchen);
    //             free_wifi.prop('checked', data.free_wifi);

    //             modal_container.removeClass('hidden');
    //         },
    //         error: function(xhr, status, error) {
    //             console.log(xhr.responseText);
    //             alert('Update failed');
    //         }
    //     });
    // })
});    

// document.getElementById('add_new_room_btn').addEventListener('click', function() {
//     document.querySelector('.modal').classList.remove('hidden');
// });

// document.getElementById('addroombackbtn').addEventListener('click', function(e) {
//     e.preventDefault();
//     document.querySelector('.modal').classList.add('hidden');
// });

