from django.db import models
from colorfield.fields import ColorField
import shortuuid
##adding bthe workspace created aoutamoticly when the 
class Workspace(models.Model):
    name = models.CharField(max_length=255, verbose_name="Workspace Name")
    sector = models.CharField(max_length=255)
    invite_code = models.CharField(max_length=22, unique=True, default=shortuuid.uuid, editable=False, verbose_name="Invite Code")

    def __str__(self):
        return self.name



class Member(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=255)
    workspace = models.ForeignKey(Workspace, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    device_token = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255)

    def __str__(self):
        return self.username


        
class Mission(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    title = models.CharField(max_length=255)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    ordered = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Task(models.Model):
    STATE_CHOICES = [
        ('missed', 'Missed'),
        ('complete', 'Complete'),
        ('incomplete', 'Incomplete'),
    ]

    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    state = models.CharField(max_length=10, choices=STATE_CHOICES)
    task_owner = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='tasks_owned')
    deadline = models.DateTimeField()
    file_attachment = models.FileField(null=True, blank=True)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    order_position = models.IntegerField()
    time_to_alert = models.DurationField(null=True, blank=True)  

    def calculate_alert_time(self):
        if self.deadline and self.time_to_alert:
            return self.deadline - self.time_to_alert
        return None

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField()
    employee = models.ForeignKey(Member, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    time_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.employee.full_name} on {self.task.title}"

class Category(models.Model):
    name = models.CharField(max_length=255)
    color = ColorField(default='#FF0000')  

    def __str__(self):
        return self.name