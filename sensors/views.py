from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Sensor
from django.templatetags.static import static

@login_required(login_url='/login/')
def allsensors(request):

    sensors = Sensor.objects.all()
    if 'view' not in request.GET.keys() or request.GET['view']=='list' :
        return render(request, 'sensors/allsensors_list.html', {'sensors':sensors})
    elif request.GET['view']=='tabular':
        return render(request, 'sensors/allsensors_tabular.html', {'sensors':sensors})

@login_required(login_url='/login/')
def sensor(request, id):
    sensor = Sensor.objects.get(id=id)
    return render(request, 'sensors/sensor.html', {'sensor':sensor} )

@login_required(login_url='/login/')
def addsensor(request):
    if request.method=="POST":
        if request.POST['name'] and request.POST['abbreviation'] and request.POST['description'] and request.POST['unit_of_measure']  and request.POST['type']:
            sensor = Sensor()
            sensor.name = request.POST['name']
            sensor.abbreviation = request.POST['abbreviation']
            sensor.description = request.POST['description']
            sensor.unit_of_measure = request.POST['unit_of_measure']
            #sensor.picture = request.FILES['picture']
            sensor.type = request.POST['type']
            if len(request.FILES)!=0:
                sensor.picture = request.FILES['picture']

                                                           #
            sensor.save()
            return redirect('/sensors/'+str(sensor.id))

    if request.method=="GET":
        return render(request, 'sensors/addsensor.html')
