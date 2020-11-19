from django.db import models

# Create your models here.
class Card(models.Model):
    id = models.AutoField(primary_key=True)
    #Public card id
    card_id = models.TextField(null=True, blank=True)
    #Card image url
    card_url = models.TextField(null=True, blank=True)
    #Raw data
    raw_data = models.TextField(null=True, blank=True)
    #response
    card_response = models.TextField(null=True, blank=True)
    #deanger level in food
    dangerousness =  models.IntegerField(null=True, blank=True)
    # The cards is visible or not
    display = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.card_id)
