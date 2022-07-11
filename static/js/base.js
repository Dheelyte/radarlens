if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/service_worker.js').then(function(registration) {
    }, /*catch*/ function(error) {
      console.log('Service worker registration failed:', error);
    });
  } else {
    console.log('Service workers are not supported.');
}

if(window.matchMedia("(max-width: 768px)").matches){
    let deferredPrompt;
    const A2HSButton = document.querySelector('.a2hs-button');
    const A2HS = document.querySelector('.a2hs-container');
    $('.a2hs-container').click(()=>{
        $('.a2hs-container').hide()
    })

    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        A2HS.style.display = 'block';
        A2HSButton.addEventListener('click', (e) => {
            A2HS.style.display = 'none';
            deferredPrompt.prompt();
        })
    })
}

function find(e){
    function showPosition(position){
        $(e.currentTarget.querySelector('#id_lon')).attr('value', position.coords.longitude);
        $(e.currentTarget.querySelector('#id_lat')).attr('value', position.coords.latitude);
        document.getElementById(e.currentTarget.id).submit();
    }
    function search() {
        $(e.currentTarget.querySelector('#id_lon')).remove();
        $(e.currentTarget.querySelector('#id_lat')).remove();
        document.getElementById(e.currentTarget.id).submit();
    }
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, search);
    }
}
$('#search-form2, #search-form, #home-search-form').submit((e)=>{
    e.preventDefault();
    find(e)
})
$('#search').on('click', function() {
    $('#header-full-search').toggle()
    $('#header-full-search input[type="search"]').focus()
})
$('#main').click(()=>{
    $('#header-full-search').hide()
    $('#user-div').hide()
})
$('#user').click(()=>{
    $('#user-div').toggle()
})

function unreadDot(){
    if($('#notification-count').text()!="" || $('#message-count').text()!=""){
        $('.user-unread').show()
    }
}
function unread(){
    $.ajax({
        type: "GET",
        url: notificationCount,
        success: function (response) {
            $('#notification-count').text(response)
        },
        cache: false,
        contentType: false,
        processData: false,
    });
    $.ajax({
        type: "GET",
        url: messageCount,
        success: function (response) {
            $('#message-count').text(response);
            unreadDot()
        },
        cache: false,
        contentType: false,
        processData: false,
    })
}
if(isAuthenticated == "True"){
    unread()
}