from django.contrib import admin
from .models import Instruction, InstructionTag


class InstructionAdmin(admin.ModelAdmin):
    pass


class InstructionTagAdmin(admin.ModelAdmin):
    pass


admin.site.register(Instruction, InstructionAdmin)
admin.site.register(InstructionTag, InstructionTagAdmin)
