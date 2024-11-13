$(document).ready(function(){
    let reports_container = $('#reports_container');

    // DISPLAY ALL REPORTS
    get_all_reports();

    reports_container.on("click", '.review_btn', function(){
        const buildingId = $(this).val();
        const url = `/building_info/${buildingId}/`;
        window.open(url, '_blank');
    })

    reports_container.on("click", '.ban_btn', function(){
        const buildingid = $(this).val();
        console.log($(this).val());
        $.ajax({
            url: '/building/delete_view/',
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'buildingid': buildingid
            },
            success: function(response){
                alert(response.success);
                get_all_reports();
            },
            error: function(xhr) {
                console.error("Error:", xhr.responseJSON.error);
            }

        })
    })

    reports_container.on("click", '.deny_btn', function(){
        const report_id = $(this).val();
        $.ajax({
            url: '/building/reports/delete/',
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'reportid': report_id
            },
            success: function(response){
                alert(response.success);
                get_all_reports();
            }, 
            error: function(xhr) {
                console.error("Error:", xhr.responseJSON.error);
            }
        })
    })

    function get_all_reports(){
        $('#reports_container').empty();
        $.ajax({
            url: '/buildings/report/get_all/',
            type: 'GET',
            success: function(response){
                console.log(response);
                $.each(response.reports, function(index, report){
                    console.log(response.reports);
    
                    let report_item = $('<div></div>', {
                        class: 'reports'
                    });
    
                    let left_container = $('<div></div>', {
                        class: 'left_container'
                    });
    
                    let right_container = $('<div></div>', {
                        class: 'right_container'
                    });
                    
                    let buttons_container = $('<div></div>', {
                        class: 'buttons_container'
                    });
    
                    let image = $('<img>', {
                        src: report.building_image,
                        alt: `Image of ${report.building_name}`,
                        class: 'report_images'
                    });
    
                    let header = $('<h3></h3>', {
                        class: 'report_header',
                        text: `${report.building_name} by ${report.reporter}`
                    });
    
                    let reason = $('<p></p>', {
                        text: report.reason
                    });
    
                    let reasontxt = $('<h5></h5>', {
                        text: "REASON"
                    });
    
                    let review = $('<button></button>', {
                        class: 'review_btn',
                        value: report.buildingid,
                        text: 'Review'
                    });
    
                    let ban_building = $('<button></button>', {
                        class: 'ban_btn',
                        value: report.buildingid,
                        text: 'Ban Building'
                    });
    
                    let deny = $('<button></button>', {
                        class: 'deny_btn',
                        value: report.reportid,
                        text: 'Deny Report'
                    });
    
                    // Set up click event for image
                    image.on('click', function() {
                        $('#photo_view_img').attr('src', report.building_image);
                        $('#photo_view_img').attr('alt', `Image of ${report.building_name}`);
                        $('.selected_photo').removeClass('hidden'); 
                    });
    
                    left_container.append(image);
    
                    right_container.append(header);
                    right_container.append(reasontxt);
                    right_container.append(reason);
    
                    buttons_container.append(review);
                    buttons_container.append(ban_building);
                    buttons_container.append(deny);
    
                    report_item.append(right_container);
                    report_item.append(buttons_container);
                    report_item.append(left_container);
                    $('#reports_container').append(report_item);
                });
            }, 
            error: function(xhr, status, error){
                console.log(error);
                alert(`Error: ${xhr.responseText.error || error}`);
            }
        });
    }
     
});