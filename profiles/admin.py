# profiles/admin.py
from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db import models
from ckeditor.widgets import CKEditorWidget
from .models import Teacher, Subject, Note, Video, PDFBook, Article, MeetupRequest, Review, ContactMessage, Course, Gallery
import re

# Custom Admin Site Configuration
admin.site.site_header = "Educational Platform Administration"
admin.site.site_title = "EduPlatform Admin"
admin.site.index_title = "Welcome to Educational Platform Dashboard"

# ==========================================
# SECTION 1: CORE ACADEMIC STRUCTURE
# ==========================================

class RichTextAdminForm(forms.ModelForm):
    """Enhanced form with rich text editing capabilities"""
    class Meta:
        widgets = {
            'bio': CKEditorWidget(config_name='default'),
            'content': CKEditorWidget(config_name='default'),
            'comment': CKEditorWidget(config_name='default'),
        }

class SubjectInline(admin.TabularInline):
    """Inline editing for subjects within courses"""
    model = Subject
    extra = 1
    fields = ('name', 'slug')
    readonly_fields = ('slug',)
    help_text = "Add subjects that belong to this course."

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """📚 Course Management - Create and organize academic programs"""
    inlines = [SubjectInline]
    list_display = ('name', 'year', 'get_subjects_count', 'slug')
    search_fields = ('name', 'description')
    prepopulated_fields = {"slug": ("name",)}
    
    fieldsets = (
        ('📚 Course Information', {
            'fields': ('name', 'year', 'description',),
            'description': 'Define the main academic program structure.'
        }),
        ('🔗 URL Settings', {
            'fields': ('slug',),
            'description': 'URL-friendly version of the course name (auto-generated).',
            'classes': ('collapse',)
        }),
    )
    
    class Meta:
        verbose_name = "📚 Course"
        verbose_name_plural = "📚 Courses"
    
    def get_subjects_count(self, obj):
        return obj.subjects.count()
    get_subjects_count.short_description = 'Number of Subjects'

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """📖 Subject Management - Organize course subjects"""
    list_display = ('name', 'course', 'get_materials_count', 'slug')
    list_display_links = ('name',)
    search_fields = ('name', 'course__name')
    list_filter = ('course',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('course__name', 'name')
    
    fieldsets = (
        ('📖 Subject Details', {
            'fields': ('course', 'name'),
            'description': 'Associate this subject with a course and provide a descriptive name.'
        }),
        ('🔗 URL Settings', {
            'fields': ('slug',),
            'description': 'URL-friendly identifier (auto-generated).',
            'classes': ('collapse',)
        }),
    )
    
    class Meta:
        verbose_name = "📖 Subject"
        verbose_name_plural = "📖 Subjects"
    
    def get_materials_count(self, obj):
        notes_count = obj.note_set.count()
        videos_count = obj.video_set.count()
        books_count = obj.pdfbook_set.count()
        return f"{notes_count + videos_count + books_count} items"
    get_materials_count.short_description = 'Learning Materials'

# ==========================================
# SECTION 2: TEACHING STAFF
# ==========================================

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """👨‍🏫 Teacher Profiles - Manage teaching staff information"""
    form = RichTextAdminForm
    list_display = ('full_name', 'experience_years', 'contact_email', 'phone', 'get_subjects_count')
    list_display_links = ('full_name',)
    search_fields = ('user__first_name', 'user__last_name', 'contact_email', 'bio')
    list_filter = ('experience_years',)
    ordering = ('user__first_name', 'user__last_name')
    
    fieldsets = (
        ('👤 Basic Information', {
            'fields': ('user', 'photo', 'bio'),
            'description': 'Basic teacher profile information including photo and biography.'
        }),
        ('🎓 Professional Details', {
            'fields': ('experience_years',),
            'description': 'Professional experience and qualifications.'
        }),
        ('📞 Contact Information', {
            'fields': ('contact_email', 'phone', 'address'),
            'description': 'Contact details for students and administration.'
        }),
        ('🌐 Social Media Links', {
            'fields': ('linkedin', 'facebook', 'instagram'),
            'description': 'Optional social media profiles (leave blank if not applicable).',
            'classes': ('collapse',)
        }),
        ('⚙️ System Fields', {
            'fields': ('slug',),
            'description': 'Auto-generated system fields.',
            'classes': ('collapse',)
        }),
    )
    
    class Meta:
        verbose_name = "👨‍🏫 Teacher"
        verbose_name_plural = "👨‍🏫 Teachers"
    
    readonly_fields = ('slug', 'get_subjects_count')
    
    def full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    full_name.short_description = 'Teacher Name'
    full_name.admin_order_field = 'user__first_name'
    
    def get_subjects_count(self, obj):
        return "N/A"  # Implement based on your actual relationships
    get_subjects_count.short_description = 'Subjects Teaching'

# ==========================================
# SECTION 3: LEARNING MATERIALS
# ==========================================

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """📝 Study Notes - Manage written learning materials"""
    form = RichTextAdminForm
    list_display = ('title', 'subject', 'uploaded_at', 'cover_image_preview', 'has_file')
    list_display_links = ('title',)
    search_fields = ('title', 'subject__name', 'content')
    list_filter = ('subject', 'uploaded_at', 'subject__course')
    date_hierarchy = 'uploaded_at'
    ordering = ('-uploaded_at',)
    
    readonly_fields = ('slug', 'uploaded_at', 'cover_image_preview')
    
    fieldsets = (
        ('📝 Content', {
            'fields': ('title', 'subject', 'content'),
            'description': 'Main content of the note. Use the rich text editor for formatting.'
        }),
        ('🎨 Files & Media', {
            'fields': ('cover_image', 'cover_image_preview', 'file'),
            'description': 'Optional cover image and downloadable file attachment.'
        }),
        ('ℹ️ Metadata', {
            'fields': ('slug', 'uploaded_at'),
            'description': 'System-generated information.',
            'classes': ('collapse',)
        }),
    )

    class Meta:
        verbose_name = "📝 Study Note"
        verbose_name_plural = "📝 Study Notes"

    def cover_image_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" width="150" height="auto" style="max-height: 100px; border-radius: 4px;" />',
                obj.cover_image.url
            )
        return mark_safe('<span style="color: #999;">No cover image</span>')
    cover_image_preview.short_description = 'Cover Image Preview'
    
    def has_file(self, obj):
        if obj.file:
            return format_html('<span style="color: green;">✓ File attached</span>')
        return format_html('<span style="color: #999;">No file</span>')
    has_file.short_description = 'Attachment'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('subject', 'subject__course')

