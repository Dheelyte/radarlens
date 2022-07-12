var fetchHome = ()=> {
  $.ajax({
    type: "GET",
    url: home,
    success: (response)=> {
      $('#home-ratings-div').append(`
        <h5 class="bg-white rounded-top p-3"><b>Business Reviews</b></h5>
      `);
      $('#loading-div').hide();
      $('#home-ratings-div').show();
      $.each(response.ratings, (index, obj)=> {
        var ratingAction;
        if (user != obj.user.id){
          ratingAction = `<li id="report-review" data-review="${obj["review"]}" class="list-group-item list-group-item-action p-2">Report</li>`
        } else {
          ratingAction = `<form action="/delete-business-review/${obj["review"]}/" method="POST">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                            <input type="submit" value="Delete" class="list-group-item list-group-item-action p-2">
                          </form>`
        };
        $('#home-ratings-div').append(`
          <article class="rating-card incomplete-card d-flex overflow-hidden position-relative border-bottom">
            <img class="lazy mr-3" src="${logo}" data-src="${webRoot}${obj["image"]}" alt="${obj["user"]["name"]}">
            <div class="position-relative">
              <p class="text-muted overflow-hidden" style="max-height: 20px">${obj["user"]["name"]} · ${obj["date_posted"]}</p>
              <div class="ratings mt-0">
                <div class="empty-stars"></div>
                <div class="full-stars" style="width: calc(${obj["rating"]}/5*100%)"></div>
              </div>
              <p class="mt-1">${obj["content"]}</p>
            </div>
            <span class="side-ellipsis option-icon p-2 text-muted position-absolute">
              <span class="icon-ellipsis-v"></span>
              <div class="options position-absolute">
                ${ratingAction}
              </div>
            </span>
        </article>`);
      });
      if (response.ratings.length == 0){
        $('#home-ratings-div').append(`
          <p class="bg-white text-center pt-4 pb-4 pr-2 pl-2">This business profile has no reviews yet</p>
        `);
      } else {
        $('#home-ratings-div').append(`
          <div class="d-flex bg-white justify-content-center rounded-bottom">
            <a href="${reviews}" class="edit-review p-2 purple m-1 pointer">See all reviews</a>
          </div>
        `);
      };
      for(var index=0;index < lazy.length;index++){
        lazyLoad(lazy[index]);
      }
    },       
    error: ()=> {
      alertDanger();
      },
      cache: false,
      contentType: false,
      processData: false,
  })
};

$(document).ready(fetchHome);

var lazy = document.getElementsByClassName('lazy');
function lazyLoad(img){
  if(!!window.IntersectionObserver){
    let observer = new IntersectionObserver((entries, observer) => { 
      entries.forEach(entry => {
        if(entry.isIntersecting){
            entry.target.src = entry.target.dataset.src;
            observer.unobserve(entry.target);
        }
      });
    }, {rootMargin: "0px 0px 0px 0px"});
    observer.observe(img);
  }
};

function alertDanger(){
  $('.danger').html(`Something went wrong`);
  $('.danger').show();
  $('.danger').delay(5000).fadeOut(300);
};

$('#action-directions').click((e)=>{
  window.location = $(e.currentTarget).data('dir');
});

$('#see-more').on('click', (e)=>{
  $('.business-description p').toggleClass('incomplete');
  if($('#see-more span').hasClass('icon-angle-down')){
    $('#see-more span').removeClass('icon-angle-down').addClass('icon-angle-up')
  } else {
    $('#see-more span').removeClass('icon-angle-up').addClass('icon-angle-down')
  }
});

$(document).on('click', '.rating-card', (e)=>{
  $(e.currentTarget).toggleClass('incomplete-card')
  $(e.currentTarget).toggleClass('complete-card')
})

$('#cta-btn1').click(()=>{
  $('.cta .options').toggle();
});

$('#cta-btn2').click(()=>{
  $('#review-modal').show()
})

$('#share-btn').on('click', (e)=>{
  $('#share-modal').show()
});

$('.close').click(()=>{
  $('.modal').hide()
})

$('body').on('click', function(e){
  if(e.target.className == "modal" && e.target.id != "crop-modal"){
    $('.modal').hide()
  }
});

$('.share-social').click((e)=>{
  window.location.href = $(e.currentTarget).data('href')
});

$('#copy').on('click', ()=>{
  var elem = document.querySelector('#link');
  elem.select();
  elem.setSelectionRange(0, 99999);
  document.execCommand("copy");
  $('#copy').text('Copied')
});

$('#report-business').click(()=>{
  if(authenticated == "False"){
    window.location.href = login
  } else if(email_verified == "False") {
    window.location.href = verify_email
  } else {
    $.ajax({
      type: "POST",
      url: reportBusiness,
      data: {
        csrfmiddlewaretoken: csrfToken
      },
      success: (response)=>{
        $('.success').html(response);
        $('.success').show();
        $('.success').delay(5000).fadeOut(300);
      },
      error: ()=>{
        alertDanger()
      }
    })
  }
});

