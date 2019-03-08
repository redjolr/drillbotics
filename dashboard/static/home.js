var  experiments = {};

$("#pane_container").css("padding-top", $("header").height());
$("#pane_container").width($(window).width());
$('#left_pane').width("230px");
$('#right_pane').width($("#pane_container").width()-$("#left_pane").width());

//Makes left pane resizable. jQuery UI funcitonality
$( function() {
$( "#left_pane" ).resizable({
  handles: "e",
  minWidth: $("#pane_container").width()*0.05,
  resize: function(){
        $("#right_pane").width( $("#pane_container").width()-$("#left_pane").width())
    }
});
} );



function load_experiment(experiment_id, experiment_date)
{
    var elem = $("#experiment"+experiment_id);

    var htmlId = 'experiment'+experiment_id;
    if($("#"+htmlId+"tab").length>0){ //The experiment is already loaded
        experiment_already_loaded(htmlId);
        return;
    }

    if($(".checkbox_exp"+experiment_id+":checkbox:checked").length==0)
    {
      alert("Choose at least one sensor to visualize!");
      return;
    }

    var sensor_id = $("#sensor_select"+experiment_id).val()
    var downsample_val = $("#slider"+experiment_id).slider("value")
    alert(downsample_val)
    var total_points = $('#total_points'+experiment_id).html()

    var checked_sensors = get_checked_sensors(experiment_id);
    var checked_sensors_url = "&sensors=";

    for(i=0; i<checked_sensors.length; i++)
    {
      checked_sensors_url+=checked_sensors[i]
      if(i<checked_sensors.length-1)
        checked_sensors_url+="_";
    }

    url = "/experiments/"+experiment_id+"?downsample="+downsample_val+"&total_points="+total_points+checked_sensors_url;
    add_new_panel(experiment_id, experiment_date);



    $.get(url, function(data, status){

          var data_object = JSON.parse(data)
          generate_chart(experiment_id, data_object);
          $('<p><strong>Data points:</strong> <span>'+data_object['n_data_points']+'</span></p>'+
            '<p><h4>Rock</h4>'+
                '<span><strong>Id:</strong> '+data_object['rock']['rock_id']+'</span><br>'+
                '<span><strong>Name:</strong> '+data_object['rock']['name']+'</span>'+
            '</p>').appendTo($('#'+htmlId+'Content .info_area').eq(0));

          $('<p><h4>Experiment</h4>'+
                '<span><strong>Duration:</strong> '+data_object['experiment']['duration']+'</span><br>'+
                '<span><strong>Sampling frequency:</strong> '+data_object['experiment']['sampling_freq']+' Hz</span></br>'+
                '<span><strong>Total points:</strong> '+data_object['experiment']['nr_data_points']+'</span></br></br>'+
                '<span><strong>Description:</strong> <div>'+data_object['experiment']['description']+'</div></span>'+
            '</p>').appendTo($('#'+htmlId+'Content .info_area').eq(0));

          $('#loading_gif').css('display', 'none');
          $('#experiment'+experiment_id).css('border-right', '2px solid #89ff89')

      });

}


function add_new_panel(experiment_id, experiment_date)
{
  var htmlId = 'experiment'+experiment_id;
  navTab = $("#nav-tab");
  navTabContent = $("#nav-tabContent");
  navTabHtml= '<a class="nav-item nav-link ui-state-default" id="'+htmlId+'tab" data-toggle="tab" href="#'+htmlId+'Content"'+
              ' role="tab" aria-controls="'+htmlId+'Content" aria-selected="true"   ><span>'+experiment_date+
              '</span>&nbsp;&nbsp; <span  class="oi oi-circle-x" onclick="close_panel('+experiment_id+')"></span></a>'
  $(navTabHtml).appendTo('#nav-tab');

  tabContentHtml = '<div  class="tab-pane fade" id="'+htmlId+'Content" style="position: relative" role="tabpanel" aria-labelledby="'+htmlId+'tab">'+
                      '<div class="container-fluid"> '+
                        '<div class="row">'+
                          '<div class="chart_area col-md-9"></div>'+
                          '<div class="info_area col-md-3"> </div>'+
                        '</div>'+
                      '</div>'+
                    '</div>';

  $(tabContentHtml).appendTo("#nav-tabContent");

  $('#loading_gif').css('display', 'block')
  $('#loading_gif').css('left', $(window).width()/2-$('#loading_gif').width()/2);
  $('#loading_gif').css('top', ($(window).height())/2-20-$('#loading_gif').height()/2);
  $('#nav-tab a:last').tab('show');

}

function close_panel(experiment_id)
{
  var isActive = false;
  var htmlId = 'experiment'+experiment_id;
  var tabId = htmlId+'tab';
  var panelId = htmlId+'Content';
  if ($('#'+panelId).hasClass('show')){ //Check if the tab being closed is the active one: has class 'show'
    isActive = true;
  }

  $('#'+panelId).remove();
  $('#'+tabId).remove();

  if(isActive)
    $('#nav-tab a:first').tab('show');
  $("#experiment"+experiment_id).css('border-right', 'none') //When a tab is open the experiment in the left has a colored border to indicate that it is active
}

function generate_chart(experiment_id, data_object)
{

  var htmlId = 'experiment'+experiment_id;
  $("<img src='/media/graphs/"+data_object['filename']+".png' id='myChart"+experiment_id+"' style='width:100%; height: 100%;' />").appendTo($('#'+htmlId+'Content .chart_area'));

}

function get_checked_sensors(experiment_id)
{

  var checkboxes = $(".checkbox_exp"+experiment_id);
  var checked_sensors = []
  for(var i=0; i< checkboxes.length; i++){
    if(checkboxes.eq(i).is(':checked')  ){
      checked_sensors.push(checkboxes.eq(i).val())
    }
  }
  return checked_sensors;
}

//When the user tries to load an experiment that is already loaded, this function is executed
function experiment_already_loaded(htmlId)
{
    alert("Experiment already in panel!")
    $('#nav-tab #'+htmlId+'tab').tab('show');

    $('#'+htmlId+'tab' ).animate({
      backgroundColor: "red"
    }, 200);
    $('#'+htmlId+'tab' ).animate({
      backgroundColor: "white"
    }, 1500);
}


function select_checkbox(checkbox, experiment_id)
{
  if( $(checkbox).hasClass('selectAllCheckBox')){
    if($(checkbox).is(":checked")){
      $('.checkbox_exp'+experiment_id).prop('checked', true);
    }
    else {
      $('.checkbox_exp'+experiment_id).prop('checked', false);
    }
  }
  else{
    if($(".checkbox_exp"+experiment_id+":checked").length==0){
      $("#selectall_exp"+experiment_id).prop("indeterminate", false);
      $("#selectall_exp"+experiment_id).prop("checked", false);
    }
    else if ($(".checkbox_exp"+experiment_id+":checked").length == $(".checkbox_exp"+experiment_id).length){
      $("#selectall_exp"+experiment_id).prop("indeterminate", false);
      $("#selectall_exp"+experiment_id).prop("checked", true);
    }
    else if($(".checkbox_exp"+experiment_id+":checked").length < $(".checkbox_exp"+experiment_id).length)
      $("#selectall_exp"+experiment_id).prop("indeterminate", true);
  }
}