class VideoAdminForm(forms.ModelForm):
    """Custom form for video validation with helpful error messages"""
    class Meta:
        model = Video
        fields = '__all__'
        help_texts = {
            'video_url': 'Enter a valid YouTube URL (e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ or https://youtu.be/dQw4w9WgXcQ)',
            'title': 'Enter a descriptive title for your video lesson',
            'subject': 'Select the subject this video belongs to',
        }

    def clean_video_url(self):
        url = self.cleaned_data['video_url']
        youtube_regex = (
            r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[a-zA-Z0-9_-]{11}'
        )
        if not re.match(youtube_regex, url):
            raise forms.ValidationError(
                "Please enter a valid YouTube URL. Supported formats:\n"
                "• https://www.youtube.com/watch?v=VIDEO_ID\n"
                "• https://youtu.be/VIDEO_ID"
            )
        return url

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """🎥 Video Lessons - Manage educational video content"""
    form = VideoAdminForm
    list_display = ('title', 'subject', 'video_thumbnail', 'uploaded_at')
    list_display_links = ('title',)
    search_fields = ('title', 'subject__name')
    list_filter = ('subject', 'uploaded_at', 'subject__course')
    date_hierarchy = 'uploaded_at'
    ordering = ('-uploaded_at',)
    
    readonly_fields = ('slug', 'uploaded_at', 'embed_preview', 'video_thumbnail')
    
    fieldsets = (
        ('🎥 Video Information', {
            'fields': ('title', 'subject', 'video_url'),
            'description': 'Enter video details and a valid YouTube URL.'
        }),
        ('🖼️ Generated Content', {
            'fields': ('embed_preview', 'video_thumbnail'),
            'description': 'Auto-generated embed code and thumbnail (read-only).',
            'classes': ('collapse',)
        }),
        ('ℹ️ Metadata', {
            'fields': ('slug', 'uploaded_at'),
            'description': 'System information.',
            'classes': ('collapse',)
        }),
    )
    
    class Meta:
        verbose_name = "🎥 Video Lesson"
        verbose_name_plural = "🎥 Video Lessons"
    
    def embed_preview(self, obj):
        if obj.embed_code:
            return format_html(
                '<div style="max-width: 300px;">{}</div>',
                obj.embed_code.replace('width="560" height="315"', 'width="300" height="169"')
            )
        return "No embed code generated"
    embed_preview.short_description = 'Video Preview'
    
    def video_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="120" height="auto" style="border-radius: 4px;" />',
                obj.image
            )
        return "No thumbnail"
    video_thumbnail.short_description = 'Thumbnail'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('subject', 'subject__course')

