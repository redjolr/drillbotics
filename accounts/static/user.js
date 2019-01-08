all_groups_register = []
if($("#selected_hidden_groups").val()=='')
  selected_groups_register=[]
else
  selected_groups_register = JSON.parse($("#selected_hidden_groups").val())

load_groups_from_db();
refresh_selected_groups();

function load_groups_from_db()
{
    var url = "/users/get_groups/";
    $.get(url, function(data, status){
        all_groups_register = JSON.parse(data);
        for(var i=0; i<all_groups_register.length; i++)
          all_groups_register[i].id = parseInt(all_groups_register[i].id)
        refresh_available_groups();
    });
}

function refresh_available_groups()
{
    $('#available_groups_div').empty();
    for(var i=0; i<all_groups_register.length; i++)
    {
      if( !group_in_array(all_groups_register[i], selected_groups_register) )
        $("<div id='group"+all_groups_register[i]['id']+"' database_id='"+all_groups_register[i]['id']+"' class='groups_available list-group-item' onclick='move_group(this)' >"+
              all_groups_register[i]['name']+
          "</div>").appendTo($('#available_groups_div'));
    }
}

function refresh_selected_groups()
{
  $('#selected_groups_div').empty();
  for(var i=0; i<selected_groups_register.length; i++)
  {

    $("<div id='group"+selected_groups_register[i]['id']+"' database_id='"+selected_groups_register[i]['id']+"' class='groups_available list-group-item' onclick='move_group(this)' >"+
          selected_groups_register[i]['name']+
      "</div>").appendTo($('#selected_groups_div'));
  }
}

function move_group(group_div)
{
  group_id = parseInt($(group_div).attr("database_id"));
  if(group_in_array(group_id, selected_groups_register)) //Remove from selected_permissions_register
    remove_group_from_array(group_id, selected_groups_register);
  else if(!group_in_array(group_id, selected_groups_register)) //
  {
      selected_groups_register.push({ 'id': group_id  ,'name':$(group_div).text()})
  }
  $("#selected_hidden_groups").val(JSON.stringify(selected_groups_register));
  refresh_available_groups()
  refresh_selected_groups()


}


function submit_form()
{
  mandatory_inputs = {"#username":"#username",  "#selected_hidden_groups":"#selected_groups_div",
                      "#first_name":"#first_name", "#last_name":"#last_name"}
  if(!updating_user)
  {
     mandatory_inputs["#password1"] = "#password1"
     mandatory_inputs["#password2"] = "#password2"
  }
  $("input").css("border-color", $("#email").css("border-color")) //Revert the border in the original color
  $("#selected_groups_div").css("border", "1px solid black")
  all_mandatory_filled = true;
  for(input in mandatory_inputs)
  {
    if($(input).val()=="" )
    {
      $(mandatory_inputs[input]).css('border', '1px solid red');
      all_mandatory_filled = false;
    }
  }

  if($("#password1").val()!=$("#password2").val()){
    alert("Passwords must match!")
    return
  }


  if($("#email").val()!="" && !isEmail($("#email").val()))
  {
    alert("Email is not correct!")
    return
  }

  if(!all_mandatory_filled)
  {
    $("#alert_message").css("display", 'block')
    return
  }
  $("#user_form").submit()
}


function remove_group_from_array(group_id)
{
  for(var i=0; i<selected_groups_register.length; i++)
  {
    if(selected_groups_register[i]['id']==group_id){
      selected_groups_register.splice(i, 1)
      break;
    }
  }
}

function group_in_array(permission, permissions_array)
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


function isEmail(emailText) {
    var pattern = /^[a-zA-Z0-9\-_]+(\.[a-zA-Z0-9\-_]+)*@[a-z0-9]+(\-[a-z0-9]+)*(\.[a-z0-9]+(\-[a-z0-9]+)*)*\.[a-z]{2,4}$/;
    if (pattern.test(emailText)) {
        return true;
    } else {

        return false;
    }
}
