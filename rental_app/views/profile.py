from .common_imports import *
from django.views.decorators.csrf import csrf_exempt


def profile(request):
    cookies_token = request.COOKIES.get(
        "otp_token"
    )  # checking for the cookies if the user is already logged in or not
    if cookies_token:
        print("browser_token : ", cookies_token)
        validate = token_validations(cookies_token)
        print("is token_match : ", validate)

        if validate:
            message_data = False
            password_not_match = False

            # checking for any user receive message

            fetching_user_id_from_token = users_credentials_IPs.objects.get(
                user_token=cookies_token
            )

            current_user_details = fetching_user_id_from_token.user_id

            checking_for_message_update = send_text_to_owner.objects.filter(
                receiver_user_id=current_user_details.id
            ).values(
                "request_user_time", "request_user_mobile_no", "request_property_id"
            )

            print("checking_for_message_update : ", checking_for_message_update)

            if checking_for_message_update:
                message_data_temp = [x for x in checking_for_message_update]
                message_data = [x for x in checking_for_message_update]
                print("message_data : ", message_data)

                list_of_product = list()

                for x in range(len(message_data)):
                    try:
                        list_of_product = [
                            x
                            for x in property_details.objects.filter(
                                id=message_data_temp[x]["request_property_id"]
                            ).values("property_name", "property_city", "monthly_rent")
                        ]
                        property_images = (
                            images.objects.filter(
                                property_name=message_data_temp[x][
                                    "request_property_id"
                                ]
                            ).values("image")
                        ).distinct()
                        message_data[x].update(list_of_product[0])
                        message_data[x].update(property_images[0])
                    except Exception as temp:
                        continue

                    print("images", property_images)

            print("Yes, User Logged_in")
            cookie_token_data = request.COOKIES.get("otp_token")
            print()
            print()
            print()
            print("profile token : ", cookie_token_data)

            # Below code is to delete property_post from users_profile
            property_post_id = request.POST.get("delete_post")

            print("property_post_id: ", property_post_id)

            if property_post_id:
                property_info = property_details.objects.get(id=property_post_id)

                property_details.objects.filter(id=property_post_id).delete()

                posted_imgs = images.objects.filter(property_name=property_post_id)
                checkk = posted_imgs.values("image")
                fetch_folder_name = (checkk[0]["image"]).split("/")

                user_liked.objects.filter(liked_property_ids=property_post_id).delete()

                # update deleted post on db

                new_deleted_data = Deleted_post_details.objects.create(
                    post_id=property_post_id,
                    post_user_email=current_user_details.email_id,
                    posted_user_contact_details=current_user_details.mobile_no,
                    post_address=property_info.property_city,
                    deleted_at=timezone.now(),
                )
                new_deleted_data.save()

                # Also Delete Post Images From MediaFiles
                import shutil

                # check for any unused user images in the db i.e 'temp' name images:
                if fetch_folder_name:
                    try:
                        shutil.rmtree(
                            f"media/{fetch_folder_name[0]}/user_posts/{fetch_folder_name[2]}"
                        )

                    except:
                        pass

                posted_imgs.delete()
                print(f"property-ID {property_post_id} successfully deleted")

            current_password = request.POST.get("current_password")

            if current_password:
                new_password = request.POST.get("new_password")
                # Check for current_password is valid or not
                if str(current_password) == str(current_user_details.user_password):
                    current_user_details.user_password = new_password
                    current_user_details.save()
                else:
                    password_not_match = True

            # Below Code is to log-out user from profile page

            # logout=request.POST.get("logout")
            # if logout :
            #     get_token_from_browser=request.COOKIES.get('otp_token')
            #     confirm = delete_cookies(get_token_from_browser)
            #     response=render(request,'index.html')
            #     response.delete_cookie('otp_token')
            #     response.delete_cookie('email_id')

            #     print('cookies clear succeess !!')

            #     return response

            # Below code is to update user_profile details
            profile_update = request.POST.get("profile_updating")
            print("Profile Update : ", profile_update)
            user_email_fetched_based_on_user_token = [
                x
                for x in users_credentials_IPs.objects.filter(
                    user_token=cookie_token_data
                ).values_list("user_email_id")[0]
            ]

            if profile_update:
                # print('uSER EMAIL = ',user_email_fetched_based_on_user_token[0])
                first_name = request.POST.get("first_name")
                last_name = request.POST.get("last_name")
                # email_id=request.POST.get('email_id')
                mobile_no = request.POST.get("mobile_no")
                Bio = request.POST.get("Bio")
                profile_update = users.objects.filter(
                    email_id=user_email_fetched_based_on_user_token[0]
                ).update(
                    first_name=first_name,
                    last_name=last_name,
                    mobile_no=mobile_no,
                    Bio=Bio,
                )
                print(
                    f'USER DETAILS UPDATED FOR "{user_email_fetched_based_on_user_token[0]}"'
                )

            # Below code is to update user profile pic

            profile_pic_change = request.FILES.get("profile_pic")
            if profile_pic_change:
                print("profile_pic_change : ", profile_pic_change)
                allowed_formats = ["JPG", "PNG", "JPEG", "WEBP"]

                user_side_img = Image.open(profile_pic_change)
                if user_side_img.format.upper() in allowed_formats:
                    print()
                    print()
                    print()
                    print("Image Satisfied the Format")
                    try:
                        os.makedirs(f"media/{current_user_details.id}/profile_img")

                    except:
                        pass
                    profile_img_loc = (
                        f"media/{current_user_details.id}/profile_img/profile_pic.jpeg"
                    )
                    user_side_img.save(profile_img_loc)

                    new_image = users.objects.get(
                        email_id=user_email_fetched_based_on_user_token[0]
                    )
                    new_image.user_profile_pic = profile_img_loc
                    new_image.save()
                    print("Profile Pic Updated !!")
                else:
                    return HttpResponse("Profile Picture Format errror")

            # fetching email_id from user_token

            user_email_fetched_based_on_user_token = [
                x
                for x in users_credentials_IPs.objects.filter(
                    user_token=cookie_token_data
                ).values_list("user_email_id")[0]
            ]
            fetching_all_user_data = users.objects.filter(
                email_id=user_email_fetched_based_on_user_token[0]
            ).values_list()[:1]
            print("user details on db, ", fetching_all_user_data)
            # Fetching property_details on user_email

            user_property_details = list(
                map(
                    lambda x: x[0],
                    property_details.objects.filter(
                        user_emailid_via_login_token=user_email_fetched_based_on_user_token[
                            0
                        ]
                    ).values_list("id"),
                )
            )
            print(user_property_details)
            user_selling_property_images = {}
            try:
                for x in user_property_details:
                    # formate:-  >   {1: 'WhatsApp_Image_2023-03-04_at_18.08.06_1.jpeg', 2: 'WhatsApp_Image_2023-03-04_at_18.07.44_1.jpeg'}

                    user_selling_property_images[x] = (
                        images.objects.filter(property_name=x).values_list("image")[:1]
                    )[0][0]
            except:
                pass

            # user_selling_property_images=list(map(lambda x:x,[images.objects.filter(property_name=x).values('image') for x in user_property_details]))
            print("user_selling_property_images : ", user_selling_property_images)
            print("user data : ", fetching_all_user_data)
            if user_selling_property_images == {}:
                user_selling_property_images = False

            print(f"Password miss match : {password_not_match}")
            data = {
                "user_data": fetching_all_user_data,
                "user_property_details": user_selling_property_images,
                "user_status1": True,
                "message_data": message_data,
                "password_not_match": password_not_match,
            }

            return render(request, "profile.html", data)
            # return render(request,'profile.html',data)
    else:
        print("No, User Not Logged_in")
        # data={

        #     'user_status1': False
        # }
        return HttpResponseRedirect("/")
        # return HttpResponse('please login')
