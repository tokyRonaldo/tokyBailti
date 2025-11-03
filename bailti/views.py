from django.shortcuts import render, redirect
from .models import User , Property

# Create your views here.
def dashboard(request):
    users=User.objects.all()
    return render(request , 'bailti/dashboard.html',{'users' : users})

# Create your views here.
def property(request):
    users=User.objects.all()
    return render(request , 'bailti/property/index.html',{'users' : users})

# Create your views here.
def property_create(request):
    users=User.objects.all()
    return render(request , 'bailti/property/create.html',{'users' : users})


# Create your views here.
def locataire(request):
    users=User.objects.all()
    return render(request , 'bailti/locataire/index.html',{'users' : users})

# Create your views here.
def locataire_create(request):
    users=User.objects.all()
    return render(request , 'bailti/locataire/create.html',{'users' : users})


# Create your views here.
def locataire_store(request):
    users=User.objects.all()
    if request.method == 'POST':
        identifiant = request.POST.get('identifiant')
        adresse = request.POST.get('adresse')
        superficie = request.POST.get('superficie')
        loyer = request.POST.get('loyer')
        description = request.POST.get('description')
        type_ = request.POST.get('type')
        meuble = request.POST.get('meuble') == 'on'  # checkbox => True ou False
        user_id = 3 #mettre la valeur de celui authentifié

        Property.objects.create(
            identifiant=identifiant,
            adresse=adresse,
            superficie=superficie,
            loyer=loyer,
            description=description,
            type=type_,
            meublé=meuble,
            user_id=user_id
        )

    return redirect('property')  # redirige vers une liste par exemple



# Create your views here.
def locations(request):
    users=User.objects.all()
    return render(request , 'bailti/locations/index.html',{'users' : users})

# Create your views here.
def location_create(request):
    users=User.objects.all()
    return render(request , 'bailti/locations/create.html',{'users' : users})


# Create your views here.
def favorie(request):
    users=User.objects.all()
    return render(request , 'bailti/favorie.html',{'users' : users})

