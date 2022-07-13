let div = document.getElementById('reviews');
if(div){
    let more = document.getElementById('more-div');
    if(div.childElementCount < 10){
        more.style.display = "none"
    }
};
function alertSuccess(text){
  $('.success').html(text);
  $('.success').show();
  $('.success').delay(5000).fadeOut(300);
}

function alertDanger(){
  $('.danger').html(`Something went wrong`);
  $('.danger').show();
  $('.danger').delay(2000).fadeOut(300);
}

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

$.ajax({
  method: "GET",
  url: relatedProducts,
  data:{
    q: $('#product-slug').html()
  },
  success: (response)=>{
    $('#loading-div').hide()
    $('#related-products').append(`<div class="scrolling-wrapper d-flex"></div>`);
    $.each(response, (index, obj)=>{
      var price = ``;
        if(obj["price"] != null){
          price = `<p class="text-muted m-0">${obj["currency"]} ${obj["price"]}</p>`;
        };
      $('#related-products .scrolling-wrapper').append(`
        <div class="card product-card mb-1 shadow-sm">
          <div class="product-image-div position-relative">
            <img class="lazy position-absolute" src="${placeholder}" data-src="${obj["image"]}" role="img">
          </div>
          <div class="card-body p-1">
            <p class="card-text m-0">${obj["name"]}</p>
            <div class="ratings">
              <div class="empty-stars"></div>
              <div class="full-stars" style="width: calc(${obj["rating"]}/5*100%)"></div>
            </div>
            ${price}
            <a href="${obj["url"]}" class="stretched-link"></a>
          </div>
        </div>
      `)
    })
    for(var index=0;index < lazy.length;index++){
      lazyLoad(lazy[index]);
    };
    if(response==""){
      $('#loading-div').hide();
      $('.products-title').hide()
    }
  },
  error: ()=>{
    alertDanger()
  }
})

$('#share').click(()=>{
  $('#share-div').show()
});

$('#share-div').click((e)=>{
  if(e.target.id == "share-div"){
    $('#share-div').hide()
  }
});

$('.share-social').click((e)=>{
  window.location.href = $(e.target).data('href')
});

$('#copy').on('click', ()=>{
  let elem = document.getElementById('share-link');
  elem.select();
  elem.setSelectionRange(0, 99999);
  document.execCommand("copy");
  $('#copy').text('Copied')
});

$('.desc-div').on('click', (e)=>{
  $('.desc-div .overflow-hidden').toggleClass('incomplete');
  if($('.desc-more span').hasClass('icon-angle-down')){
    $('.desc-more span').removeClass('icon-angle-down').addClass('icon-angle-up')
  } else {
    $('.desc-more span').removeClass('icon-angle-up').addClass('icon-angle-down')
  }
});

$(document).on('click', '.in-paragraph', (e)=>{
  $(e.currentTarget).toggleClass('incomplete-card')
  $(e.currentTarget).toggleClass('complete-card')
})

$('.cta .option-icon').click(()=>{
  $('.cta .options').toggle()
});

$(document).on('click', '.side-ellipsis', (e)=>{
  $(e.currentTarget).find('.options').toggle()
});

const showOnPx = 2000;
const backToTop = document.querySelector('.back-to-top');
const scrollContainer = () =>{
  return document.documentElement || document.body
};
document.addEventListener("scroll", ()=>{
  if(scrollContainer().scrollTop > showOnPx){
    backToTop.classList.remove("d-none")
  } else {
    backToTop.classList.add("d-none")
  }
})
const goToTop = () =>{
  document.body.scrollIntoView()
}
backToTop.addEventListener("click", goToTop)

