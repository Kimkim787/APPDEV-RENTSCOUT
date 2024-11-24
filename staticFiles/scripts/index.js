
function showNotification() {
    console.log("show called");
    const notifications = document.querySelectorAll('.message'); // Selects all elements with the 'message' class
    if (notifications.length < 1){
        return;
    }
    notifications.forEach(notification => {
        notification.style.animation = 'slideInOut 10s';
    });
}

function removeNotificationAnimation() {
    console.log("remove called");
    const notifications = document.querySelectorAll('.message');
    notifications.forEach(notification => {
        notification.style.animation = 'none';
    
        notification.offsetHeight;

        notification.style.animation = '';

        notification.remove();
    })
    
}

function MessageAnimationFlow(){
    // Call the function to show the notification
    showNotification();
    setTimeout(() => {
        removeNotificationAnimation();
    }, 10000);
    
}
MessageAnimationFlow();

function SoloMessageFlow(message, status = "success"){
    console.log("Solo called");
    const message_container = $('#messages-container');
    const message_text = $('<p></p>', {
        class: "newmessage",
        text: message
    });
    if(status === "success"){
        $(message_text).addClass('success_message');
    } else if(status === "error"){
        $(message_text).addClass("error_message");
    }

    message_container.append(message_text);

    $(message_text).css("animation", 'slideInOut 10s');

    setTimeout(() => {
        $(message_text).remove();
    }, 10000);
}

// setTimeout(() => {
//     SoloMessageFlow("Hello Nigga");
// }, 1000);

// setTimeout(() => {
//     SoloMessageFlow("Hello Nigga");
// }, 2000);

// setTimeout(() => {
//     SoloMessageFlow("Hello Nigga");
// }, 3000);