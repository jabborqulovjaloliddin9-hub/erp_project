from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'O\'qituvchi'),
        ('student', 'O\'quvchi'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Course(models.Model):
    STATUS_CHOICES = (
        ('active', 'Faol'),
        ('archive', 'Arxiv'),
        ('project', 'Loyiha'),
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    duration_months = models.IntegerField(default=1)
    category = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Group(models.Model):
    STATUS_CHOICES = (
        ('active', 'Faol'),
        ('finished', 'Yakunlangan'),
        ('pending', 'Kutilmoqda'),
    )
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='groups', null=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'teacher'}, related_name='teaching_groups')
    students = models.ManyToManyField(User, limit_choices_to={'role': 'student'}, related_name='enrolled_groups', blank=True)
    capacity = models.IntegerField(default=15)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    schedule = models.JSONField(null=True, blank=True, help_text='Dars kunlari va vaqtlari (Tuzilma: JSON)')
    room = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.name

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Keldi'),
        ('absent', 'Kelmadi'),
        ('late', 'Kech qoldi'),
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='marked_attendances')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group', 'student', 'date')

class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('paid', "To'langan"),
        ('overdue', 'Muddati o\'tgan'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    receipt_file = models.FileField(upload_to='receipts/', null=True, blank=True)

class Assignment(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='assignments')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='assignments/', null=True, blank=True)
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('assignment', 'student')

class Grade(models.Model):
    TYPE_CHOICES = (
        ('midterm', 'Oraliq'),
        ('final', 'Yakuniy'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='grades')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Material(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='materials')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_materials')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='materials/', null=True, blank=True)
    type = models.CharField(max_length=50, blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)

class SupportTicket(models.Model):
    STATUS_CHOICES = (
        ('open', 'Ochiq'),
        ('in_progress', 'Jarayonda'),
        ('resolved', 'Yopildi'),
    )
    PRIORITY_CHOICES = (
        ('low', 'Past'),
        ('medium', 'O\'rta'),
        ('high', 'Yuqori'),
        ('urgent', 'Shoshilinch'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    subject = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    type = models.CharField(max_length=50, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
