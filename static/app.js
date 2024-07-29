document.addEventListener("DOMContentLoaded", function() {
  ClassicEditor
      .create(document.querySelector('#editor'))
      .catch(err => {
          console.error(err);
      });
});

let menu = document.querySelector('nav ul')
let hamburger = document.querySelector('nav .mobile')
hamburger.addEventListener('click', function(){
  menu.classList.toggle('show')
})


function HideShowReply(){
    let replies = document.getElementsByClassName('reply_comment');
    for (let i = 0; i < replies.length; i++) {
        replies[i].classList.toggle('hide');
    }
}