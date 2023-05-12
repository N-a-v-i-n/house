from .common_imports import *


def product(request, productID):
    cookies_token = request.COOKIES.get(
        "otp_token"
    )  # checking for the cookies if the user is already logged in or not
    cookies_email_id = request.COOKIES.get("email_id")
    if cookies_token:
        print("browser_token : ", cookies_token)
        validate = token_validations(cookies_token)
        print("is token_match : ", validate)

        if validate:
            message_data = False
            is_user_logged_in = True
            limit_over_pop_up = False
            currentTime = timezone.now()

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

            fetching_user_id_from_token = users_credentials_IPs.objects.get(
                user_token=cookies_token
            )
            current_user_details = fetching_user_id_from_token.user_id
            print("current_user_details : ")
            print("user_id : ", current_user_details.id)
            print("user_email : ", current_user_details.email_id)
            # requesting_for_view_contact_no by user, the code to make count for no of request
            # validations based on Cookie Email_id and User_id through product page

            # below code will give owner account-id
            user_id_request_for_view_contact_no = request.POST.get(
                "request_for_view_contact_no"
            )

            unlocked_contact_no_details = [
                x[0]
                for x in user_free_limits.objects.filter(
                    user_id=current_user_details.id
                )
                .values_list("unlocked_contact_no_for_product_id_is")
                .distinct()
            ]
            print("unlocked_contact_no_details", unlocked_contact_no_details)
            updating_request_count = users.objects.get(id=current_user_details.id)

            # #check if the access limit is over or not
            # if updating_request_count.no_of_requests_to_view_contact_no >=3:
            #     access_limit_over=True

            # CHeck for all unlocked product-id for the user
            if productID in unlocked_contact_no_details:
                access_for_contact_no = True
            else:
                access_for_contact_no = False

            if user_id_request_for_view_contact_no:
                print(" User Account ID : ", current_user_details.id)
                print("user email : ", cookies_email_id)
                print("db email : ", updating_request_count)
                if (
                    str(updating_request_count.email_id) == str(cookies_email_id)
                    and updating_request_count.no_of_requests_to_view_contact_no <= 200
                ):
                    update_user_free_limit_table = user_free_limits.objects.create(
                        user_id=updating_request_count,
                        product_id=property_details.objects.get(id=productID),
                        unlocked_contact_no_for_product_id_is=productID,
                        unlocked_at=timezone.now(),
                    )
                    update_user_free_limit_table.save()
                    print(
                        "Before user_request_count : ",
                        updating_request_count.no_of_requests_to_view_contact_no,
                    )

                    updating_request_count.no_of_requests_to_view_contact_no = (
                        updating_request_count.no_of_requests_to_view_contact_no + 1
                    )
                    print(
                        "After user_request_count : ",
                        updating_request_count.no_of_requests_to_view_contact_no,
                    )
                    updating_request_count.save()
                    access_for_contact_no = True

                    # Updating send_text_to_owners table
                    property_owner = users.objects.get(
                        id=user_id_request_for_view_contact_no
                    )

                    send_text_to_owners = send_text_to_owner.objects.create(
                        request_user_id=current_user_details.id,
                        receiver_user_id=users.objects.get(
                            id=user_id_request_for_view_contact_no
                        ),
                        request_property_id=productID,
                        request_user_mobile_no=current_user_details.mobile_no,
                        request_user_email_id=current_user_details.email_id,
                        request_user_time=currentTime,
                    )
                    send_text_to_owners.save()
                    # try:
                    # #sending text on mail as well
                    #     product_id= property_details.objects.get(id=productID)
                    #     send_to_mail= send_mail("Hey, Looking For Your Property !! ",f"Hello {property_owner.last_name},\ni'm {current_user_details.last_name}, I hope you are having a good week. \nI'm getting in touch to request a viewing of the property at {product_id.property_city}. please reach me out on this number '{current_user_details.mobile_no}' \nThank You. ",settings.EMAIL_HOST_USER,[current_user_details.email_id])

                    #     print("Mail Has Been Sent")
                    # except:
                    #     pass

                else:
                    access_for_contact_no = False
                    limit_over_pop_up = True

            (
                product_imgs,
                fetching_the_product_details,
                fetching_price_and_user_address,
            ) = fetching_img_property_details(productID)

            # fetching user info to show on product page
            fetching_owner_email_through_product_id = property_details.objects.filter(
                id=productID
            ).values("user_emailid_via_login_token")
            print("Product Owner Details : ", fetching_owner_email_through_product_id)
            fetching_all_user_data = users.objects.filter(
                email_id=fetching_owner_email_through_product_id[0][
                    "user_emailid_via_login_token"
                ]
            ).values_list(
                "id",
                "first_name",
                "last_name",
                "mobile_no",
                "user_profile_pic",
                "created_at",
            )[
                :1
            ]
            print("Product Owner Details all info : ", fetching_all_user_data)
            fetch_house_appliances = [
                x
                for x in property_details.objects.filter(id=productID).values(
                    "appliance_TV",
                    "appliance_Fridge",
                    "appliance_sofa",
                    "appliance_bed",
                    "appliance_dresser",
                    "appliance_AC",
                    "appliance_washing_machine",
                    "appliance_water_heaters",
                    "appliance_fans",
                    "appliance_water_purifier",
                    "appliance_tubelights",
                    "appliance_Inventers",
                )
            ]

            # print('house_appliance are : ',fetch_house_appliances)
            # print('Property details : ',fetching_the_product_details)

            print("limit_over_pop_up", limit_over_pop_up)
            data = {
                "property_data": fetching_the_product_details,
                "property_house_appliance": fetch_house_appliances,
                "property_img": product_imgs,
                "fetching_price_and_user_details": fetching_price_and_user_address,
                "user_data": fetching_all_user_data,
                "access_for_contact_no": access_for_contact_no,
                "limit_over_pop_up": limit_over_pop_up,
                "user_status": is_user_logged_in,
                "message_data": message_data,
                # 'timezone':currentTime,
            }

            if request.method == "POST":
                property_id = productID
                user_email_id = request.COOKIES.get("email_id")
                print("property_id : ", property_id)
                new_data = user_liked(
                    liked_property_ids=property_id, user_email=user_email_id
                )
                new_data.save()

            return render(request, "product.html", context=data)

        else:
            is_user_logged_in = False
            print("No, User Not Logged_in")
    else:
        is_user_logged_in = False
        print("No, User Not Logged_in")
        return HttpResponseRedirect("/")

    # product_imgs,fetching_the_product_details,fetching_price_and_user_address=fetching_img_property_details(productID)

    # data={
    #     'property_data':fetching_the_product_details,
    #     'property_img':product_imgs,
    #     'fetching_price_and_user_details':fetching_price_and_user_address,
    # }

    # if request.method=='POST':
    #     property_id=productID
    #     user_email_id=request.COOKIES.get('email_id')
    #     print('property_id : ',property_id)
    #     new_data=user_liked(
    #         liked_property_ids=property_id,
    #         user_email=user_email_id
    #     )
    #     new_data.save()

    # return render(request,'product.html',context=data)
