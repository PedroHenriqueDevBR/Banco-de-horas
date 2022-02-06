from django import forms
from django.contrib.auth.models import User

class RegistrarUsuarioForm(forms.Form):
    nome = forms.CharField(required=True)
    matricula = forms.CharField(required=True)
    setor = forms.IntegerField(required=True)
    email = forms.CharField(required=True)
    senha = forms.CharField(required=True)
    ch_primeira = forms.TimeField(required=True)
    ch_segunda = forms.TimeField(required=True)
    
    def is_valid(self):
        valid = True
        if not super(RegistrarUsuarioForm, self).is_valid():
            self.adiciona_erro('Por favor verifique os campos digitados.')
            valid = False

        user_exists = User.objects.filter(username=self.cleaned_data['matricula']).exists()
        if user_exists:
            self.adiciona_erro('Usuário já cadastrado')
            valid = False

        return valid

    def adiciona_erro(self, message):
        errors = None
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
        errors.append(message)