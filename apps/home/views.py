#Standard libraries
import os
import hashlib
from datetime import datetime
import json
#Django
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
#models
from apps.home.models import Card
#Utilities
from utils.utilities import Utils
from utils.find_villians import find_villians

# WEB_URL='http://127.0.0.1:8000/'
WEB_URL = os.environ.get('WEB_URL')

# home/page/[PAGE]
def home(request,page):
    page = int(page)
    #Call utilities
    utils = Utils()
    #How many elements to display
    elements_to_display = 10
    #Return how many pages and which images will be displayed
    pages, cards = utils.pagination(page, elements_to_display)

    all_cards=[]
    for card in cards:
        all_cards.append(card)
    context = {
                'cards' : all_cards,
                'pages' : pages,
                'url' : WEB_URL,
               }
    #POST
    if request.method == 'POST':
        #Create a random string to rename the picture
        string = str(datetime.now())
        new_string = hashlib.sha256(string.encode()).hexdigest()
        #Get image
        card = request.FILES['image']
        #Change card name to a new string & extension
        complement, ext = card.name.rsplit('.', 1)
        card.name = new_string + '.' + ext
        #Upload to aws
        utils.upload_to_aws(card)
        #Create new card object
        new_card = Card.objects.create()
        #Set public card id
        new_card.card_id= new_string
        #Bucket where all images are stored
        BUCKET_URL = 'https://new-nutriapp.s3.us-east-2.amazonaws.com/images/'
        url = BUCKET_URL + new_string + '.' + ext
        # Set card url
        new_card.card_url = url
        #Call image for Google Vision
        image_to_text = utils.to_google_vision(url)
        # Set raw data
        new_card.raw_data = image_to_text
        #Process response
        procesed_response = utils.transform_text(image_to_text[0])
        villians = find_villians(procesed_response)
        # Set response from cloud vision computing
        new_card.card_response = '"' + str(villians) + '"'
        #Set dangerousness
        for i, toxicity in enumerate(villians):
            if toxicity:
                danger = i
                break
        new_card.dangerousness = danger
        # Save new card object
        new_card.save()
        return redirect('/')

    return render(request, 'base/index.html', context)

# /card/[CARD_NAME]
def card(request, id):
    #Get card
    try:
        card = Card.objects.get(card_id=id)
        villians = eval(json.loads(card.card_response))
        message = ''
        context = {
                   'card' : card,
                   'url' : WEB_URL,
                   'message' : message,
                   'peligrosos':villians[0],
                    'sospechosos':villians[1],
                    'no_nocivos':villians[2],
                    'desconocidos':villians[3],
                    'otros':villians[4],
                   }
    except:
        return  redirect('/')

    return render(request, 'base/card_page.html', context)
