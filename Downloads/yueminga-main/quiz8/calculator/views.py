from django.shortcuts import render

from calculator.forms import CalForm

# Create your views here.

def calculator(request):
    if request.method == "GET":
        return render(request, 'calculator/calculator.html', {'form': CalForm()})

    form = CalForm(request.POST)
    if not form.is_valid():
        return render(request, 'calculator/calculator.html', {'form': form})
    
    x = form.cleaned_data['x']
    y = form.cleaned_data['y']

    answer = x/y
    return render(request, 'calculator/calculator.html', {'form': CalForm(), 'answer': answer})
