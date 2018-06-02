from django.contrib import admin

from .models import Problem, TestCase


class TestCaseInLine(admin.TabularInline):
    model = TestCase
    extra = 1


class ProblemAdmin(admin.ModelAdmin):
    # fields = [
    #     'title',
    #     'description',
    #     'input_file_name',
    #     'output_file_name',
    #     'time_limit',
    #     'memory_limit',
    #     'stdio_flag',
    #     'optimize_flag',
    # ]
    inlines = [TestCaseInLine]


admin.site.register(Problem, ProblemAdmin)
