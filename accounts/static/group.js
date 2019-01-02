all_permissions_register = []
selected_permissions_register=[]

if($("#hidden_group_info").length)
  {
    selected_permissions_register = JSON.parse($("#hidden_group_info").text());
    $("#selected_hidden_permissions").val(JSON.stringify(selected_permissions_register));
  }

load_groups_from_db()
refresh_selected_permissions()
refresh_available_permissions()


function load_groups_from_db()
{
    var url = "/groups/permissions/get/";
    $.get(url, function(data, status){
        all_permissions_register = JSON.parse(data);
        for(var i=0; i<all_permissions_register.length; i++)
          all_permissions_register[i].id = parseInt(all_permissions_register[i].id)
        refresh_available_permissions();
    });
}

function refresh_available_permissions()
{
    $('#available_pemission_div').empty();
    for(var i=0; i<all_permissions_register.length; i++)
    {
      if( !permission_in_array(all_permissions_register[i], selected_permissions_register) )
        $("<div id='permission"+all_permissions_register[i]['id']+"' database_id='"+all_permissions_register[i]['id']+"' class='premissions_available list-group-item' onclick='move_permission(this)' >"+
              all_permissions_register[i]['name']+
          "</div>").appendTo($('#available_pemission_div'));
    }
}

function refresh_selected_permissions()
{
  $('#selected_pemission_div').empty();
  for(var i=0; i<selected_permissions_register.length; i++)
  {

    $("<div id='permission"+selected_permissions_register[i]['id']+"' database_id='"+selected_permissions_register[i]['id']+"' class='premissions_available list-group-item' onclick='move_permission(this)' >"+
          selected_permissions_register[i]['name']+
      "</div>").appendTo($('#selected_pemission_div'));
  }
}

function move_permission(permission_div)
{
  permission_id = parseInt($(permission_div).attr("database_id"));
  if(permission_in_array(permission_id, selected_permissions_register)) //Remove from selected_permissions_register
    remove_permission_from_array(permission_id, selected_permissions_register);
  else if(!permission_in_array(permission_id, selected_permissions_register)) //
  {
      selected_permissions_register.push({ 'id': permission_id  ,'name':$(permission_div).text()})
      $("#selected_hidden_permissions").val(JSON.stringify(selected_permissions_register));
  }
  refresh_available_permissions()
  refresh_selected_permissions()

  search_permission($("#search_available_permission"));
  search_permission($("#search_selected_permission"));
}

function search_permission(input)
{
  permissions =$("#"+ $(input).attr("target_div")).find(".premissions_available");
  search_str = $(input).val()
  for(var i=0; i<permissions.length; i++)
  {
    name_lowercase = $(permissions[i]).text().toLowerCase();
    if(name_lowercase.search(search_str)>=0)
      $(permissions[i]).css("display", "block");
    else
      $(permissions[i]).css("display", "none");
  }
}

function permission_in_array(permission, permissions_array)
{
  in_array = false;

  if(typeof permissions_array === 'string')
  {
    for(var j=0; j<permissions_array.length; j++)
    {
      if(permission==permissions_array[j]['name'])
        in_array = true;
    }
  }
  else if(typeof permission == 'object'  )
  {
    for(var j=0; j<permissions_array.length; j++)
    {
      if(permission['id']==permissions_array[j]['id'] && permission['name']==permissions_array[j]['name'])
        in_array = true;
    }
  }
  else if(typeof permission === 'number' && parseInt(permission)!=NaN)
  {
    for(var j=0; j<permissions_array.length; j++)
    {
      if(permission==permissions_array[j]['id'] )
        in_array = true;
    }
  }
  return in_array;
}

function remove_permission_from_array(permission_id)
{
  for(var i=0; i<selected_permissions_register.length; i++)
  {
    if(selected_permissions_register[i]['id']==permission_id){
      selected_permissions_register.splice(i, 1)
      break;
    }
  }
}

function submit_form()
{
  unfilled_inputs = []

  $("input").css("border-color", $("#search_available_permission").css("border-color"))
  $("#selected_pemission_div").css("border", "1px solid black")
  if($("#name").val()=="" )
    unfilled_inputs.push($("#name"))
  if($("#description").val()=="" )
    unfilled_inputs.push($("#description"))
  if(selected_permissions_register.length==0)
    unfilled_inputs.push($("#selected_pemission_div"))

  for(var i=0; i<unfilled_inputs.length; i++)
  {
    unfilled_inputs[i].css('border', '1px solid red');
  }

  if(unfilled_inputs.length>0)
  {
    $("#alert_message").css("display", 'block')
    return
  }
  $("#group_form").submit()
}