@admin.register(PDFBook)
class PDFBookAdmin(admin.ModelAdmin):
    """📚 Digital Books - Manage PDF textbooks and references"""
    form = RichTextAdminForm
    list_display = ('title', 'subject', 'uploaded_at', 'cover_image_preview', 'file_info')
    list_display_links = ('title',)
    search_fields = ('title', 'subject__name', 'content')
    list_filter = ('subject', 'uploaded_at', 'subject__course')
    date_hierarchy = 'uploaded_at'
    ordering = ('-uploaded_at',)
    
    readonly_fields = ('slug', 'uploaded_at', 'cover_image_preview', 'file_info')
    
    fieldsets = (
        ('📚 Book Information', {
            'fields': ('title', 'subject', 'content'),
            'description': 'Book details and description. Use the rich text editor for detailed content formatting.'
        }),
        ('📁 Files & Media', {
            'fields': ('cover_image', 'cover_image_preview', 'file', 'file_info'),
            'description': 'Upload the PDF file and an optional cover image.'
        }),
        ('ℹ️ Metadata', {
            'fields': ('slug', 'uploaded_at'),
            'description': 'System-generated information.',
            'classes': ('collapse',)
        }),
    )

    class Meta:
        verbose_name = "📚 Digital Book"
        verbose_name_plural = "📚 Digital Books"

    def cover_image_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" width="150" height="auto" style="max-height: 120px; border-radius: 4px;" />',
                obj.cover_image.url
            )
        return mark_safe('<span style="color: #999;">No cover image</span>')
    cover_image_preview.short_description = 'Cover Preview'
    
    def file_info(self, obj):
        if obj.file:
            try:
                size = obj.file.size
                size_mb = round(size / (1024 * 1024), 2)
                return format_html(
                    '<span style="color: green;">✓ PDF uploaded</span><br>'
                    '<small>Size: {} MB</small>',
                    size_mb
                )
            except:
                return format_html('<span style="color: green;">✓ PDF uploaded</span>')
        return format_html('<span style="color: red;">No PDF file</span>')
    file_info.short_description = 'File Status'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('subject', 'subject__course')

