# -*- coding: UTF-8 -*-
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from taggit.managers import TaggableManager
from model_utils.models import TimeStampedModel
from geoposition.fields import GeopositionField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from chineseaddress.models import Address

class AirCleanerManager(models.Manager):
    def by_user(self, user, **kwargs):
        """
        Filter objects by the 'user' field.
        """
        return self.select_related().filter(user=user)

class AirCleaner(models.Model):
    objects = AirCleanerManager()   
    id                      = models.AutoField(primary_key=True) 
    name               = models.CharField(_(u'空气净化器'),max_length=60, unique=True)   
    desc                 = models.CharField(_(u'描述'),max_length=500)    
    thumbnail       = models.ImageField(_(u'缩微图'),upload_to='device', null=True, blank=True)        
    owner             = models.ForeignKey(User, verbose_name = _(u'用户'))     
    
    date_created = models.DateField(_(u'创建日期'),null=True, blank=True)
    last_updated = models.DateTimeField(_(u'上次更新'),auto_now=True)
    notes              = models.TextField('Notes', null=False, blank=True, default='')
    tags                = TaggableManager(blank=True, help_text=None)    

    on_off             = models.BooleanField(_(u'开关机'),default=False)
    present           = models.BooleanField(_(u'存在否'),default=True)
    online             = models.BooleanField(_(u'在线'),default=True)       
    #associated     = models.ForeignKey(AirDetector, verbose_name = _(u'绑定的空气检测仪'))       
    address           = models.ForeignKey(Address, verbose_name = _(u'地址'))
    #coordinates   = GeopositionField()    
  
    def __unicode__(self):
        return self.name
   
    class Meta:
        verbose_name = _(u'空气净化器')
        verbose_name_plural = _(u'空气净化器')
        unique_together = ('name','desc')
        ordering = ['-date_created', '-last_updated']  
   
    def get_absolute_url(self):
        return reverse('air:air_detail', kwargs={'pk': self.id})
    
    def save(self, *args, **kwargs):
        super(AirCleaner, self).save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(unique=True, max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = _(u'类型') 
        ordering = ['id']

class Unit(models.Model):
    name = models.CharField(unique=True, max_length=6)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = _(u'单位') 
        ordering = ['id']

class AirDetectorManager(models.Manager):
    def by_user(self, user, **kwargs):
        """
        Filter objects by the 'user' field.
        """
        return self.select_related().filter(user=user)
    
class AirDetector(models.Model):
    objects             = AirDetectorManager()       
    id                      = models.AutoField(primary_key=True) 
    name               = models.CharField(_(u'空气检测仪'),max_length=60, unique=True)   
    desc                 = models.CharField(_(u'描述'),max_length=500)    
    thumbnail       = models.ImageField(_(u'缩微图'),upload_to='device', null=True, blank=True)        
    owner             = models.ForeignKey(User, verbose_name = _(u'用户'))       
    date_created = models.DateField(_(u'创建日期'),null=True, blank=True)
    last_updated = models.DateTimeField(_(u'上次更新'),auto_now=True)
    notes              = models.TextField('Notes', null=False, blank=True, default='')
    tags                = TaggableManager(blank=True, help_text=None)       
    address          = models.ForeignKey(Address, verbose_name = _(u'地址'))
    associated      = models.ForeignKey(AirCleaner, verbose_name = _(u'绑定的空气净化器'))   
    on_off              = models.BooleanField(_(u'开关机'),default=False)
    present           = models.BooleanField(_(u'存在否'),default=True)
    online             = models.BooleanField(_(u'在线'),default=True)       
    #coordinates   = GeopositionField()      

    def __unicode__(self):
        return self.name
   
    class Meta:
        verbose_name = _(u'空气检测仪')
        verbose_name_plural = _(u'空气检测仪')
        unique_together = ('name','desc')
        ordering = ['-date_created', '-last_updated']  
   
    def get_absolute_url(self):
        return reverse('air:air_detail', kwargs={'pk': self.id})
    
    def save(self, *args, **kwargs):
        super(AirDetector, self).save(*args, **kwargs)

class AirDetectorDataManager(models.Manager):

    def by_user(self, user, **kwargs):
        """
        Filter objects by the 'user' field.
        """
        return self.select_related().filter(user=user)

    def by_date(self, start_date, end_date, user, **kwargs):
        """
        Filter objects by date range.
        """
        resultset = self.by_user(user).filter(
            record_date__gte=start_date,
            record_date__lte=end_date,
        )

        return resultset.order_by('-record_date', '-record_time')

    def level_breakdown(self, start_date, end_date, user, **kwargs):
        """
        Filter objects by AirDetectorData level and count the records for each level.

        The range for the different levels are specified in the user's
        settings.
        """
        user_settings = user.settings
        low = user_settings.airdetectordata_low
        high = user_settings.airdetectordata_high
        target_min = user_settings.airdetectordata_target_min
        target_max = user_settings.airdetectordata_target_max

        data = self.by_date(start_date, end_date, user)
        all_count = data.count()
        low_count = data.filter(value__lte=low).count()
        high_count = data.filter(value__gte=high).count()
        target_count = data.filter(value__gte=target_min, value__lte=target_max).count()

        result = {
            'Low': low_count,
            'High': high_count,
            'Within Target': target_count,
            'Other': all_count - (low_count + high_count + target_count)
        }

        return result

    def by_category(self, start_date, end_date, user, **kwargs):
        """
        Group objects by category and take the count.
        """
        data = self.by_date(start_date, end_date, user)

        return data.values('category__name')\
            .annotate(count=models.Count('value'))\
            .order_by('category')

    def avg_by_category(self, start_date, end_date, user):
        """
        Group objects by category and take the average of the values.
        """
        data = self.by_date(start_date, end_date, user)

        return data.values('category__name')\
            .annotate(avg_value= models.Avg('value'))\
            .order_by('category')

    def avg_by_day(self, start_date, end_date, user):
        """
        Group objects by record date and take the average of the values.
        """
        data = self.by_date(start_date, end_date, user)

        return data.values('record_date')\
            .annotate(avg_value= models.Avg('value'))\
            .order_by('record_date')

class AirDetectorData(TimeStampedModel):
    objects = AirDetectorDataManager()
    
    user = models.ForeignKey(User)    
    id= models.AutoField(primary_key=True) 
    value = models.PositiveIntegerField(_(u'数值'),validators=[MaxValueValidator(58000),MinValueValidator(0)])
    record_date = models.DateField(_(u'日期'))
    record_time = models.TimeField(_(u'时间'))
    notes = models.TextField(null=False, blank=True, verbose_name = _(u'备注'))   
    airdetector = models.ForeignKey(AirDetector,null=True, blank=True)
    category  = models.ForeignKey(Category,verbose_name = _(u'类型'))
    tags = TaggableManager(blank=True, help_text=None)

    class Meta:
        verbose_name             = _(u'空气检测仪数据')
        verbose_name_plural = _(u'空气检测仪数据')
        ordering = ['id']
        
    def __unicode__(self):
        return str(self.value)

    def save(self, *args, **kwargs):
        super(AirDetectorData, self).save(*args, **kwargs)


class Marker(models.Model):
    id= models.AutoField(primary_key=True) 
    name = models.CharField(_(u'位置'),max_length=40)
    coordinates   = GeopositionField()    
    desc = models.TextField(_(u'描述'),max_length=1000)      
    #device = models.ForeignKey(Device, verbose_name="设备",null=True, blank=True)        
   
    class Meta:
        verbose_name = _(u'位置')
        verbose_name_plural = _(u'位置')
        ordering = ['id']

    def __unicode__(self):
        return u'%s %s %s' % (self.name, self.coordinates.latitude, self.coordinates.longitude)
    
    def get_lat_lon(self):
        lat_lon = [self.geometry.latitude, self.geometry.longitude]
        return lan_lon

