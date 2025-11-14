from django.shortcuts import render, redirect
from .models import User , Property, Locataire
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.contrib import messages
from django.urls import reverse
import secrets
import string

# Create your views here.
@login_required(login_url='/user/login')
def dashboard(request):
    users=User.objects.all()
    return render(request , 'bailti/dashboard.html',{'users' : users})

# Create your views here.
@login_required(login_url='/user/login')
def property(request):
    user = request.user
    if user.is_authenticated :
        print('user.email')
    else :
        print('utilisateur non connecter')
    properties= Property.objects.all()
    
    return render(request , 'bailti/property/index.html',{'properties' : properties})

# Create your views here.
@login_required(login_url='/user/login')
def property_create(request):
    users=User.objects.all()
    return render(request , 'bailti/property/create.html',{'users' : users})

@login_required(login_url='/user/login')
def property_store(request):
    user= request.user.id
    if request.method == 'POST':
        identifiant = request.POST.get('identifiant')
        adresse = request.POST.get('adresse')
        superficie = request.POST.get('superficie')
        loyer = request.POST.get('loyer')
        description = request.POST.get('description')
        type = request.POST.get('type')
        image = request.FILES.get('image')
        meuble = request.POST.get('meuble') == 'on'  # checkbox => True ou False
        user_id = user #mettre la valeur de celui authentifié
        print('image testtttttt')
        print(image)

        Property.objects.create(
            identifiant=identifiant,
            adresse=adresse,
            superficie=superficie,
            loyer=loyer,
            description=description,
            type=type,
            meublé=meuble,
            user_id=user_id,
            image=image
        )

    return redirect('property')  # redirige vers une liste par exemple



# Create your views here.
@login_required(login_url='/user/login')
def locataire(request):

    locataires = Locataire.objects.all()
    return render(request , 'bailti/locataire/index.html',{'locataires' : locataires})

# Create your views here.
@login_required(login_url='/user/login')
def locataire_create(request):
    proprieties = Property.objects.filter(user_id = request.user.id)
    return render(request , 'bailti/locataire/create.html',{'proprieties' : proprieties})


# Create your views here.
@login_required(login_url='/user/login')
def locataire_store(request):
    print(request.user.id)
    print('request.user.id')
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        date_naissance = request.POST.get('date_naissance')
        lieu_naissance = request.POST.get('lieu_naissance')
        revenu_mensuels = request.POST.get('revenu_mensuels')
        sex = request.POST.get('sex')
        adresse = request.POST.get('adresse')
        user_id = 3 #mettre la valeur de celui authentifié
        print('sexxxxxxxxx')
        print(sex)
        try:
            with transaction.atomic():

                password = generate_password()

                user, created = User.objects.get_or_create(
                    email=email,                # critère pour trouver l'utilisateur
                    defaults={                  # valeurs si on le crée
                        "nom": nom,
                        "prenom": prenom,
                        "phone": mobile,
                        "date_naissance": date_naissance,
                        "lieu_naissance": lieu_naissance,
                        "sex": sex,
                        "adresse": adresse,
                        "password": make_password(password),
                        "role": "locataire"
                    }
                )

                if not created:
                    # Si l’utilisateur existe déjà → on met à jour
                    user.nom = nom
                    user.prenom = prenom
                    user.phone = mobile
                    user.date_naissance = date_naissance
                    user.lieu_naissance = lieu_naissance
                    user.sex = sex
                    user.adresse = adresse
                    # On ne remplace le password que si tu veux VRAIMENT le changer
                    # user.password = make_password(password)
                    user.role = "locataire"
                    user.save()

                locataire = Locataire.objects.create(
                    nom=nom,
                    prenom=prenom,
                    mobile=mobile,
                    email=email,
                    date_naissance=date_naissance,
                    lieu_naissance=lieu_naissance,
                    revenu_mensuels=revenu_mensuels,
                    adresse=adresse,
                    user_locataire_id=user.id,
                    proprietaire_user_id=request.user.id,
                )

                # pour envoyer le mail, mais c'est encore à regler parce que l'envoyeur reste tjrs celui dans settings.py
                """ html_content = render_to_string('email/mon_email.html', {'nom': 'Toky'})
                email = EmailMessage(
                    subject='Email avec template',
                    body=html_content,
                    from_email='ronaldotoky62@gmail.com',
                    to=['tokyronaldo75@gmail.com'],
                )
                email.content_subtype = "html"
                email.send() """
                url = request.build_absolute_uri( reverse('dashboard') )

                data_mail = {
                    "locataire_nom": locataire.nom,
                    "locataire_prenom": locataire.prenom,
                    "locataire_email": locataire.email,
                    "locataire_pwd": password,
                    "proprietaire_nom": request.user.nom,
                    "proprietaire_prenom": request.user.prenom,
                    "proprietaire_email": request.user.email,
                    "lien_bailti" : url,
                }
                print(data_mail)
                print(data_mail['locataire_nom'])
                
                html_content = render_to_string('email/mon_email.html', {'data_mail': data_mail})
                email = EmailMessage(
                    subject='Email avec template',
                    body=html_content,
                    from_email='ronaldotoky62@gmail.com',
                    to=[data_mail['locataire_email']],
                )
                email.content_subtype = "html"
                email.send() 
                messages.success(request, "sauvegarde succès")



        except Exception as e:
            if 'Duplicate entry' in str(e):
                print('etttt')
                messages.error(request, "❌ Cet email est déjà utilisé.")
            else:
                print('errrooo')
                print(e)
                messages.error(request, "Une erreur est survenue lors de la création de l'utilisateur.")

    return redirect('locataire')  # redirige vers une liste par exemple


@login_required(login_url='/user/login')
def proprietaire(request):
    locataires = Locataire.objects.all()
    return render(request , 'bailti/locataire/index.html',{'locataires' : locataires})

# Create your views here.
@login_required(login_url='/user/login')
def locations(request):
    users=User.objects.all()
    return render(request , 'bailti/locations/index.html',{'users' : users})

# Create your views here.
@login_required(login_url='/user/login')
def location_create(request):

    properties = Property.objects.filter(user_id = request.user.id)
    locataires = Locataire.objects.filter(proprietaire_user_id = request.user.id)
    return render(request , 'bailti/locations/create.html',{'properties' : properties, 'locataires' : locataires})

@login_required(login_url='/user/login')
def location_store(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        date_naissance = request.POST.get('date_naissance')
        lieu_naissance = request.POST.get('lieu_naissance')
        revenu_mensuels = request.POST.get('revenu_mensuels')
        adresse = request.POST.get('adresse')
        user_id = 3 #mettre la valeur de celui authentifié

        Locataire.objects.create(
            nom=nom,
            prenom=prenom,
            mobile=mobile,
            email=email,
            date_naissance=date_naissance,
            lieu_naissance=lieu_naissance,
            revenu_mensuels=revenu_mensuels,
            adresse=adresse
        )

    return redirect('locations')  # redirige vers une liste par exemple




# Create your views here.
@login_required(login_url='/user/login')
def favorie(request):
    users=User.objects.all()
    return render(request , 'bailti/favorie.html',{'users' : users})


def generate_password(length=10):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))