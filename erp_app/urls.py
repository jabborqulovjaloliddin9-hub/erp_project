from django.urls import path
from .views import (RootDispatchView, PlaceholderView, AdminDashboardView, AdminUsersView, 
                    AdminGroupsView, AdminCoursesView, AdminAttendanceView, AdminPaymentsView,
                    AdminScheduleView, AdminTasksView, AdminResultsView, AdminSupportView, 
                    AdminReportsView, AdminNotificationsView, AdminSettingsView,
                    TeacherDashboardView, TeacherGroupsView, TeacherAttendanceView, TeacherTasksView, TeacherTaskCreateView,
                    TeacherGradesView, TeacherScheduleView, TeacherMaterialsView, TeacherNotificationsView,
                    StudentDashboardView, StudentCoursesView, StudentAttendanceView, StudentTasksView,
                    StudentGradesView, StudentScheduleView, StudentPaymentsView, StudentMaterialsView,
                    StudentResultsView, StudentSupportView, login_view, register_view, logout_view)

urlpatterns = [
    # Auth
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    
    # Root dispatcher
    path('', RootDispatchView.as_view(), name='root_dispatch'),
    
    # ADMIN ROUTES
    path('admin-panel/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin-panel/users/', AdminUsersView.as_view(), name='admin_users'),
    path('admin-panel/groups/', AdminGroupsView.as_view(), name='admin_groups'),
    path('admin-panel/courses/', AdminCoursesView.as_view(), name='admin_courses'),
    path('admin-panel/attendance/', AdminAttendanceView.as_view(), name='admin_attendance'),
    path('admin-panel/payments/', AdminPaymentsView.as_view(), name='admin_payments'),
    path('admin-panel/schedule/', AdminScheduleView.as_view(), name='admin_schedule'),
    path('admin-panel/tasks/', AdminTasksView.as_view(), name='admin_tasks'),
    path('admin-panel/results/', AdminResultsView.as_view(), name='admin_results'),
    path('admin-panel/support/', AdminSupportView.as_view(), name='admin_support'),
    path('admin-panel/reports/', AdminReportsView.as_view(), name='admin_reports'),
    path('admin-panel/notifications/', AdminNotificationsView.as_view(), name='admin_notifications'),
    path('admin-panel/settings/', AdminSettingsView.as_view(), name='admin_settings'),
    
    # TEACHER ROUTES
    path('teacher/dashboard/', TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('teacher/groups/', TeacherGroupsView.as_view(), name='teacher_groups'),
    path('teacher/attendance/', TeacherAttendanceView.as_view(), name='teacher_attendance'),
    path('teacher/tasks/', TeacherTasksView.as_view(), name='teacher_tasks'),
    path('teacher/tasks/add/', TeacherTaskCreateView.as_view(), name='teacher_task_add'),
    path('teacher/grades/', TeacherGradesView.as_view(), name='teacher_grades'),
    path('teacher/schedule/', TeacherScheduleView.as_view(), name='teacher_schedule'),
    path('teacher/materials/', TeacherMaterialsView.as_view(), name='teacher_materials'),
    path('teacher/notifications/', TeacherNotificationsView.as_view(), name='teacher_notifications'),
    
    # STUDENT ROUTES
    path('student/dashboard/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('student/courses/', StudentCoursesView.as_view(), name='student_courses'),
    path('student/attendance/', StudentAttendanceView.as_view(), name='student_attendance'),
    path('student/tasks/', StudentTasksView.as_view(), name='student_tasks'),
    path('student/grades/', StudentGradesView.as_view(), name='student_grades'),
    path('student/schedule/', StudentScheduleView.as_view(), name='student_schedule'),
    path('student/payments/', StudentPaymentsView.as_view(), name='student_payments'),
    path('student/materials/', StudentMaterialsView.as_view(), name='student_materials'),
    path('student/results/', StudentResultsView.as_view(), name='student_results'),
    path('student/support/', StudentSupportView.as_view(), name='student_support'),
]
