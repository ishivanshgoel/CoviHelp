from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .decorators import allowed_users
# user info model
from .models import UserInfo
from .models import Plasma, Oxygen, Pharma, Instagram

# helper functions
from .Helpers.Statesdata import Statesdata
from .Helpers.Utilities import Utilities
from .Helpers.Data import Data
import json
import datetime

# helpers
dt = Data()
available_drugs = dt.available_drugs() 
    
st = Statesdata()
states = st.getStates()
ut = Utilities()


# convert time to integer
def to_str(dt_time):
    return str(10000000*dt_time.year + 1000000*dt_time.month + 100000*dt_time.day + 10000*dt_time.hour + 10000*dt_time.minute + 1000*dt_time.second + 100*dt_time.microsecond)

def gen_id(user, name, state, ty,contact):
    time = datetime.datetime.now()
    return hash(str(user) + str(name) + str(state) + str(ty) + str(contact) + to_str(time))


# all login views
def loginview(request):
    '''
    if request is POST then verify the credentials of the user and redirect to their respective location based on their user type
    else redirect to '/'
    '''
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            u = authenticate(request, username=email, password=password)
        except:
            return HttpResponse('Some Error Occured')
        if u is not None:
            login(request, u)
            return redirect(user)
        else:
            messages.warning(request, 'Invalid username/ password')
            return render(request, "public/index.html")
    else:
        messages.warning(request, 'Not Allowed')
        return render(request, "public/index.html")

# user view - display after login
@login_required
def user(request):
    '''
    user
    '''
    return render(request, "user/oxygen.html")


@login_required
def plasma(request):
    global states
    plasma = Plasma.objects.filter(user=request.user)
    if request.method == 'POST':
        try:
            p = Plasma()
            p.user = request.user
            p.name = request.POST['name']
            p.state = request.POST['state']
            p.city = request.POST['city']
            p.donortype = request.POST['donortype']
            p.contact = request.POST['contact']
            p.blood_group = request.POST['bloodgroup']
            p.id = ut.gen_id(p.user, p.name, p.state, 'plasma', p.contact)
            p.save()

            i = Instagram()
            i.info = p
            i.id = ut.gen_id('user-name', i.info[0], 'state', 'instagram','contact')
            i.save()

            messages.success(request, 'Thankyou for sharing the information.')
        except:
            messages.warning(request, 'Error!!')
        return render(request, "user/plasma.html", {
            'states': states,
            "plasma" : plasma
        })
    else:
        return render(request, "user/plasma.html", {
            'states': states,
            "plasma" : plasma
        })


@login_required
def oxygen(request):
    global states
    oxygen = Oxygen.objects.filter(user=request.user)
    if request.method == 'POST':
        try:
            Oxy = Oxygen()
            Oxy.user = request.user
            Oxy.name = request.POST['name']
            Oxy.state = request.POST['state']
            Oxy.city = request.POST['city']
            Oxy.contact = request.POST['contact']
            Oxy.address = request.POST['address']
            Oxy.id = ut.gen_id(Oxy.user, Oxy.name, Oxy.state, 'oxygen', Oxy.contact)
            Oxy.save()

            i = Instagram()
            i.info = Oxy
            i.id = ut.gen_id('user-name', i.info[0], 'state', 'instagram','contact')
            print(i, i.id)
            i.save()

            messages.success(request, 'Thankyou for sharing the information.')
        except:
            messages.error(request, 'Error!!')
        return render(request, "user/oxygen.html", {
            'states': states,
            'oxygen' : oxygen
        })

    else:
        return render(request, "user/oxygen.html", {
            'states': states,
            'oxygen' : oxygen
        })


@login_required
def hospital(request):
    '''
    user
    '''
    print(request.user)
    return render(request, "user/hospital.html")


@login_required
def pharma(request):
    global available_drugs, states
    pharma = Pharma.objects.filter(user=request.user)

    if request.method == 'POST':
        try:
            p = Pharma()
            p.user = request.user
            p.name = request.POST['name']
            p.state = request.POST['state']
            p.city = request.POST['city']
            p.contact = request.POST['contact']
            p.address = request.POST['address']
            p.available_drugs = request.POST.getlist('checks[]')
            p.id = ut.gen_id(p.user, p.name, p.state, 'pharma', p.contact)
            p.save()

            i = Instagram()
            i.info = p
            i.id = ut.gen_id('user-name', i.info[0], 'state', 'instagram','contact')
            i.save()

            messages.success(request, 'Thankyou for sharing the information.')
        except:
            messages.error(request, 'Error!!')

        return render(request, "user/pharma.html", {
            'states': states,
            "drugs":available_drugs,
            "pharma":pharma
        })
    else:
        return render(request, "user/pharma.html", {
            'states': states,
            "drugs":available_drugs,
            "pharma":pharma
        })

@login_required
def modify(request, id):
    return HttpResponse("test")

### Helper Routes ###
def getDistricts(request):
    '''
    get all districts
    '''
    try:
        state = request.GET.getlist('state')[0]
        st = Statesdata()
        data = st.getDistricts(state)
        data = json.dumps(data)
        return HttpResponse(data, content_type='application/json')
    except:
        return HttpResponse('Error')

@login_required
@allowed_users(allowed_roles=['Verification'])
def completelist(request):
    if request.method == 'POST':
        posted = request.POST.get('postedCheckbox',False)
        if posted=="on":
            return HttpResponse("ok")
    
    instalist = Instagram.objects.all()
    return render(request, "user/completelist.html", context={'instalist':instalist})