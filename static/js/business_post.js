function alertDanger(){
    $('.danger').html(`Something went wrong`);
    $('.danger').show();
    $('.danger').delay(5000).fadeOut(300);
};

$(document).on('click', '.like-post', (e)=>{
    if(authenticated == "False"){
        window.location.href = login;
    } else if(email_verified == "False") {
        window.location.href = email_verify_url;
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

$(document).on('click', '#report-comment', (e)=>{
    if(authenticated == "False"){
        window.location.href = login;
    } else if(email_verified == "False") {
        window.location.href = verify_email;
    } else {
        let comment = $(e.currentTarget).data('comment');
        $.ajax({
            type: "POST",
            url: reportComment,
            data: {
                csrfmiddlewaretoken: csrfToken,
                comment: comment
            },
            success: (response)=>{
                $(e.currentTarget).find('#report-comment').hide();
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

$(document).on('click', '#report-post', (e)=>{
    if(authenticated == "False"){
        window.location.href = login;
    } else if(email_verified == "False") {
        window.location.href = verify_email;
    } else {
        let post = $(e.currentTarget).data('post');
        $.ajax({
            type: "POST",
            url: reportPost,
            data: {
                csrfmiddlewaretoken: csrfToken,
                post: post
            },
            success: (response)=>{
                $(e.currentTarget).hide()
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

$(document).on('click', '.side-ellipsis', (e)=>{
    $(e.currentTarget).find('.options').toggle();
})

var page = 2;
$('#more').click(()=>{
  $('#more-div').hide();
  $('#loading-div').show();
  $.ajax({
    method: "GET",
    url: comments,
    data: {
      page: page
    },
    success: (response)=>{
      page += 1;
      $.each(response.comments, (index, comment)=>{
        var action;
        if(user != comment.user.id && user != comment.post.user){
          action = `<li id="report-comment" class="list-group-item list-group-item-action p-2" data-comment="${comment["id"]}">Report</li>`
        } else if(user == comment.user.id && user == comment.post.user) {
          action = `<form action="/delete-comment/${comment["id"]}/" method="POST">
                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                        <input type="submit" value="Delete" class="list-group-item list-group-item-action p-2">
                    </form>`
        } else if(user != comment.user.id && user == comment.post.user){
            action = `<li id="report-comment" class="list-group-item list-group-item-action p-2" data-comment="${comment["id"]}">Report</li>
                    <form action="/delete-comment/${comment["id"]}/" method="POST">
                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                        <input type="submit" value="Delete" class="list-group-item list-group-item-action p-2">
                    </form>`
        } else if(user == comment.user.id && user != comment.post.user){
            action = `<form action="/delete-comment/${comment["id"]}/" method="POST">
                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                        <input type="submit" value="Delete" class="list-group-item list-group-item-action p-2">
                    </form>`
        };
        $('.comments-div').append(`
            <article class="bg-white p-2 border-bottom position-relative">
                <div class="d-flex mb-2">
                    <img src="${comment["user"]["image"]}" style="width: 50px; height: 50px; border-radius: 50px;" alt="${comment["user"]["name"]}">
                    <div>
                        <p class="text-muted ml-2">${comment["user"]["name"]} · ${comment["date"]}</p>
                        <p class="ml-2">${comment["content"]}</p>
                    </div>
                    <span tabindex="1" class="side-ellipsis option-icon pointer p-2 text-muted position-absolute">
                        <i class="icon-ellipsis-v"></i>
                        <div class="options position-absolute">
                            ${action}
                        </div>
                    </span>
                </div>
            </article>
        `);
      });
      $('#loading-div').hide();
      $('#more-div').show();
      if(response.has_next == false || response==""){
        $('#more-div').hide();
      }
    }
  })
})
function submitComment(){
    document.getElementById("id_content").value = document.getElementById("content_editable").innerText;
}