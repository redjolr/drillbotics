
$(document).ready(function(){  //Activate tooltips
    $('[data-toggle="tooltip"]').tooltip();
});



function edit_sensor_data()
{
  if($(".sensor_input").css("display")=="none"){
    $(".sensor_data").css("display", "none");
    $(".sensor_input").css("display", "inline" );
    $(".btn").css("display", "inline" );
  }
  else {
    $(".sensor_data").css("display", "inline");
    $(".sensor_input").css("display", "none" );
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
