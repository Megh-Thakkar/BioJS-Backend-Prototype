
// JS for Desktops and large screens
if($(window).width() >= 992){

 // console.log($("#back-btn"))
// console.log("big js");



  /*Animating the form*/
var scrollCheck = 0;
var index = 0;  
var topPadding = -100;
var fields,wrapper;
var halfHeight = $(window).height()/2;

// To make a field active
function changeActiveField(index){
  $('.active').removeClass('active');
  var activeField = $('.field:eq(' + index + ')')
  // console.log(activeField, "change")
  activeField.addClass('active'); 
  activeField.find('input').focus();
  // console.log("changeActiveField")
}


// To scroll to a particular field 
function scrollToActiveField(field){  
  // console.log($(field),$(field).index() )
  var newIndex = $(field).index() - 1;
  // console.log(newIndex)
  if(newIndex != index){
    index = newIndex;
    var offset = $(field).offset().top;
    var screen  = $('html,body');
    // screen.animate({scrollTop: screen.scrollTop() + offset - halfHeight + topPadding}, 300)
    screen.animate({scrollTop: $(field).offset().top + $(field).height()/2 - $(window).height()/2}, 300)
    // console.log("scrollToActiveField")
    scrollCheck = 0;
    // changeActiveField(index);
  }
}

$(document).ready(function(){
   $("#back-btn").css('display', "none");
// console.log($('#select_info'));
$('#select_info').text('(Press Ctrl+ ( command on mac ) to add more than one event)');
// $.ajax({
//   method:"GET",
//   url:""
// }).done(function(data){
//     $.each(data.events,function(index,val){
//       $option = $("<option>",{value:val});
//       $option.appendTo($('#event-select'));
//     })
// })
fields = $('.field');
wrapper = $('.wrapper');
  
  $('#event-select-btn').click(function(){
    var val = $('#event-select').val();
    var text = $('#event-select').text()
    $box = $('#events-box');
    $div = $("<div>",{value:val}).addClass('event')
    $p = $("<p>").text(text);
    $innerDiv = $("<div>",{id:"minus-btn"});
    $img = $("<img>",{src:"minus.svg"});
    $p.appendTo($div);
    $img.appendTo($innerDiv);    
    $innerDiv.appendTo($div);
    $div.appendTo($('.events-box'));
    $innerDiv.click(function(e){
    // console.log("taneja madar chod")
    $(this).parent().remove();  
  })
  })


  //Toggle on scrolling
  $(window).scroll(function(e){
    if(scrollCheck == 0)
    {
      var scroll = $(window).scrollTop();
      for(var i = 0;i < fields.length;i++)
      {
        // if(i == fields.length - 1)
        // {
        //   // console.log($(fields[i]).offset().top) 
        //   if (scroll >= $(fields[i]).offset().top + topPadding) 
        //   {
        //       index = i;
        //       changeActiveField(index);
        //       continue;
        //   }
        // }
        // else{
          // if((scroll >= $(fields[i]).offset().top - halfHeight + topPadding) && (scroll <= $(fields[i+1]).offset().top - halfHeight+topPadding))
          if((scroll + halfHeight > $(fields[i]).offset().top ) && (scroll + halfHeight < $(fields[i]).offset().top + $(fields[i]).height()))
          { 
              index = i;
              changeActiveField(index);
          }
        // }
      }
    }
  })

  // To move to a particular field on focusing on an input
    var inputs = $('.field input');

    inputs.focus(function(){
      // console.log("focuscallback")
      // console.log("inputs",this)
      scrollToActiveField($(this).parent().parent());
    });

    var target_labels = $('.field input[type=radio] + label');
    target_labels.focus(function(){
      // console.log("focuscallback")
      // console.log("labels ...",$(this).parent().parent())
      scrollToActiveField($(this).parent().parent());
    });

    var select = $('.field select');
    select.focus(function(){
      // console.log("focuscallback")
      // console.log("select ...",$(this).parent().parent())
      scrollToActiveField($(this).parent().parent());
    })

    // To move to next field on keydown or Enter
    var temp;
    inputs.keydown(function(event) {
      if ((event.keyCode === 13||event.keyCode === 40) && this.validity.valid) { 
         scrollCheck = 1;
         console.log("keydown")
          var newIndex = inputs.index(this) + 1;
          console.log(inputs.length)
          if (newIndex < inputs.length) {
              temp = inputs.eq(newIndex);
              console.log(temp)
              temp.focus();
          }
      }
      if(event.keyCode === 38){
          scrollCheck = 1;
          newIndex = inputs.index(this) - 1;
          if(newIndex >= 0){
            temp = inputs.eq(newIndex);
            temp.focus();
          }
      }
    });
    
    $('.field').click(function(){
      scrollCheck = 1;
      scrollToActiveField(this);
      console.log("click")
    })
    // To make the first field active
    changeActiveField(index);
$('#submit-button').click(function(){
    submitFormData(changeActiveField);
  })
})
}
// JS for small and mobile screens
if($(window).width() < 992){
$(document).ready(function(){
// console.log("small js");
var index = 0;
var fields = $('.field');

  $('#event-select-btn').click(function(){
    var val = $('#event-select').val();
    var text = $('#event-select').val();
    $box = $('#events-box');
    $div = $("<div>").addClass('event')
    $p = $("<p>").text(text);
    $innerDiv = $("<div>",{id:"minus-btn"});
    $img = $("<img>",{src:"minus.svg"});
    $p.appendTo($div);
    $img.appendTo($innerDiv);    
    $innerDiv.appendTo($div);
    $div.appendTo($('.events-box'));
    $innerDiv.click(function(e){
      console.log("taneja madar chod")
      $(this).parent().remove();  
    })
})
function changeActiveField(index){

      $('.active').css({"display":"none"});
      $('.active').removeClass('active');
      $(fields[index]).fadeIn(400);
      console.log($(fields[index]))
      $(fields[index]).addClass('active');
}
  fields = $('.field');
  fields.css("display","none");
  $('#next-btn').click(function(){    
    index++;
    if(index == fields.length - 1){
      $('#next-btn').css({"display":"none"});
      $('#submit-btn').css({"display":"block"});
    }
    changeActiveField(index);
  })

  var input = $('.field input');

  input.keydown(function(event){
    if(event.keyCode === 13) { 
      index++;
      if(index == fields.length - 1){
        $('#next-btn').css({"display":"none"});
        $('#submit-btn').css({"display":"block"});
      }
      changeActiveField(index);
    }
    })
  $('#back-btn').click(function(){
    if(index > 0){
    if(index == fields.length - 1){
      $('#next-btn').css({"display":"block"});
      $('#submit-btn').css({"display":"none"});
    }
    index--;
    changeActiveField(index);
  }
  })

  changeActiveField(index);

  $('#submit-btn').click(function(){
    submitFormData(changeActiveField);
  })
})
}
var disabled = false;

