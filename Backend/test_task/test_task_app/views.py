from django.shortcuts import render

def hello_world(request):
    return render(request, 'test_task_app/hello_world.html')
