from django.contrib import admin
from .models import Board,Post,Topic

# Register your models here.
# username = vipulraut
# password = board

admin.site.register([Board,Post,Topic])
