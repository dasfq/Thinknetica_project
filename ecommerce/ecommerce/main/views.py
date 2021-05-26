from django.shortcuts import render
from django.contrib.flatpages.models import FlatPage


# Create your views here.

def IndexView(request):
    template_name = 'index.html'
    queryset = FlatPage.objects.all()
    context = {
        'pages': queryset,
    }
    return render(request, template_name,context)