function submitFormData(func){
  if(!disabled){
    // console.log("form submitted!")
    var data = {}
    var inputs = $('input');
    var baseUrl = window.location.href;
    // $.each(inputs,function(index,key){
    //   data[key.name] = key.value;
    //   console.log(key)
    // })
    var flag = 0;
    $('#register-form').serializeArray().forEach(function(element, index) {
      console.log(element.value == "", element)
      if(element.name != "referral" && element.value == "" && !flag){
        flag = 1;
        showMsg('please fill the form', 3000);

        return func(index-1);
      }
      if(element.name!="states[]"){
        // if data[element.name] = ''
        data[element.name] = element.value;

      }
      else{
        if(data.events){
          data.events.push(element.value)
        }else{
          data.events = [element.value];
        }
      }
      
    }, this);
    if(flag)return;
    var n = $('input[name=phone]')[0].value;
    // console.log(n.match('\/d+\'));
    var r = new RegExp("^\d{10}$");
    // console.log("phone", n, (n.match(/^\d{10}$/)));
    var b = (n.match(/^\d{10}$/));
    
      // console.log(grecaptcha.getResponse())
      disabled = true;
      $('#submit-button').css('background', '#666');
      console.log(data);
      $.ajax({
        method:"POST",
        url:baseUrl,
        data:data,
      }).done(function(response){
        $('#submit-button').css('background', '#fc0c84');
        disabled = false;
        console.log(response);
        showMsg(response.message, 3000);
        if(response.status == 0){
          func(8);
          
        }
      });
    
  }
}

function showMsg(text, time){
  $('#resp_msg p').text(text);
      
      $('#resp_msg').fadeIn();
      setTimeout(function(){
        $('#resp_msg').fadeOut();
      }, time);
}

$(document).ready(function() {
  $('#event-select').select2({
    'placeholder': 'Search event name',
    width: "resolve",
  });
   $('#college').select2({
    'placeholder': 'Search college name',
    width: "resolve",
  });
});

console.clear();