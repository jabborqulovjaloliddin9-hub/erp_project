from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView
from django.urls import reverse_lazy
from django.db.models import Sum
from .models import Payment, SupportTicket, Group, User, Course, Attendance, Assignment, Grade, Notification, Submission, Material

class RootDispatchView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        role = request.user.role
        if role == 'admin':
            return redirect('admin_dashboard')
        elif role == 'teacher':
            return redirect('teacher_dashboard')
        else:
            return redirect('student_dashboard')

class PlaceholderView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fake context data for dashboard so it doesn't crash empty
        context['total_students'] = User.objects.filter(role='student').count()
        context['open_tickets'] = SupportTicket.objects.filter(status='open').count()
        return context

class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_students'] = User.objects.filter(role='student').count()
        context['total_teachers'] = User.objects.filter(role='teacher').count()
        revenue = Payment.objects.filter(status='paid').aggregate(Sum('amount'))['amount__sum']
        context['total_revenue'] = revenue if revenue else 0
        context['open_tickets'] = SupportTicket.objects.filter(status='open').count()
        context['active_courses'] = Course.objects.filter(status='active').count()
        context['recent_users'] = User.objects.all().order_by('-date_joined')[:5]
        return context

class AdminUsersView(LoginRequiredMixin, ListView):
    template_name = 'admin/users.html'
    context_object_name = 'users'
    model = User

class AdminGroupsView(LoginRequiredMixin, ListView):
    template_name = 'admin/groups.html'
    context_object_name = 'groups'
    model = Group

class AdminCoursesView(LoginRequiredMixin, ListView):
    template_name = 'admin/courses.html'
    context_object_name = 'courses'
    model = Course

class AdminAttendanceView(LoginRequiredMixin, ListView):
    template_name = 'admin/attendance.html'
    context_object_name = 'attendances'
    model = Attendance

class AdminPaymentsView(LoginRequiredMixin, ListView):
    template_name = 'admin/payments.html'
    context_object_name = 'payments'
    model = Payment

class AdminScheduleView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/schedule.html'

class AdminTasksView(LoginRequiredMixin, ListView):
    template_name = 'admin/tasks.html'
    context_object_name = 'assignments'
    model = Assignment

class AdminResultsView(LoginRequiredMixin, ListView):
    template_name = 'admin/results.html'
    context_object_name = 'grades'
    model = Grade

class AdminSupportView(LoginRequiredMixin, ListView):
    template_name = 'admin/support.html'
    context_object_name = 'tickets'
    model = SupportTicket

class AdminReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/reports.html'

class AdminNotificationsView(LoginRequiredMixin, ListView):
    template_name = 'admin/notifications.html'
    context_object_name = 'notifications'
    model = Notification

class AdminSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/settings.html'

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('root_dispatch')
        else:
            try:
                user_obj = User.objects.get(username=u)
                if not user_obj.is_active:
                    return render(request, 'login.html', {'error': 'Sizning hisobingiz hali admin tomonidan tasdiqlanmagan.'})
            except User.DoesNotExist:
                pass
            return render(request, 'login.html', {'error': 'Login yoki parol noto\'g\'ri.'})
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        f = request.POST.get('first_name')
        l = request.POST.get('last_name')
        m = request.POST.get('middle_name')
        r = request.POST.get('role')
        
        if User.objects.filter(username=u).exists():
            return render(request, 'register.html', {'error': 'Bu foydalanuvchi nomi band.'})
            
        user = User.objects.create_user(
            username=u, 
            password=p, 
            first_name=f, 
            last_name=l, 
            middle_name=m, 
            role=r,
            is_active=False
        )
        return render(request, 'login.html', {'message': 'Ro\'yxatdan muvaffaqiyatli o\'tdingiz. Admin tasdiqlashini kuting!'})
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('login')

class TeacherDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'teacher/dashboard.html'
    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        teacher = self.request.user
        c['total_groups'] = Group.objects.filter(teacher=teacher).count()
        c['active_assignments'] = Assignment.objects.filter(teacher=teacher).count()
        c['recent_submissions'] = Submission.objects.filter(assignment__teacher=teacher).order_by('-submitted_at')[:5]
        return c

