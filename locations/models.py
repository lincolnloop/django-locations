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
    official_name = models.CharField(max_length=128)
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
        return unicode(self.display_name)

class SubDivisionType(models.Model):
    """SubDivision Types (State, Province, etc.)"""
    name = models.CharField(max_length=100)

    class Admin:
        pass

    def __unicode__(self):
        return self.name


class SubDivision(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=55)
    country = models.ForeignKey(Country)
    sub_division_type = models.ForeignKey(SubDivisionType)
    parent = models.ForeignKey("SubDivision", blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Admin:
        pass

    class Meta:
        verbose_name = "State/Province"
        

class Location(models.Model):
    slug = models.SlugField(prepopulate_from=("city",))
    city = models.CharField(max_length=50)
    sub_division = models.ForeignKey(SubDivision, name="State/Province")
    country = models.ForeignKey(Country)

    def __unicode__(self):
        return "%s, %s %s" % (self.city, self.state_province,
                              str(self.country))

    class Meta:
        unique_together = ("city", "sub_division", "country")
        
    class Admin:
        pass
        
    def save(self):
        unique_slugify(self, "%s %s" % (self.city))
        super(Location, self).save()