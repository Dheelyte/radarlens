const cropBox = document.getElementById('modal-body');
const cropBtn = document.getElementById('confirm-btn');
const name = document.getElementById('id_name');
const description = document.getElementById('id_description');
const price = document.getElementById('id_price');
const input = document.getElementById('id_image');
const submit = document.getElementById('submit');
const form = document.getElementById('product-form');
var cropper;
var newBlob;

$('#image-button').on('click', ()=>{
    $('#id_image').trigger('click');
});

function alertDanger(){
    $('.danger').html(`Oops...Something went wrong.`);
    $('.danger').show();
    $('.danger').delay(5000).fadeOut(300);
};

input.addEventListener('change', ()=>{
    $('#exampleModalCenter').show();
    let image = input.files[0];
    let url = URL.createObjectURL(image);
    cropBox.innerHTML = `<img src="${url}" id="image">`;
    var $image = $('#image');
    $image.cropper({
        aspectRatio: 1 / 1,
    });
    cropper = $image.data('cropper');
});

cropBtn.addEventListener('click', ()=>{
    $('#exampleModalCenter').hide();
    $('#image-button').attr('value', 'Change Image');
    cropper.getCroppedCanvas().toBlob((blob)=>{
        $('#preview').html(`<img src="${URL.createObjectURL(blob)}" style="width: 100%;">`);
        let url = URL.createObjectURL(blob);
        const img = new Image();
        img.src = url;
        img.onload = ()=>{
            const canvas = document.createElement("canvas");
            canvas.width = 600;
            canvas.height = 600;
            const ctx = canvas.getContext("2d");
            ctx.drawImage(img, 0, 0, 600, 600);
            canvas.toBlob((newblob)=>{
                newBlob = newblob;
            },
            "image/jpeg",
            0.9
        )};
    })
});

form.addEventListener('submit', (e)=>{
    e.preventDefault();
    if(name.value.length==0 || description.value.length==0 || price.value.length==0){
        return;
    } else {
        submit.disabled = true;
        $('#product-form #submit').val('Uploading...');
        const fd = new FormData();
        fd.append('csrfmiddlewaretoken', csrf_token);
        fd.append('name', name.value);
        fd.append('description', description.value);
        if(price.value){
            fd.append('price', price.value);
        };
        if(newBlob != null){
            fd.append('image', newBlob, name.value+'.jpeg')
        };
        $.ajax({
            type: 'POST',
            url: product,
            enctype: 'multipart/form-data',
            data: fd,
            success: function(response) {
                $('#view-product').attr('href', response);
                $('#success').show();
            },
            error: function() {
                alertDanger();
                submit.disabled = false;
                $('#product-form #submit').val('Add Product');
            },
            cache: false,
            contentType: false,
            processData: false,
        })
    }
});

$('#close-btn1, #close-btn2, #confirm-btn').on('click', ()=>{
    $('#exampleModalCenter').hide();
    cropBtn.disabled = false;
    input.value = null;
    input.value = "";
});

$('#add-product').click(()=>{
    $('#success').hide();
    $('#preview').html(`
        <div class="center">
            <span class="fas fa-image"></span>
            <p>Add image</p>
        </div>
    `);
    $('#product-form input, #product-form textarea').each(function(){
        $(this).val('')
    });
    submit.disabled = false;
    $('#product-form #submit').val('Add Product');
    newBlob = null;
});