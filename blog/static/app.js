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