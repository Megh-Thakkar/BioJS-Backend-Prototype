from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import JsonResponse
from .models import *
import re
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
import sendgrid
import os
from sendgrid.helpers.mail import *
from django.contrib.auth.decorators import login_required
import requests
from django.contrib import messages
from BioJS import settings
from wsgiref.util import FileWrapper
from BioJS.keyconfig import API_KEY

def home(request):
    if request.user.is_authenticated():
        try:
            user_p = UserProfile.objects.get(user=request.user)
        except:
            logout(request)
            return redirect('main:home')
        rows = [{'data':[component.name,component.ratings, component.download_set.all().count()],'link':[{'title':component.github_url, 'url':get_component_url(component)},{'title':component.user_p.name, 'url':reverse('main:get_profile', kwargs={'u_id':component.user_p.id})},{'title':'Download', 'url':reverse('main:download_component', kwargs={'c_id':component.id})}, {'title':'Rate', 'url':reverse('main:rate_component', kwargs={'c_id':component.id})}, {'title':'View Details', 'url':reverse('main:comment', kwargs={'c_id':component.id})}] } for component in Component.objects.all()]
        tables = [{'title':'Components', 'rows':rows, 'headings':['Name', 'Rating', 'Downloads', 'Github URL','Uploaded by','Download', 'Rate', 'View Details']}]
        return render(request, 'main/tables.html', {'tables':tables})
    else:
        rows = [{'data':[component.name,component.ratings, component.download_set.all().count()],'link':[{'title':component.github_url, 'url':get_component_url(component)},{'title':component.user_p.name, 'url':reverse('main:get_profile', kwargs={'u_id':component.user_p.id})},{'title':'Download', 'url':reverse('main:download_component', kwargs={'c_id':component.id})}, {'title':'Rate', 'url':reverse('main:rate_component', kwargs={'c_id':component.id})}, {'title':'View Details', 'url':reverse('main:comment', kwargs={'c_id':component.id})}] } for component in Component.objects.all()]
        tables = [{'title':'Components', 'rows':rows, 'headings':['Name', 'Rating', 'Downloads', 'Github URL','Uploaded by','Download', 'Rate', 'View Details']}]
        return render(request, 'main/tables.html', {'tables':tables})

def register(request):
    if request.user.is_authenticated():
        user = request.user
        try:
            user_p = UserProfile.objects.get(user=user)
        except:
            logout(request)
            return redirect('main:register')
        return redirect('main:home')

    if request.method == 'POST':
        data = request.POST
        print data
        email = data['email']
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            messages.warning(request, 'Invalid Email Address.')
            return request.META.get('HTTP_REFERER')
        try:
            p = UserProfile.objects.get(email=data['email'])
            messages.warning(request, 'Email already registered.')
            return redirect('main:register')
        except:
            pass
        user_p = UserProfile()
        user_p.name = data['name']
        user_p.email = data['email']
        user_p.save()
        username = str(data['username'])
        try:
            user = User.objects.get(username=username)
            messages.warning(request, 'Username exists. Please select a different username.')
            return redirect('main:register')
        except:
            pass
        password = str(data['password'])
        user = User.objects.create_user(username=username, password=password)
        user.is_active = False
        user.save()
        user_p.user = user
        user_p.save()
        send_to = data['email']
        name = data['name']
        body = '''<link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
<pre style="font-family:Roboto,sans-serif">
Hello %s!

Thank you for registering for BioJS.
Please click on the link below to verify your email address, after which you can successfully login and start contributing!

<a href='%s'>Click Here</a> to verify your email.

</pre>
        '''%(name, str(request.build_absolute_uri(reverse("main:home"))) + 'email_confirm/' + generate_email_token(UserProfile.objects.get(email=send_to)) + '/')

        sg = sendgrid.SendGridAPIClient(apikey=API_KEY)
        from_email = Email('no-reply@abc.org')
        to_email = Email(send_to)
        subject = "Sign-up for BioJS"
        content = Content('text/html', body)
        
        try:
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())
        except :
            user_p.delete()
            messages.warning(request, 'Error sending email. Please try again.')
            return request.META.get('HTTP_REFERER')
        message = "A confirmation link has been sent to %s. Kindly click on it to verify your email address." %(send_to)
        context = {
                'error_heading': "Registered",
                'message': message,
                'url':request.build_absolute_uri(reverse('main:home'))
                }
        return render(request, 'main/message.html', context)
                
    else:
        return render(request, 'main/signup.html',)

