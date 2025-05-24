# profiles/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone
from profiles.models import Article, Subject, Teacher, Note, PDFBook, Video, Review, MeetupRequest, ContactMessage,Course,Gallery

def home_view(request):
    featured_articles = Article.objects.order_by('-created_at')[:3]
    subjects = Subject.objects.all()
    course=Course.objects.all()
    print(course)
    teacher = Teacher.objects.first()
    latest_notes = Note.objects.order_by('-uploaded_at')[:3]
    latest_books = PDFBook.objects.order_by('-uploaded_at')[:3]
    latest_videos = Video.objects.order_by('-uploaded_at')[:3]
    reviews = Review.objects.order_by('-submitted_at')[:3]
    latest_articles = Article.objects.order_by('-created_at')[:3]
    context = {
        'subjects': subjects,
        'courses':course,
        'featured_articles': featured_articles,
        'gallery_list':Gallery.objects.all().order_by('-created_at')[:10],
        'teacher': teacher,
        'latest_notes': latest_notes,
        'latest_books': latest_books,
        'latest_videos': latest_videos,
        'reviews': reviews,
        'latest_articles': latest_articles,
    }
    return render(request, 'pages/home.html', context)

def subject_detail_view(request, slug):
    subject = get_object_or_404(Subject, slug=slug)
    notes = Note.objects.filter(subject=subject).order_by('-uploaded_at')
    books = PDFBook.objects.filter(subject=subject).order_by('-uploaded_at')
    videos = Video.objects.filter(subject=subject).order_by('-uploaded_at')
    context = {
        'subject': subject,
        'notes': notes,
        'books': books,
        'videos': videos,
        'subjects': Subject.objects.all()[:3],
        'teacher': Teacher.objects.first(),
    }
    return render(request, 'pages/subject_detail.html', context)

def note_detail_view(request, slug):
    note = get_object_or_404(Note, slug=slug)
    context = {
        'note': note,
        'subjects': Subject.objects.all()[:3],
        'teacher': Teacher.objects.first(),
    }
    return render(request, 'pages/note_detail.html', context)

def book_detail_view(request, slug):
    book = get_object_or_404(PDFBook, slug=slug)
    context = {
        'book': book,
        'subjects': Subject.objects.all()[:3],
        'teacher': Teacher.objects.first(),
    }
    return render(request, 'pages/book_detail.html', context)

def article_detail_view(request, slug):
    article = get_object_or_404(Article, slug=slug)
    context = {
        'article': article,
        'subjects': Subject.objects.all()[:3],
        'teacher': Teacher.objects.first(),
    }
    return render(request, 'pages/article_detail.html', context)

def course_detail_view(request, slug):
    course = get_object_or_404(Course, slug=slug)
    subjects = course.subjects.all()
    # Aggregate resources for all subjects
    notes = Note.objects.filter(subject__in=subjects)
    videos = Video.objects.filter(subject__in=subjects)
    books = PDFBook.objects.filter(subject__in=subjects)
    context = {
        'course': course,
        'subjects': subjects,
        'notes': notes,
        'videos': videos,
        'books': books,
        'teacher': Teacher.objects.first(),
    }
    return render(request, 'pages/resources.html', context)

def articles_view(request):
    articles = Article.objects.order_by('-created_at')[:10]
    context = {
        'articles': articles,
        'subjects': Subject.objects.all()[:3],
        'teacher': Teacher.objects.first(),
    }
    return render(request, 'pages/articles.html', context)

def about_view(request):
    teacher = Teacher.objects.first()
    subjects = Subject.objects.all()[:3]
    reviews = Review.objects.order_by('-submitted_at')[:3]
    context = {
        'teacher': teacher,
        'subjects': subjects,
        'reviews': reviews,
    }
    return render(request, 'pages/about.html', context)

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Validation
        if not name or not email or not message:
            messages.error(request, "All fields are required.")
        else:
            try:
                validate_email(email)
                teacher = Teacher.objects.first()
                ContactMessage.objects.create(
                    teacher=teacher,
                    name=name,
                    email=email,
                    message=message,
                )
                messages.success(request, "Your message has been sent successfully!")
                return redirect('contact')
            except ValidationError:
                messages.error(request, "Please enter a valid email address.")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        
        # Re-render form with errors
        context = {
            'subjects': Subject.objects.all()[:3],
            'teacher': Teacher.objects.first(),
            'form_data': {'name': name, 'email': email, 'message': message},
        }
        return render(request, 'pages/contact.html', context)
    
    context = {
        'subjects': Subject.objects.all()[:3],
        'teacher': Teacher.objects.first(),
    }
    return render(request, 'pages/contact.html', context)

