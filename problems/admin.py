from django.contrib import admin

from .models import Problem, TestCase


class TestCaseInLine(admin.TabularInline):
    model = TestCase
    extra = 1


class ProblemAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'time_limit',
        'memory_limit',
        'description',
    ]
    inlines = [TestCaseInLine]


admin.site.register(Problem, ProblemAdmin)
