from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives



def competitions (request):
    if request.method == 'POST':
        name=request.POST['comp_name']
        email=request.POST['comp_email']
        memory_game_flips=request.POST['memory_game_flips']


        mail_supject='نتائجك في اخر مسابقه في ازاد'
        message=render_to_string('email.html',{
            'name':name,
            'memory_game_flips':memory_game_flips,
            })
        
        platn=strip_tags(message)

        to_email=email
        from_email=settings.EMAIL_HOST_USER

        mess=EmailMultiAlternatives(subject=mail_supject,body=platn,from_email=from_email,to=[to_email])
        mess.attach_alternative(message,'text/html')
        # mess.send()
        return redirect('competition:competitions')
    else:
        return render(request,'competitions.html')


