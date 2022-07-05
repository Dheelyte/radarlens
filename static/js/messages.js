function alertDanger(){
  $('.danger').html(`Something went wrong`);
  $('.danger').show();
  $('.danger').delay(5000).fadeOut(300);
};

function urlify(text){
  var urlRegex = /((http(s)?(\:\/\/))?(www\.)?([\a-zA-Z0-9-_\.\/])*(\.[a-zA-Z]{2,3}\/?))([\a-zA-Z0-9-_\/?=&#])*(?!(.*a>)|(\'|\"))/g;
  return text.replace(urlRegex, function(url){
    return '<a href="'+url+'">'+url+'</a>'
  })
}

let div = document.getElementById('messages');
if(div){
    let more = document.getElementById('more-div');
    if(div.childElementCount < 15){
        more.style.display = "none"
    }
};

var chats_page = 2;
$('#more').click(()=>{
  $('#more-div').hide();
  $('#loading-div').show();
  $.ajax({
    method: "GET",
    url: messages,
    data: {
      page: chats_page
    },
    success: (response)=>{
      page += 1;
      $.each(response.chats, (index, chat)=>{
        var last_message = chat.last_message;
        var last_message_timestamp = chat.last_message_timestamp;
        if(chat.sender == user){
          var chat_slug = chat.receiver;
          var chat_image = chat.receiver_image;
          var chat_name = chat.receiver_name;
        } else {
          var chat_slug = chat.sender;
          var chat_image = chat.sender_image;
          var chat_name = chat.sender_name;
        }
        if(chat.last_message_sender != user){
          if(!chat.last_message_seen){
            var last_message_seen = `<span class="icon-circle unread" style="right: 20px; top: 50px;"></span>`;
          } else {
            var last_message_seen = ``;
          }
        }
        $('#messages').append(`
          <div class="message-list pointer d-flex position-relative p-3 bg-white border-bottom" call="${webRoot}/messages/${chat_slug}/">
            <img class="mr-3 rounded-circle" style="width: 50px; height: 50px;" src="${chat_image}" alt="">
            <div class="d-block">
              <p class="font-weight-bold overflow">${chat_name}</p>
              <p class="text-muted pr-3 overflow">${last_message}</p>
            </div>
            <div class="d-block">
              <p class="text-muted position-absolute" style="right:5px; top: 10px;">${last_message_timestamp}</p>
              ${last_message_seen}
            </div>
          </div>
        `)
        $('#loading-div').hide();
        $('#more-div').show();
        if(response.has_next == false || response == ""){
          $('#more-div').hide();
        }
      })
    }
  })
})


var call;
var page = 2;
$(document).on('click', '#previous-messages', (e)=>{
  let slug = call.split('/').filter(e => e).pop();
  $.ajax({
    type: "GET",
    url: `/previous-messages/${slug}/`,
    data: {
      page: page
    },
    success: (response)=>{
      page += 1;
      if (!response.has_next) {
        $(e.target).hide()
      };
      $.each(response.messages, (index, message)=>{
        if (message.sent) {
          let sent = document.createElement('li');
          sent.classList.add('sent');
          sent.innerHTML = `
            <p>
              <span class="msg-content">${message.message}</span>
              <span class="mt-1 sent-time">${message.timestamp}</span>
            </p>`
          $('#messages-area ul').prepend(sent)
          sent.querySelector('.msg-content').innerHTML = urlify(sent.querySelector('.msg-content').innerHTML)
        } else {
          let reply = document.createElement('li');
          reply.classList.add('reply');
          reply.innerHTML = `
            <p>
              <span class="msg-content">${message.message}</span>
              <span class="text-muted mt-1">${message.timestamp}</span>
            </p>`
          $('#messages-area ul').prepend(reply)
          reply.querySelector('.msg-content').innerHTML = urlify(reply.querySelector('.msg-content').innerHTML)
        }
      })
    },
    error: ()=>{
      alertDanger()
    }
  })
});

$(document).on('click', '.message-list', function (e) {
  if(email_verified == "False") {
      window.location.href = verify_email
  } else {
    $('#main').addClass('main-margin');
    $(e.currentTarget).find('.unread').hide();
    $('#messages-area').empty();
    $('#spinner').removeClass('d-none').addClass('d-flex');
    $('.message-info').empty();
    $('#main-div').hide();
    $('#main-2').show();
    $('#header-user').empty();
    call = $(this).attr('call');
    window.history.pushState(call, "", null);
    $.ajax({
      type: "GET",
      url: call,
      success: function (response) {
        $('#header-user').html(`
          <img src="${webRoot}${response["other_user"]["image"]}" width="40px" alt="profile picture" style="border-radius: 50px;">
          <span><h6 class="mt-2 ml-2">${response["other_user"]["name"]}</h6></span>
        `);
        document.title = response["other_user"]["name"];
        $('#messages-area').append(`<ul></ul>`);
        $('#spinner').removeClass('d-flex').addClass('d-none');
        $.each(response.messages, function(index, message) {
          if (message.sent) {
            $('#messages-area ul').append(`
              <li class="sent">
                <p>
                  <span class="msg-content">${message.message}</span>
                  <span class="mt-1 sent-time">${message.timestamp}</span>
                </p>
              </li>
            `);
          } else {
            $('#messages-area ul').append(`
              <li class="reply">
                <p>
                  <span class="msg-content">${message.message}</span>
                  <span class="text-muted mt-1">${message.timestamp}</span>
                </p>
              </li>
            `)
            $('#messages-area .msg-content').each(function(){
              this.innerHTML = urlify(this.innerHTML)
            })
          }
        });
        $('#messages-area ul').append(`
          <li class="mb-1 mt-0" id="seen" style="display: inline-block">
            <p style="display: inline-block; float: right" class="p-0 text-muted">${response["seen"]}</p>
          </li>
        `)
        if(document.querySelector('#messages-area ul').childElementCount > 20){
          $('.message-info').append(`
              <button id="previous-messages" class="p-2 rounded-pill btn"><i class="fas fa-arrow-up"></i> Previous messages</button>
          `)
        };
        window.scroll(0, document.documentElement.scrollHeight);
        setInterval(load_messages, 10000);
        $('#messages-area ul li p .msg-content').each(function(e){
          this.innerHTML = urlify(this.innerHTML)
        })
      },
      error: function () {
        alertDanger()
        }
    })
  }
});

let message_send_btn = document.getElementById("send-btn");
let content_editable = document.getElementById("content_editable");
function send_message() {
  content_editable.focus();
  let slug = call.split('/').filter(e => e).pop();
  let message = content_editable.innerText;
  if (message === "") {
    return;
  };
  $.ajax({
    url: `${webRoot}/ajax/message/${slug}/`,
    method: "POST",
    data: {
      message: message,
      csrfmiddlewaretoken: csrf_token
    },
    success:(messages) =>{
      for (message of messages) {
        construct_message(message);
      };
      content_editable.innerText = ""
      $('#seen').hide();
    }
  })
};

function load_messages(){
  if (call==null){
    return;
  } else {
    let slug = call.split('/').filter(e => e).pop();
    fetch(`${webRoot}/ajax/message/${slug}/`)
    .then(e => e.json())
    .then(messages => {
      for (message of messages) {
        construct_message(message);
      }
    })
  }
};

function construct_message(message) {
  let messages_container = document.querySelector("#messages-area ul");
  let class_name = "reply";
  if (message.sent) {
    class_name = "sent"
  }
  let div = document.createElement("div");
  div.innerHTML = `
    <li class="${class_name}">
      <p>
        <span class="msg-content">${message.message}</span>
        <span class="mt-1 sent-time">${message.timestamp}</span>
      </p>
    </li>
  `;
  messages_container.appendChild(div);
  div.scrollIntoView();
  div.querySelector('.msg-content').innerHTML = urlify(div.querySelector('.msg-content').innerHTML)
};

message_send_btn.addEventListener('click', send_message);

window.addEventListener('popstate', function(e) {
  e.preventDefault();
  if (e.state == null) {
    $('#main-2').hide();
    $('#main-div').show();
    call = null;
  } else {
    call = e.state;
    $('#main-div').hide();
    $('#main-2').show();
  }
});
  
$('#header-back-button').on('click', ()=>{
  window.history.back()
});
