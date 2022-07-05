$('#edit-icon').one('click', ()=>{
    $.getScript("https://cdnjs.cloudflare.com/ajax/libs/cropper/4.1.0/cropper.min.js");
    $('head').append(`<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/cropper/4.1.0/cropper.css" />`);
});
function alertDanger(){
    $('.danger').html(`Something went wrong`);
    $('.danger').show();
    $('.danger').delay(5000).fadeOut(300);
};

const editIcon = document.getElementById('edit-icon');
const imageForm = document.getElementById('image-form');
const imageBox = document.getElementById('modal-body');
const confirmBtn = document.getElementById('confirm-btn');
var cropper;
var fd = new FormData();

editIcon.addEventListener('click', (e)=>{
    e.preventDefault();
    $('#image-form').trigger('click');
});

function uploadThumbnail(blob, url){
    console.log(blob);
    fd.append('image', blob, 'pic.png');
    fd.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        type: 'POST',
        url: updateThumbnail,
        enctype: 'multipart/form-data',
        data: fd,
        success: function(response) {
            $('#edit-profile-pic').hide();
            $('#thumbnail').attr('src', url);
            $('.success').html(response);
            $('.success').show();
            $('.success').delay(5000).fadeOut(300);
            $('#confirm-btn').attr('disabled', false);
        },
        error: function() {
            $('#edit-profile-pic').hide();
            $('#confirm-btn').attr('disabled', false);
            alertDanger();
        },
        cache: false,
        contentType: false,
        processData: false,
    })
}

imageForm.addEventListener('change', ()=>{
    $('#edit-profile-pic').show();
    const image = imageForm.files[0];
    const url = URL.createObjectURL(image);
    imageBox.innerHTML = `<img src="${url}" id="image">`;   
    var $image = $('#image');
    $image.cropper({
        aspectRatio: 1 / 1,
    });
    cropper = $image.data('cropper');
});

confirmBtn.addEventListener('click', ()=>{
    $('#confirm-btn').attr('disabled', true);
    console.log("1");
    cropper.getCroppedCanvas().toBlob((blob)=>{
        console.log("2");
        const url = URL.createObjectURL(blob);
        const img = new Image();
        img.src = url;
        img.onload = function() {
            const canvas = document.createElement("canvas");
            canvas.width = 150;
            canvas.height = 150;
            const ctx = canvas.getContext("2d");
            ctx.drawImage(img, 0, 0, 150, 150);
            canvas.toBlob((new_blob)=>{
                uploadThumbnail(new_blob, url)
            },
            "image/jpeg",
            0.9
            )
        };      
    })
})

$('#close-btn1, #close-btn2').on('click', ()=>{
    $('#edit-profile-pic, #upload-modal').hide();
    $('#image-form').val(null);
})

$('#close-btn3').click(()=>{
    $('#edit-profile').hide()
})
$('.update').click(()=>{
    $('#edit-profile').show()
})