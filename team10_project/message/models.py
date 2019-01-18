from django.db import models
from django.contrib.auth.models import User
from onlinestore.models import Item


class Messages(models.Model):

    sender = models.ForeignKey(User, related_name="sender")
    receiver = models.ForeignKey(User, related_name="receiver")
    msg = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, related_name="item", null=True)
    
    class Meta:
        verbose_name_plural = "Messages"

    
    def __str__(self):
        return str(self.id) + ": from " + str(self.sender) + " to " + str(self.receiver)

