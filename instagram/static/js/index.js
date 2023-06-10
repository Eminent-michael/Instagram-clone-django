/** @format */

$(document).ready(function () {
  const modal = $(".modal");
  slideIndex = 1;

  $(".showModal").on("click", function (e) {
    console.log("Showmodal clicked....  ");
    let url = this.dataset.story
    console.log("url:", url)
    $.ajax({
      type:'GET',
      url:url,
      dataType: 'json',
      
      success: function(data) {
        console.log("data:", data)
        $.each(data, function(i, v){
          console.log("v:", v)
          if (v.content.slice(v.content.length - 3) === 'mp4'){
            var div_slide_html = `<div class="mySlides fade"><video width="640" controls="controls" preload="metadata">
            <source src="/media/${v.content}#t=0.5" type="video/mp4">
            </video></div>`
          } else{
            var div_slide_html = `<div class="mySlides fade"><figure class="image is-4by3">
            <img src="/media/${v.content}" alt="Placeholder image">
            </figure></div>`
          }
          $('#jsondata').append(div_slide_html);
        })
      },

      complete: function() {
        showSlides(slideIndex);
      }
    })
    modal.addClass(" is-active");
  });

  $(".closeModal").on("click", function (e) {
    const slide = document.getElementById('jsondata');
    slide.innerHTML = ''
    modal.removeClass(" is-active");
  });
});

/** @format */

// showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides((slideIndex += n));
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides((slideIndex = n));
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  if (n > slides.length) {
    slideIndex = 1;
  }
  if (n < 1) {
    slideIndex = slides.length;
  }
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  slides[slideIndex - 1].style.display = "block";
}
