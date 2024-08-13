from django.shortcuts import render
import locale
from .models import Homework,Teacher,Years
from django.utils import timezone
from babel.dates import format_date
import locale
from django.contrib import messages
from django.db.models import Case, When, Value
from datetime import timedelta
from .signals import delete_old_homeworks


def get_arabic_date(date):
    locale.setlocale(locale.LC_TIME, "ar_SA.utf8")
    formatted_date = format_date(date, format='long', locale='ar')
    return formatted_date



def get_homework(request, year):
    today = timezone.now().today().date()
    weekday_cases = Case(
        When(date__week_day=1, then=Value("Sunday")),
        When(date__week_day=2, then=Value("Monday")),
        When(date__week_day=3, then=Value("Tuesday")),
        When(date__week_day=4, then=Value("Wednesday")),
        When(date__week_day=5, then=Value("Thursday")),
    )

    arabic_dayes={
        "Sunday":"الأحد",
        "Monday":"الأثنين",
        "Tuesday":"الثلاثاء",
        "Wednesday":"الأربعاء",
        "Thursday":"الخميس",

    }
    day=request.GET.get('day')



    # حساب بداية ونهاية الأسبوع الحالي
    start_of_this_week = today - timedelta(days=today.weekday())
    end_of_this_week = start_of_this_week + timedelta(days=6)

    # حساب بداية ونهاية الأسبوع الماضي
    start_of_last_week = start_of_this_week - timedelta(weeks=1)
    end_of_last_week = start_of_last_week + timedelta(days=6)


    if not day:
        homeworks = Homework.objects.filter(year__year=year, date=today).order_by('date').order_by('-time')
        homeworks_last_week=[]
    else:
        homeworks = Homework.objects.annotate(day_name=weekday_cases).filter(day_name=day, year__year=year).filter(date__gte=start_of_this_week, date__lte=end_of_this_week).order_by('date').order_by('time')
        homeworks_last_week = Homework.objects.annotate(day_name=weekday_cases).filter(day_name=day, year__year=year).filter(date__gte=start_of_last_week, date__lte=end_of_last_week).order_by('date').order_by('time')
        
        
    for homework in homeworks:
        homework.arabic_date = get_arabic_date(homework.date)
    for homework in homeworks_last_week:
        homework.arabic_date = get_arabic_date(homework.date)
        
    context = {
        'homeworks': homeworks,
        'homeworks_last_week': homeworks_last_week,
        'year': year,
        'arabic_dayes': arabic_dayes.get(day,None),
    }
    return render(request, 'homework/homeworks.html', context)


def add_homework(request):
    years=Years.objects.all()
    if request.method == 'POST':
        teacher_number=request.POST['teacher_number']
        educational_level=request.POST['educational_level']
        homework=request.POST['homework']
        homework_img_1=request.FILES.get('homework-img-1',None)
        homework_img_2=request.FILES.get('homework-img-2',None)
        homework_img_3=request.FILES.get('homework-img-3',None)
        try:
            teacher=Teacher.objects.get(number=teacher_number)
            year=Years.objects.get(year=educational_level)
            Homework.objects.create(
                year=year,
                teacher=teacher,
                homework=homework,
                image_1=homework_img_1,
                image_2=homework_img_2,
                image_3=homework_img_3,
            )
            messages.success(request,'تم اضافة الواجب المنزلي بنجاح')
        except:
            messages.error(request,'تم ادخال رقم تعريفي خاطئ.')
        return render(request,'homework/add-homework.html',context={'years':years}) 
    else:
        return render(request,'homework/add-homework.html',context={'years':years}) 
    
