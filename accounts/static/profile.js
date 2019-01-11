$('#myTab a').on('click', function (e) {
e.preventDefault()
$(this).tab('show')
})



$( function() {
  n_allowed = 3;

  groups = $(".group_div");

  for(var i=0; i<groups.length; i++)
  {
    longer_than_allowed = false;
    permissions = $(groups[i]).find(".permission")
    for(var j=0; j<permissions.length; j++)
    {
      if(j>=n_allowed){
        $(permissions[j]).css('display', 'none')
        longer_than_allowed = true;
      }
    }
    if(longer_than_allowed)
      $(groups[i]).find('.see_more_btn').css('display', 'block')
  }

} );

function see_more(see_more_btn, evt)
{
  evt.preventDefault();
  $(see_more_btn).parent().find('.permission').css('display', 'block')
  $(see_more_btn).parent().find('.see_less_btn').css('display', 'block')
  $(see_more_btn).css('display', 'none')
}

function see_less(see_less_btn, evt)
{
  evt.preventDefault();
  permissions = $(see_less_btn).parent().find('.permission')
  for(var i=0; i<permissions.length; i++)
  {
    if(i>=n_allowed)
      $(permissions[i]).css('display', 'none')
  }

  $(see_less_btn).parent().find('.see_more_btn').css('display', 'block')
  $(see_less_btn).css('display', 'none')
}


function submit_change_pass()
{
  if($("#password1").val()!=$("#password2").val()){
    $(".alert").css('display', 'none');
    $("#pass_dont_match_alert").css('display', 'block')
    return
  }
  if($("#password1").val()=="" || $("#password2").val()=="" || $("#current_password").val()=="" )
  {
    $(".alert").css('display', 'none');
    $("#fill_out_fields_alert").css('display', 'block')
    return
  }
  url = '/users/change_password/'
  $(".password_field").prop('disabled', true)
  $("#change_pass_btn").prop('disabled', true)
  $("#loading_gif").css('display', 'inline')
  jQuery.ajax({
    type: 'POST',
    url: url,
    data: { 'csrfmiddlewaretoken': csrf_token, 'password1': $("#password1").val(), 'password2': $("#password2").val(), 'current_password': $("#current_password").val()},
    dataType: 'text',
    success: function(response) {

      $(".alert").css('display', 'none');
      $("#invalid_password_messages").find("div").remove()
      if(response=="passwords_missing")
        respective_alert = "#fill_out_fields_alert"
        // $("#fill_out_fields_alert").css('display', 'block')
      else if(response=="passwords_dont_match")
        respective_alert = "#pass_dont_match_alert"
      else if(response=="wrong_current_password")
        respective_alert = "#wrong_current_password"
      else if(response=="success")
        respective_alert = "#password_change_success"
      else
      {
        invalid_password_messages = JSON.parse(response)
        for(var i=0; i<invalid_password_messages.length; i++)
        {
          $("#invalid_password_messages").append("<div>"+invalid_password_messages[i]+"</div>")
        }
        respective_alert = "#invalid_password_messages"
      }

      $(respective_alert).css('display', 'block')

      $(".password_field").prop('disabled', false)
      $("#change_pass_btn").prop('disabled', false)
      $("#loading_gif").css('display', 'none')
    }
  });
}


//Executed when an image is selected
$(function() {
   $("#picture_input").change(function (){
     var fileName = $(this).val().split('\\').pop();
     $("#upload_picture_label").text(fileName + " selected");
   });
});

function edit_profile()
{
    if($("#save_profile_btn").css('display')=='none' )
    {
      $(".user_input").css('display', 'inline-block')
      $("#save_profile_btn").css('display', 'inline')
      $("#cancel_profile_btn").css('display', 'inline')
      $(".detail_info").css('display', 'none')
      $("#upload_picture_label").css('display', 'block')
    }
    else{
      $(".user_input").css('display', 'none')
      $("#save_profile_btn").css('display', 'none')
      $("#cancel_profile_btn").css('display', 'none')
      $(".detail_info").css('display', 'inline-block')
      $("#upload_picture_label").css('display', 'none')
    }

}

function save_profile(profile_form)
{
  if($('#first_name_field').val()=='' || $("#last_name_field").val()=='' )
  {
    alert('First name and last name must be filled!');
    return
  }
  $(profile_form).submit()
}
