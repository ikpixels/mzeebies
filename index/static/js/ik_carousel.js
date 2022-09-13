 $(".vertical-center-3").slick({
        //infinite: true,
        rows:2,
        autoplay:true,
        slidesToShow:4,
        speed: 1000,
        slidesToScroll:4,
        arrows: true,
        nextArrow: '<i class="fa fa-arrow-right ik-next"></i>',
        prevArrow: '<i class="fa fa-arrow-left ik-prev"></i>',
        pauseOnFocus:true,
        //edgeFriction:4.5,
        //focusOnSelect:true,
        //centerPadding:'100px',
        //fade:true,
        //centerMode:true,
        //autoplaySpeed:1000,
    
        responsive: [
        {
            breakpoint: 1024,
            settings: {
                slidesToShow: 4,
                slidesToScroll: 4,
            }
        },
        {
            breakpoint: 600,
            settings: {
                slidesToShow: 3,
                slidesToScroll: 3
            }
        },
        {
            breakpoint: 480,
            settings: {
                rows:4,
                slidesToShow: 2,
                slidesToScroll:2
            }
        }

  ]
        
      });




       $(".Related").slick({
        //infinite: true,
        //rows:2,
        autoplay:true,
        slidesToShow:5,
        rows:2,
        slidesToScroll:5,
        nextArrow: '<i class="fa fa-arrow-right ik-next"></i>',
        prevArrow: '<i class="fa fa-arrow-left ik-prev"></i>',
        speed: 1000,
        arrows: true,
        pauseOnFocus:true,
        //edgeFriction:4.5,
        //focusOnSelect:true,
        //centerPadding:'100px',
        //fade:true,
        //centerMode:true,
        //autoplaySpeed:1000,
    
        responsive: [
        {
            breakpoint: 1024,
            settings: {
                slidesToShow:5,
                rows:2,
                slidesToScroll:5,
            }
        },
        {
            breakpoint: 600,
            settings: {
                slidesToShow: 3,
                rows:2,
                slidesToScroll: 3
            }
        },
        {
            breakpoint: 480,
            settings: {
                rows:2,
                slidesToShow: 2,
                slidesToScroll:2
            }
        }

  ]
        
      });



       $(".brand_ik").slick({
        //infinite: true,
        //rows:2,
        autoplay:true,
        slidesToShow:5,
        nextArrow: '<i class="fa fa-arrow-right ik-next"></i>',
        prevArrow: '<i class="fa fa-arrow-left ik-prev"></i>',
        speed: 1000,
        slidesToScroll:6,
        arrows: true,
        pauseOnFocus:true,
        //edgeFriction:4.5,
        //focusOnSelect:true,
        //centerPadding:'100px',
        //fade:true,
        //centerMode:true,
        //autoplaySpeed:1000,
    
        responsive: [
        {
            breakpoint: 1024,
            settings: {
                slidesToShow: 6,
                slidesToScroll:6,
            }
        },
        {
            breakpoint: 600,
            settings: {
                slidesToShow: 3,
                slidesToScroll:3
            }
        },
        {
            breakpoint: 480,
            settings: {
                slidesToShow: 2,
                slidesToScroll:2
            }
        }

  ]
        
      });



$("#slick_work").slick({
        infinite: true,
        dots: true,
        autoplay:true,
        //nextArrow: '<i class="fa fa-arrow-right ik-next"></i>',
        //prevArrow: '<i class="fa fa-arrow-left ik-prev"></i>',
        slidesToShow:4,
        speed: 1000,
        slidesToScroll:4,
        arrows: true,
        pauseOnFocus:true,
        responsive: [
        {
            breakpoint: 1024,
            settings: {
                slidesToShow:4,
                slidesToScroll:4,
            }
        },
        {
            breakpoint: 780,
            settings: {
                slidesToShow:3,
                slidesToScroll:3
            }
        },
        {
            breakpoint: 480,
            settings: {
                slidesToShow: 1,
                slidesToScroll: 1
            }
        }

  ]
       

        
      });