def email_confirm(request, token):
    member = authenticate_email_token(token)
    if member:
        user = member.user
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('main:home')
    else:
        context = {
            'error_heading': "Invalid Token",
            'message': "Sorry! This is an invalid token. Email couldn't be verified. Please try again.",
            'url':request.build_absolute_uri('main:home')
        }
        return render(request, 'registrations/message.html', context)

def user_login(request):
    if request.user.is_authenticated():
        logout(request)
        return redirect('main:user_login')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print request.POST
        user = authenticate(username=username, password=password)
        print user
        if user is not None:
                if not UserProfile.objects.get(user=user).email_verified:
                    context = {'error_heading' : "Email not verified", 'message' :  'It seems you haven\'t verified your email yet. Please verify it as soon as possible to proceed,', 'url':request.build_absolute_uri(reverse('main:home'))}
                    return render(request, 'main/message.html', context)
                login(request, user)
                return redirect('main:home')
        else:
            messages.warning(request,'Invalid login credentials/Inactive user. Verify email first')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'main/login.html')

@login_required
def upload_component(request):
    user_p = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        data = request.POST
        from django.core.files import File
        name = data['name']
        if not name:
            messages.warning(request, 'Enter a valid name')
            return redirect('main:upload_component')
        try:
            component = Component.objects.get(name=name)
            messages.warning(request, 'Component with the name exists.')
            return redirect('main:upload_component')
        except:
            pass
        try:
            github_url = data['url']
        except:
            messages.warning(request, 'Enter a valid GitHub URL')
            return redirect('main:upload_component')
        if not 'github.com' in github_url:
            messages.warning(request, 'URL should be from github only.')
            return redirect('main:upload_component')
        try:
            component = Component.objects.create(github_url=github_url, name=name, user_p=user_p)
        except:
            messages.warning(request, 'Enter a valid GitHub URL')
            return redirect('main:upload_component')
        try:
            u_file = request.FILES['component']
            c_file = File(u_file)
            component.c_file.save(name, c_file)
        except:
            pass
        return redirect('main:get_user_profile')
    components = user_p.component_set.all()
    return render(request, 'main/upload_component.html', {'components':components})

def comment(request, c_id):
    component = get_object_or_404(Component, pk=c_id)
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return redirect(reverse('main:comment', kwargs={'c_id':component.id}))
        user_p = UserProfile.objects.get(user=request.user)
        data = request.POST
        title = data['title']
        details = data['details']
        comment = Comment.objects.create(title=title, details=details, component=component, user_p=user_p)
    comments = component.comment_set.all()
    return render(request, 'main/comment.html', {'component':component, 'comments':comments})

@login_required
def request_component(request):
    curr_user_p = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        data = request.POST
        try:
            user_p_list = UserProfile.objects.filter(id__in=data.getlist('user_p_list'))
        except:
            return redirect('main:home')
        body = data['body']
        for user_p in user_p_list:
            send_to = user_p.email
            sg = sendgrid.SendGridAPIClient(apikey=API_KEY)
            from_email = Email('request@abc.org')
            to_email = Email(send_to)
            subject = "Request for a New BioJS Component by %s" %(curr_user_p.name)
            content = Content('text/html', body)
            try:
                mail = Mail(from_email, subject, to_email, content)
                response = sg.client.mail.send.post(request_body=mail.get())
            except :
                messages.warning(request, 'Error sending email. Please try again.')
                return redirect(request.META.get('HTTP_REFERRER'))
        context = {
            'error_heading': "Success!",
            'message': "Email sent successfully.",
            'url':request.build_absolute_uri(reverse('main:home'))
            }
        return render(request, 'main/message.html', context)
    user_p_list = UserProfile.objects.all()
    return render(request, 'main/request_component.html', {'user_p_list':user_p_list})

