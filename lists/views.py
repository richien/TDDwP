from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from lists.models import Item

@csrf_exempt
def home_page(request):
	if request.method == 'POST':
		new_item_text = request.POST['item_text']
		Item.objects.create(text=new_item_text)
		return redirect('/lists/')

	items = Item.objects.all()
	return render(request, 'lists/home.html', {'items':items})