$('.multiple-items').slick({
  autoplay:true,
  infinite: true,
  slidesToShow:1,
  slidesToScroll:1,
  arrows: false,
  //prevArrow: '<div class="slick-prev"><i class="fa fa-angle-left" aria-hidden="true"></i></div>',
  //nextArrow: '<div class="slick-next"><i class="fa fa-angle-right" aria-hidden="true"></i></div>',
});

// On before slide change
$('.multiple-items').on('beforeChange', function(event, slick, currentSlide, nextSlide){
    var k = $('.isaac').attr('accesskey');
    var elt = slick.$slides.get(currentSlide);
    //$('.content').hide();
    $('.content[data-id=' + (currentSlide + 1) + ']').show();
})


$(document).ready(function(){
  $("#item_list").owlCarousel({
    loop:true,
    margin:100,
    items:4,
    autoplay:true,
    nav    : true,
    smartSpeed :900,
    navText :["<i class='fa fa-long-arrow-left'></i>", "<i class='fa fa-long-arrow-right'></i>"],
    responsive:{
        0:{
            items:2
        },
        600:{
            items:4
        },
        1000:{
            items:6,
            
        }
    }
  });
});


$(document).ready(function(){
  $("#item_list2").owlCarousel({
    loop:true,
    margin:100,
    items:4,
    autoplay:true,
    nav    : true,
    smartSpeed :900,
    navText :["<i class='fa fa-long-arrow-left'></i>", "<i class='fa fa-long-arrow-right'></i>"],
    responsive:{
        0:{
            items:1
        },
        600:{
            items:2
        },
        1000:{
            items:3,
            
        }
    }
  });
});

$(document).ready(function(){
  $("#item_list9").owlCarousel({
    loop:true,
    margin:100,
    items:4,
    autoplay:true,
    nav    : true,
    smartSpeed :900,
    navText :["<i class='fa fa-long-arrow-left'></i>", "<i class='fa fa-long-arrow-right'></i>"],
    responsive:{
        0:{
            items:2
        },
        600:{
            items:4
        },
        1000:{
            items:6,
            
        }
    }
  });
});


//Get the button
var mybutton = document.getElementById("scroll_up_btn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
$(document).ready(function(){
  $('#scroll_up_btn').click(function(){
       document.body.scrollTop = 0;
       document.documentElement.scrollTop = 0;
  })
})


$(".music_ik").slick({
        //infinite: true,
        //rows:2,
        autoplay:true,
        slidesToShow:4,
        nextArrow: '<i class="fa fa-arrow-right ik-next"></i>',
        prevArrow: '<i class="fa fa-arrow-left ik-prev"></i>',
        speed: 1000,
        slidesToScroll:6,
        arrows: true,
        pauseOnFocus:true,
        //edgeFriction:4.5,
        //focusOnSelect:true,
        //centerPadding:'100px',
        //fade:true,
        //centerMode:true,
        //autoplaySpeed:1000,
    
        responsive: [
        {
            breakpoint: 1024,
            settings: {
                slidesToShow: 4,
                slidesToScroll:4,
            }
        },
        {
            breakpoint: 600,
            settings: {
                slidesToShow: 3,
                slidesToScroll:3
            }
        },
        {
            breakpoint: 480,
            settings: {
                slidesToShow: 2,
                slidesToScroll:2
            }
        }

  ]
        
      });

       $(".music_ik").slick({
        //infinite: true,
        //rows:2,
        autoplay:true,
        slidesToShow:5,
        nextArrow: '<i class="fa fa-arrow-right ik-next"></i>',
        prevArrow: '<i class="fa fa-arrow-left ik-prev"></i>',
        speed: 1000,
        slidesToScroll:6,
        arrows: true,
        pauseOnFocus:true,
        //edgeFriction:4.5,
        //focusOnSelect:true,
        //centerPadding:'100px',
        //fade:true,
        //centerMode:true,
        //autoplaySpeed:1000,
    
        responsive: [
        {
            breakpoint: 1024,
            settings: {
                slidesToShow: 4,
                slidesToScroll:4,
            }
        },
        {
            breakpoint: 600,
            settings: {
                slidesToShow: 3,
                slidesToScroll:3
            }
        },
        {
            breakpoint: 480,
            settings: {
                slidesToShow: 2,
                slidesToScroll:2
            }
        }

  ]
        
      });