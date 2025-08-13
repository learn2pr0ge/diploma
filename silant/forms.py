from django import forms
from django.utils.translation import gettext_lazy as _
from .models import (Car, Technicalmaintenance, Claimservice, Booktechnic, Bookengine, Bookclutch,
                     Bookaxle, Bookbridge, Bookcompanies, Bookclaimpart, Bookclaimrecover)

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'factory_number',
            'model_technic',
            'model_engine',
            'engine_factory_number',
            'model_clutch',
            'clutch_factory_number',
            'driven_axle_model',
            'driven_axle_factory_number',
            'managed_bridge_model',
            'managed_bridge_factory_number',
            'agreement_number',
            'agreement_date',
            'receiver',
            'receiver_address',
            'configuration',
            'client_name',
            'service_company',
        ]
        labels = {
            'factory_number': _('Заводской номер машины'),
            'model_technic': _('Модель техники'),
            'model_engine': _('Модель двигателя'),
            'engine_factory_number': _('Зав. № двигателя'),
            'model_clutch': _('Модель сцепления'),
            'clutch_factory_number': _('Зав. № сцепления'),
            'driven_axle_model': _('Модель ведущего моста'),
            'driven_axle_factory_number': _('Зав. № ведущего моста'),
            'managed_bridge_model': _('Модель управляемого моста'),
            'managed_bridge_factory_number': _('Зав. № управляемого моста'),
            'agreement_number': _('№ договора'),
            'agreement_date': _('Дата договора'),
            'receiver': _('Получатель'),
            'receiver_address': _('Адрес получателя'),
            'configuration': _('Комплектация (доп. опции)'),
            'client_name': _('Клиент'),
            'service_company': _('Сервисная компания'),
        }
        widgets = {
            'agreement_date': forms.DateInput(attrs={'type': 'date'}),
            'factory_number': forms.TextInput(attrs={'placeholder': 'Например, ЗАВ-1000'}),
            'engine_factory_number': forms.TextInput(attrs={'placeholder': 'Например, ЕНГ-2000'}),
            'clutch_factory_number': forms.TextInput(attrs={'placeholder': '…'}),
            'driven_axle_factory_number': forms.TextInput(attrs={'placeholder': '…'}),
            'managed_bridge_factory_number': forms.TextInput(attrs={'placeholder': '…'}),
            'receiver_address': forms.Textarea(attrs={'rows': 2}),
            'configuration': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name in [
            'model_technic', 'model_engine', 'model_clutch',
            'driven_axle_model', 'managed_bridge_model', 'service_company'
        ]:
            if name in self.fields and hasattr(self.fields[name], 'empty_label'):
                self.fields[name].empty_label = '— выберите —'

        for f in self.fields.values():
            f.widget.attrs.setdefault('class', 'form-control')

class TOForm(forms.ModelForm):
    class Meta:
        model = Technicalmaintenance
        fields = [
            'tm_car',
            'tm_service_company',
            'tm_type',
            'tm_number_date',
            'tm_date',
            'tm_hours',
            'tm_number',
        ]
        labels = {
            'tm_car': _('Машина'),
            'tm_service_company': _('Сервисная компания'),
            'tm_type': _('Тип ТО'),
            'tm_number_date': _('Дата документа'),
            'tm_date': _('Дата проведения ТО'),
            'tm_hours': _('Наработка, м/ч'),
            'tm_number': _('Номер документа'),
        }
        widgets = {
            'tm_car': forms.Select(),
            'tm_service_company': forms.Select(),
            'tm_type': forms.Select(),
            'tm_number_date': forms.DateInput(attrs={'type': 'date'}),
            'tm_date': forms.DateInput(attrs={'type': 'date'}),
            'tm_hours': forms.NumberInput(attrs={'min': 0, 'step': 1, 'placeholder': 'Напр.: 350'}),
            'tm_number': forms.TextInput(attrs={'placeholder': 'Напр.: №123'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('tm_car', 'tm_service_company', 'tm_type'):
            if name in self.fields and hasattr(self.fields[name], 'empty_label'):
                self.fields[name].empty_label = '— выберите —'

        for f in self.fields.values():
            f.widget.attrs.setdefault('class', 'form-control')

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claimservice
        fields = [
            'claim_car',
            'claim_service_company',
            'claim_part',
            'claim_date',
            'claim_description',
            'claim_hours',
            'claim_recover',
            'claim_used_parts',
            'claim_finish_date',
            'claim_downtime',
        ]
        labels = {
            'claim_car':            _('Машина'),
            'claim_service_company':_('Сервисная компания'),
            'claim_part':           _('Узел/деталь неисправности'),
            'claim_date':           _('Дата обращения'),
            'claim_description':    _('Описание рекламации'),
            'claim_hours':          _('Наработка, м/ч'),
            'claim_recover':        _('Устранено'),
            'claim_used_parts':     _('Использованные запчасти'),
            'claim_finish_date':    _('Дата завершения ремонта'),
            'claim_downtime':       _('Время простоя, дни'),
        }
        widgets = {
            'claim_date':        forms.DateInput(attrs={'type': 'date'}),
            'claim_finish_date': forms.DateInput(attrs={'type': 'date'}),
            'claim_description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Кратко опишите неисправность…'}),
            'claim_used_parts':  forms.Textarea(attrs={'rows': 2, 'placeholder': 'Перечислите запчасти…'}),
            'claim_hours':       forms.NumberInput(attrs={'min': 0, 'step': 1, 'placeholder': 'Напр.: 350'}),
            'claim_downtime':    forms.NumberInput(attrs={'min': 0, 'step': 1}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name in ('claim_car', 'claim_service_company', 'claim_part'):
            f = self.fields.get(name)
            if f and hasattr(f, 'empty_label'):
                f.empty_label = '— выберите —'

        for f in self.fields.values():
            f.widget.attrs.setdefault('class', 'form-control')

class EngineForm(forms.ModelForm):
    class Meta:
        model = Bookengine
        fields = ['model_engine_name', 'model_engine_desc']
        labels = {
            'model_engine_name': _('Модель двигателя'),
            'model_engine_desc': _('Описание модели двигателя'),
        }
        widgets = {
            'model_engine_name': forms.TextInput(attrs={'placeholder': 'Напр.: ЯМЗ-238'}),
            'model_engine_desc': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Краткое описание…'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.setdefault('class', 'form-control')


class TechnicForm(forms.ModelForm):
    class Meta:
        model = Booktechnic
        fields = ['model_technic_name', 'model_technic_desc']
        labels = {
            'model_technic_name': _('Модель техники'),
            'model_technic_desc': _('Описание модели техники'),
        }
        widgets = {
            'model_technic_name': forms.TextInput(attrs={'placeholder': 'Напр.: К-744'}),
            'model_technic_desc': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Краткое описание…'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.setdefault('class', 'form-control')

class ClutchForm(forms.ModelForm):
    class Meta:
        model = Bookclutch
        fields = ['model_clutch_name', 'model_clutch_desc']
        labels = {
            'model_clutch_name': _('Модель сцепления'),
            'model_clutch_desc': _('Описание модели сцепления'),
        }
        widgets = {
            'model_clutch_name': forms.TextInput(attrs={'placeholder': 'Напр.: СЦ-186'}),
            'model_clutch_desc': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Краткое описание…'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.setdefault('class', 'form-control')

class AxleForm(forms.ModelForm):
    class Meta:
        model = Bookaxle
        fields = ['model_axle_name', 'model_axle_desc']
        labels = {
            'model_axle_name': _('Модель моста'),
            'model_axle_desc': _('Описание модели моста'),
        }
        widgets = {
            'model_axle_name': forms.TextInput(attrs={'placeholder': 'Напр.: Carraro 709'}),
            'model_axle_desc': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Краткое описание…'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.setdefault('class', 'form-control')

class BridgeForm(forms.ModelForm):
    class Meta:
        model = Bookbridge
        fields = ['model_bridge_name', 'model_bridge_desc']
        labels = {
            'model_bridge_name': _('Модель моста'),
            'model_bridge_desc': _('Описание модели моста'),
        }
        widgets = {
            'model_bridge_name': forms.TextInput(attrs={'placeholder': 'Напр.: МВ-40 / Carraro 709'}),
            'model_bridge_desc': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Краткое описание…'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.setdefault('class', 'form-control')

class ServiceCompanyForm(forms.ModelForm):
    class Meta:
        model = Bookcompanies
        fields = ['model_company_name', 'model_company_desc']
        labels = {
            'model_company_name': _('Название сервисной компании'),
            'model_company_desc': _('Описание'),
        }
        widgets = {
            'model_company_name': forms.TextInput(attrs={'placeholder': 'Напр.: ООО «Силант-Сервис»'}),
            'model_company_desc': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Краткое описание…'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.setdefault('class', 'form-control')

class ClaimPartForm(forms.ModelForm):
    class Meta:
        model = Bookclaimpart
        fields = ['model_claimpart_name', 'model_claimpart_desc']
        labels = {
            'model_claimpart_name': _('Узел/деталь рекламации'),
            'model_claimpart_desc': _('Описание'),
        }
        widgets = {
            'model_claimpart_name': forms.TextInput(attrs={'placeholder': 'Напр.: Гидронасос НШ-50'}),
            'model_claimpart_desc': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Краткое описание…'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.setdefault('class', 'form-control')

class ClaimRecoverForm(forms.ModelForm):
    class Meta:
        model = Bookclaimrecover
        fields = ['model_claimrecover_name', 'model_claimrecover_desc']
        labels = {
            'model_claimrecover_name': _('Способ устранения'),
            'model_claimrecover_desc': _('Описание'),
        }
        widgets = {
            'model_claimrecover_name': forms.TextInput(attrs={'placeholder': 'Напр.: Замена узла'}),
            'model_claimrecover_desc': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Краткое описание…'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.setdefault('class', 'form-control')


class ClaimPersonalForm(forms.ModelForm):
    class Meta:
        model = Claimservice
        fields = [
            'claim_car',
            'claim_service_company',
            'claim_recover',
            'claim_part',
            'claim_date',
            'claim_description',
            'claim_hours',
            'claim_finish_date',
            'claim_downtime',
        ]
        labels = {
            'claim_car':           _('Машина'),
            'claim_service_company': _('Сервисная компания'),
            'claim_recover':       _('Способ устранения'),
            'claim_part':          _('Узел/деталь'),
            'claim_date':          _('Дата обращения'),
            'claim_description':   _('Описание рекламации'),
            'claim_hours':         _('Наработка, м/ч'),
            'claim_finish_date':   _('Дата окончания'),
            'claim_downtime':      _('Время простоя')
        }
        widgets = {
            'claim_date':        forms.DateInput(attrs={'type': 'date'}),
            'claim_description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Кратко опишите неисправность…'}),
            'claim_hours':       forms.NumberInput(attrs={'min': 0, 'step': 1, 'placeholder': 'Напр.: 350'}),
            'claim_finish_date': forms.DateInput(attrs={'type': 'date'}),
            'claim_downtime':    forms.NumberInput(attrs={'min': 0, 'step': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name in ('claim_car', 'claim_service_company', 'claim_recover', 'claim_part'):
            f = self.fields.get(name)
            if f and hasattr(f, 'empty_label'):
                f.empty_label = '— выберите —'

        for f in self.fields.values():
            f.widget.attrs.setdefault('class', 'form-control')