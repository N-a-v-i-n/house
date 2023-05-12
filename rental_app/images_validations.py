from PIL import Image , ImageDraw,ImageFont
import os,sys
import random,datetime,base64
from django.utils import timezone
from django.shortcuts import HttpResponse



allowed_formats=['JPG','PNG','JPEG','WEBP']


def images_validate(img,id):




    user_side_img=Image.open(img)

    image_properties={
         "image_format":False,
         "image_size":False,

    }
    if user_side_img.format.upper() in allowed_formats:
        print()
        print()
        print()
        print("Image Satisfied the Format")
        image_properties['image_format']=True


    # for python anywere
    #  default_img=Image.open('/home/naveen6213/new_rental_update/rental_app/Black_bg_img.jpg')



        default_img=Image.open('rental_app/Black_bg_img.jpg')
        file_name,exe=os.path.splitext(str(img))
        file_name1=timezone.now().timestamp()
        print(file_name,exe)
        user_img_width,user_img_height=user_side_img.size
        print("Img width is : ",user_img_width,"Img Height is : ",user_img_height)

        # New change After FE image Otimizations


        # for python anywhere
        # title_font=ImageFont.truetype('/home/naveen6213/new_rental_update/rental_app/vermin_vibes_roundhouse.ttf',size=150)

        title_font=ImageFont.truetype('rental_app/vermin_vibes_roundhouse.ttf',size=150)
        title_text='RYS'
        image_to_edit=ImageDraw.Draw(user_side_img)
        image_to_edit.text((user_side_img.width-500,user_side_img.height-200),title_text,(237, 230, 211),title_font)
        # user_side_img.show()

        try:
            os.makedirs(f"media/{id}")
            # user_side_img.save(f"media/{id}/{file_name}.jpeg",)

        except:
            pass
        user_side_img.save(f"media/{id}/{file_name}_{file_name1}.jpeg",)


        
        file_img= f"media/{id}/{file_name}_{file_name1}.jpeg"   

        # print("image : ",file_img)

        with open(file_img,'rb') as f:
            encode_image=(base64.b64encode(f.read())).decode("utf-8")

        # below code is to check for is_image safe to show or not
        
        
        import requests

        url = "https://nsfw-image-detector-or-classifier.p.rapidapi.com/api-v1.0/SafeUnsafeImageWithTags"

        payload = {
            "api_key": "test_image_rapid",
            "base64_image": str(encode_image)
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "2d5f9283c7msh593b74279861127p1f86acjsn0b196b9397ba",
            "X-RapidAPI-Host": "nsfw-image-detector-or-classifier.p.rapidapi.com"
        }

        response = requests.post(url, json=payload, headers=headers)
        result_response=response.json()
        # print("response : ",result_response)




        
        image_properties['image_size']=True
            # image_properties['image_size']=True

    else:
        print("Image fucked-up")
        return HttpResponse("Unsupported Image")

    print('image_properties',image_properties)




    if all(image_properties):
        return (f"{id}/{file_name}_{file_name1}.jpeg",result_response)






# Check for the images sizes and modifiy it 

    # if user_img_width>2000:
    #     resizing=user_side_img.resize((user_img_width,user_img_height),Image.ANTIALIAS)
    #     try:
    #         os.makedirs(f"media/{id}")

    #     except:
    #         pass

    #     quality=10

    #     final_touch=final_img_logo_adding(resizing,file_name,id,quality)


    # elif user_img_width>1000 and user_img_width<=2000:
    #     resizing=user_side_img.resize((user_img_width,user_img_height),Image.ANTIALIAS)
    #     try:
    #         os.makedirs(f"media/{id}")

    #     except:
    #         pass

    #     quality=20

    #     final_touch=final_img_logo_adding(resizing,file_name,id,quality)



    # elif user_img_width>700 and user_img_width<=1000:
    #     resizing=user_side_img.resize((user_img_width,user_img_height),Image.ANTIALIAS)
    #     try:
    #         os.makedirs(f"media/{id}")

    #     except:
    #         pass

    #     quality=30
    #     final_touch=final_img_logo_adding(resizing,file_name,id,quality)

    # elif user_img_width>=300 and user_img_width<=700:
    #     resizing=user_side_img.resize((user_img_width,user_img_height),Image.ANTIALIAS)
    #     try:
    #         os.makedirs(f"media/{id}")

    #     except:
    #         pass
    #     quality=60
    #     final_touch=final_img_logo_adding(resizing,file_name,id,quality)


    # elif user_side_img.width < 800:

    #     Image.Image.paste(default_img,user_side_img,(int(default_img.width/2)-int(user_side_img.width/2),int(default_img.height/2)-int(user_side_img.height/2)))

    #     try:
    #         os.makedirs(f"media/{id}")
    #         # default_img.save(f"B:/project_unknown/house/media/{id}/{file_name}.png",)
    #         # image_properties['image_size']=True

    #     except:
    #         # default_img.save(f"B:/project_unknown/house/media/{id}/{file_name}.png",)
    #         # image_properties['image_size']=True
    #         pass
    #         # default_img=Image.open('/home/naveen6213/home/house/rental_app/Black_bg_img.jpg')
    #         # title_font=ImageFont.truetype('/home/naveen6213/home/house/rental_app/vermin_vibes_roundhouse.ttf',size=150)

    #     title_font=ImageFont.truetype('rental_app/vermin_vibes_roundhouse.ttf',size=150)
    #     title_text='SCN'

    #     image_to_edit=ImageDraw.Draw(default_img)
    #     image_to_edit.text((default_img.width-500,default_img.height-200),title_text,(237, 230, 211),title_font)
    #     # user_side_img.show()

    #     default_img.save(f"media/{id}/{file_name}.jpg",)
    #     image_properties['image_size']=True


    # else:
    #     try:
    #         os.makedirs(f"media/{id}")

    #     except:
    #         pass

        # title_font=ImageFont.truetype('rental_app/vermin_vibes_roundhouse.ttf',size=150)
        # title_text='SCN'
        # image_to_edit=ImageDraw.Draw(user_side_img)
        # image_to_edit.text((user_side_img.width-500,user_side_img.height-200),title_text,(237, 230, 211),title_font)
        # # user_side_img.show()

        # user_side_img.save(f"media/{id}/{file_name}.jpg",)
        # image_properties['image_size']=True
        #     # image_properties['image_size']=True

                



    # if all(image_properties):
    #     return (f"{id}/{file_name}.jpg")


#-----------------------------------------------------------#
#Repeated Logics fun

# def final_img_logo_adding(resizing,file_name,id,quality):
#     try:
#         title_font=ImageFont.truetype('rental_app/vermin_vibes_roundhouse.ttf',size=300)
#         title_text='SCN'
#         image_to_edit=ImageDraw.Draw(resizing)
#         image_to_edit.text((resizing.width-1000,resizing.height-500),title_text,(237, 230, 211),title_font)
#         # user_side_img.show()

#         resizing.save(f"media/{id}/{file_name}.jpg",quality=quality,optimize=True)
#         images_validate.image_properties['image_size']=True
#         return (True, 'ALLSuccess')
#     except Exception as error :
#         print("Error Occur : ",error)
#         return (False,'Not Success')












