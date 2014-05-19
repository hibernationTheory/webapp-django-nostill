# Create your views here.

from django.http import HttpResponse

def about(request):
	return HttpResponse("about")

def index(request):
	return HttpResponse("index")

def submit(request):
	return HttpResponse("submit")

def login(request):
	return HttpResponse("login")