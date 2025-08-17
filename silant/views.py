from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import (Car, Technicalmaintenance, Claimservice, Bookengine, Booktechnic, Bookclutch, Bookaxle,
                     Bookbridge, Bookcompanies, Booktm, Bookclaimpart, Bookclaimrecover)
from .serializers import CarSerializer, CarListSerializer, TOSerializer, ClaimserviceSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .forms import (CarForm, TOForm, ClaimForm, EngineForm, TechnicForm, ClutchForm, AxleForm, BridgeForm,
                    ServiceCompanyForm, ClaimPartForm, ClaimRecoverForm, ClaimPersonalForm)


from drf_spectacular.views import SpectacularSwaggerView


class CarView(APIView):
    def post(self, request):
        car = request.data.get('factory_number')
        try:
            result = Car.objects.filter(factory_number=car)
            serializer = CarSerializer(result, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Car.DoesNotExist:
            return Response({'error': 'Нет авто с таким заводским номером'}, status=400)


@login_required
def get_token(request):
    token, _ = Token.objects.get_or_create(user=request.user)
    return render(request, 'memberzone.html', {'token': token.key})

#страница данные по машине
@login_required
def carlist(request, factory_number):
    try:
       car = Car.objects.get(factory_number=factory_number.strip())
       # проверка что пользователь может получить данные об авто
       if request.user.client_name == car.client_name:
           return render(request, 'cardetail.html', {'car': car})
       elif request.user.service_organization == car.service_company.model_company_name:
           return render(request, 'cardetail.html', {'car': car})
       elif request.user.management:
           return render(request, 'cardetail.html', {'car': car})
       else:
           return render(request,'cardetail.html', {'error': 'У вас нет доступа для просмотра данной информации' })
    except Car.DoesNotExist:
        return render(request,'cardetail.html', {'error': 'Нет такого авто' })
    return render(request, 'memberzone.html')

#страница данных по модели двигателя
@login_required
def enginelist(request, engine_number):
    try:
        car = Car.objects.filter(model_engine__model_engine_name=engine_number.strip(),
                                 client_name=request.user.client_name).exists()
        car_service = Car.objects.filter(model_engine__model_engine_name=engine_number.strip(),service_company__model_company_name=request.user.service_organization).exists()
        if car:
            engine = Bookengine.objects.get(model_engine_name=engine_number.strip())
            return render(request, 'enginemodel.html', {'engine': engine})
        elif car_service:
            engine = Bookengine.objects.get(model_engine_name=engine_number.strip())
            return render(request, 'enginemodel.html', {'engine': engine})
        elif request.user.management:
            engine = Bookengine.objects.get(model_engine_name=engine_number.strip())
            return render(request, 'enginemodel.html', {'engine': engine})
        else:
            return render(request,'enginemodel.html', {'error': 'У вас нет доступа для просмотра данной информации'})
    except Bookengine.DoesNotExist:
        return render(request,'enginemodel.html', {'error:':'Нет такой модели двигателя'})
    return render(request, 'memberzone.html')

#страница данных по модели техники

@login_required
def techlist(request, model_technic):
    try:
        car = Car.objects.filter(model_technic__model_technic_name=model_technic.strip(),
                                 client_name=request.user.client_name).exists()
        car_service = Car.objects.filter(model_technic__model_technic_name=model_technic.strip(),service_company__model_company_name=request.user.service_organization).exists()
        if car:
            model_technic_name = Booktechnic.objects.get(model_technic_name=model_technic.strip())
            return render(request, 'techmodel.html', {'model_technic': model_technic_name})
        elif car_service:
            model_technic_name = Booktechnic.objects.get(model_technic_name=model_technic.strip())
            return render(request, 'techmodel.html', {'model_technic': model_technic_name})
        elif request.user.management:
            model_technic_name = Booktechnic.objects.get(model_technic_name=model_technic.strip())
            return render(request, 'techmodel.html', {'model_technic': model_technic_name})
        else:
            return render(request, 'techmodel.html', {'error': 'У вас нет доступа для просмотра данной информации'})
    except Booktechnic.DoesNotExist:
        return render(request, 'techmodel.html', {'error': 'Нет такой модели'})
    return render(request, 'memberzone.html')

#страница данных по модели трансмиссии

@login_required
def clutchlist(request, model_clutch):
    try:
        car = Car.objects.filter(model_clutch__model_clutch_name=model_clutch.strip(),
                                 client_name=request.user.client_name).exists()
        car_service = Car.objects.filter(model_clutch__model_clutch_name=model_clutch.strip(),service_company__model_company_name=request.user.service_organization).exists()
        if car:
            model_clutch_name = Bookclutch.objects.get(model_clutch_name=model_clutch.strip())
            return render(request, 'clutchmodel.html', {'model_clutch': model_clutch_name})
        elif car_service:
            model_clutch_name = Bookclutch.objects.get(model_clutch_name=model_clutch.strip())
            return render(request, 'clutchmodel.html', {'model_clutch': model_clutch_name})
        elif request.user.management:
            model_clutch_name = Bookclutch.objects.get(model_clutch_name=model_clutch.strip())
            return render(request, 'clutchmodel.html', {'model_clutch': model_clutch_name})
        else:
            return render(request, 'clutchmodel.html', {'error': 'У вас нет доступа для просмотра этой информации'})
    except Bookclutch.DoesNotExist:
        return render(request, 'clutchmodel.html', {'error':'Нет такой модели'})
    return render(request, 'memberzone.html')

#страница данных о модели сцепления

@login_required
def axlelist(request, model_axle):
    try:
        car = Car.objects.filter(driven_axle_model__model_axle_name=model_axle.strip(),
                                 client_name=request.user.client_name).exists()
        car_service = Car.objects.filter(driven_axle_model__model_axle_name=model_axle.strip(),service_company__model_company_name=request.user.service_organization).exists()
        if car:
            model_axle_name = Bookaxle.objects.get(model_axle_name=model_axle.strip())
            return render(request, 'axlemodel.html', {'model_axle': model_axle_name})
        elif car_service:
            model_axle_name = Bookaxle.objects.get(model_axle_name=model_axle.strip())
            return render(request, 'axlemodel.html', {'model_axle': model_axle_name})
        elif request.user.management:
            model_axle_name = Bookaxle.objects.get(model_axle_name=model_axle.strip())
            return render(request, 'axlemodel.html', {'model_axle': model_axle_name})
        else:
            return render(request, 'axlemodel.html', {'error': 'У вас нет доступа для просмотра этой информации'})
    except Bookaxle.DoesNotExist:
        return render(request, 'axlemodel.html', {'error': 'Нет такой модели'})
    return render(request, 'memberzone.html')

#страница данных о модели управляемого моста

@login_required
def bridgelist(request, model_bridge):
    try:
        car = Car.objects.filter(managed_bridge_model__model_bridge_name=model_bridge.strip(),
                                 client_name=request.user.client_name).exists()
        car_service = Car.objects.filter(managed_bridge_model__model_bridge_name=model_bridge.strip(),service_company__model_company_name=request.user.service_organization).exists()
        if car:
            model_bridge_name = Bookbridge.objects.get(model_bridge_name=model_bridge.strip())
            return render(request, 'bridgemodel.html', {'model_bridge': model_bridge_name})
        elif car_service:
            model_bridge_name = Bookbridge.objects.get(model_bridge_name=model_bridge.strip())
            return render(request, 'bridgemodel.html', {'model_bridge': model_bridge_name})
        elif request.user.management:
            model_bridge_name = Bookbridge.objects.get(model_bridge_name=model_bridge.strip())
            return render(request, 'bridgemodel.html', {'model_bridge': model_bridge_name})
        else:
            return render(request, 'bridgemodel.html', {'error': 'У вас нет доступа для просмотра этой информации'})
    except Bookbridge.DoesNotExist:
        return render(request, 'bridgemodel.html', {'error': 'Нет такой модели'})
    return render(request, 'memberzone.html')

#страница данных о сервисных компаниях

@login_required
def servicelist(request, model_service):
    try:
        car = Car.objects.filter(service_company__model_company_name=model_service.strip(),
                                 client_name=request.user.client_name).exists()
        car_service = Car.objects.filter(service_company__model_company_name=request.user.service_organization).exists()

        if car:
            service_name = Bookcompanies.objects.get(model_company_name=model_service.strip())
            return render(request, 'servicemodel.html', {'service_company': service_name})
        elif car_service:
            service_name = Bookcompanies.objects.get(model_company_name=model_service.strip())
            return render(request, 'servicemodel.html', {'service_company': service_name})
        elif request.user.management:
            service_name = Bookcompanies.objects.get(model_company_name=model_service.strip())
            return render(request, 'servicemodel.html', {'service_company': service_name})
        else:
            return render(request, 'servicemodel.html', {'error': 'У вас нет доступа для просмотра этой информации'})
    except Bookcompanies.DoesNotExist:
        return render(request, 'servicemodel.html', {'error': 'Нет такой модели'})
    return render(request, 'memberzone.html')

#страница данных о типе ТО

@login_required
def tolist(request,tm_type):
    try:
        to_list = Technicalmaintenance.objects.filter(tm_type__model_tm_name=tm_type.strip(), tm_car__client_name=request.user.client_name).exists()
        to_service = Technicalmaintenance.objects.filter(tm_type__model_tm_name=tm_type.strip(), tm_service_company__model_company_name=request.user.service_organization).exists()
        if to_list:
            tm_type_name = Booktm.objects.get(model_tm_name=tm_type.strip())
            return render(request, 'tolist.html', {'tm_type': tm_type_name})
        elif to_service:
            tm_type_name = Booktm.objects.get(model_tm_name=tm_type.strip())
            return render(request, 'tolist.html', {'tm_type': tm_type_name})
        elif request.user.management:
            tm_type_name = Booktm.objects.get(model_tm_name=tm_type.strip())
            return render(request, 'tolist.html', {'tm_type': tm_type_name})
        else:
            return render(request, 'tolist.html', {'error': 'У вас нет доступа для просмотра этой информации'})
    except Booktm.DoesNotExist:
        return render(request, 'tolist.html', {'error': 'Нет такой модели'})
    return render(request, 'memberzone.html')

# страница данных о сломавшемся узле

@login_required
def claimpart(request, claim_part):
    try:
        claim = Claimservice.objects.filter(claim_part__model_claimpart_name=claim_part.strip(),claim_car__client_name=request.user.client_name).exists()
        claim_service = Claimservice.objects.filter(claim_part__model_claimpart_name=claim_part.strip(),claim_service_company__model_company_name=request.user.service_organization).exists()
        if claim:
            claim_part_name = Bookclaimpart.objects.get(model_claimpart_name=claim_part.strip())
            return render(request, 'claimpart.html', {'claim_part': claim_part_name})
        elif claim_service:
            claim_part_name = Bookclaimpart.objects.get(model_claimpart_name=claim_part.strip())
            return render(request, 'claimpart.html', {'claim_part': claim_part_name})
        elif request.user.management:
            claim_part_name = Bookclaimpart.objects.get(model_claimpart_name=claim_part.strip())
            return render(request, 'claimpart.html', {'claim_part': claim_part_name})
        else:
            return render(request, 'claimpart.html', {'error': 'У вас нет доступа для просмотра этой информации'})
    except Bookclaimpart.DoesNotExist:
        return render(request, 'claimpart.html', {'error': 'Нет такой модели'})
    return render(request, 'memberzone.html')

# страница данных о способах восстановления

def claimrecover(request, claim_recover):
    try:
        claim = Claimservice.objects.filter(claim_recover__model_claimrecover_name=claim_recover.strip(),claim_car__client_name=request.user.client_name).exists()
        claim_service = Claimservice.objects.filter(claim_recover__model_claimrecover_name=claim_recover.strip(),claim_service_company__model_company_name=request.user.service_organization).exists()
        if claim:
            claim_recover_name = Bookclaimrecover.objects.get(model_claimrecover_name=claim_recover.strip())
            return render(request, 'claimrecover.html', {'claim_recover': claim_recover_name})
        elif claim_service:
            claim_recover_name = Bookclaimrecover.objects.get(model_claimrecover_name=claim_recover.strip())
            return render(request, 'claimrecover.html', {'claim_recover': claim_recover_name})
        elif request.user.management:
            claim_recover_name = Bookclaimrecover.objects.get(model_claimrecover_name=claim_recover.strip())
            return render(request, 'claimrecover.html', {'claim_recover': claim_recover_name})
        else:
            return render(request, 'claimrecover.html', {'error': 'У вас нет доступа для просмотра этой информации'})
    except Bookclaimrecover.DoesNotExist:
        return render(request, 'claimrecover.html', {'error': 'Нет такой модели'})
    return render(request, 'memberzone.html')




# основные API ендпоинты

class CarList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.client_name:
            cars = Car.objects.filter(client_name=request.user.client_name).order_by('-agreement_date')
            serializer = CarListSerializer(cars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.service_organization:
            cars = Car.objects.filter(service_company__model_company_name=request.user.service_organization).order_by('-agreement_date')
            serializer = CarListSerializer(cars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.management:
            cars = Car.objects.all().order_by('-agreement_date')
            serializer = CarListSerializer(cars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

# вывод машин с сортировкой по переменной

class CarListSort(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sort = request.data.get('sort_by')
        direct = request.data.get('direction')
        ALLOWED = {'factory_number', 'model_technic__model_technic_name', 'model_engine__model_engine_name', 'engine_factory_number',
                   'model_clutch__model_clutch_name', 'clutch_factory_number', 'managed_bridge_model__model_bridge_name',
                   'driven_axle_model__model_axle_name', 'driven_axle_factory_number', 'managed_bridge_factory_number','agreement_number','agreement_date', 'receiver', 'receiver_address', 'configuration', 'client_name', 'service_company', 'asc','desc'}
        if not sort and direct or sort and direct not in ALLOWED:
            return Response({'error': 'Введите правильное имя фильтра'}, status=status.HTTP_400_BAD_REQUEST)
        if direct == 'asc':
            sort = f'{sort}'
        else:
            sort = f'-{sort}'
        if request.user.client_name:
            cars = Car.objects.filter(client_name=request.user.client_name).order_by(sort)
            serializer = CarListSerializer(cars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.service_organization:
            cars = Car.objects.filter(service_company__model_company_name=request.user.service_organization).order_by(sort)
            serializer = CarListSerializer(cars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.management:
            cars = Car.objects.all().order_by(sort)
            serializer = CarListSerializer(cars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

# вывод ТО с сортировкой по переменной

class TOListSort(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sort = request.data.get('sort_by')
        direct = request.data.get('direction')
        ALLOWED = {'tm_date','tm_hours','tm_number','tm_number_date','tm_car__factory_number', 'tm_service_company__model_company_name', 'tm_type__model_tm_name' ,'asc','desc'}
        if not sort and direct or sort and direct not in ALLOWED:
            return Response({'error': 'Введите правильное имя фильтра'}, status=status.HTTP_400_BAD_REQUEST)
        if direct == 'asc':
            sort = f'{sort}'
        else:
            sort = f'-{sort}'
        if request.user.client_name:
            cars = Technicalmaintenance.objects.filter(tm_car__client_name=request.user.client_name).order_by(sort)
            serializer = TOSerializer(cars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.service_organization:
            cars = Technicalmaintenance.objects.filter(
                tm_service_company__model_company_name=request.user.service_organization).order_by(sort)
            serializer = TOSerializer(cars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.management:
            cars = Technicalmaintenance.objects.all().order_by(sort)
            serializer = TOSerializer(cars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

#вывод рекламаций с сортировкой по переменной

class ClaimListSort(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        sort = request.data.get('sort_by')
        direct = request.data.get('direction')
        ALLOWED = {'claim_car__factory_number', 'claim_service_company__model_company_name', 'claim_recover__model_claimrecover_name','claim_part__model_claimpart_name','claim_date','claim_hours','claim_description','asc','desc','claim_used_parts','claim_finish_date','claim_downtime'}
        if not sort and direct or sort and direct not in ALLOWED:
            return Response({'error': 'Введите правильное имя фильтра'}, status=status.HTTP_400_BAD_REQUEST)
        if direct == 'asc':
            sort = f'{sort}'
        else:
            sort = f'-{sort}'
        if request.user.client_name:
            cars = Claimservice.objects.filter(claim_car__client_name=request.user.client_name).order_by(sort)
            serializer = ClaimserviceSerializer(cars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.service_organization:
            cars = Claimservice.objects.filter(
                claim_service_company__model_company_name=request.user.service_organization).order_by(sort)
            serializer = ClaimserviceSerializer(cars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.management:
            cars = Claimservice.objects.all().order_by(sort)
            serializer = ClaimserviceSerializer(cars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)




#вывод полного списка TO

class TOList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.client_name:
            technical_maintenance = Technicalmaintenance.objects.filter(tm_car__client_name=request.user.client_name).order_by('-tm_date')
            serializer = TOSerializer(technical_maintenance, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.service_organization:
            technical_maintenance = Technicalmaintenance.objects.filter(tm_service_company__model_company_name=request.user.service_organization).order_by('-tm_date')
            serializer = TOSerializer(technical_maintenance, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.management:
            technical_maintenance = Technicalmaintenance.objects.all().order_by('-tm_date')
            serializer = TOSerializer(technical_maintenance, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class ClaimsList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.client_name:
            claim = Claimservice.objects.filter(claim_car__client_name=request.user.client_name).order_by('-claim_date')
            serializer = ClaimserviceSerializer(claim, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.service_organization:
            claim = Claimservice.objects.filter(claim_service_company__model_company_name=request.user.service_organization).order_by('-claim_date')
            serializer = ClaimserviceSerializer(claim, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.management:
            claim = Claimservice.objects.all().order_by('-claim_date')
            serializer = ClaimserviceSerializer(claim, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

# поиск по фильтрам машины

class FilterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        filter = request.data.get('filter')
        value = request.data.get('value')
        sort = request.data.get('sort_by')
        direct = request.data.get('direction')
        ALLOWED = {'factory_number', 'model_technic__model_technic_name', 'model_engine__model_engine_name', 'model_clutch__model_clutch_name', 'managed_bridge_model__model_bridge_name', 'driven_axle_model__model_axle_name', 'asc', 'desc','engine_factory_number', 'clutch_factory_number', 'driven_axle_factory_number', 'managed_bridge_factory_number','agreement_date', 'receiver', 'receiver_address', 'configuration', 'client_name', 'asc','desc','model_technic__model_technic_name','service_company__model_company_name'}
        if not filter and sort and direct or filter and sort and direct not in ALLOWED:
            return Response({'error': 'Введите правильное имя фильтра'}, status=status.HTTP_400_BAD_REQUEST)
        if direct == 'asc':
            sort = f'{sort}'
        else:
            sort = f'-{sort}'
        if request.user.client_name:
            cars = Car.objects.filter(client_name=request.user.client_name, **{filter: value}).order_by(sort)
            serializer = CarListSerializer(cars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.service_organization:
            cars = Car.objects.filter(service_company__model_company_name=request.user.service_organization, **{filter: value}).order_by(sort)
            serializer = CarListSerializer(cars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.management:
            cars = Car.objects.filter(**{filter: value}).order_by(sort)
            serializer = CarListSerializer(cars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

# поиск по фильтрам машины ТО

class FilterTOView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        filter = request.data.get('filter')
        value = request.data.get('value')
        sort = request.data.get('sort_by')
        direct = request.data.get('direction')
        ALLOWED = {'tm_date', 'tm_hours', 'tm_number', 'tm_number_date', 'tm_car__factory_number',
                   'tm_service_company__model_company_name', 'tm_type__model_tm_name', 'asc', 'desc'}
        if not filter and sort and direct or filter and sort and direct not in ALLOWED:
            return Response({'error': 'Введите правильное имя фильтра'}, status=status.HTTP_400_BAD_REQUEST)
        if direct == 'asc':
            sort = f'{sort}'
        else:
            sort = f'-{sort}'
        if request.user.client_name:
            technical_maintenance = Technicalmaintenance.objects.filter(tm_car__client_name=request.user.client_name, **{filter: value}).order_by(sort)
            serializer = TOSerializer(technical_maintenance, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.service_organization:
            technical_maintenance = Technicalmaintenance.objects.filter(tm_service_company__model_company_name=request.user.service_organization, **{filter: value}).order_by(sort)
            serializer = TOSerializer(technical_maintenance, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.management:
            technical_maintenance = Technicalmaintenance.objects.filter(**{filter: value}).order_by(sort)
            serializer = TOSerializer(technical_maintenance, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

# поиск по фильтрам рекламации

class FilterClaimView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        filter = request.data.get('filter')
        value = request.data.get('value')
        sort = request.data.get('sort_by')
        direct = request.data.get('direction')
        ALLOWED = {'claim_car__factory_number', 'claim_service_company__model_company_name', 'claim_recover__model_claimrecover_name','claim_part__model_claimpart_name','claim_date','claim_hours','claim_description','asc','desc','claim_used_parts','claim_finish_date','claim_downtime'}

        if not filter and sort and direct or filter and sort and direct not in ALLOWED:
            return Response({'error': 'Введите правильное имя фильтра'}, status=status.HTTP_400_BAD_REQUEST)
        if direct == 'asc':
            sort = f'{sort}'
        else:
            sort = f'-{sort}'
        if request.user.client_name:
            claims = Claimservice.objects.filter(claim_car__client_name=request.user.client_name, **{filter: value}).order_by(sort)
            serializer = ClaimserviceSerializer(claims, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.service_organization:
            claims = Claimservice.objects.filter(claim_service_company__model_company_name=request.user.service_organization, **{filter: value}).order_by(sort)
            serializer = ClaimserviceSerializer(claims, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.management:
            claims = Claimservice.objects.filter(**{filter: value}).order_by(sort)
            serializer = ClaimserviceSerializer(claims, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)



class CarCreate(LoginRequiredMixin, CreateView):
    model = Car
    form_class = CarForm
    # fields = ['factory_number', 'model_technic', 'model_engine', 'engine_factory_number', 'model_clutch', 'clutch_factory_number', 'driven_axle_model', 'driven_axle_factory_number', 'managed_bridge_model', 'managed_bridge_factory_number', 'agreement_number', 'agreement_date', 'receiver', 'receiver_address', 'configuration', 'client_name', 'service_company']
    template_name = 'carcreate.html'
    success_url = '/memberzone/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# создание нового ТО

class TOCreate(LoginRequiredMixin, CreateView):
    model = Technicalmaintenance
    form_class = TOForm
    # fields = ['tm_car', 'tm_service_company', 'tm_type', 'tm_number_date', 'tm_date', 'tm_hours', 'tm_number']
    template_name = 'tocreate.html'
    success_url = '/memberzone/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# создание новой рекламации

class ClaimCreate(LoginRequiredMixin, CreateView):
    model = Claimservice
    form_class = ClaimForm
    # fields = ['claim_car', 'claim_service_company', 'claim_recover', 'claim_part', 'claim_date', 'claim_description', 'claim_hours', 'claim_recover',
    #           'claim_used_parts', 'claim_finish_date', 'claim_downtime']
    template_name = 'claimcreate.html'
    success_url = '/memberzone/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# создание нового двигателя

class EngineCreate(LoginRequiredMixin, CreateView):
    model = Bookengine
    form_class = EngineForm
    # fields = ['model_engine_name', 'model_engine_desc']
    template_name = 'enginecreate.html'
    success_url = '/memberzone/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# создание новой модели техники

class ModelCreate(LoginRequiredMixin, CreateView):
    model = Booktechnic
    form_class = TechnicForm
    # fields = ['model_technic_name', 'model_technic_desc']
    template_name = 'modelcreate.html'
    success_url = '/memberzone/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# создание новой модели трансмиссии

class ClutchCreate(LoginRequiredMixin, CreateView):
    model = Bookclutch
    form_class = ClutchForm
    # fields = ['model_clutch_name', 'model_clutch_desc']
    template_name = 'clutchcreate.html'
    success_url = '/memberzone/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# создание модели ведущего моста

class AxleCreate(LoginRequiredMixin, CreateView):
    model = Bookaxle
    form_class = AxleForm
    # fields = ['model_axle_name', 'model_axle_desc']
    template_name = 'axlecreate.html'
    success_url = '/memberzone/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# создание модели управляемого моста

class BridgeCreate(LoginRequiredMixin, CreateView):
    model = Bookbridge
    form_class = BridgeForm
    # fields = ['model_bridge_name', 'model_bridge_desc']
    template_name = 'bridgecreate.html'
    success_url = '/memberzone/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# создание модели сервисной компании

class ServiceCompanyCreate(LoginRequiredMixin, CreateView):
    model = Bookcompanies
    form_class = ServiceCompanyForm
    # fields = ['model_company_name', 'model_company_desc']
    template_name = 'servicecompanycreate.html'
    success_url = '/memberzone/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

#создание модели узла отказа

class ClaimPartCreate(LoginRequiredMixin, CreateView):
    model = Bookclaimpart
    form_class = ClaimPartForm
    # fields = ['model_claimpart_name', 'model_claimpart_desc']
    template_name = 'claimpartcreate.html'
    success_url = '/memberzone/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# создание модели способа восстановления

class ClaimRecoverCreate(LoginRequiredMixin, CreateView):
    model = Bookclaimrecover
    form_class = ClaimRecoverForm
    # fields = ['model_claimrecover_name', 'model_claimrecover_desc']
    template_name = 'claimrecovercreate.html'
    success_url = '/memberzone/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


#создание ТО для личных пользователей и сервисных компаний

class TOCreatePersonal(LoginRequiredMixin, CreateView):
    model = Technicalmaintenance
    form_class = TOForm
    # fields = ['tm_car', 'tm_service_company', 'tm_type', 'tm_number_date', 'tm_date', 'tm_hours', 'tm_number']
    template_name = 'tocreatepersonal.html'
    success_url = '/memberzone/'

    def get_allowed_cars(self):
        u = self.request.user
        qs = Car.objects.all()
        if getattr(u, 'client_name', None):
            qs = qs.filter(client_name=u.client_name)
        elif getattr(u, 'service_organization', None):
            qs = qs.filter(service_company__model_company_name=u.service_organization)

        return qs


    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['tm_car'].queryset = self.get_allowed_cars()
        u = self.request.user
        if getattr(u, 'service_organization', None):
            form.fields['tm_service_company'].queryset = Bookcompanies.objects.filter(
                model_company_name=u.service_organization
            )
            form.initial['tm_service_company'] = form.fields['tm_service_company'].queryset.first()

        return form

    def form_valid(self, form):
        u = self.request.user
        car = form.cleaned_data['tm_car']


        if not self.get_allowed_cars().filter(pk=car.pk).exists():
            form.add_error('tm_car', 'Вы не можете создавать ТО для этой машины.')
            return self.form_invalid(form)

        if getattr(u, 'service_organization', None):
            company = Bookcompanies.objects.filter(model_company_name=u.service_organization).first()
            if not company:
                form.add_error('tm_service_company', 'Сервисная компания пользователя не найдена.')
                return self.form_invalid(form)
            form.instance.tm_service_company = company

        form.instance.user = u
        return super().form_valid(form)

#модель добавления рекламаций для своих авто

class ClaimCreatePersonal(LoginRequiredMixin, CreateView):
    model = Claimservice
    form_class = ClaimPersonalForm
    template_name = 'claimcreatepersonal.html'
    success_url = '/memberzone/'

    def get_allowed_cars(self):
        u = self.request.user
        qs = Car.objects.all()
        if getattr(u, 'client_name', None):
            qs = qs.filter(client_name=u.client_name)
        elif getattr(u, 'service_organization', None):
            qs = qs.filter(service_company__model_company_name=u.service_organization)

        return qs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['claim_car'].queryset = self.get_allowed_cars()
        u = self.request.user
        if getattr(u, 'service_organization', None):
            comp_qs = Bookcompanies.objects.filter(model_company_name=u.service_organization)
            form.fields['claim_service_company'].queryset = comp_qs
            form.initial['claim_service_company'] = comp_qs.first()
        return form
    def form_valid(self, form):
        u = self.request.user
        car = form.cleaned_data['claim_car']

        if not self.get_allowed_cars().filter(pk=car.pk).exists():
            form.add_error('claim_car', 'Вы не можете создавать рекламацию для этой машины.')
            return self.form_invalid(form)
        if getattr(u, 'service_organization', None):
            company = Bookcompanies.objects.filter(model_company_name=u.service_organization).first()
            if not company:
                form.add_error('claim_service_company', 'Сервисная компания пользователя не найдена.')
                return self.form_invalid(form)
            form.instance.claim_service_company = company

        form.instance.user = u
        return super().form_valid(form)

def apidescription(request):
    return render(request, 'api.html')




