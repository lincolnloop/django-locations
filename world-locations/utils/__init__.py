#http://www.djangosnippets.org/snippets/690/
import re

from django.template.defaultfilters import slugify

RE_SLUG_STRIP = re.compile(r'^-+|-+$')

def unique_slugify(instance, value, slug_field_name='slug', queryset=None):
    """
    Calculates a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug. Chop its length down if we need to.
    slug = slugify(value)
    if not queryset:
        queryset = instance.__class__._default_manager.all()
        if instance.pk:
            queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '-%s' % next
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len-len(end)]
            slug = RE_SLUG_STRIP.sub('', slug)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)
    
def reverse_lookup(point):  
    """
    Lookup point at geonames
    """
    import httplib2
    from django.utils import simplejson
    from world_locations.models import Location, Country, Subdivision
    
    get_string = "lng=%s&lat=%s" % point
    h = httplib2.Http()
    
    #Place Name Lookup
    url = "http://ws.geonames.org/findNearbyPlaceNameJSON?%s" % get_string
    resp, content = h.request(url)
    print url,content
    data = simplejson.loads(content)
    location_dict = {}
    if data.has_key('geonames') and data['geonames']:
        data = data['geonames'][0]
        location_dict['country'] = Country.objects.get(alpha2=data['countryCode'])
        if data['adminName1']:
            location_dict['subdivision'], created = Subdivision.objects.get_or_create(
                                                            country=location_dict['country'], 
                                                            name=data['adminName1'])
        if data['name']:
            location_dict['city'] = data['name']
            
    #Subdivision lookup
    else:
        url = "http://ws.geonames.org/countrySubdivisionJSON?%s" % get_string
        resp, content = h.request(url)
        data = simplejson.loads(content)
        
        #couldn't perform reverse lookup
        if not data.has_key('countryCode'):
            return None
        
        location_dict['country'] = Country.objects.get(alpha2=data['countryCode'])
        if data['adminName1']:
            location_dict['subdivision'], created = Subdivision.objects.get_or_create(
                                                            country=location_dict['country'], 
                                                            name=data['adminName1'])
        
    location, created = Location.objects.get_or_create(**location_dict)
    return location