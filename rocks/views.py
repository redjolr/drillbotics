from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Rock
from .models import RockComposition
from .models import Material

@login_required(login_url='/login/')
def allrocks(request):
    rock_compositions = RockComposition.objects.select_related('rock', 'material').values('rock__name', 'material__name')
    rocks = {}
    print(rock_compositions)
    for rock_comp in rock_compositions:
        if rock_comp['rock__name'] not in rocks:
            rocks[rock_comp['rock__name']] = []
        rocks[rock_comp['rock__name']].append(rock_comp['material__name'])
    rocks = list(rocks.items())
    print(rocks)
    return render(request, 'rocks/allrocks.html', {'rocks':rocks})
