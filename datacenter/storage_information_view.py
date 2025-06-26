from datacenter.models import get_duration, format_duration
from django.utils.timezone import localtime
from datacenter.models import Visit
from django.shortcuts import render


def storage_information_view(request):
    visits = Visit.objects.filter(leaved_at__iexact=None)
    visits_not_closed = []
    for visit in visits:
        name = visit.passcard.owner_name
        entered_at = localtime(visit.entered_at)
        leaved_at = localtime(visit.leaved_at)
        duration = format_duration(
            duration=get_duration(
                leaved=leaved_at,
                entered=entered_at,
            )
        )

        non_closed_visits = {
                'who_entered': name,
                'entered_at': entered_at,
                'duration': duration,
            }
        visits_not_closed.append(non_closed_visits)

    context = {
        'non_closed_visits': visits_not_closed,
    }
    return render(request, 'storage_information.html', context)
