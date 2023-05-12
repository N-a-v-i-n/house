from .common_imports import *



def favour(request):

    cookie_email_id=request.COOKIES.get('email_id')
    cookies_token=request.COOKIES.get('otp_token')
    print(cookie_email_id)

    if cookies_token:


        print("browser_token : ",cookies_token)

        validate=token_validations(cookies_token)

        print("is token_match : ",validate)
    


        if validate:
            message_data=False


            #checking for any user receive message

            fetching_user_id_from_token=users_credentials_IPs.objects.get(user_token=cookies_token)

            current_user_details=fetching_user_id_from_token.user_id

            

            checking_for_message_update=send_text_to_owner.objects.filter(receiver_user_id=current_user_details.id).values('request_user_time','request_user_mobile_no','request_property_id')

            print("checking_for_message_update : ",checking_for_message_update)

            if checking_for_message_update:

                message_data_temp=[x for x in checking_for_message_update]
                message_data=[x for x in checking_for_message_update]
                print('message_data : ',message_data)

                list_of_product=list()


                for x in range(len(message_data)):
                    try :
                        list_of_product=[x for x in property_details.objects.filter(id=message_data_temp[x]['request_property_id']).values('property_name','property_city','monthly_rent')]
                        property_images=(images.objects.filter(property_name=message_data_temp[x]['request_property_id']).values('image')).distinct()
                        message_data[x].update(list_of_product[0])
                        message_data[x].update(property_images[0])
                    except Exception as temp:
                        continue

                    print('images',property_images)

                    # --------------------------------------------

            is_user_logged_in=True

            print('Yes, User Logged_in')

            fetched_liked_id=[x for x in user_liked.objects.filter(user_email=cookie_email_id).values('liked_property_ids').distinct()]
            print('fetched_liked_id',fetched_liked_id)
            all_in_one={}
            y=0
            for x in fetched_liked_id:
                all_in_one[y]=fetching_img_property_details(x['liked_property_ids'])
                y+=1
            # print(all_in_one[1])
            print(all_in_one)
            print()
            # print(all_in_one[2])
            needed_data_to_show_on_favour={}

            for x,y in all_in_one.items():
                # THis will return like :->   ['WhatsApp_Image_2023-03-04_at_18.07.44_1.jpeg', (6000, 'chittoor', 'andhar pradesh')]
                needed_data_to_show_on_favour[x]=[y[0][0],y[2][0],y[1][0]['id']]
            print('needed_data_to_show_on_favour : ',needed_data_to_show_on_favour)

            if needed_data_to_show_on_favour=={}:
                needed_data_to_show_on_favour = False
            data={
                'data': needed_data_to_show_on_favour,
                'user_status':is_user_logged_in,
                'message_data':message_data,

            }

            return render(request,'favour.html',data)
        

        else:
            response=render(request,'index.html')
            response.delete_cookie('otp_token')
            response.delete_cookie('email_id')
            return response


    else:
        return HttpResponseRedirect('/')
