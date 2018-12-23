var  experiments = {};

$("#pane_container").css("padding-top", $("header").height());
$("#pane_container").width($(window).width());
$('#left_pane').width("230px");
$('#right_pane').width($("#pane_container").width()-$("#left_pane").width());

$( function() {
$( "#left_pane" ).resizable({
  handles: "e",
  minWidth: $("#pane_container").width()*0.05,
  resize: function(){
        $("#right_pane").width( $("#pane_container").width()-$("#left_pane").width())
    }
});
} );

function load_experiment_data(dbId, experiment_date)
{
    var elem = $("#experiment"+dbId);

    var htmlId = 'experiment'+dbId;
    if($("#"+htmlId+"tab").length>0){ //The experiment is already loaded
        experiment_already_loaded(htmlId);
        return;
    }

    if($(".checkbox_exp"+dbId+":checkbox:checked").length==0)
    {
      alert("Choose at least one sensor to visualize!");
      return;
    }

    var sensor_id = $("#sensor_select"+dbId).val()
    var downsample_val = $("#slider"+dbId).slider("value")*0.01
    var total_points = $('#total_points'+dbId).html()



    var checked_sensors = get_checked_sensors(dbId);
    var checked_sensors_url = "&sensors=";

    for(i=0; i<checked_sensors.length; i++)
    {
      checked_sensors_url+=checked_sensors[i]
      if(i<checked_sensors.length-1)
        checked_sensors_url+="_";
    }

    url = "/experiments/"+dbId+"?downsample="+downsample_val+"&total_points="+total_points+checked_sensors_url;
    add_new_panel(dbId, experiment_date);



    $.get(url, function(data, status){

          var data_object = JSON.parse(data)


          generate_chart(dbId, data_object)
          $('<p><strong>Data points:</strong> <span>'+data_object['data']['time'].length+'</span></p>'+
            '<p><h4>Rock</h4>'+
                '<span><strong>Id:</strong> '+data_object['rock']['id']+'</span><br>'+
                '<span><strong>Name:</strong> '+data_object['rock']['name']+'</span>'+
            '</p>').appendTo($('#'+htmlId+'Content .info_area').eq(0));
            $('#loading_gif').css('display', 'none');

      });







}


function add_new_panel(dbId, experiment_date)
{
  var htmlId = 'experiment'+dbId;
  navTab = $("#nav-tab");
  navTabContent = $("#nav-tabContent");
  navTabHtml= '<a class="nav-item nav-link " id="'+htmlId+'tab" data-toggle="tab" href="#'+htmlId+'Content"'+
              ' role="tab" aria-controls="'+htmlId+'Content" aria-selected="true"   ><span>'+experiment_date+
              '</span>&nbsp;&nbsp; <span  class="oi oi-circle-x" onclick="close_panel('+dbId+')"></span></a>'
  $(navTabHtml).appendTo('#nav-tab');

  tabContentHtml = '<div  class="tab-pane fade" id="'+htmlId+'Content" style="position: relative" role="tabpanel" aria-labelledby="'+htmlId+'tab">'+
                      '<div class="container-fluid"> '+
                        '<div class="row">'+
                          '<div class="chart_area col-md-9"></div>'+
                          '<div class="info_area col-md-3"> </div>'+
                        '</div>'+
                      '</div>'+
                    '</div>'
  $(tabContentHtml).appendTo("#nav-tabContent");

  $('#loading_gif').css('display', 'block')
  $('#loading_gif').css('left', $(window).width()/2-$('#loading_gif').width()/2);
  $('#loading_gif').css('top', ($(window).height())/2-20-$('#loading_gif').height()/2);
  $('#nav-tab a:last').tab('show');

}

function close_panel(dbId)
{
  var isActive = false;
  var htmlId = 'experiment'+dbId;
  var tabId = htmlId+'tab';
  var panelId = htmlId+'Content';
  if ($('#'+panelId).hasClass('show'))
  {
    isActive = true;
  }

  $('#'+panelId).remove();
  $('#'+tabId).remove();

  if(isActive)
    $('#nav-tab a:first').tab('show');
}

function generate_chart(dbId, data_object)
{
  var htmlId = 'experiment'+dbId;
  $('<canvas id="myChart'+dbId+'" width="1000px" height="600px" ></canvas>').appendTo($('#'+htmlId+'Content .chart_area'));
  var colors = ['blue', 'green', 'red', 'yellow', 'pink', 'purple', '#f1ca3a','black', '#7f7fff', 'brown', '#98FB98']
  var sensor_datasets = [];

  for(var i=0; i<data_object['data']['sensors'].length; i++)
  {
    sensor_datasets.push({
      label: data_object['data']['sensors'][i]['sensor_name'],
      data: data_object['data']['sensors'][i]['values'],

      fill: false,
      borderColor: [colors[i]],
      borderWidth: 1,
      backgroundColor: [colors[i]]
    });

  }
  var ctx = document.getElementById('myChart'+dbId)//.getContext('2d');
  var myChart = new Chart(ctx, {
      type: 'line',
      data: {
          labels: data_object['data']["time"],
          datasets: sensor_datasets
      },
      options: {
          responsive: true,
          scales: {
              yAxes: [{
                  ticks: {
                      beginAtZero:true
                  }
              }],

              xAxes: [{
                ticks: {
                    suggestedMax: 700,
                    suggestedMin: 0,
                    stepSize: 20
                }
            }]
          },

      }
  });

  $('#myChart'+dbId).width($('.chart_area').width()+"px")
  $('#myChart'+dbId).height( $('#right_pane').height()*0.9 )

  $('#myChart'+dbId).attr('width', $('.chart_area').width()+"px")
  $('#myChart'+dbId).attr('height', $('#right_pane').height()*0.9+"px" )

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
