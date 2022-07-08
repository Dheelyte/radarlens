const alertBox = document.getElementById('alert-box');
const imageBox = document.getElementById('modal-body');
const imageForm = document.getElementById('image-form');
const confirmBtn = document.getElementById('confirm-btn');
const input = document.getElementById('id_thumbnail');
const phone = document.getElementById('id_phone');
const submit = document.getElementById('submit');
var cropper;
var newBlob;

$('#image-button').on('click', ()=>{
    $('#id_thumbnail').trigger('click')
});

input.addEventListener('change', ()=>{
    $('#exampleModalCenter').show();
    alertBox.innerHTML = "";
    const img_data = input.files[0];
    const url = URL.createObjectURL(img_data);
    imageBox.innerHTML = `<img src="${url}" id="image">`;
    var $image = $('#image');
    $image.cropper({
        aspectRatio: 40 / 18,
    });
    cropper = $image.data('cropper');
})

confirmBtn.addEventListener('click', ()=>{
    $('#exampleModalCenter').hide();
    cropper.getCroppedCanvas().toBlob((blob)=>{
        let url = URL.createObjectURL(blob);
        $('#preview').html(`<img src="${url}" style="width: 100%">`);
        let img = new Image();
        img.src = url;
        img.onload = ()=>{
            const canvas = document.createElement("canvas");
            const width = 600;
            const scaleFactor = width / img.width;
            canvas.width = width;
            canvas.height = img.height * scaleFactor;
            const ctx = canvas.getContext("2d");
            ctx.drawImage(img, 0, 0, width, img.height * scaleFactor);
            canvas.toBlob((newblob)=>{
                newBlob = newblob;
            },
            "image/jpeg",
            0.9
        )};
    })
})


submit.addEventListener('click', (e)=>{
    e.preventDefault();
    if(phone.value == "" || phone.value == null){
        $('.danger').html(`Enter a phone number`);
        $('.danger').show();
        $('.danger').delay(5000).fadeOut(300);
    } else {
        submit.disabled = true;
        const fd = new FormData();
        fd.append('csrfmiddlewaretoken', csrf_token);
        fd.append('phone', phone.value);
        if(newBlob != null){
            fd.append('thumbnail', newBlob, business+'.jpeg');
        };
        $.ajax({
            method: 'POST',
            url: businessImage,
            enctype: 'multipart/form-data',
            data: fd,
            success: function() {
                $('#exampleModalCenter').hide();
                window.location.href = next;
            },
            error: function() {
                $('#exampleModalCenter').hide();
                submit.disabled = false;
                alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                                        Oops...something went wrong
                                    </div>`;
            },
            cache: false,
            contentType: false,
            processData: false,
        })
    }
});

$('#close-btn1, #close-btn2, #confirm-btn').on('click', ()=>{
  $('#exampleModalCenter').hide();
  input.value = null;
  confirmBtn.disabled = false
})