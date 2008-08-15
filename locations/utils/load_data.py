import pycountry

from locations.models import Country, SubCountry

def create_subdivision(subdivision, country):
    """
    Recursively create Django SubDivision objects
    
    Note:
    subdivision is a pycountry object
    country is a Django object
    """
    t = SubDivisionType.objects.get_or_create(name=subdivision.type)
    if subdivision.parent_code:
        parent = subdivision.parent
        p = create_subdivision(parent)
    else:
        p = None
    sd, created = SubDivision.objects.get_or_create(code=subdivision.code,
                                                    country=country,
                                                    name=subdivision.name,
                                                    sub_division_type=t,
                                                    parent=p)
    return sd
    

for country in pycountry.countries.objects:
    c, created = Country.objects.get_or_create(alpha2=country.alpha2,
                                               alpha2=country.alpha3,
                                               name=country.name,
                                               numeric=country.numeric,
                                               official_name=country.official_name,
                                               published=True)

    for subdivision in pycountry.subdivisions.get(country_code=c.alpha2):
        create_subdivision(subdivision)
        