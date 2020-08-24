import logging

from country_list import countries_for_language
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response

from .models import Relationship
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound

# Create your views here.
from .serializers import RelationshipSerializer


def getRelationships(request, departure_country):
    """
    sends back the relationships that are registered in the the db and there status
    :param request:
    :param departure_country:
    :return: json response
    """
    if request.method == "GET":
        COUNTRY_DICTIONARY = dict(countries_for_language('en'))
        country_iso = list(COUNTRY_DICTIONARY.keys())[list(COUNTRY_DICTIONARY.values()).index(departure_country)]
        query = Relationship.objects.filter(departure_country__startswith=country_iso)

        return HttpResponse(serializers.serialize("json", query), content_type='application/json')

    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')


def getRelations(request, departure_country):
    """
    same as the getRelationships() but gives less info and harder to scale and maintain
    :param request:
    :param departure_country:
    :return:
    """
    COUNTRY_DICTIONARY = dict(countries_for_language('en'))
    country_iso = list(COUNTRY_DICTIONARY.keys())[list(COUNTRY_DICTIONARY.values()).index(departure_country)]
    query = Relationship.objects.filter(departure_country__startswith=country_iso)
    # preparing response
    resp = {}
    for i in range(1, 5):
        resp[i] = {}

    for item in query:
        resp[int(item.status)][item.arrival_country] = item.arrival_country

    return JsonResponse(resp)


class RestView(viewsets.ModelViewSet, mixins.DestroyModelMixin):
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        departure_country = self.request.query_params.get('departure_country', None)
        if departure_country is not None:
            self.queryset = self.queryset.filter(departure_country=departure_country)
        return self.queryset

    def destroy(self, request, *args, **kwargs):
        departure_country = request.query_params.get('departure_country', None)
        arrival_country = request.query_params.get('arrival_country', None)
        instance = Relationship.objects.get(departure_country=departure_country, arrival_country=arrival_country)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def test(request):
    res = "IT WORKS 🎉" if request.user.is_authenticated else "New phone who dis?"
    return HttpResponse(res)
