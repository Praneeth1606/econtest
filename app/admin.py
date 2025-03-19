from django.contrib import admin

from .models import Participant
from .models import Result
from .models import Submission

admin.site.register(Participant)
admin.site.register(Result)
admin.site.register(Submission)
