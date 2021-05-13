from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .models import Oxygen, Pharma, Plasma, Hospital, Report

from .Helpers.Statesdata import Statesdata
import json

# Create your views here.
def index(request):
    return render(request, "public/index.html")

### send state and district wise
def oxygen(request):
    try:
        state = request.GET.getlist('state')[0]
        city = request.GET.getlist('city')[0]
        resources=Oxygen.objects.filter(state=state,city=city)
        return render(request, "public/oxygenView.html", {
            "resources":resources
        })
    except:
        st = Statesdata()
        states = st.getStates()
        return render(request, "public/oxygen.html", {'states': states})

def pharma(request):
    try:
        state = request.GET.getlist('state')[0]
        city = request.GET.getlist('city')[0]
        resources=Pharma.objects.filter(state=state,city=city)
        drugs=[]
        for med in resources:
            med=med.available_drugs.strip("[]").split(",")
            drugs.append(med)
        return render(request, "public/pharmaView.html", {
            "cleaned_resources": zip(resources, drugs)
        })
    except:
        st = Statesdata()
        states = st.getStates()
        return render(request, "public/pharma.html", {'states': states})

def hospitals(request):
    try:
        state = request.GET.getlist('state')[0]
        city = request.GET.getlist('city')[0]
        resources=Hospital.objects.filter(state=state,city=city)
        return render(request, "public/oxygenView.html", {
            "resources":resources
        })
    except:
        st = Statesdata()
        states = st.getStates()
        return render(request, "public/hospitals.html", {'states': states})

def plasma(request):
    try:
        state = request.GET.getlist('state')[0]
        city = request.GET.getlist('city')[0]
        resources=Plasma.objects.filter(state=state,city=city)
        return render(request, "public/plasmaView.html", {
            "resources":resources
        })
    except:
        st = Statesdata()
        states = st.getStates()
        return render(request, "public/plasma.html", {'states': states})

def report(request, id):
    if request.method == 'POST':
        try:
            r = Report()
            r.comments = request.POST['comments']
            modelType = request.POST['ModelType']
            if modelType == "Oxygen":
                r.item = Oxygen.objects.get(id=id)
            elif modelType == "Pharma":
                r.item = Pharma.objects.get(id=id)
            elif modelType == "Plasma":
                r.item = Plasma.objects.get(id=id)
            r.save()
            messages.success(request, 'Comment Submitted!')
            return redirect(request.META.get('HTTP_REFERER'))
        except:
            messages.warning(request, 'Error!!')
            return render(request, "public/index.html")
    else:
        messages.warning(request, 'Method Not Allowed!')
        return render(request, "public/index.html")
