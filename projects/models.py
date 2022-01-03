from django.db import models
import uuid
from users.models import Profile
# Create your models here.


class Project(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(
        null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']
    
    def count_votes(self):
        total_votes = self.review_set.all().count()
        up_votes = self.review_set.filter(value="up").count()
        up_votes_ratio = (up_votes / total_votes) * 100
        self.vote_total = total_votes
        self.vote_ratio = up_votes_ratio    
        self.save()
    
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

class Tag(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'), # up for database and up Vote for frontend/form
        ('down', 'Down Vote'),
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=4, choices=VOTE_TYPE) # up or down
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [["owner", "project"]]
    
    def __str__(self):
        return self.value
