from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, render, redirect
from .models import User , Property, Locataire , Location
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
    # properties= Property.objects.all()
    if request.user.role == 'proprietaire' :

        properties = Property.objects.filter(
           user_id = request.user.id
        )
    else : 

        properties = Property.objects.filter(
            locations__locataire__user_locataire=request.user
        ).distinct()
        print('iciiiiiooijjjo')
        print(properties)
    
    
    return render(request , 'bailti/property/index.html',{'properties' : properties})

# Create your views here.
@login_required(login_url='/user/login')
def property_create(request, id=None):
    if id is None:
        property_obj = None  # pas d'édition, création
    else:
        property_obj = Property.objects.filter(id=id).first()
    return render(request , 'bailti/property/create.html',{'property' : property_obj})

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

        try:
            with transaction.atomic():
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
                messages.success(request, "sauvegarde succès")

        except Exception as e:
            print('errrooo')
            print(e)
            messages.error(request, "Une erreur est survenue lors de la création de l'utilisateur.")


    return redirect('property')  # redirige vers une liste par exemple


@login_required(login_url='/user/login')
def property_update(request, id):
    try:
        with transaction.atomic():
            # Récupérer le property à modifier
            property_obj = Property.objects.filter(id=id).first()
            if not property_obj:
                return redirect('property')  # ou 404

            if request.method == 'POST':

                property_obj.identifiant = request.POST.get('identifiant')
                property_obj.adresse = request.POST.get('adresse')
                property_obj.superficie = request.POST.get('superficie')
                property_obj.loyer = request.POST.get('loyer')
                property_obj.description = request.POST.get('description')
                property_obj.type = request.POST.get('type')
                property_obj.meublé = (request.POST.get('meuble') == 'on')
                #property_obj.user_id = request.user.id  # utilisateur connecté

                # Si une nouvelle image a été uploadée → on remplace
                image = request.FILES.get('image')
                if image:
                    property_obj.image = image

                property_obj.save()
            messages.success(request, "sauvegarde succès")

    except Exception as e:
        print('errrooo')
        print(e)
        messages.error(request, "Une erreur est survenue lors de la création de l'utilisateur.")

    return redirect('property')

@login_required(login_url='/user/login')
def property_delete(request, id):
    property_obj = get_object_or_404(Property, id=id)
    
    try:
        with transaction.atomic():
            property_obj.delete()
            messages.success(request, "Bien supprimé avec succès.")
    except Exception as e:
        print("Erreur deletion property:", e)
        messages.error(request, "Une erreur est survenue lors de la suppression du bien.")
    
    return redirect('property')



# Create your views here.
@login_required(login_url='/user/login')
def locataire(request):

    locataires = Locataire.objects.filter(proprietaire_user_id = request.user.id)
    return render(request , 'bailti/locataire/index.html',{'locataires' : locataires})

# Create your views here.
@login_required(login_url='/user/login')
def locataire_create(request,id=None):
    if id is None:
        locataire_obj = None  # pas d'édition, création
    else:
        locataire_obj = Locataire.objects.filter(id=id).first()
    return render(request , 'bailti/locataire/create.html',{'locataire' : locataire_obj})


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

                locataire_exist = Locataire.objects.filter(
                    email=email,
                    proprietaire_user_id=request.user.id
                ).first()

                if locataire_exist:
                    messages.error(request, "❌ Ce locataire existe déjà pour ce propriétaire.")
                    return redirect('locataire')

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
                    password=password,
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
def locataire_update(request, id):
    # Récupérer le locataire existant
    locataire = Locataire.objects.filter(id=id).first()
    if not locataire:
        messages.error(request, "Locataire introuvable.")
        return redirect('locataire')

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

        try:
            with transaction.atomic():
                # Vérifier qu'aucun autre locataire du même propriétaire n'a le même email
                locataire_exist = Locataire.objects.filter(
                    email=email,
                    proprietaire_user_id=request.user.id
                ).exclude(id=locataire.id).first()

                if locataire_exist:
                    messages.error(request, "❌ Un locataire avec ce même email existe déjà pour ce propriétaire.")
                    return redirect('locataire')

                # Récupérer l'user associé au locataire
                user = locataire.user_locataire  

                # Mettre à jour l'utilisateur associé
                user.nom = nom
                user.prenom = prenom
                user.phone = mobile
                user.date_naissance = date_naissance
                user.lieu_naissance = lieu_naissance
                user.sex = sex
                user.adresse = adresse
                user.email = email
                user.save()

                # Mettre à jour le locataire
                locataire.nom = nom
                locataire.prenom = prenom
                locataire.mobile = mobile
                locataire.email = email
                locataire.date_naissance = date_naissance
                locataire.lieu_naissance = lieu_naissance
                locataire.revenu_mensuels = revenu_mensuels
                locataire.adresse = adresse
                locataire.proprietaire_user_id = request.user.id
                locataire.save()

                messages.success(request, "Mise à jour effectuée avec succès.")

        except Exception as e:
            print(e)
            messages.error(request, "Une erreur est survenue.")

    return redirect('locataire')


