

$("#pane_container").css("padding-top", $("header").height());
$("#pane_container").width($(window).width());
$('#left_pane').width($("#pane_container").width()*0.15);
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
    var sensor_id = $("#sensor_select"+dbId).val()
    var downsample_val = $("#slider"+dbId).slider("value")*0.01
    var total_points = $('#total_points'+dbId).html()




    url = "/experiments/"+dbId+"/"+sensor_id+"?downsample="+downsample_val+"&total_points="+total_points;
    $.get(url, function(data, status){
          var data_object = JSON.parse(data)
          add_new_panel(htmlId, experiment_date);

          generate_chart(dbId, data_object)
          $('<p><strong>Data points:</strong> <span>'+data_object['data']['time'].length+'</span></p>'+
            '<p><h4>Rock</h4>'+
                '<span><strong>Id:</strong> '+data_object['rock']['id']+'</span><br>'+
                '<span><strong>Name:</strong> '+data_object['rock']['name']+'</span>'+
            '</p>').appendTo($('#'+htmlId+'Content .info_area').eq(0));

      });



}


function add_new_panel(htmlId, experiment_date)
{
  navTab = $("#nav-tab");
  navTabContent = $("#nav-tabContent");
  navTabHtml= '<a class="nav-item nav-link " id="'+htmlId+'tab" data-toggle="tab" href="#'+htmlId+'Content" role="tab" aria-controls="'+htmlId+'Content" aria-selected="true">'+experiment_date+'</a>'
  $(navTabHtml).appendTo('#nav-tab');

  tabContentHtml = '<div  class="tab-pane fade" id="'+htmlId+'Content" role="tabpanel" aria-labelledby="'+htmlId+'tab">'+
                      '<div class="container-fluid"> '+
                        '<div class="row">'+
                          '<div class="chart_area col-md-9"></div>'+
                          '<div class="info_area col-md-3"> </div>'+
                        '</div>'+
                      '</div>'+
                    '</div>'
  $(tabContentHtml).appendTo("#nav-tabContent");
  $('#nav-tab a:last').tab('show');
}


function generate_chart(dbId, data_object)
{
  var htmlId = 'experiment'+dbId;
  $('<canvas id="myChart'+dbId+'" width="1000px" height="600px" ></canvas>').appendTo($('#'+htmlId+'Content .chart_area').eq(0));

  var ctx = document.getElementById('myChart'+dbId).getContext('2d');
  var myChart = new Chart(ctx, {
      type: 'line',
      data: {
          labels: data_object['data']["time"],
          datasets: [{
              label: 'Sensor',
              data: data_object['data']['values'],
              backgroundColor: [
                  'rgba(255, 99, 132, 0.2)',

              ],
              fill: false,
              borderColor: [
                  'rgba(255,99,132,1)',

              ],
              borderWidth: 2
          }]
      },
      options: {
          responsive: false,
          scales: {
              yAxes: [{
                  ticks: {
                      beginAtZero:true
                  }
              }]
          }
      }
  });

  $('#myChart'+dbId).width($('.chart_area').width()+"px")
  $('#myChart'+dbId).height( $('#right_pane').height()*0.9 )

  $('#myChart'+dbId).attr('width', $('.chart_area').width()+"px")
  $('#myChart'+dbId).attr('height', $('#right_pane').height()*0.9+"px" )

}
