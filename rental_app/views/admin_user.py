from .common_imports import *
from django.views.decorators.csrf import csrf_exempt


def admin_user(request):

    Is_logout=False

    cookies_token=request.COOKIES.get('otp_token')  #checking for the cookies if the user is already logged in or not


    if cookies_token:

        print("browser_token : ",cookies_token)

        validate=token_validations(cookies_token)

        print("is token_match : ",validate)



        if validate and str(validate[3])=='admin':

            is_user_logged_in=True
            
            user_added=False
            user_existance=False
            Previous_posted_info=False

            print('Yes, User Logged_in')
            get_user_id=users.objects.get(email_id=validate[1])
            print(get_user_id.id)
            try:
                login_entry=super_Admin_users.objects.get(user_id=get_user_id.id)
                print("login_entry : ",login_entry)
                login_entry.last_login_time=timezone.now()
                login_entry.user_ip_address=validate[2] 
                login_entry.save()

                print("Login-entry Updated")

            except:
                new_entry=super_Admin_users.objects.create(
                    user_id=get_user_id,
                    role=validate[3],
                    created_At=timezone.now(),
                    last_login_time=timezone.now(),
                    user_ip_address=validate[2]
                )
                new_entry.save()
                print("new_entry Updated")

            # user addind

            user_fn=request.POST.get("admin_firstname")
            user_mobile=request.POST.get("admin_mobile_no")
            user_email=request.POST.get("admin_email_id")

            print("user_name : ",user_fn)
            if user_fn:
                try:
                    from django.db.models import Q

                    check_user_existance=users.objects.get(Q(email_id=user_email) | Q(mobile_no=user_mobile))
                    print(check_user_existance)
                    user_added=True
                    user_existance=True
                    user_fn=check_user_existance.first_name
                    user_mobile=check_user_existance.mobile_no
                    user_email=check_user_existance.email_id

                    # IF any Temp images added will be deleted

                        
                    
                    import shutil  
                    # check for any unused user images in the db i.e 'temp' name images:
                    unused_images=(images.objects.filter(user_email_id=user_email)).filter(property_name='temp').values('image')
                    print("unused_images : ",unused_images)
                    # delete the folder from media dir using shell-utilities 'shutil'
                    if unused_images:
                        try:
                            folder_id=(unused_images[0]['image']).split('/')
                            shutil.rmtree(f"media/{folder_id[0]}/user_posts/{folder_id[2]}")
                            
                        except:
                            pass

                        # also delete from db

                        (images.objects.filter(user_email_id=user_email)).filter(property_name='temp').delete()



                    print("unused images are deleted : ",unused_images)




                    try:

                        Previous_posted_info=(property_details.objects.filter(user_emailid_via_login_token=user_email).values(
                            'id',
                            'property_name',
                            'property_type',
                            'property_city',
                            'property_state',
                            'property_pincode',
                            'property_distict',
                            'property_floor',
                            'monthly_rent',
                            'house_area',
                            'furnished_or_semi',
                            'rooms',
                            'appliance_TV',                                    
                            'appliance_Fridge',
                            'appliance_sofa',
                            'appliance_bed',
                            'appliance_dresser',
                            'appliance_AC',
                            'appliance_washing_machine',
                            'appliance_water_heaters',
                            'appliance_fans',
                            'appliance_water_purifier',
                            'appliance_tubelights',
                            'appliance_Inventers',
                            'parking'
                        )).last()          

                        # print("Previous_posted_info",Previous_posted_info)

                    except Exception as temp:
                        print("error : ",temp)
                        pass



                except Exception as e:
                    print(e)
                    new_user_creation=users.objects.create(
                        first_name=user_fn,
                        email_id=user_email,
                        mobile_no=user_mobile,
                        user_password=user_mobile,
                        created_at=timezone.now(),
                        user_added_by_admin=validate[1]

                    )
                    new_user_creation.save()
                    user_added=True

            # ==================================================================

            try:
                property_name=request.POST.get('property_name').lower()
                new_user_email=request.POST.get("new_user_email").lower()
            
                print(property_name)
                print()
                print()
                property_type=request.POST.get('property_type').lower()
                property_city=request.POST.get('property_city').lower()
                property_state=request.POST.get('property_state').lower()
                # property_located_in_city=request.POST.get('property_located_in_city')
                property_pincode=request.POST.get('property_pincode').lower()
                property_distict=request.POST.get('property_distict').lower()
                property_floor=request.POST.get('property_floor').lower()
                property_rooms=request.POST.get('property_rooms')
                monthly_rent=request.POST.get('monthly_rent').lower()
                # monthly_maintance=request.POST.get('monthly_maintance')
                # required_doc=request.POST.get('required_doc')
                # advance_amount=request.POST.get('advance_amount')
                # contact_no=0
                house_area=request.POST.get('house_area').lower()
                furnished_or_semi=request.POST.get('furnished_or_semi')
                # tenure_period=request.POST.get('tenure_period')
                parking=request.POST.get('parking').lower()
                # variable_or_fixed=request.POST.get('variable_or_fixed')

                #newlyy added fileds are : -
                appliance_tv= True if request.POST.get('appliance_tv') else False
                appliance_fridge=True if request.POST.get('appliance_fridge') else False
                appliance_sofa= True if request.POST.get('appliance_sofa') else False
                appliance_bed=True if request.POST.get('appliance_bed') else False
                appliance_dresser=True if request.POST.get('appliance_dresser') else False
                appliance_ac=True if request.POST.get('appliance_ac') else False
                appliance_washing_machine=True if request.POST.get('appliance_washing_machine') else False
                appliance_water_heater=True if request.POST.get('appliance_water_heater') else False
                appliance_water_purifier=True if request.POST.get('appliance_water_purifier') else False
                appliance_fans=True if request.POST.get('appliance_fan') else False
                appliance_tubelights=True if request.POST.get('appliance_tubelights') else False
                appliance_Inventers=True if request.POST.get('appliance_Inventers') else False


                new_data=property_details(
                    user_emailid_via_login_token=new_user_email,
                    property_distict=property_distict,
                    property_name=property_name,
                    property_type=property_type,
                    property_city=property_city,
                    property_state=property_state,
                    property_pincode=property_pincode,
                    # property_located_in_city=property_located_in_city,
                    property_floor=property_floor,
                    rooms=property_rooms,
                    monthly_rent=monthly_rent,
                    # monthly_maintance=monthly_maintance,
                    # required_doc=required_doc,
                    # advance_amount=advance_amount,
                    # contact_no=contact_no,
                    house_area=house_area,
                    furnished_or_semi=furnished_or_semi,
                    # tenure_period=tenure_period,
                    parking=parking,
                    # variable_or_fixed=variable_or_fixed,

                    #newlyy added fields are :- 
                    appliance_TV=appliance_tv,
                    appliance_Fridge=appliance_fridge,
                    appliance_sofa=appliance_sofa,
                    appliance_bed=appliance_bed,
                    appliance_dresser=appliance_dresser,
                    appliance_AC=appliance_ac,
                    appliance_washing_machine=appliance_washing_machine,
                    appliance_water_heaters=appliance_water_heater,
                    appliance_fans=appliance_fans,
                    appliance_water_purifier=appliance_water_purifier,
                    appliance_tubelights=appliance_tubelights,
                    appliance_Inventers=appliance_Inventers,
                    created_at=timezone.now(),
                    post_expire_date=timezone.now() + datetime.timedelta(days=30),
                    ad_posted_by=validate[1]
                    
                )
                new_data.save()

                added_user_details=users.objects.get(email_id=new_user_email)
                # Updating user posted logs table 
                update_user_ad_posted_logs=ad_posted_logs.objects.create(
                    user_details=added_user_details,
                    user_posted_ad_property_id=new_data.id,
                    user_posted_date=timezone.now()

                )
                update_user_ad_posted_logs.save()

                # update added post image id

                migrate_images_table=(images.objects.filter(user_email_id=new_user_email)).filter(property_name='temp').update(
                    property_name=new_data.id
                )

                

                #updating user posted ad counts through finding user via email filter
                
                added_user_details.no_of_free_ad_posted_count+=1
                added_user_details.save()

            except Exception as err:
                print("error : ",err)
                pass



            # ==================================================================


                
            data={
                    'user_added':user_added,
                    'user_existance':user_existance,
                    'user_firstname':user_fn,
                    'user_mobile_no':user_mobile,
                    'user_email_id':user_email,
                    'Previous_posted_info':Previous_posted_info,
                    }

            print("data : ",data)
            response = render(request,'admin_user.html',data)
            return response
        
        return HttpResponseRedirect('/')
    
    return HttpResponseRedirect('/')


