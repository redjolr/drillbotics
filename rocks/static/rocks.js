


//Executed when an image is selected
$(function(){
   $("#pictureInput").change(function (){
     var fileName = $(this).val().split('\\').pop();
     var input = $(this)[0];
     var file = input.files[0];

     var reader = new FileReader();
     reader.onload = function(e){
       $('#loaded_picture').attr('src', e.target.result);
       $('#loaded_picture').css("display", "block")
       $('#imagePlaceHolder').css("display", "none")
     }
     reader.readAsDataURL(file);
   });
});




function submit_form()
{
  // alert($("#hidden_materials").val())
  //  materials_ids = []
  //  for(var i=0; i<selected_materials_register.length; i++)
  //  {
  //    materials_ids.push(selected_materials_register[i]['id'])
  //  }
  //  $("#hidden_materials").val(JSON.stringify(materials_ids));
   $("#rock_form").submit()
}
