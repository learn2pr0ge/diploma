from django.contrib import admin
from django.urls import path, include
from .views import (CarView,  get_token, CarList, TOList, ClaimsList, carlist, FilterView, enginelist, FilterTOView, FilterClaimView, CarCreate,
                    TOCreate, ClaimCreate, EngineCreate, techlist, ModelCreate, clutchlist, ClutchCreate, axlelist,
                    AxleCreate, bridgelist, BridgeCreate, servicelist, ServiceCompanyCreate, tolist,
                    TOCreatePersonal, claimpart, ClaimPartCreate, claimrecover, ClaimRecoverCreate, ClaimCreatePersonal,
                    apidescription, CarListSort, TOListSort, ClaimListSort)
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularSwaggerView, SpectacularRedocView







urlpatterns = [
    path('cars/', CarView.as_view(), name='cars'),
    path('', get_token, name='memberzone'),
    path('cars/list/', CarList.as_view(), name='carlist'),
    path('cars/listsort/', CarListSort.as_view(), name='carlistsort'),
    path('cars/to/', TOList.as_view(), name='tolist'),
    path('cars/tosort/', TOListSort.as_view(), name='tolistsort'),
    path('cars/claims/', ClaimsList.as_view(), name='claimslist'),
    path('cars/claimssort/', ClaimListSort.as_view(), name='claimslistsort'),
    path('cars/filter/', FilterView.as_view(), name='filter'),
    path('listcars/<str:factory_number>/', carlist, name='carinfo'),
    path('listengines/<str:engine_number>/', enginelist, name='engineinfo'),
    path('listmodels/<str:model_technic>/', techlist, name='modeltechnic'),
    path('listclutch/<str:model_clutch>/', clutchlist, name='clutchtype'),
    path('listaxle/<str:model_axle>/', axlelist, name='axletype'),
    path('listbridge/<str:model_bridge>/', bridgelist, name='bridgetype'),
    path('listservice/<str:model_service>/', servicelist, name='servicetype'),
    path('tolist/<str:tm_type>/', tolist, name='tolist'),
    path('claimpart/<str:claim_part>/', claimpart, name='claimpart'),
    path('claimrecover/<str:claim_recover>/', claimrecover, name='claimrecover'),
    path('cars/filterto/', FilterTOView.as_view(), name='filterto'),
    path('cars/filterclaims/', FilterClaimView.as_view(), name='filterclaims'),
    path('cars/create/', CarCreate.as_view(), name='createcar'),
    path('cars/createto/', TOCreate.as_view(), name='createto'),
    path('cars/createclaim/', ClaimCreate.as_view(), name='createclaims'),
    path('cars/createengine/', EngineCreate.as_view(), name='createengine'),
    path('cars/createmodel/', ModelCreate.as_view(), name='createmodel'),
    path('cars/createclutch/', ClutchCreate.as_view(), name='createclutch'),
    path('cars/createaxle/', AxleCreate.as_view(), name='createaxle'),
    path('cars/createbridge/', BridgeCreate.as_view(), name='createbridge'),
    path('cars/createservice/', ServiceCompanyCreate.as_view() , name='createservice'),
    path('cars/createtopersonal/', TOCreatePersonal.as_view(), name='createtopersonal'),
    path('cars/createclaimpart/', ClaimPartCreate.as_view(), name='claimpartcreate'),
    path('cars/createclaimrecover/', ClaimRecoverCreate.as_view(), name='claimrecovercreate' ),
    path('cars/createclaimpersonal/', ClaimCreatePersonal.as_view(), name='claimcreatepersonal'),
    path('start/', apidescription, name='apidesc' ),
    path('docs/', SpectacularSwaggerView.as_view(url='/static/schema.yaml'), name='swagger-ui'),



]