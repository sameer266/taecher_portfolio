from profiles.models import Subject , Course

def navbar(request):
    return {
        'subjects_list':Subject.objects.all(),
        'course_list':Course.objects.all()
    }