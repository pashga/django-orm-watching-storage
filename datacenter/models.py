import datetime
from django.db import models
from django.utils.timezone import localtime

MINUTES_IN_HOUR = 60
SECONDS_IN_HOUR = 3600


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


def get_duration(leaved, entered):
    if leaved is None:
        duration = localtime(datetime.datetime.now()) - localtime(entered)
    else:
        duration = localtime(leaved) - localtime(entered)
    return duration.total_seconds()


def format_duration(duration):
    seconds = duration
    minutes = int((seconds % SECONDS_IN_HOUR) // MINUTES_IN_HOUR)
    hours = int(seconds // SECONDS_IN_HOUR)
    return f"{hours} ч {minutes} мин"


def is_visit_long(visit, minutes=60):
    return datetime.timedelta(minutes=minutes).total_seconds() < visit
