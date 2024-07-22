from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from .models import Competitors



def competitions (request):
    if request.method == 'POST':
        # games 
        memory_game_flips=request.POST['memory_game_flips']
        puzzle_game_flips=request.POST['puzzle_game_flips']
        questions_game_worng=request.POST['questions_game_worng']
        # games 
        name=request.POST['comp_name']
        email=request.POST['comp_email']
        if Competitors.objects.filter(email__iexact=email).exists():
            plyer=Competitors.objects.get(email__iexact=email)
            plyer.score=int(memory_game_flips+puzzle_game_flips+questions_game_worng)
            plyer.save()
        else:
            Competitors.objects.create(
                name=name,
                email=email,
                score=int(memory_game_flips+puzzle_game_flips+questions_game_worng)
                )
        rankink=1
        for i in Competitors.objects.filter(score__lt=Competitors.objects.get(email__iexact=email).score):
            rankink+=1
            

        mail_supject='نتائجك في اخر مسابقه في ازاد'
        message=render_to_string('email.html',{
            'name':name,
            'memory_game_flips':memory_game_flips,
            'puzzle_game_flips':puzzle_game_flips,
            'questions_game_worng':10 - int(questions_game_worng),
            'rankink':rankink,
            })
        
        platn=strip_tags(message)

        to_email=email
        from_email=settings.EMAIL_HOST_USER

        mess=EmailMultiAlternatives(subject=mail_supject,body=platn,from_email=from_email,to=[to_email])
        mess.attach_alternative(message,'text/html')
        mess.send()
        return redirect('competition:competitions')
    else:
        return render(request,'competitions/competitions.html')


