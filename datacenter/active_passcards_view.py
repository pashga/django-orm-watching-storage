from datacenter.models import Passcard
from django.shortcuts import render


def active_passcards_view(request):
    passcard_active = Passcard.objects.filter(is_active=True)
    context = {
        'active_passcards': passcard_active,
    }
    return render(request, 'active_passcards.html', context)
