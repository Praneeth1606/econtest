from django.contrib import admin

# Register your models here.
from .models import User
from .models import Result
from .models import Submission

admin.site.register(User)
admin.site.register(Result)
admin.site.register(Submission)