var hiddenrating = document.getElementById('hiddenrating');
  $('.star').on('click', function(event){
    hiddenrating.value = event.target.id;
    $('#rating-textarea').show();
    $('#rating-textarea textarea').focus();
  });
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

  $("#product-rating-form").submit(function (e) {
    e.preventDefault();
    document.getElementById('submit-rating').disabled = true;
    $('#submit-rating').html('Rating...');
    var serializedData = $(this).serialize();
    $.ajax({
        type: 'POST',
        url: rating,
        data: serializedData,
        success: function () {
          alertSuccess('You have successfully rated this product')
          $('.rating-div').hide();
        },
        error: function () {
          alertDanger()
        }
    })
});

$('#action-call').click((e)=>{
  e.preventDefault();
  $.ajax({
    type: "POST",
    url: call,
    data: {
      csrfmiddlewaretoken: csrfToken,
      slug: $(e.currentTarget).data('business')
    },
    success: ()=>{},
    error: ()=>{
      alertDanger();
    }
  })
  window.location = $(e.currentTarget).attr('href');
});

$('#save').click((e)=>{
    if(authenticated == "False"){
        window.location.href = login
    } else if(email_verified == "False") {
        window.location.href = verify_email
    } else {
      if ($('#save-text').html === 'Saved') {
        $('#save-text').html('Save');
        $('#save-icon').removeClass('icon-heart').addClass('icon-heart-o');
      } else {
        $('#save-text').html('Saved');
        $('#save-icon').removeClass('icon-heart-o').addClass('icon-heart');
      };
      $.ajax({
          method: 'POST',
          url: save,
          data:{
              csrfmiddlewaretoken: csrfToken,
          },
          success: (response)=>{
            if(response === "saved"){
              $('#save-icon').removeClass('icon-heart-o').addClass('icon-heart');
              $('#save-text').html('Saved');
              alertSuccess('Product saved')
            } else{
              $('#save-icon').removeClass('icon-heart').addClass('icon-heart-o');;
              $('#save-text').html('Save');
            }
          },
          error: ()=>{
            alertDanger()
          }
      })
    }
});

$(document).on('click', '#report', (e)=>{
  if(authenticated == "False"){
    window.location.href = login
  } else if(email_verified == "False") {
    window.location.href = verify_email
  } else {
    $.ajax({
      type: "POST",
      url: report,
      data: {
        csrfmiddlewaretoken: csrfToken,
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

var page = 2;
$('#more').click(()=>{
  $.ajax({
    method: "GET",
    url: reviews,
    data: {
      page: page
    },
    success: (response)=>{
      page += 1;
      $.each(response.reviews, (index, obj)=> {
        if(obj["user"]["id"]==user){
          var action = `<form action="/delete-product-review/${obj["id"]}/" method="POST">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                            <input type="submit" value="Delete" class="list-group-item list-group-item-action p-2">
                        </form>`
        } else {
          var action = `<li id="report-review" data-review="${obj["id"]}" class="list-group-item list-group-item-action p-2">Report</li>`
        }
        $('.reviews-div').append(`
          <article class="rating-card p-2 pb-3 bg-white border-bottom d-flex">
            <img class="mr-3 lazy rounded-circle" src="${placeholder}" data-src="${obj["user"]["image"]}">
            <div>
                <p class="text-muted overflow-hidden">${obj["user"]["name"]} · ${obj["date"]}</p>
                <div class="ratings">
                    <div class="empty-stars"></div>
                    <div class="full-stars" style="width: calc(${obj["rating"]}/5*100%)"></div>
                </div>
                <p class="mt-1 incomplete-card in-paragraph">${obj["content"]}</p>
            </div>
            <span tabindex="1" class="side-ellipsis option-icon p-2 text-muted position-absolute">
                <span class="icon-ellipsis-v"></span>
                <div class="options position-absolute shadow pointer" id="delete-product">
                    ${action}
                </div>
            </span>
          </article>
        `)
      });
      if(response.has_next == false || response==""){
        $('#more').hide();
      }
      for(var index=0;index < lazy.length;index++){
        lazyLoad(lazy[index]);
      }
    },
    error: ()=>{
      alertDanger()
    }
  })
});