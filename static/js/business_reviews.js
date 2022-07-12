function alertDanger(){
  $('.danger').html(`Something went wrong`);
  $('.danger').show();
  $('.danger').delay(5000).fadeOut(300);
};

let div = document.getElementById('reviews');
if(div){
    let more = document.getElementById('more-div');
    if(div.childElementCount < 10){
        more.style.display = "none"
    }
};

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

for(var index=0;index < lazy.length;index++){
  lazyLoad(lazy[index]);
};

$(document).on('click', '#report', (e)=>{
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

$('#see-more').on('click', ()=>{
  $('.business-description p').toggleClass('incomplete')
});

$(document).on('click', '.rating-card', (e)=>{
  $(e.currentTarget).toggleClass('incomplete-card')
  $(e.currentTarget).toggleClass('complete-card')
})

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

$(document).on('click', '.side-ellipsis', (e)=>{
  $(e.currentTarget).find('.options').toggle()
});

var page = 2;
$('#more').click(()=>{
  $('#more-div').hide();
  $('#loading-div').show();
  $.ajax({
    method: "GET",
    url: reviews,
    data: {
      page: page
    },
    success: (response)=>{
      page += 1;
      $.each(response.reviews, (index, obj)=>{
        var action;
        if(obj.user.id == user){
          action = `<form action="/delete-business-review/${obj["id"]}/" method="POST">
                      <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                      <input type="submit" value="Delete" class="list-group-item list-group-item-action p-2">
                    </form>`
        } else {
          action = `<li id="report" class="list-group-item list-group-item-action p-2" data-review="${obj["id"]}">Report</li>`
        };
        $('.reviews-div').append(`
          <article class="rating-card overflow-hidden incomplete-card d-flex border-bottom position-relative p-2">
            <img class="mr-3 lazy" src="${ph}" data-src="${obj["user"]["image"]}">
            <div>
                <p class="text-muted">${obj["user"]["name"]} · ${obj["date"]}</p>
                <div class="ratings mt-0">
                    <div class="empty-stars"></div>
                    <div class="full-stars" style="width: calc(${obj["rating"]}/5*100%)"></div>
                </div>
                <p class="mt-1">${obj["content"]}</p>
            </div>
            <span tabindex="1" class="side-ellipsis option-icon p-2 text-muted position-absolute">
              <i class="fas fa-ellipsis-v"></i>
              <div class="options position-absolute ">
                  ${action}
              </div>
          </span>
          </article>
        `);
      });
      $('#loading-div').hide();
      $('#more-div').show();
      for(var index=0;index < lazy.length;index++){
        lazyLoad(lazy[index]);
      };
      if(response.has_next == false || response == ""){
        $('#more-div').hide();
      }
    }
  })
});

var hiddenrating = document.getElementById('hiddenrating');
$('.star').on('click', function(event){
    hiddenrating.value = event.target.id;
    $('#rating-textarea').show();
    $('#rating-textarea textarea').focus();
});

$('#1').on('mouseover click', ()=>{
  $('#1').html(`&#9733;`);
  $('#2, #3, #4, #5').html(`&#9734;`);
});
$('#2').on('mouseover click', ()=>{
  $('#1, #2').html(`&#9733;`);
  $('#3, #4, #5').html(`&#9734;`);
});
$('#3').on('mouseover click', ()=>{
  $('#1, #2, #3').html(`&#9733;`);
  $('#4, #5').html(`&#9734;`);
});
$('#4').on('mouseover click', ()=>{
  $('#1, #2, #3, #4').html(`&#9733;`);
  $('#5').html(`&#9734;`);
})
$('#5').on('mouseover click', ()=>{
  $('#1, #2, #3, #4, #5').html(`&#9733;`);
});

$("#business-rating-form").submit(function (e) {
  e.preventDefault();
  document.getElementById('submit-rating').disabled = true;
  $('#submit-rating').html('Posting...');
  var serializedData = $(this).serialize();
  $.ajax({
    type: 'POST',
    url: rate,
    data: serializedData,
    success: function () {
        $('.success').html(`You have successfully rated this business`);
        $('.rating-div').hide();
        $('.success').show();
        $('.success').delay(5000).fadeOut(300);
    },
    error: function () {
      alertDanger()
    }
  })
});