def meetup_request_view(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name', '').strip()
        contact_email = request.POST.get('contact_email', '').strip()
        message = request.POST.get('message', '').strip()
        preferred_date = request.POST.get('preferred_date', '').strip()
        preferred_time = request.POST.get('preferred_time', '').strip()
        
        # Validation
        errors = []
        if not student_name or not contact_email or not message or not preferred_date or not preferred_time:
            errors.append("All fields are required.")
        try:
            validate_email(contact_email)
        except ValidationError:
            errors.append("Please enter a valid email address.")
        try:
            preferred_date_obj = timezone.datetime.strptime(preferred_date, '%Y-%m-%d').date()
            if preferred_date_obj < timezone.now().date():
                errors.append("Preferred date must be in the future.")
        except ValueError:
            errors.append("Invalid date format.")
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            try:
                teacher = Teacher.objects.first()
                MeetupRequest.objects.create(
                    teacher=teacher,
                    student_name=student_name,
                    contact_email=contact_email,
                    message=message,
                    preferred_date=preferred_date,
                    preferred_time=preferred_time,
                )
                messages.success(request, "Your meetup request has been submitted successfully!")
                return redirect('meetup_request')
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        
        # Re-render form with errors
        context = {
            'subjects': Subject.objects.all()[:3],
            'teacher': Teacher.objects.first(),
            'form_data': {
                'student_name': student_name,
                'contact_email': contact_email,
                'message': message,
                'preferred_date': preferred_date,
                'preferred_time': preferred_time,
            },
        }
        return render(request, 'pages/meetup_request.html', context)
    
    context = {
        'subjects': Subject.objects.all()[:3],
        'teacher': Teacher.objects.first(),
    }
    return render(request, 'pages/meetup_request.html', context)



# profiles/views.py
def blogs_view(request):
    videos = Video.objects.all()
    subjects = Subject.objects.all()
    context = {
        'videos': videos,
        'subjects': subjects,
        'teacher': Teacher.objects.first(),
    }
    return render(request, 'pages/blogs.html', context)



from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count

def gallery_list_view(request):
    """
    Display paginated gallery with filtering capabilities
    """
    # Get filter parameters
    category_filter = request.GET.get('category', 'all')
    search_query = request.GET.get('search', '')
    page = request.GET.get('page', 1)
    per_page = int(request.GET.get('per_page', 12))
    
    # Base queryset - only published items
    gallery_items = Gallery.objects.filter(is_published=True).select_related().order_by('-created_at')
    
    # Apply category filter
    if category_filter and category_filter != 'all':
        gallery_items = gallery_items.filter(category=category_filter)
    
    # Apply search filter
    if search_query:
        gallery_items = gallery_items.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Get category statistics
    category_stats = Gallery.objects.filter(is_published=True).values('category').annotate(
        count=Count('category')
    ).order_by('category')
    
    # Pagination
    paginator = Paginator(gallery_items, per_page)
    
    try:
        gallery_page = paginator.page(page)
    except PageNotAnInteger:
        gallery_page = paginator.page(1)
    except EmptyPage:
        gallery_page = paginator.page(paginator.num_pages)
    
    # Prepare context
    context = {
        'gallery_items': gallery_page,
        'category_stats': category_stats,
        'current_category': category_filter,
        'search_query': search_query,
        'total_items': paginator.count,
        'categories': Gallery.GALLERY_CATEGORY,
        'has_next': gallery_page.has_next(),
        'has_previous': gallery_page.has_previous(),
        'page_range': paginator.get_elided_page_range(gallery_page.number, on_each_side=2, on_ends=1)
    }
    
    return render(request, 'pages/gallery.html', context)