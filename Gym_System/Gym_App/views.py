from django.shortcuts import render, HttpResponse

def loginPage(request):
    return render(request, 'loginPage.html')

def dashboard(request):
    return render(request, 'basetemplate.html' , {'page_title':'dashboard'})

def members(request):
    return render(request, 'members.html' ,{'page_title':'members'})

def trainers(request):
    return render(request, 'trainers.html' ,{'page_title':'trainers'})

def instructors(request):
    return render(request, 'instructors.html' ,{'page_title':'instructors'})

def general_employees(request):
    return render(request, 'general_employees.html' ,{'page_title':'general_Employees'})

def reports(request):
    return render(request, 'reports.html' ,{'page_title':'reports'})

def register_members(request):
    return render(request, 'register_members.html' ,{'page_title':'register Members'})

def class_scheduling(request):
    return render(request, 'class_scheduling.html' ,{'page_title':'classes'})