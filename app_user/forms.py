from django import forms
from bailti.models import User  # 💡 on importe le modèle défini dans l'autre app

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'nom', 'prenom', 'date_naissance', 'lieu_naissance', 'sex', 'phone']

        # 🎨 Personnalisation des widgets HTML :
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6',
                'placeholder': 'Votre adresse email'
            }),
            'nom': forms.TextInput(attrs={
                'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6',
                'placeholder': 'Nom'
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6',
                'placeholder': 'Prénom'
            }),
            'date_naissance': forms.DateInput(attrs={
                'type': 'date',
                'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6',
            }),
            'lieu_naissance': forms.TextInput(attrs={
                'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6',
                'placeholder': 'Lieu de naissance'
            }),
            'sex': forms.Select(attrs={
                'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6',
            }, choices=[('Homme', 'Homme'), ('Femme', 'Femme')]),
            'phone': forms.TextInput(attrs={
                'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6',
                'placeholder': 'Téléphone'
            }),
        }