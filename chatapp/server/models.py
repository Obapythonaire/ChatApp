from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .validators import validate_icon_image_size, validate_banner_image_size, validate_image_file_extension


# Upload path functions - organize uploaded files by model type and instance ID
def server_icon_upload_path(instance, filename):
    """Generate upload path for server icons"""
    return f'server/{instance.id}/server_icon/{filename}'


def server_banner_upload_path(instance, filename):
    """Generate upload path for server banners"""
    return f'server/{instance.id}/server_banner/{filename}'


def category_icon_upload_path(instance, filename):
    """Generate upload path for category icons"""
    return f'category/{instance.id}/category_icon/{filename}'


class Category(models.Model):
    """Represents a category for organizing servers"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.FileField(upload_to=category_icon_upload_path, null=True, blank=True)
    

    def save(self, *args, **kwargs):
        """Override save to delete old icon file when updated"""
        if self.id:
            existing = get_object_or_404(Category, id=self.id)
            # Delete old icon if it's being replaced
            if existing.icon != self.icon:
                existing.icon.delete()
        
        super(Category, self).save(*args, **kwargs)
    
    @receiver(models.signals.pre_delete, sender='server.Category')
    def category_delete_files(sender, instance, **kwargs):
        """Signal handler to delete associated files when category is deleted"""
        for field in instance._meta.fields:
            if field.name == 'icon':
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)

    def __str__(self):
        return self.name
    

class Server(models.Model):
    """Represents a chat server with members and channels"""
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='server_owner')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='server_category')
    description = models.CharField(max_length=250, blank=True, null=True)
    member = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return f'{self.name}--{self.id}'
    

class Channel(models.Model):
    """Represents a communication channel within a server"""
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='channel_owner')
    topic = models.CharField(max_length=200)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='channel_server')
    
    # Image fields with size and format validation
    banner = models.ImageField(
        upload_to=server_banner_upload_path, 
        null=True, 
        blank=True, 
        validators=[validate_banner_image_size, validate_image_file_extension],
    )
    icon = models.ImageField(
        upload_to=server_icon_upload_path, 
        null=True, 
        blank=True, 
        validators=[validate_icon_image_size, validate_image_file_extension],
    )

 
    def save(self, *args, **kwargs):
        """Override save to delete old image files when updated"""
        if self.id:
            existing = get_object_or_404(Channel, id=self.id)
            # Delete old icon if it's being replaced
            if existing.icon != self.icon:
                existing.icon.delete()
            # Delete old banner if it's being replaced
            if existing.banner != self.banner:
                existing.banner.delete()
        super(Channel, self).save(*args, **kwargs)
    
    @receiver(models.signals.pre_delete, sender='server.Channel')
    def channel_delete_files(sender, instance, **kwargs):
        """Signal handler to delete associated files when channel is deleted"""
        for field in instance._meta.fields:
            if field.name == 'icon' or field.name == 'banner':
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)
    
    def __str__(self):
        return self.name