# ==========================================
# SECTION 4: CONTENT & MEDIA
# ==========================================

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """📰 Articles & Blogs - Manage educational articles and blog posts"""
    form = RichTextAdminForm
    list_display = ('title', 'created_at', 'updated_at', 'thumbnail_preview')
    list_display_links = ('title',)
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    readonly_fields = ('slug', 'created_at', 'updated_at', 'thumbnail_preview')
    
    fieldsets = (
        ('📰 Article Content', {
            'fields': ('title', 'thumbnail', 'thumbnail_preview', 'content'),
            'description': 'Create engaging articles with rich content formatting.'
        }),
        ('ℹ️ Metadata', {
            'fields': ('slug', 'created_at', 'updated_at'),
            'description': 'System timestamps and URL identifier.',
            'classes': ('collapse',)
        }),
    )
    
    class Meta:
        verbose_name = "📰 Article"
        verbose_name_plural = "📰 Articles & Blogs"
    
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="150" height="auto" style="max-height: 100px; border-radius: 4px;" />',
                obj.thumbnail.url
            )
        return mark_safe('<span style="color: #999;">No thumbnail</span>')
    thumbnail_preview.short_description = 'Thumbnail Preview'

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    """🖼️ Photo Gallery - Manage institutional photos and media"""
    list_display = ('title', 'category', 'created_at', 'is_published')
    list_filter = ('category', 'created_at', 'is_published')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('🖼️ Gallery Item', {
            'fields': ('title', 'slug', 'category', 'image', 'description', 'is_published')
        }),
        ('📅 Timestamps', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )
    
    class Meta:
        verbose_name = "🖼️ Gallery Item"
        verbose_name_plural = "🖼️ Photo Gallery"
    
    readonly_fields = ('created_at', 'updated_at')

# ==========================================
# SECTION 5: STUDENT INTERACTIONS
# ==========================================

