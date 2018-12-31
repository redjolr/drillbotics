$(document).ready(function(){  //Activate tooltips
    $('[data-toggle="tooltip"]').tooltip();
});

function edit_rock_data()
{
  if($(".rock_input").css("display")=="none"){
    $(".rock_data").css("display", "none");
    $(".rock_input").css("display", "inline" );
    $(".btn").css("display", "inline" );
  }
  else {
    $(".rock_data").css("display", "inline");
    $(".rock_input").css("display", "none" );
    $(".btn").css("display", "none" );
  }

}

//Executed when an image is selected
$(function() {
   $("#picture_input").change(function (){
     var fileName = $(this).val().split('\\').pop();
     $("#upload_picture_label").text(fileName + " selected");
   });
});
