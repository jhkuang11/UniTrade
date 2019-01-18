from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth import get_user_model
from sorl.thumbnail import ImageField
from django.utils.text import slugify # used to generate valid url based on a field of the model
from users.models import User
from onlinestore.formatChecker import ContentTypeRestrictedFileField


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Create slug based on category's name and save it for url."""
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("onlinestore:item_list", kwargs={"slug":self.slug})

    class Meta:
        # define category's plural form, otherwise Django will use "Categorys"
        verbose_name_plural = "Categories"


class Item(models.Model):
    title = models.CharField(max_length=100, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=12, blank=False)
    description = models.TextField(blank=True, default='')
    category = models.ForeignKey(Category, related_name="items", blank=False, null=True)
    create_time = models.DateTimeField(auto_now=True)
    image = ContentTypeRestrictedFileField(upload_to='uploads/', content_types=['image/jpg', 'image/jpeg', 'image/pdf', 'image/pneg', 'image/png', 'image/tiff'],max_upload_size=3145728,blank=True, null=True)
    seller = models.ForeignKey(User, null=True, blank=True)
    approved = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]


