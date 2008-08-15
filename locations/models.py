from django.db import models
from utils import unique_slugify

class CountryManager(models.Manager):
    """
    Manager for Active Countries.
    """
    def get_query_set(self):
        queryset = super(CountryManager, self).get_query_set()
        return queryset.filter(published=True)
        
class Country(models.Model):
    alpha2 = models.CharField('ISO alpha-2', max_length=2, unique=True)
    alpha3 = models.CharField('ISO alpha-3', max_length=3, unique=True)
    numeric = models.PositiveSmallIntegerField('ISO numeric', unique=True)
    name = models.CharField(max_length=128)
    official_name = models.CharField(max_length=128, blank=True)
    published = models.BooleanField(default=True, db_index=True)
    objects = models.Manager()
    active = CountryManager()

    class Meta:
        verbose_name_plural = 'Countries'
        ordering = ('name',)

    class Admin:
        fields = (
            ('Name', {'fields': ('name', 'official_name')}),
            ('ISO', {'fields': ('alpha2', 'alpha3', 'numeric')}),
            ('Published', {'fields': ('published',)}),
        )
        list_display = ('name', 'alpha2', 'alpha3', 'published')
        list_filter = ('published',)
        search_fields = ('name', 'alpha2', 'alpha3')
        ordering = ('name', )

    def __unicode__(self):
        return unicode(self.name)

class SubdivisionType(models.Model):
    """Subdivision Types (State, Province, etc.)"""
    name = models.CharField(max_length=100)

    class Admin:
        pass
    
    class Meta:
        ordering = ['name',]

    def __unicode__(self):
        return self.name


class Subdivision(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=55)
    country = models.ForeignKey(Country)
    subdivision_type = models.ForeignKey(SubdivisionType)
    parent = models.ForeignKey("Subdivision", blank=True, null=True)

    def __unicode__(self):
        return '%s %s' % (self.name, self.country.name)

    class Admin:
        list_display = ('name', 'subdivision_type', 'code', 'country',)
        list_filter = ('country',)

    class Meta:
        ordering = ['name',]
        

class Location(models.Model):
    slug = models.SlugField(prepopulate_from=("city",))
    city = models.CharField(max_length=50)
    subdivision = models.ForeignKey(Subdivision)

    def __unicode__(self):
        return "%s, %s" % (self.city, self.subdivision)

    class Meta:
        unique_together = ("city", "subdivision")
        
    class Admin:
        pass
        
    def save(self):
        unique_slugify(self, "%s %s" % (self.city))
        super(Location, self).save()
