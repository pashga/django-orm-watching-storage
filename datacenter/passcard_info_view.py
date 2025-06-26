from django.utils.timezone import localtime
from datacenter.models import Passcard, Visit
from datacenter.models import format_duration, get_duration, is_visit_long
from django.shortcuts import render, get_object_or_404


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)
    man_visits = []
    for visit in visits:

        entered_at = localtime(visit.entered_at)
        leaved_at = localtime(visit.leaved_at)
        durations = format_duration(
            duration=get_duration(
                leaved=leaved_at,
                entered=entered_at
            )
        )
        is_strange = is_visit_long(
            visit=get_duration(
                leaved=leaved_at,
                entered=entered_at
            )
        )

        this_passcard_visits = {
                'entered_at': entered_at,
                'duration': durations,
                'is_strange': is_strange
            }
        man_visits.append(this_passcard_visits)
    context = {
        'passcard': passcard,
        'this_passcard_visits': man_visits
    }
    return render(request, 'passcard_info.html', context)
