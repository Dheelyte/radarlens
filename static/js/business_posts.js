function alertDanger(){
  $('.danger').html(`Something went wrong`);
  $('.danger').show();
  $('.danger').delay(5000).fadeOut(300);
};

$('#see-more').on('click', ()=>{
    $('.business-description p').toggleClass('incomplete')
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

$(document).on('click', '.like-post', (e)=>{
    if(authenticated == "False"){
        window.location.href = login
    } else if(email_verified == "False") {
        window.location.href = verify_email
    } else {
    let post = $(e.currentTarget).data('post');
    $.ajax({
      type: "POST",
      url: `/post/like/`,
      data: {
          csrfmiddlewaretoken: csrfToken,
          post: post
      },
      success: (response)=> {
        if (response == "liked") {
          $('span[data-post='+post+']').css('background-color', 'rgb(243, 213, 157)')
        } else {
          $('span[data-post='+post+']').css('background-color', '#e3dff0')
        }
      },
      error: ()=> {
        alertDanger()
      }
    })
  }
});

$(document).on('click', '.side-ellipsis', (e)=>{
  $(e.currentTarget).find('.options').toggle()
});

var page = 2;
$('#more').click(()=>{
  $('#more-div').hide();
  $('#loading-div').show();
  $.ajax({
    method: "GET",
    url: posts,
    data: {
      page: page
    },
    success: (response)=>{
      var action;
      page += 1;
      $.each(response.posts, (index, obj)=>{
        if(user != obj.business.user){
          action = `<li id="report" class="list-group-item list-group-item-action p-2" data-review="${obj["id"]}">Report</li>`
        } else {
          action = `<form action="delete-post/${obj["id"]}/" method="POST">
                      <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                      <input type="submit" value="Delete" class="list-group-item list-group-item-action p-2">
                  </form>`
        };
        let is_liked = "style='background-color : rgb(243, 213, 157)'";
        if (!obj["liked"]) {
          is_liked = ''           
        };
        $('.posts').append(`
          <article class="position-relative bg-white p-3 border-bottom rounded-bottom">
            <span class="side-ellipsis option-icon p-2 text-muted position-absolute">
              <i class="fas fa-ellipsis-v"></i>
              <div class="options position-absolute ">
                  ${action}
              </div>
            </span>
            <div class="d-flex mb-2">
                <a href="/${obj["business"]["slug"]}/" class="font-weight-bold mr-2">${obj["business"]["name"]}</a> · 
                <p class="text-muted ml-2">${obj["date"]}</p>
            </div>
            <p class="mb-3">${obj["content"]}</p>
            <div class="post-actions d-flex justify-content-between text-center">
                <span class="like-post p-2" ${is_liked} data-post="${obj["post"]}"><i class="far fa-thumbs-up"></i> Like</span>
                <a href="/${obj["business"]["slug"]}/post/${obj["post"]}/" class="stretched-link comment p-2"><i class="far fa-comment"></i> Comments</a>
            </div>
          </article>
        `);
      });
      $('#loading-div').hide();
      $('#more-div').show();
      if(response.has_next == false || response == ""){
        $('#more-div').hide();
      }
    }
  })
})