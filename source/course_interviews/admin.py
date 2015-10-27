from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Student, Teacher, InterviewerFreeTime, InterviewSlot


class StudentAdmin(admin.ModelAdmin):

    def get_first_task(self, obj):
        return u"<a href='{0}' target='_blank'>link</a>".format(obj.first_task)
    get_first_task.allow_tags = True
    get_first_task.short_description = "First task"
    get_first_task.admin_order_field = 'first_task'

    def get_second_task(self, obj):
        return u"<a href='{0}' target='_blank'>link</a>".format(obj.second_task)
    get_second_task.allow_tags = True
    get_second_task.short_description = "Second task"
    get_second_task.admin_order_field = 'second_task'

    def get_third_task(self, obj):
        return u"<a href='{0}' target='_blank'>link</a>".format(obj.third_task)
    get_third_task.allow_tags = True
    get_third_task.short_description = "Third task"
    get_third_task.admin_order_field = 'third_task'

    list_display = [
        'name',
        'email',
        'skype',
        'phone_number',
        'applied_course',
        'get_first_task',
        'get_second_task',
        'get_third_task',
        'code_skills_rating',
        'code_design_rating',
        'fit_attitude_rating',
        'has_interview_date',
        'has_confirmed_interview',
        'has_been_interviewed',
        'is_accepted'
    ]
    list_filter = [
        'applied_course',
        'code_skills_rating',
        'code_design_rating',
        'fit_attitude_rating',
        'has_confirmed_interview',
        'has_been_interviewed',
        'is_accepted'
    ]
    search_fields = ['name', 'email', 'skype']
    readonly_fields = ('uuid',)

admin.site.register(Student, StudentAdmin)


class InterviewerFreeTimeAdmin(admin.ModelAdmin):
    model = InterviewerFreeTime

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            self.exclude = ['teacher']
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change and not request.user.is_superuser:
            obj.teacher = request.user.teacher
        obj.save()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(teacher=request.user.teacher)

    list_display = [
        "teacher",
        "date",
        "start_time",
        "end_time"
    ]
    list_filter = ["date", "start_time", "end_time"]
    search_fields = ["teacher"]
    ordering = ['date', 'start_time']

admin.site.register(InterviewerFreeTime, InterviewerFreeTimeAdmin)


class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False


class UserAdmin(UserAdmin):
    inlines = (TeacherInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class InterviewSlotAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        if obj and request.POST and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(
            teacher_time_slot=request.user.teacher.interviewerfreetime_set.all())

    def get_date(self, obj):
        return obj.teacher_time_slot.date
    get_date.short_description = 'Date'
    get_date.admin_order_field = 'teacher_time_slot__date'

    def get_start_time(self, obj):
        return obj.start_time
    get_start_time.short_description = "Starting"
    get_start_time.admin_order_field = "start_time"

    def get_student(self, obj):
        if obj.student_id and obj.student.name:
            return u"<a href='../student/{0}/'>{1}</a>".format(obj.student_id, obj.student.name)
        return
    get_student.short_description = "Student"
    get_student.allow_tags = True

    def get_teacher(self, obj):
        return obj.teacher_time_slot.teacher
    get_teacher.short_description = "Teacher"

    def get_student_confirmation(self, obj):
        if obj.student_id:
            return obj.student.has_confirmed_interview
        return
    get_student_confirmation.short_description = "Confirmed interview"
    get_student_confirmation.boolean = True

    def get_student_has_been_interviewed(self, obj):
        if obj.student_id:
            return obj.student.has_been_interviewed
        return
    get_student_has_been_interviewed.short_description = "Has been interviewed"
    get_student_has_been_interviewed.boolean = True

    list_display = [
        'get_date',
        'get_start_time',
        'get_student',
        'get_student_confirmation',
        'get_student_has_been_interviewed',
        'get_teacher',
    ]
    ordering = ['teacher_time_slot__date', 'start_time']

admin.site.register(InterviewSlot, InterviewSlotAdmin)
