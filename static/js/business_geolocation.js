function allowAccess(){
    $('.info').html(`Allow location access or turn on location`);
    $('.info').show();
    $('.info').delay(5000).fadeOut(300);
}

document.getElementById('use-location').addEventListener('click', function(){
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(setPosition, allowAccess);
    }
})

function setPosition(position){
    $.ajax({
        type: "POST",
        url: useLocation,
        data: {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            csrfmiddlewaretoken: csrf_token
        },
        success: ()=>{
            window.location.href = business
        },
        error: ()=>{
            $('.danger').html(`Something went wrong`);
            $('.danger').show();
            $('.danger').delay(5000).fadeOut(300);
        },
        cache: false,
    })
};

$('#use-map').click(()=>{
    $('.modal').show()
});

$('#close-btn1').click(()=>{
    $('.modal').hide()
})