var selected_materials_register = []
var all_materials_register = []
var new_materials_register = []
var chosen_materials_register = []
var materials_input_text = $("#materials_textfield")
var materials_input_hidden = $("#hidden_materials")

materials_input_text.hover(function(){
  materials_input_text.css("cursor", "pointer");
});

$(function(){
  $("#new_material_input").on('keyup', function (e) {
      if (e.keyCode == 13) {
          $("#new_material_btn").click();
      }
  });
  load_materials_from_db()
});

//Populate all_materials_register
function load_materials_from_db()
{
    var url = "/rocks/getmaterials";
    $.get(url, function(data, status){
        all_materials_register = JSON.parse(data);
        for(var i=0; i<all_materials_register.length; i++)
          all_materials_register[i]['id'] = parseInt(all_materials_register[i]['id'])
        refresh_materials_list();
    });
}

function refresh_materials_list()
{
  $('#materials_list').empty();
  for(var i=0; i<all_materials_register.length; i++)
  {
    if( !material_in_array(all_materials_register[i], selected_materials_register) )
      $("<div id='material"+all_materials_register[i]['id']+"' database_id='"+all_materials_register[i]['id']+"' class='materials_available list-group-item' onclick='move_material(this)' >"+
            all_materials_register[i]['name']+
        "</div>").appendTo($('#materials_list'));
  }
}

function refresh_selected_materials()
{
  $("#selected_materials").empty();
  materials = selected_materials_register;
  for(var i=0; i<selected_materials_register.length; i++)
  {
    $("<div id='material"+materials[i]['id']+"' database_id='"+materials[i]['id']+"' class='materials_available list-group-item' onclick='move_material(this)' >"+
          materials[i]['name']+
      "</div>").appendTo($('#selected_materials'));
  }
}

function refresh_new_materials()
{
  $('#new_materials_list').empty()
  for(var i=0; i<new_materials_register.length; i++)
  {
    $("<div class='new_materials list-group-item py-1'  >"+
          "<span>"+new_materials_register[i]+"</span><span class='oi oi-circle-x new_material_oi-x' onclick='remove_new_material(this)'></span>"+
      "</div>").appendTo($('#new_materials_list'));
  }

}

function refresh_materials_input()
{
  materials_str = ""
  materials_ids = []
  for(var i=0; i<chosen_materials_register.length; i++)
  {
     materials_str += chosen_materials_register[i]["name"]+",";
     materials_ids.push(chosen_materials_register[i]["id"])
  }
  materials_input_text.val(materials_str.slice(0,-1))
  materials_input_hidden.val(JSON.stringify(materials_ids))
}

function open_materials_window()
{
  $("body> *").not("#materials_container").css("filter", "blur(0.8px)"); //Select every DOM element except materials window
  $("#materials_container").css("display", "block");
  $("#submit_btn").attr("disabled", "disabled")
   refresh_materials_list()
  // selected_materials_register = chosen_materials_register.splice();
  refresh_selected_materials()
}

function move_material(material_div)
{
  material_id = parseInt($(material_div).attr("database_id"));
  if(material_in_array(material_id, selected_materials_register)) //Remove from selected_materials_register
    remove_material_from_array(material_id, selected_materials_register);
  else if(!material_in_array(material_id,selected_materials_register)) //
    selected_materials_register.push({ 'id': material_id  ,'name':$(material_div).text()})
  refresh_materials_list()
  refresh_selected_materials()
}

function add_new_material()
{
  new_material = $("#new_material_input").val();
  if(material_in_array(new_material, all_materials_register))
    alert("Material already exists");
  else
    new_materials_register.push($("#new_material_input").val());
  $("#new_material_input").val("")
  refresh_new_materials()
}

function remove_new_material(material)
{
  material_name = $(material).parent().text();
  for(var i=0; i<new_materials_register.length; i++)
  {
    if(material_name==new_materials_register[i])
      new_materials_register.splice(i,1);
  }
  refresh_new_materials();
  alert(new_materials_register)
}

function save_materials_to_db()
{
  var url = "/rocks/materials/add";
  if(new_materials_register.length==0){
    return;
  }
  materials_json = JSON.stringify(new_materials_register);

  jQuery.ajax({
    type: 'POST',
    url: url,
    data: { 'csrfmiddlewaretoken': csrf_token, 'materials': materials_json },
    dataType: 'json',
    success: function(data) {
      new_materials_register=[]
      refresh_new_materials();
      $('#materials_added_check' ).animate({
        opacity: 1
      }, 200);
      $('#materials_added_check' ).animate({
        opacity: 0
      }, 2500);
      load_materials_from_db();

    }
  });
}



//
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
//
function choose_selected_materials()
{
  chosen_materials_register = selected_materials_register.slice(); //Copy array
  refresh_materials_input()

  $("body> *").not("#materials_container").css("filter", "blur(0)"); //Select every DOM element except materials window
  $("#materials_container").css("display", "none");
  $("#submit_btn").removeAttr("disabled");
}

function close_materials_window()
{
  selected_materials_register = chosen_materials_register.slice()
  $("#materials_container").css('display', 'none');
  $("body> *").not("#materials_container").css("filter", "blur(0)"); //Select every DOM element except materials window
  $("#submit_btn").removeAttr("disabled");

  // var materials_input = materials_input_text.val().split(",");
  // selected_materials = $("#selected_materials").find(".materials_available")
  // for(var i=selected_materials.length-1; i>=0; i--)
  // {
  //   if( materials_input.indexOf($(selected_materials[i]).text())==-1  ) //-1 is returned when element is not in array
  //   {
  //     selected_materials_register.splice(selected_materials_register.indexOf($(selected_materials[i]).text()),1);
  //   }
  // }
}

function material_in_array(material, materials_array)
{
  in_array = false;

  if(typeof material === 'string')
  {
    for(var j=0; j<materials_array.length; j++)
    {
      if(material==materials_array[j]['name'])
        in_array = true;
    }
  }
  else if(typeof material == 'object'  )
  {
    for(var j=0; j<materials_array.length; j++)
    {
      if(material['id']==materials_array[j]['id'] && material['name']==materials_array[j]['name'])
        in_array = true;
    }
  }
  else if(typeof material === 'number' && parseInt(material)!=NaN)
  {
    for(var j=0; j<materials_array.length; j++)
    {
      if(material==materials_array[j]['id'] )
        in_array = true;
    }
  }
  return in_array;
}

function remove_material_from_array(material_id)
{
  for(var i=0; i<selected_materials_register.length; i++)
  {
    if(selected_materials_register[i]['id']==material_id){
      selected_materials_register.splice(i, 1)
      break;
    }
  }
}
