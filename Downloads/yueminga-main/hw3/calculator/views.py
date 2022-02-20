from curses.ascii import isdigit
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def calculator(request):
    context = {}
    if request.method == 'GET':
        context['entering'] = 'True'
        context['stack0'] = '0'
        context['stack1'] = ''
        context['stack2'] = ''
        context['output'] = 0
        context['color'] = "moccasin"
        return render(request, 'calculator/index.html', context)

    if 'entering' not in request.POST or 'button' not in request.POST or 'stack0' not in request.POST or 'stack1' not in request.POST or 'stack2' not in request.POST:
        context['message'] = 'Parameter lost'
        return render(request, 'calculator/error.html', context)

    if request.POST['entering'] not in ['True', 'False']:
        context['message'] = 'Parameter entering changed'
        return render(request, 'calculator/error.html', context)

    if request.POST['stack0'].isalpha():
        context['message'] = 'Parameter stack0 changed'
        return render(request, 'calculator/error.html', context)
    if request.POST['stack1'].isalpha():
        context['message'] = 'Parameter stack1 changed'
        return render(request, 'calculator/error.html', context)
    if request.POST['stack2'].isalpha():
        context['message'] = 'Parameter stack2 changed'
        return render(request, 'calculator/error.html', context)

    context['button'] = request.POST['button']
    if context['button'] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        return digitClick(request)
    elif context['button'] == 'push':
        return pushClick(request)
    elif context['button'] in ['plus', 'minus', 'times', 'divide']:
        return opClick(request)
    else:
        context['message'] = 'missing/invalid parameters'
        return render(request, 'calculator/error.html', context)


def digitClick(request):
    context = {}
    entering = request.POST['entering']
    stack = list()
    context['button'] = request.POST['button']
    if request.POST['stack0'] != '':
        stack.append(request.POST['stack0'])
    if request.POST['stack1'] != '':
        stack.append(request.POST['stack1'])
    if request.POST['stack2'] != '':
        stack.append(request.POST['stack2'])
    if entering == 'True':
        bottom = int(stack[-1])
        bottom = bottom * 10 + int(context['button'])
        stack[-1] = str(bottom)
        context['output'] = bottom
        context['color'] = "moccasin"
        if len(stack) == 1:
            context['stack0'] = stack[0]
        elif len(stack) == 2:
            context['stack0'] = stack[0]
            context['stack1'] = stack[1]
        elif len(stack) == 3:
            context['stack0'] = stack[0]
            context['stack1'] = stack[1]
            context['stack2'] = stack[2]
        context['entering'] = 'True'
    else:
        if len(stack) >= 3:
            stack = list()
            stack.append('0')
            context['entering'] = 'True'
            context['message'] = 'stack overflow'
            context['color'] = "red"
            context['stack0'] = stack[0]

            context['stack1'] = ''
            context['stack2'] = ''
            return render(request, 'calculatoe/error.html', context)
        else:
            stack.append('0')
            context['entering'] = 'True'
            bottom = int(stack[-1])
            bottom = bottom * 10 + int(context['button'])
            context['output'] = bottom
            stack[-1] = str(bottom)
            if len(stack) == 1:
                context['stack0'] = stack[0]
            elif len(stack) == 2:
                context['stack0'] = stack[0]
                context['stack1'] = stack[1]
    return render(request, 'calculator/index.html',context)


def pushClick(request):
    context = {}
    entering = request.POST['entering']
    stack = list()
    if request.POST['stack0'] != '':
        stack.append(request.POST['stack0'])
    if request.POST['stack1'] != '':
        stack.append(request.POST['stack1'])
    if request.POST['stack2'] != '':
        stack.append(request.POST['stack2'])
    
    if len(stack) == 3:
        context['message'] = 'stack overflow'
        context['color'] = "red"
        stack = list()
        stack.append('0')
        context['entering'] = 'True'
        return render(request, 'calculator/error.html', context)
    else:
        stack.append('0')
        context['output'] = 0
        context['entering'] = 'True'
        context['color'] = "moccasin"
        if len(stack) == 1:
                context['stack0'] = stack[0]
                context['stack1'] = ''
                context['stack2'] = ''
        elif len(stack) == 2:
                context['stack0'] = stack[0]
                context['stack1'] = stack[1]
                context['stack2'] = ''
        elif len(stack) == 3:
            context['stack0'] = stack[0]
            context['stack1'] = stack[1]
            context['stack2'] = stack[2]
        return render(request, 'calculator/index.html', context)

def opClick(request):
    context = {}
    entering = request.POST['entering']
    stack = list()
    context['button'] = request.POST['button']
    if request.POST['stack0'] != '':
        stack.append(request.POST['stack0'])
    if request.POST['stack1'] != '':
        stack.append(request.POST['stack1'])
    if request.POST['stack2'] != '':
        stack.append(request.POST['stack2'])
    if len(stack) < 2:
        context['message'] = 'stack underfolw'
        context['color'] = "red"
        stack = list()
        stack.append('0')
        context['entering'] = 'True'
        return render(request, 'calculator/error.html', context)
    else:
        second = int(stack.pop())
        first = int(stack.pop())
        if second == 0:
            context['message'] = 'divide by zero'
            context['color'] = "red"
            stack = list()
            stack.append('0')
            context['entering'] = 'True'
            return render(request, 'calculator/error.html', context)
        else:
            operator = request.POST['button']
            if operator == 'plus':
                result = first + second
            elif operator == 'minus':
                result = first - second
            elif operator == 'times':
                result = first * second
            elif operator == 'divide':
                result = int(first / second)
            stack.append(result)
            context['output'] = result
            context['entering'] = 'False'
            if len(stack) == 1:
                context['stack0'] = stack[0]
                context['stack1'] = ''
                context['stack2'] = ''
            elif len(stack) == 2:
                context['stack0'] = stack[0]
                context['stack1'] = stack[1]
                context['stack2'] = ''
        return render(request, 'calculator/index.html',context)
