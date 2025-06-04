from profiles.models import Subject , Course, Teacher

def navbar(request):
    teacher=Teacher.objects.all().first()
    
    # profile_img=teacher.
    return {
        'profile_image':teacher.photo,
        'subjects_list':Subject.objects.all(),
        'course_list':Course.objects.all()
    }