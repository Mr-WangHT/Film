from django.contrib import admin
from movie.models import *

# Register your models here.
admin.site.register(Movie)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Cinema)
admin.site.register(UserToken)
admin.site.register(Hall)
admin.site.register(Schedule)
admin.site.register(Order)
