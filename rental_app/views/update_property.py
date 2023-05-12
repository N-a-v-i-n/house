from .common_imports import *


def update_property(request, productID):
    cookies_token = request.COOKIES.get(
        "otp_token"
    )  # checking for the cookies if the user is already logged in or not

    if cookies_token:
        print("browser_token : ", cookies_token)

        validate = token_validations(cookies_token)

        print("is token_match : ", validate)

        if validate:
            if request.method == "POST":
                property_name = request.POST.get("property_name").lower()

                print(property_name)
                # property_images_temp = request.FILES.getlist("property_images1")

                print()
                # print()
                # print("check : ", property_images_temp)
                property_type = request.POST.get("property_type").lower()
                property_city = request.POST.get("property_city").lower()
                property_state = request.POST.get("property_state").lower()
                # property_located_in_city=request.POST.get('property_located_in_city')
                property_pincode = request.POST.get("property_pincode").lower()
                property_distict = request.POST.get("property_distict").lower()
                property_floor = request.POST.get("property_floor").lower()
                property_rooms = request.POST.get("property_rooms")
                monthly_rent = request.POST.get("monthly_rent").lower()
                # monthly_maintance=request.POST.get('monthly_maintance')
                # required_doc=request.POST.get('required_doc')
                # advance_amount=request.POST.get('advance_amount')
                # contact_no=0
                house_area = request.POST.get("house_area").lower()
                furnished_or_semi = request.POST.get("furnished_or_semi")
                # tenure_period=request.POST.get('tenure_period')
                parking = request.POST.get("parking").lower()
                # variable_or_fixed=request.POST.get('variable_or_fixed')

                # newlyy added fileds are : -
                appliance_tv = True if request.POST.get("appliance_tv") else False
                appliance_fridge = (
                    True if request.POST.get("appliance_fridge") else False
                )
                appliance_sofa = True if request.POST.get("appliance_sofa") else False
                appliance_bed = True if request.POST.get("appliance_bed") else False
                appliance_dresser = (
                    True if request.POST.get("appliance_dresser") else False
                )
                appliance_ac = True if request.POST.get("appliance_ac") else False
                appliance_washing_machine = (
                    True if request.POST.get("appliance_washing_machine") else False
                )
                appliance_water_heater = (
                    True if request.POST.get("appliance_water_heater") else False
                )
                appliance_water_purifier = (
                    True if request.POST.get("appliance_water_purifier") else False
                )
                appliance_fans = True if request.POST.get("appliance_fan") else False
                appliance_tubelights = (
                    True if request.POST.get("appliance_tubelights") else False
                )
                appliance_Inventers = (
                    True if request.POST.get("appliance_Inventers") else False
                )

                new_data = property_details.objects.filter(id=productID).update(
                    property_name=property_name,
                    property_type=property_type,
                    property_city=property_city,
                    property_state=property_state,
                    property_pincode=property_pincode,
                    # property_located_in_city=property_located_in_city,
                    property_floor=property_floor,
                    # property_conditions=property_conditions,
                    monthly_rent=monthly_rent,
                    # monthly_maintance=monthly_maintance,
                    # required_doc=required_doc,
                    # advance_amount=advance_amount,
                    # contact_no=contact_no,
                    house_area=house_area,
                    # furnished_or_semi=furnished_or_semi,
                    # tenure_period=tenure_period,
                    parking=parking,
                    # variable_or_fixed=variable_or_fixed,
                    # newlyy added fields are :-
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
                )

                data = {"Property_updated_success": True}

                return render(request, "update_property.html", data)

            get_all_posted_ad_ids = [
                x[0]
                for x in property_details.objects.filter(
                    user_emailid_via_login_token=validate[1]
                ).values_list("id")
            ]

            print("user posted product id's are : ", get_all_posted_ad_ids)

            if productID in get_all_posted_ad_ids:
                fetching_product_for_update = property_details.objects.filter(
                    id=productID
                ).values(
                    "property_name",
                    "property_type",
                    "property_city",
                    "property_state",
                    "property_pincode",
                    "property_distict",
                    "property_floor",
                    "monthly_rent",
                    "house_area",
                    "furnished_or_semi",
                    "rooms",
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
                    "parking",
                )
                fetching_img_property_details = images.objects.filter(
                    property_name=productID
                ).values("image")
                print("imag : ", fetching_img_property_details)
                print(fetching_product_for_update[0])
                data = {
                    "product_details": fetching_product_for_update[0],
                    "product_img": fetching_img_property_details[0],
                    "user_status": True,
                }

                return render(request, "update_property.html", data)

            else:
                return HttpResponse("No Buddy, Please Don't do")

        else:
            print("Token Not Match")
            return HttpResponseRedirect("/login")

    else:
        return HttpResponseRedirect("/login")
