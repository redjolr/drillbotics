from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.http import HttpResponse
from .models import Rock
from .models import RockComposition
from .models import Material
import json
from operator import itemgetter
from django.template.defaulttags import register
from accounts.accounts_utils import user_changed_password, check_permissions
from django.contrib.auth.models import User, Group, Permission

@register.filter
def get_item(dictionary, key):

    if key in dictionary:
        return dictionary[key]

@login_required(login_url='/login/')
@user_passes_test(user_changed_password, login_url='/first_login_password/')
@permission_required('rocks.view_rock', login_url='home')
def allrocks(request):
    rocks =  Rock.objects.all()
    materials = {}
    for rock in rocks:
        composition = list( map(itemgetter('material__name'), list(RockComposition.objects.select_related('material').values( 'material__name').filter(rock= rock)) ) )
        materials[rock.id] =  ", ".join(composition)
    if 'view' not in request.GET or request.GET['view']=='list':
        return render(request, 'rocks/allrocks_list.html', {'rocks':rocks, 'materials':materials})
    else:
        return render(request, 'rocks/allrocks_tabular.html', {'rocks':rocks, 'materials':materials})



@login_required(login_url='/login/')
@user_passes_test(user_changed_password, login_url='/first_login_password/')
def get_materials(request):
    materials = Material.objects.all()
    materials = [{'id':material.id, 'name':material.name} for material in materials]
    return HttpResponse(json.dumps(materials))


@login_required(login_url='/login/')
@user_passes_test(user_changed_password, login_url='/first_login_password/')
@permission_required('materials.add_material', login_url='rocks')
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
@user_passes_test(user_changed_password, login_url='/first_login_password/')
@permission_required('rocks.view_rock', login_url='home')
def rock(request, id):
    rock = Rock.objects.get(id=id)
    composition = list( map(itemgetter('material__name'), list(RockComposition.objects.select_related('material').values( 'material__name').filter(rock= rock)) ) )
    materials =  ", ".join(composition)
    return render(request, 'rocks/rock.html', {'rock':rock, 'materials':materials} )


@login_required(login_url='/login/')
@user_passes_test(user_changed_password, login_url='/first_login_password/')
@permission_required('rocks.add_rock', login_url='rocks')
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
        materials = json.loads(request.POST['materials'])
        for material_id in materials:
            material = Material.objects.get(pk=material_id)
            rock_composition = RockComposition()
            rock_composition.rock = rock
            rock_composition.material = material
            rock_composition.save()

        return redirect('/rocks')


@login_required(login_url='/login/')
@user_passes_test(user_changed_password, login_url='/first_login_password/')
@permission_required('rocks.change_rock', login_url='rocks')
def update_rock(request, id):
    if request.method=="POST":
        rock = get_object_or_404(Rock, id=id)
        rock.name = request.POST['name']
        rock.description = request.POST['description']
        if len(request.FILES)!=0:
            for key in request.FILES.keys():
                print(key)
            rock.picture = request.FILES['picture']
        rock.save()
        RockComposition.objects.filter(rock=rock).delete()
        materials = json.loads(request.POST['materials'])
        for material_id in materials:
            rock_composition = RockComposition()
            rock_composition.rock = rock
            rock_composition.material = get_object_or_404(Material, id = material_id)
            rock_composition.save()
        return redirect('/rocks/'+str(rock.id))




def lalala():
    pass
