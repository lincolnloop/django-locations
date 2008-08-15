import pycountry

from locations.models import Country, SubDivision, SubDivisionType

def create_subdivision(subdivision, country):
    """
    Recursively create Django SubDivision objects
    
    Note:
    subdivision is a pycountry object
    country is a Django object
    """
    t, created = SubDivisionType.objects.get_or_create(name=subdivision.type)
    sd, created = SubDivision.objects.get_or_create(code=subdivision.code,
                                                    country=country,
                                                    name=subdivision.name,
                                                    sub_division_type=t)
    if subdivision.parent_code:
        parent = subdivision.parent
        p = create_subdivision(parent, country)
        sd.parent = p
        sd.save()

    return sd
    

for country in pycountry.countries.objects:
    c, created = Country.objects.get_or_create(alpha2=country.alpha2,
                                               alpha3=country.alpha3,
                                               name=country.name,
                                               numeric=country.numeric,
                                               published=True)
    try:
        c.official_name=country.official_name
        c.save()
    except AttributeError:
        pass

    try:
        subdivisions = pycountry.subdivisions.get(country_code=c.alpha2)
    except KeyError:
        subdivisions = []
    for subdivision in subdivisions:
        create_subdivision(subdivision, c)
        
