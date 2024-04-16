from django.shortcuts import render

# Create your views here.

def index(request):
    # send_mail_code('mamatmusayev.uz@gmail.com', '1234')
    return render(request, 'home.html', {})