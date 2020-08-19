from django.db import models
from country_list import countries_for_language


# Create your models here.
# class Country(models.Model):
#     name = models.CharField(max_length=30)
#     open_countries = models.ManyToManyField("self", null=True)
#     open_with_retrictions_countries = models.ManyToManyField("self", null=True)
#     closed = models.ManyToManyField("self", null=True)
#
#     def __str__(self):
#         return self.name


class Relationship(models.Model):
    COUNTRY_DICTIONARY = dict(countries_for_language('en'))
    COUNTRY_DICTIONARY['*'] = 'all'
    COUNTRIES = [('*', 'all')]  # to signal the same status for all the countries
    for key in list(COUNTRY_DICTIONARY.keys()):
        COUNTRIES += [(key, COUNTRY_DICTIONARY[key])]
    COUNTRIES = tuple(COUNTRIES)
    OPENNESS = (
        ('1', 'open'),
        ('2', 'open with restrictions'),
        ('3', 'closed'),
        ('4', 'unknown'),
    )
    departure_country = models.CharField(max_length=30, choices=COUNTRIES)
    arrival_country = models.CharField(max_length=30, choices=COUNTRIES)
    status = models.CharField(max_length=1, choices=OPENNESS, default='4')
    info = models.CharField(max_length=160, default="")

    def __str__(self):
        return f"from {self.COUNTRY_DICTIONARY[self.departure_country]} to {self.COUNTRY_DICTIONARY[self.arrival_country]}"
