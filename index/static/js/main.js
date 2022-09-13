$(document).ready(function(){

  $('#comment_btn').click(function(){
       $('#comment_btn').css('display','none');
       $('.Comment_content').slideToggle(1000)
  });

  $('#learn_more').click(function(){
       $('#learn_detail').css('display','block');
       $('#learn_hide').css('display','block');
       $('#learn_more').css('display','none');
  });

   $('#learn_hide').click(function(){
       $('#learn_detail').css('display','none');
       $('#learn_hide').css('display','none');
       $('#learn_more').css('display','block');
  });

  
	$('#search_btn').click(function(){
		$('#search_menu').slideToggle(1000);
	});

  $('#Dicription_btn').click(function(){
    $('#Dicription').toggle(1000)
    $('#Related').toggle(1000)
    $('#Review').toggle(1000)
  });

   $('#Related_btn').click(function(){
    $('#Dicription').toggle(1000);
    $('#Related').toggle(1000);
    $('#Review').toggle(1000);
  });

    $('#Review_btn').click(function(){
    $('#Dicription').toggle(1000);
    $('#Related').toggle(1000);
    $('#Review').toggle(1000);
  });


$('#Unsubscribe_btn').click(function(){
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    var email = document.getElementById('Subscribe_email').value
    var this_form = document.getElementById('Subscribe-form');
    var url = "/unsubscribe/"

    if(email.match(mailformat)){
        $.ajax({
        type  : "GET",
        url   : url,
        data  :{'email':email , 'csrfmiddlewaretoken': '{{ csrf_token }}'},

        

        success : function(data){
            this_form.reset();
            if(data['data']=="true"){
              $('#subscr_info').html('<p style="color:green;"><strong>unsubscribing complete</strong></p>');  
          }else{
            $('#subscr_info').html('<p style="color:red;"><strong>You did not subscribed</strong></p>');
          }
            
        },
        error :function(error){
            $('#subscr_info').html('<p style="color:red;"><strong>Sorry!!,Something is wrong</strong></p>');
        }
    })
    }else{
       $('#subscr_info').html('<p style="color:red;"><strong>Your email is not valid</strong></p>'); 
    }
    
    
  });
//__________________________________________________________________
$('#Subscribe_btn').click(function(){
    
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    var email = document.getElementById('Subscribe_email').value;
    var this_form = document.getElementById('Subscribe-form');
    var url = "/Subscribe"

    if(email.match(mailformat)){
        $.ajax({
        type  : "GET",
        url   : url,
        data  :{'email':email , 'csrfmiddlewaretoken': '{{ csrf_token }}'},

        

        success : function(data){
            this_form.reset();
            if(data['data']=="true"){
              $('#subscr_info').html('<p style="color:green;">Thank you for subscribing</p>');  
            }else{
              $('#subscr_info').html('<p style="color:red;">You have already subscribed</p>');  
            }
            
            
        },
        error :function(error){
            $('#subscr_info').html('<p style="color:red;">Sorry!!,Something is wrong</p>');
        }
    })
    }else{
      $('#subscr_info').html('<p style="color:red;">Your email is not valid</p>');  
    }
 });



})

function Quick_btn(args){
  var id = '#' + args;
  $(id).css('display','block');
}
function Quick_btn2(args){
  var id = '#' + args;
  $(id).css('display','none');
}
function displaynav(){
  $('#nav_menu').toggle(500);
}
function hidenav(){
  $('#nav_menu').hide(500);
}
function display_category(){
  $('#main_category').show(1000);
  $('#hide_category').show(3000);
  $('#display_category').hide(3000);
}
function hide_category(){
  $('#main_category').hide(1000);
  $('#hide_category').hide(3000);
  $('#display_category').show(3000);

}


function music_manager(args){
  var id = '#ikmusic_' + args;
  $(id).show();
}
function music_manager2(args){
  var id = '#ikmusic_' + args;
  $(id).hide();
}


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

function hide_alert(){
  $('#outer_complete_msg').hide();
}

function disply_music_button(args){
  var id = "#music_detail_button" + args;
  $(id).toggle();
}
function display_pass(args){
  var id = '#pass_' + args;
  var id2 = '#pass2_' + args;
  $(id).css('display','block');
  $(id2).css('display','none');
}
function hide_pass(args){
  var id = '#pass_' + args;
  var id2 = '#pass2_' + args;
  $(id2).css('display','block');
  $(id).css('display','none');
}
function display_payment_info(args){
  var id = '#pyt_' + args;
  $(id).toggle(1000);
}

function display_oder_place_detail(args){
    var id = '.place_order_' + args;
    $(id).toggle(1000);

}

function place_order(){
    $('#order_btn_img').css('height','74');
}
function place_order2(){
    $('#order_btn_img').css('height','64');
}

function display_place_order_form(){
   $('#place_order_popup').slideToggle(1000);
}


function display_alert_msg_area(){

    $('#alert_msg_nofication').toggle(1000);
       
   }
function diisplay_popup_advert_ajax(){
     $.ajax({
        type  : "GET",
        url   : window.location.pathname,
        data  : {'pops':"popups", 'csrfmiddlewaretoken': '{{ csrf_token }}'},
        

        success : function(response){
            //alert(response['data'])
            $("#diisplay_popup_advert_ajax").html(response['data'])
            $('#alert_msg_nofication').toggle(1000);              
        },
        error :function(error){
            main_error();
        }
    })
}
var time = setInterval(diisplay_popup_advert_ajax,15000);