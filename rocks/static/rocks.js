
selected_materials_register = []

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



function  choose_materials()
{
  $("#form_container").css("filter", "blur(0.8px)");
  $("#header").css("filter", "blur(0.8px)");
  $("#materials_container").css("display", "block");
  $("#submit_btn").attr("disabled", "disabled")
  materials = selected_materials_register;
  $("#selected_materials").empty();

  for(var i=0; i<selected_materials_register.length; i++)
  {
    $("<div id='material"+materials[i]['id']+"' database_id='"+materials[i]['id']+"' class='materials_available list-group-item' onclick='move_material(this)' >"+
          materials[i]['name']+
      "</div>").appendTo($('#selected_materials'));
  }
  get_all_materials()

}

function get_all_materials()
{
  var url = "/rocks/getmaterials";
  $("#materials_list").empty();

  $.get(url, function(data, status){
      var materials = JSON.parse(data);
      for(var i=0; i<materials.length; i++)
      {
        material_is_selected = false;
        for (var j=0; j<selected_materials_register.length; j++)
          if(selected_materials_register[j]['name']==materials[i]['name'])
            material_is_selected = true;

        if(!material_is_selected)
          $("<div id='material"+materials[i]['id']+"' database_id='"+materials[i]['id']+"' class='materials_available list-group-item' onclick='move_material(this)' >"+
                materials[i]['name']+
            "</div>").appendTo($('#materials_list'));
      }
  });
}

$(function(){
  $("#new_material_input").on('keyup', function (e) {
      if (e.keyCode == 13) {
          $("#new_material_btn").click();
      }
  });
});
function add_new_material_btn()
{
  new_material = $("#new_material_input").val();
  materials = $(".materials_available");
  material_exists = false;
  for(var i=0; i<materials.length; i++)
  {
    name_lowercase = $(materials[i]).text().toLowerCase();
    if(name_lowercase== new_material.toLowerCase())
      material_exists = true;
  }

  if(material_exists)
    alert("Material already exists")
  else
    $("<div class='new_materials list-group-item py-1'  >"+
          "<span>"+new_material+"</span><span class='oi oi-circle-x new_material_oi-x' onclick='remove_new_material(this)'></span>"+
      "</div>").appendTo($('#new_materials_list'));
  $("#new_material_input").val("")
}

function remove_new_material(material)
{
  $(material).parent().remove();
}


function save_materials_to_db()
{
  var url = "/rocks/materials/add";
  materials = $(".new_materials");
  if(materials.length==0){
    return;
  }

  material_names = []
  for(var i=0; i<materials.length; i++){
    material_names.push($(materials[i]).text())
  }
  materials_json = JSON.stringify(material_names);

  jQuery.ajax({
    type: 'POST',
    url: url,
    data: { 'csrfmiddlewaretoken': csrf_token, 'materials': materials_json },
    dataType: 'json',
    success: function(data) {

      get_all_materials()
      $("#new_materials_list").empty();
      $('#materials_added_check' ).animate({
        opacity: 1
      }, 200);
      $('#materials_added_check' ).animate({
        opacity: 0
      }, 2500);
    }
  });
}


function move_material(material)
{
  if($("#materials_list").has($(material)).length ) //Material has  not been selected
  {
    $(material).appendTo($("#selected_materials"));
    selected_materials_register.push({ 'id': $(material).attr('database_id')  ,'name':$(material).text()})
  }
  else if( $("#selected_materials").has($(material)).length  ) //Material has already been selected selected
  {
    $("#materials_list").prepend($(material));
    selected_materials_register.splice(selected_materials_register.indexOf($(material).text()),1);
  }


}

function search_material(search_field)
{
  materials = $(".materials_available");
  search_str = search_field.value.toLowerCase();
  for(var i=0; i<materials.length; i++)
  {
    name_lowercase = $(materials[i]).text().toLowerCase();
    if(name_lowercase.search(search_str)>=0)
      $(materials[i]).css("display", "block");
    else
      $(materials[i]).css("display", "none");
  }
}

function choose_selected_materials()
{
  materials = $("#selected_materials").find(".materials_available")
  materials_str = ""
  for(var i=0; i<materials.length; i++)
  {
     materials_str += $(materials[i]).text()+","
  }
  $("#materials").val(materials_str.slice(0,-1))
  $("#form_container").css("filter", "blur(0px)");
  $("#header").css("filter", "blur(0px)");
  $("#materials_container").css("display", "none");
  $("#submit_btn").removeAttr("disabled");
}

function close_materials_window()
{
  $("#materials_container").css('display', 'none');
  $("#form_container").css("filter", "blur(0px)");
  $("#header").css("filter", "blur(0px)");
  $("#materials_container").css("display", "none");
  $("#submit_btn").removeAttr("disabled");

  var materials_input = $("#materials").val().split(",");


  selected_materials = $("#selected_materials").find(".materials_available")
  for(var i=selected_materials.length-1; i>=0; i--)
  {

    if( materials_input.indexOf($(selected_materials[i]).text())==-1  ) //-1 is returned when element is not in array
    {
      selected_materials_register.splice(selected_materials_register.indexOf($(selected_materials[i]).text()),1);

    }
  }



}


function submit_form()
{
   materials_ids = []
   for(var i=0; i<selected_materials_register.length; i++)
   {
     materials_ids.push(selected_materials_register[i]['id'])
   }
   $("#hidden_materials").val(JSON.stringify(materials_ids));
   alert( $("#hidden_materials").val())
   $("#rock_form").submit()
}