@admin.register(MeetupRequest)
class MeetupRequestAdmin(admin.ModelAdmin):
    """🤝 Meeting Requests - Handle student meeting appointments"""
    list_display = ('student_name', 'contact_email', 'preferred_date', 'preferred_time', 'approval_status', 'submitted_at')
    list_display_links = ('student_name',)
    search_fields = ('student_name', 'contact_email', 'message')
    list_filter = ('is_approved', 'submitted_at', 'preferred_date')
    date_hierarchy = 'submitted_at'
    ordering = ('-submitted_at',)
    
    readonly_fields = ('submitted_at',)
    
    fieldsets = (
        ('👤 Student Information', {
            'fields': ('student_name', 'contact_email'),
            'description': 'Contact details of the student requesting the meetup.'
        }),
        ('🤝 Meetup Details', {
            'fields': ('message', 'preferred_date', 'preferred_time'),
            'description': 'Student\'s message and preferred meeting schedule.'
        }),
        ('✅ Administrative', {
            'fields': ('is_approved',),
            'description': 'Approve or reject this meetup request.'
        }),
        ('ℹ️ Metadata', {
            'fields': ('submitted_at',),
            'description': 'When this request was submitted.',
            'classes': ('collapse',)
        }),
    )
    
    class Meta:
        verbose_name = "🤝 Meeting Request"
        verbose_name_plural = "🤝 Meeting Requests"
    
    actions = ['approve_meetups', 'reject_meetups']
    
    def approval_status(self, obj):
        if obj.is_approved:
            return format_html('<span style="color: green; font-weight: bold;">✓ Approved</span>')
        else:
            return format_html('<span style="color: orange; font-weight: bold;">⏳ Pending</span>')
    approval_status.short_description = 'Status'

    def approve_meetups(self, request, queryset):
        count = queryset.update(is_approved=True)
        self.message_user(request, f'{count} meetup request(s) approved successfully.')
    approve_meetups.short_description = "✓ Approve selected meetup requests"

    def reject_meetups(self, request, queryset):
        count = queryset.update(is_approved=False)
        self.message_user(request, f'{count} meetup request(s) rejected.')
    reject_meetups.short_description = "✗ Reject selected meetup requests"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """⭐ Student Reviews - Manage feedback and ratings"""
    form = RichTextAdminForm
    list_display = ('student_name', 'rating_stars', 'submitted_at', 'comment_preview')
    list_display_links = ('student_name',)
    search_fields = ('student_name', 'comment')
    list_filter = ('rating', 'submitted_at')
    date_hierarchy = 'submitted_at'
    ordering = ('-submitted_at',)
    
    readonly_fields = ('submitted_at', 'rating_stars')
    
    fieldsets = (
        ('⭐ Review Details', {
            'fields': ('student_name', 'rating', 'rating_stars', 'comment'),
            'description': 'Student feedback and rating.'
        }),
        ('ℹ️ Metadata', {
            'fields': ('submitted_at',),
            'description': 'When this review was submitted.',
            'classes': ('collapse',)
        }),
    )
    
    class Meta:
        verbose_name = "⭐ Student Review"
        verbose_name_plural = "⭐ Student Reviews"
    
    def rating_stars(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        color = 'green' if obj.rating >= 4 else 'orange' if obj.rating >= 3 else 'red'
        return format_html(
            '<span style="color: {}; font-size: 16px;">{}</span> ({})',
            color, stars, obj.rating
        )
    rating_stars.short_description = 'Rating'
    
    def comment_preview(self, obj):
        if len(obj.comment) > 50:
            return obj.comment[:50] + "..."
        return obj.comment
    comment_preview.short_description = 'Comment Preview'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """📧 Contact Messages - Handle general inquiries and messages"""
    list_display = ('name', 'email', 'submitted_at', 'message_preview')
    list_display_links = ('name',)
    search_fields = ('name', 'email', 'message')
    list_filter = ('submitted_at',)
    date_hierarchy = 'submitted_at'
    ordering = ('-submitted_at',)
    
    readonly_fields = ('submitted_at',)
    
    fieldsets = (
        ('👤 Contact Information', {
            'fields': ('name', 'email'),
            'description': 'Details of the person who sent this message.'
        }),
        ('📧 Message Content', {
            'fields': ('message',),
            'description': 'The message content sent through the contact form.'
        }),
        ('ℹ️ Metadata', {
            'fields': ('submitted_at',),
            'description': 'When this message was received.',
            'classes': ('collapse',)
        }),
    )
    
    class Meta:
        verbose_name = "📧 Contact Message"
        verbose_name_plural = "📧 Contact Messages"
    
    def message_preview(self, obj):
        if len(obj.message) > 60:
            return obj.message[:60] + "..."
        return obj.message
    message_preview.short_description = 'Message Preview'

# ==========================================
# CUSTOM ADMIN SITE ORGANIZATION
# ==========================================

# Custom admin site class to organize app sections
class CustomAdminSite(admin.AdminSite):
    site_header = "📚 Educational Platform Administration"
    site_title = "EduPlatform Admin"
    index_title = "Welcome to Educational Platform Dashboard"
    
    def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        
        This method organizes models into logical sections for better UX.
        """
        app_dict = {}
        
        # Define custom sections
        sections = {
            '📚 Academic Structure': [
                'Course', 'Subject'
            ],
            '👨‍🏫 Teaching Staff': [
                'Teacher'
            ],
            '📝 Learning Materials': [
                'Note', 'Video', 'PDFBook'
            ],
            '🎨 Content & Media': [
                'Article', 'Gallery'
            ],
            '👥 Student Interactions': [
                'MeetupRequest', 'Review', 'ContactMessage'
            ]
        }
        
        # Get the default app list
        original_app_list = super().get_app_list(request, app_label)
        
        # Reorganize into custom sections
        for section_name, model_names in sections.items():
            models = []
            for app in original_app_list:
                if app['app_label'] == 'profiles':  # Adjust to your app name
                    for model in app['models']:
                        model_name = model['object_name']
                        if model_name in model_names:
                            models.append(model)
            
            if models:
                app_dict[section_name] = {
                    'name': section_name,
                    'app_label': section_name.lower().replace(' ', '_'),
                    'models': models,
                    'has_module_perms': True,
                }
        
        return list(app_dict.values())

# Uncomment the following lines if you want to use the custom admin site
custom_admin_site = CustomAdminSite(name='custom_admin')

# Register all models with the custom admin site
custom_admin_site.register(Course, CourseAdmin)
custom_admin_site.register(Subject, SubjectAdmin)
custom_admin_site.register(Teacher, TeacherAdmin)
custom_admin_site.register(Note, NoteAdmin)
custom_admin_site.register(Video, VideoAdmin)
custom_admin_site.register(PDFBook, PDFBookAdmin)
custom_admin_site.register(Article, ArticleAdmin)
custom_admin_site.register(Gallery, GalleryAdmin)
custom_admin_site.register(MeetupRequest, MeetupRequestAdmin)
custom_admin_site.register(Review, ReviewAdmin)
custom_admin_site.register(ContactMessage, ContactMessageAdmin)