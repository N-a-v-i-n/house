from .common_imports import *
from urllib.request import urlopen
import re as r


def getIP():
    try:
        try:
            d = urlopen("https://api.bigdatacloud.net/data/client-ip", timeout=5).read()
        except:
            d = urlopen("https://api.ipify.org/?format=json", timeout=5).read()
        daa = d.decode("utf-8")
        ip = (daa.split('"'))[3]
        return ip
    except:
        return None


def login(request):
    # #checking for user token validations
    # get_user_token_from_cookie=request.COOKIES.get('otp_token')
    # print('Cookie Token is : ',get_user_token_from_cookie)
    # if get_user_token_from_cookie:
    #     validate_token=token_validations(get_user_token_from_cookie)
    #     print("is token Valid : ",validate_token)

    # below code will check if email valid or not and if valid then proceed otp_generate and store on table
    user_entered_email = request.POST.get("user_entered_email")
    if user_entered_email:
        print("user entered email is : ", user_entered_email)
        check_for_email_existance = (
            True if (users.objects.filter(email_id=user_entered_email)) else False
        )
        print("db search for email : ", check_for_email_existance)
        if check_for_email_existance:
            generate_otp = otp_gen()
            store_otp = user_otp.objects.create(
                email_id=user_entered_email, otp=generate_otp
            )
            store_otp.save()
            print("user otp is : ", generate_otp)
            # send_mail("Login Verification",f"Your Otp is : {generate_otp}",settings.EMAIL_HOST_USER,[user_entered_email])
            print("OTP Send Via EMail")

            data = {"user_existance": True, "email_id": user_entered_email}
            return render(request, "login.html", data)

        else:
            data = {"user_existance": False}
            return render(request, "login.html", data)

    # check for the user otp enterd match with data base or not, if match generate token and add to cookie
    otp_email_id = request.POST.get("otp_email_id")

    if otp_email_id:
        user_enter_otp = request.POST.get("User_Entered_OTP")
        get_latest_otp_on_db = [
            x
            for x in user_otp.objects.filter(email_id=otp_email_id).values_list(
                "id", "otp"
            )
        ]
        get_latest_otp_on_db.sort(reverse=True)
        print("Latest otp is : ", get_latest_otp_on_db[:1])
        try:
            is_match_otp = (
                True
                if str((get_latest_otp_on_db[:1])[0][1]) == str(user_enter_otp)
                and users.objects.get(email_id=otp_email_id)
                else False
            )

        except:
            return HttpResponse("SomeThing Went Wrong")
        user_details = users.objects.get(email_id=otp_email_id)
        print("user otp matched : ", is_match_otp)
        if is_match_otp:
            generate_token = token_gen()
            user_ip_address = getIP()
            new_token_entry = users_credentials_IPs.objects.create(
                user_id=user_details,
                user_email_id=otp_email_id,
                user_ip_address=user_ip_address,
                user_token=generate_token,
                createdAt=timezone.now(),
            )
            new_token_entry.save()
            print("token : ", generate_token)

            data = {"is_match_otp": is_match_otp}

            response = render(request, "login.html", data)
            response.set_cookie(key="otp_token", value=str(generate_token))
            response.set_cookie(key="email_id", value=str(otp_email_id))
            print("TOken Generated and added to COOKIE", generate_token)
            return response
        else:
            data = {"is_match_otp": is_match_otp}
            return render(request, "login.html", data)

    return render(request, "login.html")
