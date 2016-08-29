from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, redirect

from datetime import date
from PartyShiftSchedule.templatetags.schedule_table_tags import toggle_button
import itertools

from .models import Slot, Position, Party, Time


def pss_landing(request):
    user = request.user
    return render(request, 'PartyShiftSchedule/landing_page.html', {'username': user})


@login_required()
def shift_schedule(request):
    next_party = _get_next_party()
    positions = Position.objects.all()
    times = Time.objects.filter(party=next_party).order_by('beginning')

    context = {
        'positions': positions,
        'times': times,
        'user': request.user,
    }
    return render(request, 'PartyShiftSchedule/shift_schedule.html', context=context)


@login_required()
def enter(request):
    if request.method == 'POST':
        post = request.POST
        checked = post['checked'] == 'true'
        next_party = _get_next_party()
        time = Time.objects.get(id=post['time'], party=next_party)
        position = Position.objects.get(id=post['position'], party=next_party)
        user = request.user

        slot = Slot.objects.filter(time=time, position=position, user=user)

        if not slot.exists() and checked:
            Slot(time=time, position=position, user=user).save()

        elif slot.exists() and not checked:
            slot[0].delete()

        print("Debug: {0} {1} {2}".format(post['checked'], post['time'], post['position']))

        return HttpResponse(status=200)

    return HttpResponse(status=405)  # 405: Method not allowed


def pad_list(l, pad, c):
    for _ in itertools.repeat(None, c):
        l.append(pad)
    return l


def _get_next_party():
    next_partys = Party.objects.filter(date__gte=date.today()).order_by('date')
    if len(next_partys) == 0:
        return
    return next_partys[0]