'''
def download_component(request, c_id):
    component = get_object_or_404(Component, pk=c_id)
    if component.c_file:
        file_name = component.name
        file_path = settings.MEDIA_ROOT +'/'+ file_name
        file_wrapper = FileWrapper(file(file_path,'rb'))
        file_mimetype = mimetypes.guess_type(file_path)
        response = HttpResponse(file_wrapper, content_type=file_mimetype )
        response['X-Sendfile'] = file_path
        response['Content-Length'] = os.stat(file_path).st_size
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name) 
        download = Download.objects.create(component=component)
        return response
    else:
        context = {
            'error_heading': "File not uploaded!",
            'message': "Click the link below to open the github repository",
            'url':component.github_url
            }
        return render(request, 'main/message.html', context)   

'''
def download_component(request, c_id):
    component = get_object_or_404(Component, pk=c_id)
    if component.c_file:
        download = Download.objects.create(component=component)
        file_path = os.path.join(settings.MEDIA_ROOT, component.name)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404
    else:
        print component.github_url
        context = {
            'error_heading': "File not uploaded!",
            'message': "Click the link below to open the github repository",
            'url':get_component_url(component)
            }
        print context['url']
        return render(request, 'main/message.html', context)

def rate_component(request, c_id):
    component = get_object_or_404(Component, pk=c_id)
    if request.user.is_authenticated():
        user_p = UserProfile.objects.get(user=request.user)
        if component.user_p == user_p:
            messages.warning(request, 'You uploaded this.')
            return redirect('main:get_user_profile')
    if request.method == 'POST':
        data = request.POST
        rate = data['rating']
        if rate < 1 or rate > 5:
            messages.warning(request, 'Invalid input.')
            return redirect(reverse('main:rate_component', kwargs={'c_id':component.id}))
        rating = Rating(component=component, value=rate)
        return redirect('main:home')
    return render(request, 'main/rate.html', {'component':component})

def get_profile(request, u_id):
    user_p = get_object_or_404(UserProfile, pk=u_id)
    components = user_p.component_set.all()
    rows = [{'data':[component.name,component.ratings, component.download_set.all().count()],'link':[{'title':component.github_url, 'url':get_component_url(component)},{'title':'Download', 'url':reverse('main:download_component', kwargs={'c_id':component.id})}, {'title':'Rate', 'url':reverse('main:rate_component', kwargs={'c_id':component.id})}, {'title':'View Details', 'url':reverse('main:comment', kwargs={'c_id':component.id})}] } for component in Component.objects.all()]
    tables = [{'title':'Components of %s'%(user_p.name), 'rows':rows, 'headings':['Name', 'Rating', 'Downloads', 'Github URL','Download', 'Rate', 'View Details']}]
    return render(request, 'main/tables.html', {'tables':tables})

@login_required
def get_user_profile(request):
    user = request.user
    user_p = UserProfile.objects.get(user=user)
    components = user_p.component_set.all()
    rows = [{'data':[component.name,component.ratings, component.download_set.all().count()],'link':[{'title':component.github_url, 'url':get_component_url(component)},{'title':'Download', 'url':reverse('main:download_component', kwargs={'c_id':component.id})},{'title':'View Details', 'url':reverse('main:comment', kwargs={'c_id':component.id})}] } for component in Component.objects.all()]
    tables = [{'title':'Your components', 'rows':rows, 'headings':['Name', 'Rating', 'Downloads', 'Github URL','Download','View Details']}]
    return render(request, 'main/tables.html', {'tables':tables})

@login_required
def user_logout(request):
	logout(request)
	return redirect('main:home')


############ Helper Functions ######################

def generate_email_token(user_p):

	import uuid
	token = uuid.uuid4().hex
	registered_tokens = [user_p.email_token for user_p in UserProfile.objects.all()]

	while token in registered_tokens:
		token = uuid.uuid4().hex

	user_p.email_token = token
	user_p.save()
	
	return str(token)

def authenticate_email_token(token):

	try:
		user_p = UserProfile.objects.get(email_token=token)
		user_p.email_verified = True
		user_p.save()
		return user_p

	except :
		return False

def get_component_url(component):
    url = component.github_url
    if not 'http' in url:
        url = 'https://' + url
    return url