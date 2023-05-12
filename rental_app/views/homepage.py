from .common_imports import *
import geocoder
from urllib.request import urlopen
import re as r
import urllib.error


def getIP():
    try:
        try:
            d = urlopen("https://api.bigdatacloud.net/data/client-ip", timeout=5).read()
        except:
            d = urlopen("https://api.ipify.org/?format=json", timeout=5).read()
        daa = d.decode("utf-8")
        ip = (daa.split('"'))[3]
        return ip
        # return r.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)
    except urllib.error.HTTPError as err:
        # print(f"A HTTPError was thrown: {err.code} {err.reason}")
        pass


def homepage(request, page_no=1):
    import socket

    #  Locating user state

    client_ip_address = getIP()
    # print("client_ip_address : ", client_ip_address)
    geoloc = geocoder.ip(f"{client_ip_address}").state
    # print("geoloc", geoloc)
    location_state = str(geoloc).lower()

    user_landed_to_homepage = user_collections.objects.create(
        user_visited_ip_address=client_ip_address,
        visted_time=timezone.now(),
        user_state_by_geo_loc=location_state,
    )
    user_landed_to_homepage.save()
    # print("client_ip_address", client_ip_address)

    # Auto_create_selling_properties_for_testing

    # adding_rents_house()

    # Below Code will Auto Delete post which was expired

    # post_auto_delete_cron()

    message_data = False

    search_cities = False

    Is_logout = False

    cookies_token = request.COOKIES.get(
        "otp_token"
    )  # checking for the cookies if the user is already logged in or not

    if cookies_token:
        # print("browser_token : ", cookies_token)

        validate = token_validations(cookies_token)

        # print("is token_match : ", validate)

        if validate:
            is_user_logged_in = True

            # print("Yes, User Logged_in")

            # get_all_user_liked_images=True

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

            # print("checking_for_message_update : ", checking_for_message_update)

            if checking_for_message_update:
                message_data_temp = [x for x in checking_for_message_update]
                message_data = [x for x in checking_for_message_update]
                # print("message_data : ", message_data)

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

                    # print("images", property_images)

            # user_id_through token

            user_id_through_token = users_credentials_IPs.objects.filter(
                user_token=cookies_token
            ).values_list("user_email_id")

            user_email_id = ""

            for x in user_id_through_token[0]:
                user_email_id = x

            fetch_user_id_via_email = users.objects.filter(
                email_id=user_email_id
            ).values_list("id")

            user_id = ""

            for x in fetch_user_id_via_email[0]:
                user_id = x

            get_all_user_liked_images = []

            for x in user_id_for_product.objects.filter(user_id=user_id).values_list(
                "product"
            ):
                get_all_user_liked_images.append(str(x[0]))

            # print("get_all_user_liked_images : ", get_all_user_liked_images)

        else:
            is_user_logged_in = False

            get_all_user_liked_images = False

            # print("No, User Not Logged_in1")

            response = render(request, "index.html")

            response.delete_cookie("otp_token")
            response.delete_cookie("email_id")

            return response

    else:
        is_user_logged_in = False

        # print("No, User Not Logged_in2")

        get_all_user_liked_images = False

    no_data_found = False

    # Below code for filter_ data
    product_ids = []

    state_selected = request.POST.get("state_selected")
    # if values is Others the us name 'city_others_entered'
    select_cities = request.POST.get("select_cities")

    manual_entry_city = request.POST.get("city_others_entered")
    # below is included on bottom sort
    # max_min_radio=request.POST.get("max_min_radio")  #if values then take input from user i.e = Min_Range,Max_Range
    manual_entry_min = request.POST.get("Min_Range")
    manual_entry_max = request.POST.get("Max_Range")

    # print("state_selected : ", state_selected)
    # print("select_cities : ", select_cities)

    # print("manual_entry_city : ", manual_entry_city)

    # print("manual_entry_min : ", manual_entry_min)
    # print("manual_entry_max : ", manual_entry_max)

    # filtered_data=[]

    if bool(state_selected):
        if state_selected and (bool(select_cities) or bool(manual_entry_city)):
            product_ids = [
                x[0]
                for x in (
                    property_details.objects.filter(
                        property_state=state_selected.lower()
                    )
                )
                .filter(property_city=select_cities.lower())
                .values_list("id")
            ]
            # print("testing : ", product_ids)
            if product_ids:
                pass
            else:
                try:
                    product_ids = [
                        x[0]
                        for x in (
                            property_details.objects.filter(
                                property_state=state_selected.lower()
                            )
                        )
                        .filter(property_city=manual_entry_city.lower())
                        .values_list("id")
                    ]
                    if product_ids:
                        pass
                    else:
                        no_data_found = True
                except:
                    no_data_found = True

            # print("filtered_data : ", product_ids)

        elif state_selected:
            # print()
            # print()
            # print("enter")
            product_ids = [
                x[0]
                for x in property_details.objects.filter(
                    property_state=state_selected.lower()
                ).values_list("id")
            ]
            # print("product_ids : ", product_ids)
            if product_ids:
                pass
            else:
                no_data_found = True
            # print("filtered_data : ", product_ids)

    # below code for Search Engine

    # product_ids=[]

    getdata = request.GET.get("search_area")

    if getdata:
        # Below code is for searching product through area_name

        search_data = getdata.lower()

        # print("searched data : ", search_data)

        if search_data:
            temp = property_details.objects.filter(
                property_city=search_data
            ).values_list("id")

            if temp:
                pass

            else:
                temp = property_details.objects.filter(
                    property_pincode=search_data
                ).values_list("id")

                if temp:
                    pass

                else:
                    no_data_found = True

            # print("product_ids", temp)
            for x in temp:
                product_ids.append(x[0])

    # searched from backend [7, 8, 9, 10, 11]

    if product_ids:
        temp = []

        temp2 = []

        fetch_unique_id = []

        fetch_image = []

        for x in product_ids:
            temp.append(images.objects.filter(property_name=x).values_list())

            temp2.append(
                (
                    images.objects.filter(property_name=x)
                    .values_list("property_name")
                    .distinct()
                )[0]
            )

            # temp2.append(x)

        # print("temp2", temp2)

        for x in temp:
            fetch_image.append(x[0])

        for x in temp2:
            fetch_unique_id.append(x[0])

        # print("fetch_image : ", fetch_image)

        # print("fetch_unique_id : ", fetch_unique_id)

        # fetch_image :  [(31, 10, 'navintamil31@gmail.com', 'WhatsApp_Image_2023-03-04_at_18.08.09_kzvurpi.jpeg')]

        # fetch_unique_id :  [31]

    else:
        # fetch_image :  [(31, 10, 'navintamil31@gmail.com', 'WhatsApp_Image_2023-03-04_at_18.08.09_kzvurpi.jpeg')]

        # fetch_unique_id :  [31]
        fetch_image = []

        temp4 = (
            (images.objects.all().values_list()).exclude(property_name="temp")
        ).exclude(Is_image_safe=False)

        for x in temp4:
            fetch_image.append(x)

        fetch_unique_id = []
        # print("fetch_unique_id : ", fetch_unique_id)

        temp3 = (
            images.objects.filter().values_list("property_name").distinct()
        ).exclude(property_name="temp")

        for x in temp3:
            fetch_unique_id.append(x[0])

    # print()

    # print()

    # print()

    monthly_rent = []

    for x in fetch_unique_id:
        # house_img_monthly_rent.append(property_details.objects.filter(id=x[0]).values_list('monthly_rent'))

        monthly_rent.append(
            [
                property_details.objects.filter(id=x).values_list(
                    "monthly_rent",
                    "property_state",
                    "no_of_likes",
                    "property_city",
                    "rooms",
                    "furnished_or_semi",
                )[0],
                x,
            ]
        )

    # This code is used to get filter of unique id and for that unique fetch only one image

    store_ref = []

    store_ref_img = []  # storing email_id & images

    for x in fetch_image:
        if x[1] in store_ref:
            continue

        else:
            store_ref.append(x[1])

            store_ref_img.append([x[2], x[3]])

    # getting each image of ever user from the database

    # print()

    # print()

    # print()

    # print()

    # print()

    # print()

    area_amt_img = []

    for each in store_ref_img:
        # Pattern match for media, so that if image does not contain media/{image} --> will add that 'media/' in front

        # each[5]=city,  each[11]=rent_amt,   each[3]=image

        pattern = "media/"

        string = each[1]

        match = re.match(pattern, string)

        if match:
            area_amt_img.append((each))

        else:
            area_amt_img.append((f"/media/{each[1]}"))

    all_in_one = []

    for x in range(len(monthly_rent)):
        try:
            all_in_one.append([monthly_rent[x][0], area_amt_img[x], monthly_rent[x][1]])
        except Exception as error:
            new_error = failure_response.objects.create(
                other_responses=error,
                failure_user_details=current_user_details,
                created_At=timezone.now(),
            )
            new_error.save()
    # Check for filter option by rooms

    select_rooms = request.POST.get("select_rooms")

    select_furnish = request.POST.get("select_furnish")

    if bool(select_rooms) and bool(select_furnish):
        main_ref = all_in_one
        all_in_one = []

        for x in main_ref:
            if str(select_rooms) in x[0] and str(select_furnish) in x[0]:
                all_in_one.append(x)
            else:
                no_data_found = True

    elif bool(select_rooms):
        main_ref = all_in_one
        all_in_one = []
        for x in main_ref:
            # print("x[0]  ", x[0])
            if str(select_rooms) in x[0]:
                all_in_one.append(x)
            else:
                no_data_found = True

    elif bool(select_furnish):
        main_ref = all_in_one
        all_in_one = []
        for x in main_ref:
            if str(select_furnish) in x[0]:
                all_in_one.append(x)
            else:
                no_data_found = True

    if request.POST.get("max_min_radio") == "0":
        all_in_one.sort()

    elif request.POST.get("max_min_radio") == "1":
        all_in_one.sort(reverse=True)

    elif manual_entry_min:  # and request.POST.get("Max_Range"):
        filter_based_on_ranges = []

        for x in all_in_one:
            # print("x[0][0]", x[0][0])
            if int(x[0][0]) >= int(manual_entry_min) and int(x[0][0]) <= int(
                manual_entry_max
            ):
                filter_based_on_ranges.append(x)

        if filter_based_on_ranges:
            all_in_one = filter_based_on_ranges
        else:
            all_in_one = filter_based_on_ranges
            no_data_found = True

        # print("filter_based_on_ranges : ", filter_based_on_ranges)

    No_of_pages_needed = math.ceil(len(all_in_one) / 20)

    # print("details :  ", all_in_one, page_no)

    data = {
        "area_amt": pagination_wise_data(all_in_one, page_no),
        "No_of_pages_needed": [x for x in range(1, No_of_pages_needed + 1)],
        "user_status": is_user_logged_in,
        "user_liked_data": get_all_user_liked_images,
        "no_data_found": no_data_found,
        "message_data": message_data,
        "state_data": search_cities,
        "Log_out_success": Is_logout,
    }

    if request.method == "POST":
        # Below Code is to log-out user from profile page

        logout = request.POST.get("logout")

        if logout:
            get_token_from_browser = request.COOKIES.get("otp_token")

            confirm = delete_cookies(get_token_from_browser)

            data["Log_out_success"] = True

            response = render(request, "index.html", data)

            response.delete_cookie("otp_token")

            response.delete_cookie("email_id")

            # print("cookies clear succeess !!")

            return response

        # Login_From DAta

        user_email = request.POST.get("login_email_id")

        if user_email:
            password = request.POST.get("login_email_password")

            # print("user email : ", user_email)

            # print("user password : ", password)

            # Checking User Credentials
            try:
                user_details = users.objects.get(email_id=user_email)

                # print("user_details : ", user_details)

            except:
                data = {"user_not_match": True}

                return render(request, "index.html", data)

            check_email = users.objects.filter(email_id=user_email).values(
                "email_id", "user_password"
            )

            # print(check_email)

            if check_email and str(password) == str(check_email[0]["user_password"]):
                # print("User Login success")

                ## Taking users ip address and passing a token ND BOTH TOKEN nd IP address are stored in db

                gen_token = token_gen()

                new_user_credentials = users_credentials_IPs.objects.create(
                    user_id=user_details,
                    user_email_id=user_email,
                    user_ip_address=client_ip_address,
                    user_token=gen_token,
                    createdAt=timezone.now(),
                    user_state_by_geo_loc=location_state,
                )

                new_user_credentials.save()

                response = HttpResponseRedirect("/")

                # removing the secure in cookies due to check that cookie existing on header.html for sell btn

                response.set_cookie("otp_token", gen_token, max_age=84600)

                response.set_cookie("email_id", user_email, max_age=84600)

                # response.set_cookie('email_id',user_email,secure=True,httponly=True,max_age=84600)

                return response

            else:
                data = {"user_not_match": True}

                return render(request, "index.html", data)

        # SignUp Form Integrations

        email = request.POST.get("email_id")

        mobile_no = request.POST.get("mobile_no")

        Is_Exist = mobile_no_r_email_existance(email, mobile_no)

        # print("User_Exists : ", Is_Exist)

        if email:
            if Is_Exist == False:
                # print()

                # print()

                # print()

                # print()

                first_name = request.POST.get("first_name")

                last_name = request.POST.get("last_name")

                # email_id=request.POST.get('email_id')

                # mobile_no=request.POST.get('mobile_no')

                password = request.POST.get("login_email_password")

                # Bio=request.POST['Bio']

                new_data = users(
                    first_name=first_name,
                    last_name=last_name,
                    email_id=email,
                    mobile_no=mobile_no,
                    user_password=password,
                    # Bio=Bio,
                    created_at=timezone.now(),
                    user_state_by_geo_loc=location_state,
                )

                new_data.save()

                # print()

                # print()

                # print("signup success for : ", email)

                # after signup user should be logined_state

                ## Taking users ip address and passing a token ND BOTH TOKEN nd IP address are stored in db

                gen_token = token_gen()

                new_user_credentials = users_credentials_IPs.objects.create(
                    user_id=new_data,
                    user_email_id=new_data.email_id,
                    user_ip_address=client_ip_address,
                    user_token=gen_token,
                    createdAt=timezone.now(),
                    user_state_by_geo_loc=location_state,
                )

                new_user_credentials.save()

                response = HttpResponseRedirect("/")

                # removing the secure in cookies due to check that cookie existing on header.html for sell btn

                response.set_cookie("otp_token", gen_token, max_age=84600)

                response.set_cookie(
                    "email_id",
                    new_data.email_id,
                    max_age=84600,
                )

                return response

            else:
                data = {"user_already_exist": True}

                return render(request, "index.html", data)

        Product_id = request.POST.get("product-ID")

        # print("product_id : ", Product_id)

        if Product_id:
            get_token_from_browser = request.COOKIES.get("otp_token")

            user_id_through_token = users_credentials_IPs.objects.filter(
                user_token=get_token_from_browser
            ).values_list("user_email_id")

            user_email_id = ""

            for x in user_id_through_token[0]:
                user_email_id = x

            fetch_user_id_via_email = users.objects.filter(
                email_id=user_email_id
            ).values_list("id")

            user_id = ""

            for x in fetch_user_id_via_email[0]:
                user_id = x

            property_Search = property_details.objects.get(id=Product_id)

            storing_userID_ProductID = user_id_for_product.objects.create(
                user_id=user_id, product=property_Search
            )

            storing_userID_ProductID.save()

            increase_count_for_likes = property_details.objects.get(id=Product_id)

            increase_count_for_likes.no_of_likes = (
                increase_count_for_likes.no_of_likes
            ) + 1

            increase_count_for_likes.save()

            return HttpResponseRedirect("/")

    return render(request, "index.html", data)
