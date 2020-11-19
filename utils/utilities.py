#Standard libraries
import os
import math
#aws
import boto3
#Google cloud
from google.cloud import vision
#models
from apps.home.models import Card

class Utils:

    def upload_to_aws(self, img):
        """Storage an image to a S3 bucket"""
        self.img = img
        AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
        AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
        s3 = boto3.client('s3',
                          aws_access_key_id=AWS_ACCESS_KEY,
                          aws_secret_access_key=AWS_SECRET_KEY
                          )
        S3_BUCKET = os.environ.get('S3_BUCKET')
        s3.upload_fileobj(img,
                          S3_BUCKET,
                          'images/'+img.name,
                          ExtraArgs={
                                      "ContentType": "image/jpeg",
                                      'ACL':'public-read'
                                     }
                        )

    def to_google_vision(self, img_url):
        """"Return the raw tex from an image """
        self.img_url = img_url
        client = vision.ImageAnnotatorClient()
        response = client.annotate_image({
            'image': {
                'source': {
                    'image_uri':self.img_url}},
            'features': [{
                'type': vision.enums.Feature.Type.TEXT_DETECTION}],
        })
        texts=response.text_annotations
        response=[]
        # #text_resp
        response.append(texts[0].description)
        #language
        response.append(texts[0].locale)
        return response

    def transform_text(self, response):
        """Apply some transformation to response"""
        self.response = response
        raw_data=response
        #Make all text lower
        lower_txt=raw_data.lower()
        position=lower_txt.find("ingredient")
        ing_str=lower_txt[position:]
        position=lower_txt.find("s: ")
        strings_to_replace = [".",
                              "(",
                              ")",
                              ":",
                              " y ",
                              " como ",
                              " de c",
                              " and ",
                              ",,",
                              "\n",
                              "\'",
                              "\""
        ]
        #Replace strings_to_replace to with a ","
        for string in strings_to_replace:
            ing_str = ing_str.replace(string, ",")
        #Split string
        ing_vctr = ing_str.split(',')
        ing_vctr.pop(0)
        #delete all ingredients with len<4
        n=0
        while n==0:
            n=1
            for i,ingredient in enumerate(ing_vctr):
                if(len(ingredient)<4):
                    n=0
                    ing_vctr.pop(i)
        #Delete if it is necessary a space at the beggining of sting
        for i,ingredient in enumerate(ing_vctr):
            if ingredient[0]==" ":
                ing_vctr[i]=ing_vctr[i].replace(" ","",1)
        return ing_vctr

    #Return how many pages and which images will be displayed
    def pagination(self, page, elements_to_display):
        self.page = page
        self.elements_to_display = elements_to_display
        #Call all element from DB
        elements = Card.objects.all()
        total_elements = elements.count()
        #Calculus num of pages
        num_pages = math.ceil(total_elements/self.elements_to_display)
        pages = []
        for i in range(0,num_pages):
            pages.append(i+1)
        if self.elements_to_display*self.page >= total_elements:
            if total_elements > self.elements_to_display:
                start =self.elements_to_display*(num_pages-1)
            else:
                start = 0
            end = total_elements
        else:
            start=self.page*self.elements_to_display-self.elements_to_display
            end = self.page*self.elements_to_display
        #Call all element from DB
        elements = Card.objects.all()
        #Sort all database by image_id
        elements = elements.order_by('-id')
        #Split element to display
        elements = elements[start:end]
        return pages, elements
