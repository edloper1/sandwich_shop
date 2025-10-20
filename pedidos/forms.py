from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Div
from .models import Pedido

class CheckoutForm(forms.Form):
    nombre_cliente = forms.CharField(
        max_length=100,
        label='Nombre completo',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre completo'})
    )
    
    email_cliente = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tu@email.com'})
    )
    
    telefono_cliente = forms.CharField(
        max_length=20,
        label='Teléfono',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1234567890'})
    )
    
    tipo_entrega = forms.ChoiceField(
        choices=Pedido.TIPO_ENTREGA_CHOICES,
        label='Tipo de entrega',
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    
    direccion_entrega = forms.CharField(
        required=False,
        label='Dirección de entrega',
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 3, 
            'placeholder': 'Dirección completa para delivery'
        })
    )
    
    notas_cliente = forms.CharField(
        required=False,
        label='Notas especiales',
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 3, 
            'placeholder': 'Instrucciones especiales para tu pedido...'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nombre_cliente', css_class='form-group col-md-6 mb-3'),
                Column('email_cliente', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('telefono_cliente', css_class='form-group col-md-6 mb-3'),
            ),
            Div(
                'tipo_entrega',
                css_class='form-group mb-3'
            ),
            'direccion_entrega',
            'notas_cliente',
            Submit('submit', 'Confirmar Pedido', css_class='btn btn-primary btn-lg w-100')
        )

    def clean(self):
        cleaned_data = super().clean()
        tipo_entrega = cleaned_data.get('tipo_entrega')
        direccion_entrega = cleaned_data.get('direccion_entrega')

        if tipo_entrega == 'delivery' and not direccion_entrega:
            raise forms.ValidationError('La dirección de entrega es requerida para delivery.')

        return cleaned_data