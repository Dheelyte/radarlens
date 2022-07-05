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

let div = document.getElementById('products');
if(div){
    let more = document.getElementById('more-div');
    if(div.childElementCount < 15){
        more.style.display = "none"
    }
};

$('#see-more').on('click', (e)=>{
  $('.business-description p').toggleClass('incomplete');
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

var page = 2;
$('#more').click(()=>{
  $('#more-div').hide();
  $('#loading-div').show();
  $.ajax({
    method: "GET",
    url: products,
    data: {
      page: page
    },
    success: (response)=>{
      page += 1;
      $.each(response.products, (index, obj)=>{
        var price = ``;
        if(obj["price"] != null){
          price = `<p class="text-muted m-0">${obj["currency"]} ${obj["price"]}</p>`;
        };
        $('.products').append(`
          <div class="card home-product-card mb-1 shadow-sm">
            <div class="product-image-div position-relative">
              <img class="lazy position-absolute" src="${ph}" data-src="${obj["image"]}" role="img">
            </div>
            <div class="card-body">
              <p class="card-text">${obj["name"]}</p>
              <div class="ratings">
                <div class="empty-stars"></div>
                <div class="full-stars" style="width: calc(${obj["rating"]}/5*100%)"></div>
              </div>
              ${price}
              <a href="/product/${obj["slug"]}/" class="stretched-link"></a>
            </div>
            <div class="pl-2 pr-2 pb-2 pt-0" style="z-index: 1;">
              <button class="save not-saved btn shadow-none" data-save="/save-product/${obj["slug"]}/">Save For Later</button>
            </div>
          </div>
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

$(document).on('click', '.save', (e)=>{
  if("{{ request.user.is_authenticated }}" == "False"){
      window.location.href = "{% url 'login' %}"
  } else if("{{ request.user.email_is_verified }}" == "False") {
      window.location.href = "{% url 'verify-email' %}"
  } else {
    const save = $(e.currentTarget)
    if (save.html === 'Saved') {
      save.html('Save For Later');
    } else {
      save.html('Saved');
    };
    $.ajax({
        method: 'POST',
        url: save.data('save'),
        data:{
            csrfmiddlewaretoken: csrfToken,
        },
        success: (response)=>{
          if(response === "saved"){
            save.html('Saved');
            save.removeClass('not-saved').addClass('saved')
            $('.success').html('Product Saved');
            $('.success').show();
            $('.success').delay(5000).fadeOut(300);
          } else{
            save.html('Save For Later');
            save.removeClass('saved').addClass('not-saved')
          }
        },
        error: ()=>{
          alertDanger()
        }
    })
  }
});