window.scroll(0, document.documentElement.scrollHeight);
if(document.querySelector('#messages-area ul').childElementCount < 20){
  $('#previous-messages').hide()
};

let message_send_btn = document.getElementById("send-btn");
let content_editable = document.getElementById("content_editable");

const urlParams = new URLSearchParams(window.location.search)
const text = urlParams.get('text')
content_editable.innerText = text

function urlify(textn){
  var urlRegex = /(https?:\/\/[^\s]+)/g;
  return textn.replace(urlRegex, function(url){
    return `<a href="${url}">${url}</a>`
  })
}
$('#messages-area ul li p .msg-content').each(function(){
  this.innerHTML = urlify(this.innerHTML)
})

function alertDanger(){
  $('.danger').html(`Something went wrong`);
  $('.danger').show();
  $('.danger').delay(5000).fadeOut(300);
};

var page = 2;
$(document).on('click', '#previous-messages', (e)=>{
  let slug = otherUser;
  $.ajax({
    type: "GET",
    url: `/previous-messages/${slug}/`,
    data: {
      page: page
    },
    success: (response)=>{
      page += 1
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
                <span class="mt-1">${message.timestamp}</span>
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


function send_message() {
  let message = content_editable.innerText;
  if (message === "") {
    return;
  };
  let slug = otherUser;
  content_editable.focus();
  $.ajax({
    url: `${webRoot}/ajax/message/${slug}/`,
    method: "POST",
    data: {
      message: message,
      csrfmiddlewaretoken: csrfToken
    },
    success:(messages) =>{
      for (message of messages) {
        construct_message(message);
      }
      content_editable.innerText = "";
      $('#seen').hide();
    },
    error:()=>{
      $('.danger').html(`Something went wrong`);
      $('.danger').show();
      $('.danger').delay(2000).fadeOut(300);
    }
  })
};

function load_messages(){
  let slug = otherUser;
  fetch(`${webRoot}/ajax/message/${slug}/`)
  .then(e => e.json())
  .then(messages => {
    for (message of messages) {
      construct_message(message)
    }
  })
};

setInterval(load_messages, 10000);

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
        <span class="mt-1">${message.timestamp}</span>
      </p>
    </li>`;
  messages_container.appendChild(div);
  div.scrollIntoView();
  div.querySelector('.msg-content').innerHTML = urlify(div.querySelector('.msg-content').innerHTML)
}

message_send_btn.addEventListener('click', send_message);

$('#header-back-button').on('click', ()=>{
  window.history.back()
});