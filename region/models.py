from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from jsonfield import JSONField

COMPONENT_TYPE_CHOICES = (
        ('1', 'Tmin'),
        ('2', 'Tmax'),
        ('3', 'Tmean'),
        ('4', 'Sunshine'),
        ('5', 'Rainfall'),
    )
# Create your models here.
class Region(MPTTModel):
    name  = models.CharField(max_length=1024)
    file_name = models.CharField(max_length=1024)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    def __unicode__(self):
        """Returns string representation of object"""
        return self.name

class StatisticalData(models.Model):
    year = models.IntegerField()
    region = models.ForeignKey(Region)
    component = models.CharField(max_length=1, choices=COMPONENT_TYPE_CHOICES)
    blob = JSONField()

    def __unicode__(self):
        """Returns string representation of object"""
        return self.region.name + " : " + str(self.year) + "("+self.component+")"

    class Meta:
        """Metadata for class Statistical Data"""
        verbose_name = 'Statistical Data'
        verbose_name_plural = 'Statistical Data'
