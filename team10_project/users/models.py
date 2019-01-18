from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.admin import ModelAdmin
from django.utils.text import slugify # used to generate valid url based on a field of the model


User = get_user_model()
