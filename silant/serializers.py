from rest_framework import serializers
from .models import Car, Technicalmaintenance, Claimservice


class CarSerializer(serializers.ModelSerializer):
    Зав_номер = serializers.CharField(source='factory_number')
    Модель_техники = serializers.CharField(source='model_technic.model_technic_name')
    Модель_двигателя = serializers.CharField(source='model_engine.model_engine_name')
    Зав_номер_двигателя = serializers.CharField(source='engine_factory_number')
    Модель_транс = serializers.CharField(source='model_clutch.model_clutch_name')
    Зав_ном_транс = serializers.CharField(source='clutch_factory_number')
    Ведущий_мост = serializers.CharField(source='driven_axle_model.model_axle_name')
    Зав_номер_вед_моста = serializers.CharField(source='driven_axle_factory_number')
    Управляемый_мост = serializers.CharField(source='managed_bridge_model.model_bridge_name')
    Зав_номер_упр_моста = serializers.CharField(source='managed_bridge_factory_number')

    class Meta:
        model = Car
        fields = [
            'Зав_номер',
            'Модель_техники',
            'Модель_двигателя',
            'Зав_номер_двигателя',
            'Модель_транс',
            'Зав_ном_транс',
            'Ведущий_мост',
            'Зав_номер_вед_моста',
            'Управляемый_мост',
            'Зав_номер_упр_моста'
        ]

class CarListSerializer(serializers.ModelSerializer):
    Зав_номер = serializers.CharField(source='factory_number')
    Модель_техники = serializers.CharField(source='model_technic.model_technic_name')
    Модель_двигателя = serializers.CharField(source='model_engine.model_engine_name')
    Зав_номер_двигателя = serializers.CharField(source='engine_factory_number')
    Модель_транс = serializers.CharField(source='model_clutch.model_clutch_name')
    Зав_ном_транс = serializers.CharField(source='clutch_factory_number')
    Ведущий_мост = serializers.CharField(source='driven_axle_model.model_axle_name')
    Зав_номер_вед_моста = serializers.CharField(source='driven_axle_factory_number')
    Управляемый_мост = serializers.CharField(source='managed_bridge_model.model_bridge_name')
    Зав_номер_упр_моста = serializers.CharField(source='managed_bridge_factory_number')
    Ном_договора = serializers.CharField(source='agreement_number')
    Дата_договора = serializers.DateField(source='agreement_date')
    Получатель = serializers.CharField(source='receiver')
    Адрес_получ = serializers.CharField(source='receiver_address')
    Конфиг = serializers.CharField(source='configuration')
    Имя_клиента = serializers.CharField(source='client_name')
    Серв_компания = serializers.CharField(source='service_company.model_company_name')

    class Meta:
        model = Car
        fields = [
            'Зав_номер',
            'Модель_техники',
            'Модель_двигателя',
            'Зав_номер_двигателя',
            'Модель_транс',
            'Зав_ном_транс',
            'Ведущий_мост',
            'Зав_номер_вед_моста',
            'Управляемый_мост',
            'Зав_номер_упр_моста',
            'Ном_договора',
            'Дата_договора',
            'Получатель',
            'Адрес_получ',
            'Конфиг',
            'Имя_клиента',
            'Серв_компания'

        ]

class TOSerializer(serializers.ModelSerializer):
    Тип_ТО = serializers.CharField(source='tm_type.model_tm_name')
    Дата_ТО = serializers.DateField(source='tm_date')
    Мото_ч = serializers.IntegerField(source='tm_hours')
    Номер_ЗН = serializers.CharField(source='tm_number')
    Дата_ЗН = serializers.DateField(source='tm_number_date')
    Сервисная_комп = serializers.CharField(source='tm_service_company.model_company_name')
    Авто = serializers.CharField(source='tm_car.factory_number')

    class Meta:
        model = Technicalmaintenance
        fields = [
        'Тип_ТО',
        'Дата_ТО',
        'Мото_ч',
        'Номер_ЗН',
        'Дата_ЗН',
        'Сервисная_комп',
        'Авто',
            ]

class ClaimserviceSerializer(serializers.ModelSerializer):
    Дата_откз = serializers.DateField(source='claim_date')
    Нара_МЧ = serializers.IntegerField(source='claim_hours')
    Узел_отк = serializers.CharField(source='claim_part.model_claimpart_name')
    Опис_отк = serializers.CharField(source='claim_description')
    Способ_вост = serializers.CharField(source='claim_recover.model_claimrecover_name')
    Исп_ЗЧ = serializers.CharField(source='claim_used_parts')
    Дата_вост = serializers.DateField(source='claim_finish_date')
    Время_прост = serializers.IntegerField(source='claim_downtime')
    Сервисная_комп = serializers.CharField(source='claim_service_company.model_company_name')
    Авто = serializers.CharField(source='claim_car.factory_number')

    class Meta:
        model = Claimservice
        fields = [
            'Дата_откз',
            'Нара_МЧ',
            'Узел_отк',
            'Опис_отк',
            'Способ_вост',
            'Исп_ЗЧ',
            'Дата_вост',
            'Время_прост',
            'Сервисная_комп',
            'Авто',

        ]