@login_required(login_url='/user/login')
def locataire_delete(request, id):
    locataire = get_object_or_404(Locataire, id=id)
    
    try:
        with transaction.atomic():
            # Supprimer aussi l'utilisateur associé si nécessaire
            user = locataire.user_locataire
            locataire.delete()
            if user:
                user.delete()
            messages.success(request, "Locataire supprimé avec succès.")
    except Exception as e:
        print("Erreur deletion locataire:", e)
        messages.error(request, "Une erreur est survenue lors de la suppression du locataire.")
    
    return redirect('locataire')


@login_required(login_url='/user/login')
def proprietaire(request):

    proprietaires = User.objects.filter(
        proprietaire_user__user_locataire=request.user
    ).distinct()
    
    return render(request , 'bailti/locataire/index.html',{'proprietaires' : proprietaires})

# Create your views here.
@login_required(login_url='/user/login')
def locations(request):
    user = request.user
    # properties= Property.objects.all()
    if request.user.role == 'proprietaire' :

        locations = Location.objects.filter(
           user_id = request.user.id
        )
    else : 
        locations = Location.objects.filter(
            locataire__user_locataire=request.user
        )

    return render(request , 'bailti/locations/index.html',{'locations' : locations})

# Create your views here.
@login_required(login_url='/user/login')
def location_create(request , id=None):
    if id is None:
        location_obj = None  # pas d'édition, création
    else:
        location_obj = Location.objects.filter(id=id).first()
    properties = Property.objects.filter(user_id = request.user.id)
    locataires = Locataire.objects.filter(proprietaire_user_id = request.user.id)
    return render(request , 'bailti/locations/create.html',
        {
            'properties' : properties,
            'locataires' : locataires,
            'location' : location_obj
         })

@login_required(login_url='/user/login')
def location_store(request):
    if request.method == 'POST':
        identifiant = request.POST.get('identifiant')
        property = request.POST.get('property')
        locataire = request.POST.get('locataire')
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        loyer = request.POST.get('loyer')
        garantie = request.POST.get('garantie')
        commentaire = request.POST.get('commentaire')
        try:
            with transaction.atomic():

                Location.objects.create(
                    identifiant=identifiant,
                    property=Property.objects.get(id=property),
                    locataire=Locataire.objects.get(id=locataire),
                    date_debut=date_debut,
                    date_fin=date_fin,
                    loyer=loyer,
                    garantie=garantie,
                    commentaire=commentaire,
                    user = User.objects.get(id=request.user.id)
                )
                messages.success(request, "sauvegarde succès")



        except Exception as e:
            print('errrooo')
            print(e)
            messages.error(request, "Une erreur est survenue lors de la création du location.")


    return redirect('locations')  # redirige vers une liste par exemple


@login_required(login_url='/user/login')
def location_update(request, id):
    location = get_object_or_404(Location, id=id)

    if request.method == 'POST':
        identifiant = request.POST.get('identifiant')
        property_id = request.POST.get('property')
        locataire_id = request.POST.get('locataire')
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        loyer = request.POST.get('loyer')
        garantie = request.POST.get('garantie')
        commentaire = request.POST.get('commentaire')

        try:
            with transaction.atomic():

                location.identifiant = identifiant
                location.property = Property.objects.get(id=property_id)
                location.locataire = Locataire.objects.get(id=locataire_id)
                location.date_debut = date_debut
                location.date_fin = date_fin
                location.loyer = loyer
                location.garantie = garantie
                location.commentaire = commentaire
                location.user = request.user  # AUTOMATIQUE

                location.save()

                messages.success(request, "Mise à jour effectuée avec succès.")

        except Exception as e:
            print("Erreur update:", e)
            messages.error(
                request,
                "Une erreur est survenue lors de la mise à jour de la location."
            )

    return redirect('locations')

@login_required(login_url='/user/login')
def location_delete(request, id):
    location = get_object_or_404(Location, id=id)
    
    try:
        with transaction.atomic():
            location.delete()
            messages.success(request, "Location supprimée avec succès.")
    except Exception as e:
        print("Erreur deletion location:", e)
        messages.error(request, "Une erreur est survenue lors de la suppression de la location.")
    
    return redirect('locations')


# Create your views here.
@login_required(login_url='/user/login')
def favorie(request):
    users=User.objects.all()
    return render(request , 'bailti/favorie.html',{'users' : users})

# Create your views here.
@login_required(login_url='/user/login')
def quittance(request):
    users=User.objects.all()
    return render(request , 'bailti/quittance.html',{'users' : users})


def generate_password(length=10):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))