$(document).on('click', '#report-review', (e)=>{
  if(authenticated == "False"){
    window.location.href = login
  } else if(email_verified == "False") {
    window.location.href = verify_email
  } else {
    let review = $(e.currentTarget).data('review');
    $.ajax({
      type: "POST",
      url: reportReview,
      data: {
        csrfmiddlewaretoken: csrfToken,
        review: review
      },
      success: (response)=>{
        $(e.currentTarget).hide();
        $('.success').html(response);
        $('.success').show();
        $('.success').delay(5000).fadeOut(300);
      },
      error: ()=>{
        alertDanger()
      }
    })
  }
});

var hiddenrating = document.getElementById('hiddenrating');
$('.star').on('click', function(event){
    hiddenrating.value = event.target.id;
    $('#rating-textarea').show();
    $('#rating-textarea textarea').focus();
})
$('#1').on('mouseover click', (e)=>{
  $('#1').html(`&#9733;`);
  $('#2, #3, #4, #5').html(`&#9734;`);
});
$('#2').on('mouseover click', (e)=>{
  $('#1, #2').html(`&#9733;`);
  $('#3, #4, #5').html(`&#9734;`);
});
$('#3').on('mouseover click', (e)=>{
  $('#1, #2, #3').html(`&#9733;`);
  $('#4, #5').html(`&#9734;`);
});
$('#4').on('mouseover click', (e)=>{
  $('#1, #2, #3, #4').html(`&#9733;`);
  $('#5').html(`&#9734;`);
});
$('#5').on('mouseover click', (e)=>{
  $('#1, #2, #3, #4, #5').html(`&#9733;`);
});

$("#business-rating-form").submit(function (e) {
  e.preventDefault();
  document.getElementById('submit-rating').disabled = true;
  $('#submit-rating').html('Rating...');
  var serializedData = $(this).serialize();
  $.ajax({
    type: 'POST',
    url: rating,
    data: serializedData,
    success: function () {
        $('.success').html(`You have successfully rated this business`);
        $('#review-modal').hide();
        $('#review-modal').html(`<p class="text-center pt-2 ml-3">You have rated this business page</p>`)
        $('.success').show();
        $('.success').delay(5000).fadeOut(300);
    },
    error: function () {
      alertDanger()
    }
  })
});

$('#edit-image').one('click', ()=>{
  $.getScript("https://cdnjs.cloudflare.com/ajax/libs/cropper/4.1.0/cropper.min.js");
  $('head').append(`<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/cropper/4.1.0/cropper.css"/>`);
});

$('#edit-image').on('click', ()=>{
  $('#id_thumbnail').trigger('click');
});

function uploadThumbnail(newblob, blob){
  let fd = new FormData()
  fd.append('thumbnail', newblob, businessName+'.jpeg');
  fd.append('csrfmiddlewaretoken', csrfToken);
  $.ajax({
    method: 'POST',
    url: businessImage,
    enctype: 'multipart/form-data',
    data: fd,
    success: function() {
        $('#crop-modal').hide();
        confirmBtn.disabled = false;
        $('#image-form').trigger('reset');
        $('#business-thumbnail').attr('src', URL.createObjectURL(blob));
        URL.revokeObjectURL(blob);
        $('.success').html(`Cover photo updated`);
        $('.success').show();
        $('.success').delay(5000).fadeOut(300);
    },
    error: function() {
        $('#crop-modal').hide();
        confirmBtn.disabled = false;
        $('#image-form').trigger('reset');
        alertDanger();
    },
    cache: false,
    contentType: false,
    processData: false,
  })
}

const input = document.getElementById('id_thumbnail');
if(input != null){
  input.addEventListener('change', ()=>{
    $('#crop-modal').show();
    let img = input.files[0];
    let url = URL.createObjectURL(img);
    $('#crop-modal #modal-body').html(`<img src="${url}" id="image">`);
    let $image = $('#image');
    $image.cropper({
      aspectRatio: 40 / 17,
    });
    cropper = $image.data('cropper');
  })
}

const confirmBtn = document.getElementById('confirm-btn');
confirmBtn.addEventListener('click', ()=>{
  confirmBtn.disabled = true;
  cropper.getCroppedCanvas().toBlob((blob)=>{
    let url = URL.createObjectURL(blob);
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
        uploadThumbnail(newblob, blob)
      },
      "image/jpeg",
      0.9
    )};
  })
})

$('#close-btn1, #close-btn2').on('click', ()=>{
  $('#crop-modal').hide();
  $('#image-form').trigger('reset');
  confirmBtn.disabled = false;
});

$(document).on('click', '.side-ellipsis', (e)=>{
  $(e.currentTarget).find('.options').toggle();
});