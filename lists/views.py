from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home_page(request):
	# if request.method == 'POST':
	# 	return HttpResponse(request.POST['item_text'])
	return render(request, 'lists/home.html', {'new_item_text' : request.POST.get('item_text', ''),})
