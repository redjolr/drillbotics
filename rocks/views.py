from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Rock
from .models import RockComposition
from .models import Material
import json

@login_required(login_url='/login/')
def allrocks(request):
    rock_compositions = RockComposition.objects.select_related('rock', 'material').values('rock__name', 'material__name')
    rocks = {}
    for rock_comp in rock_compositions:
        if rock_comp['rock__name'] not in rocks:
            rocks[rock_comp['rock__name']] = []
        rocks[rock_comp['rock__name']].append(rock_comp['material__name'])
    rocks = list(rocks.items())
    return render(request, 'rocks/allrocks_list.html', {'rocks':rocks})

def get_materials(request):
    materials = Material.objects.all()
    materials = [{'id':material.id, 'name':material.name} for material in materials]
    return HttpResponse(json.dumps(materials))

def add_materials(request):
    if request.method=="POST":
        materials_json = request.POST["materials"]
        material_names = json.loads(materials_json)

        saved_rocks = []
        for name in material_names:
            material = Material()
            material.name = name
            material.save()
            saved_rocks.append(material.name)
        return HttpResponse(json.dumps(saved_rocks))



@login_required(login_url='/login/')
def rock(request, id):
    pass




@login_required(login_url='/login/')
def addrock(request):

    if request.method=="GET":
        return render(request, 'rocks/addrock.html')
    elif request.method=="POST":
        rock = Rock()
        rock.name = request.POST['name']
        rock.description = request.POST['description']
        if len(request.FILES)!=0:
            rock.picture = request.FILES['picture']
        rock.save()
        print("ASASASDASD", rock.id)


        materials = json.loads(request.POST['materials'])
        for material_id in materials:
            material = Material.objects.get(pk=material_id)
            rock_composition = RockComposition()
            rock_composition.rock = rock
            rock_composition.material = material
            rock_composition.save()

        return redirect('/rocks')




@login_required(login_url='/login/')
def update_rock(request, id):
    pass
