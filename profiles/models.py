# profiles/models.py
from django.db import models
from django.utils.text import slugify
import re

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} at {self.submitted_at}"

    class Meta:
        ordering = ['-submitted_at']

# Existing models (for reference, no changes needed)
class Teacher(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='teachers/', blank=True, null=True)
    bio = models.TextField()
    experience_years = models.PositiveIntegerField()
    contact_email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    address = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.get_full_name())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.get_full_name()


class Course(models.Model):
    COURSE_YEARS = [
        ('All Year', 'All Year'),
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year'),
    ]
    name = models.CharField(max_length=100, unique=True)
    year = models.CharField(max_length=20, choices=COURSE_YEARS,null=True,blank=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects',null=True,blank=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.course.name}-{self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} "


class Note(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    cover_image=models.ImageField(upload_to='notes/',null=True,blank=True)
    content = models.TextField()
    file = models.FileField(upload_to='notes/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.subject.name}-{self.title}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Video(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    embed_code = models.TextField(blank=True)
    image = models.URLField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if self.video_url:
            youtube_regex = (
                r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
            )
            match = re.match(youtube_regex, self.video_url)
            if match:
                video_id = match.group(1)
                self.embed_code = (
                    f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" '
                    f'title="YouTube video player" frameborder="0" '
                    f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
                    f'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'
                )
                self.image = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        if not self.slug:
            self.slug = slugify(f"{self.subject.name}-{self.title}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class PDFBook(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    cover_image=models.ImageField(upload_to='pdfbook/',null=True,blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    file = models.FileField(upload_to='books/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.subject.name}-{self.title}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Article(models.Model):
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='articles/', blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class MeetupRequest(models.Model):
    student_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    message = models.TextField()
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    is_approved = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Meetup request from {self.student_name}"

class Review(models.Model):

    student_name = models.CharField(max_length=100)
    rating = models.PositiveIntegerField()  # 1 to 5
    comment = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.student_name}"



class Gallery(models.Model):
    
    
    GALLERY_CATEGORY = [
    ('program', 'Program'),
    ('event', 'Event'),
    ('education', 'Education'),
    ('achievement', 'Achievement'),
    ('training', 'Training'),
    ('workshop', 'Workshop'),
    ('seminar', 'Seminar'),
    ('other', 'Other'),
]
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=50, choices=GALLERY_CATEGORY)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