class TeacherGroupsView(LoginRequiredMixin, ListView):
    template_name = 'teacher/groups.html'
    context_object_name = 'groups'
    def get_queryset(self):
        return Group.objects.filter(teacher=self.request.user)

class TeacherAttendanceView(LoginRequiredMixin, ListView):
    template_name = 'teacher/attendance.html'
    context_object_name = 'groups'
    def get_queryset(self):
        return Group.objects.filter(teacher=self.request.user)

class TeacherTasksView(LoginRequiredMixin, ListView):
    template_name = 'teacher/tasks.html'
    context_object_name = 'assignments'
    def get_queryset(self):
        return Assignment.objects.filter(teacher=self.request.user)

class TeacherTaskCreateView(LoginRequiredMixin, CreateView):
    model = Assignment
    template_name = 'teacher/task_form.html'
    fields = ['group', 'title', 'description', 'file', 'due_date']
    success_url = reverse_lazy('teacher_tasks')
    
    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['group'].queryset = Group.objects.filter(teacher=self.request.user)
        # style fields with tailwind
        for name, field in form.fields.items():
            field.widget.attrs['class'] = 'w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-2'
        form.fields['due_date'].widget.input_type = 'datetime-local'
        return form

class TeacherGradesView(LoginRequiredMixin, ListView):
    template_name = 'teacher/grades.html'
    context_object_name = 'submissions'
    def get_queryset(self):
        return Submission.objects.filter(assignment__teacher=self.request.user)

class TeacherScheduleView(LoginRequiredMixin, TemplateView):
    template_name = 'teacher/schedule.html'

class TeacherMaterialsView(LoginRequiredMixin, ListView):
    template_name = 'teacher/materials.html'
    context_object_name = 'materials'
    def get_queryset(self):
        return Material.objects.filter(teacher=self.request.user)

class TeacherNotificationsView(LoginRequiredMixin, ListView):
    template_name = 'teacher/notifications.html'
    context_object_name = 'notifications'
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'student/dashboard.html'
    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        student = self.request.user
        c['my_courses_count'] = student.enrolled_groups.count()
        c['pending_tasks'] = Assignment.objects.filter(group__students=student).count() - Submission.objects.filter(student=student).count()
        c['unpaid_payments'] = Payment.objects.filter(user=student, status='pending').count()
        avg = Grade.objects.filter(student=student).aggregate(Sum('score'))['score__sum']
        c['overall_grade_avg'] = avg if avg else 0
        return c

class StudentCoursesView(LoginRequiredMixin, ListView):
    template_name = 'student/courses.html'
    context_object_name = 'groups'
    def get_queryset(self):
        return self.request.user.enrolled_groups.all()

class StudentAttendanceView(LoginRequiredMixin, ListView):
    template_name = 'student/attendance.html'
    context_object_name = 'attendances'
    def get_queryset(self):
        return Attendance.objects.filter(student=self.request.user)

class StudentTasksView(LoginRequiredMixin, ListView):
    template_name = 'student/tasks.html'
    context_object_name = 'assignments'
    def get_queryset(self):
        return Assignment.objects.filter(group__students=self.request.user)

class StudentGradesView(LoginRequiredMixin, ListView):
    template_name = 'student/grades.html'
    context_object_name = 'grades'
    def get_queryset(self):
        return Grade.objects.filter(student=self.request.user)

class StudentScheduleView(LoginRequiredMixin, TemplateView):
    template_name = 'student/schedule.html'

class StudentPaymentsView(LoginRequiredMixin, ListView):
    template_name = 'student/payments.html'
    context_object_name = 'payments'
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

class StudentMaterialsView(LoginRequiredMixin, ListView):
    template_name = 'student/materials.html'
    context_object_name = 'materials'
    def get_queryset(self):
        return Material.objects.filter(group__students=self.request.user)

class StudentResultsView(LoginRequiredMixin, TemplateView):
    template_name = 'student/results.html'

class StudentSupportView(LoginRequiredMixin, ListView):
    template_name = 'student/support.html'
    context_object_name = 'tickets'
    def get_queryset(self):
        return SupportTicket.objects.filter(user=self.request.user)