@csrf_exempt
def admin_user_upload(request):
   
    user_login_token=request.COOKIES.get('otp_token')
    user_email_id=request.POST.get('user_email')
    current_user=users.objects.get(email_id=user_email_id)

    print("current_user : ",current_user,"email : ",user_email_id) 
    if current_user:
        
        property_images_temp=request.FILES.getlist('temp')
        print("property_images_temp : ",property_images_temp)



        users_previous_product_id=[x[0] for x in property_details.objects.filter(user_emailid_via_login_token=user_email_id).values_list('id')]
        users_previous_product_id.sort(reverse=True)

        print("users_previous_product_id : ",users_previous_product_id)


        try:
            id=f"{current_user.id}/user_posts/{current_user.id}.pre_{(users_previous_product_id[:1])[0]}"

        except:
            id=f"{current_user.id}/user_posts/{current_user.id}.pre_{0}"

        validate=validate_img(property_images_temp[0],id)
        print("output from validate",validate)

        if validate:
            new_images=images.objects.create(image=validate,user_email_id=user_email_id)
            new_images.save()
            result_response=validate[1]

            safe=1
            print("safe : ",bool(safe))
            if bool(safe):
                update_image=images.objects.get(id=new_images.id)
                update_image.Is_image_safe=True
                update_image.save() 

        

    return render(request,'images.html')

allowed_formats=['JPG','PNG','JPEG','WEBP']

from PIL import Image , ImageDraw,ImageFont
import os,sys


def validate_img(img,id):

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

        image_properties['image_size']=True
            # image_properties['image_size']=True

    else:
        print("Image fucked-up")
        return HttpResponse("Unsupported Image")

    print('image_properties',image_properties)

    if all(image_properties):
        return (f"{id}/{file_name}_{file_name1}.jpeg")

