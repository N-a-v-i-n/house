from .common_imports import *
from urllib.request import urlopen
import re as r


def fetching_img_property_details(productID):
    fetching_the_product_details = property_details.objects.filter(id=productID).values(
        "property_name",
        "property_city",
        "property_state",
        "property_pincode",
        # 'property_located_in_city',
        "property_floor",
        # 'property_conditions',
        # 'monthly_maintance',
        # 'required_doc',
        # 'advance_amount',
        "house_area",
        # 'furnished_or_semi',
        # 'tenure_period',
        "parking",
        # 'variable_or_fixed',
        "id",
        "furnished_or_semi",
        "rooms",
    )
    fetching_price_and_user_address = property_details.objects.filter(
        id=productID
    ).values_list(
        "monthly_rent",
        "property_city",
        "property_state",
        "created_at",
        "id",
    )
    # print()
    # print()
    # print()
    # print(fetching_price_and_user_address)

    fetching_the_product_img = (
        images.objects.filter(property_name=productID).values_list("image")
    ).exclude(Is_image_safe=False)
    product_imgs = []
    for x in fetching_the_product_img:
        product_imgs.append(x[0])

    return product_imgs, fetching_the_product_details, fetching_price_and_user_address


def token_gen():
    token = secrets.token_hex(5)
    print()
    print()
    print("Token Generated : ", token)
    return token


def getIP():
    try:
        d = urlopen("https://api.bigdatacloud.net/data/client-ip", timeout=5).read()
    except:
        d = urlopen("https://api.ipify.org/?format=json", timeout=5).read()
    print("sjhxnjwdkx : ", d)
    daa = d.decode("utf-8")
    ip = (daa.split('"'))[3]
    return ip


def token_validations(token):
    user_ip_address = getIP()

    print("user_ip_address : ", user_ip_address)

    checking_for_credentials_match = users_credentials_IPs.objects.filter(
        user_token=token
    ).values("user_token", "user_email_id", "user_id")
    # checking_for_credentials_match=users_credentials_IPs.objects.filter(user_token=token).values_list('user_token','user_email_id',)

    print("Token on DB : ", checking_for_credentials_match)
    if checking_for_credentials_match:
        if token == checking_for_credentials_match[0]["user_token"]:
            user_role = users.objects.get(
                id=checking_for_credentials_match[0]["user_id"]
            )
            user_email_id = checking_for_credentials_match[0]["user_email_id"]
            # role=checking_for_credentials_match[0]['user_id.role']
            return True, user_email_id, user_ip_address, user_role.role
        else:
            return False
    else:
        return False


def delete_cookies(token):
    # Below Code is to log-out user from profile page
    users_credentials_IPs.objects.filter(user_token=token).delete()
    print("User_token Deleted from DB Success !!")
    return True


def mobile_no_r_email_existance(email, number):
    is_exist = ""
    if users.objects.filter(mobile_no=number) or users.objects.filter(email_id=email):
        is_exist = True
    else:
        is_exist = False

    print("Mobile_R_email_exist_on db : ", is_exist)
    return is_exist


# This Function is to Auto Delete the Post which are expired


def post_auto_delete_cron():
    list_of_post_expire_today = property_details.objects.all().values(
        "post_expire_date",
        "id",
        "user_emailid_via_login_token",
        "contact_no",
        "property_city",
        "property_state",
        "property_pincode",
    )
    post_ids_expired = []

    for x in list_of_post_expire_today:
        # if x['post_expire_date'].date() == datetime.datetime.now().date():
        if str(x["post_expire_date"].date()) == "2023-04-17":
            post_ids_expired.append(x["id"])
            new_deleting_data = Deleted_post_details.objects.create(
                post_id=x["id"],
                post_user_email=x["user_emailid_via_login_token"],
                posted_user_contact_details=x["contact_no"],
                post_address=(
                    x["property_city"],
                    x["property_state"],
                    x["property_pincode"],
                ),
            )
            new_deleting_data.save()

            delete_posts = property_details.objects.get(id=x["id"]).delete()
            delete_images = images.objects.filter(property_name=x["id"]).delete()
    print("Post_id's expiring today : ", post_ids_expired)


# function for paginations
def pagination_wise_data(total_data, page_no):
    default_product_in_per_page = 20

    if page_no > 1:
        start_value = default_product_in_per_page * (page_no - 1)
    else:
        start_value = 0

    total_data_length = len(total_data)
    pages_needed = total_data_length / default_product_in_per_page

    print("total_data_length : ", total_data_length)
    print("pages_needed : ", pages_needed)

    if page_no:
        data = total_data[start_value : default_product_in_per_page * page_no : 1]
        print("data : ", data)

        return data


def otp_gen():
    list_of_num = [7, 8, 4, 1, 2, 5, 9, 6, 3]
    otp_generate = set()
    while len(otp_generate) < 5:
        otp_generate.add(random.choice(list_of_num))
    return "".join(map(str, otp_generate))


def success(request):
    response = HttpResponse("Welcome")
    response.set_cookie("user", True)
    return response


def high_to_low(list):
    list.sort(reverse=True)
    print(list)


def low_to_high(list):
    list.sort()
    print(list)


def search_cities_through_state(state):
    # State wise cities

    ap = [
        "VISAKHAPATNAM",
        "VIZIANAGARAM",
        "EAST GODAVARI",
        "GUNTUR",
        "YSR KADAPA",
        "KURNOOL",
        "KRISHNA",
        "NELLORE",
        "ANANTHAPUR",
        "CHITTOOR",
        "SRIKAKULAM",
        "VISHAKAPATNAM",
        "WEST GODAVARI",
        "ANANTHAPURAM",
        "PENUKONDA",
        "URAVAKONDA",
        "BELUGUPPA",
        "BATHALAPALLI",
        "BUKKARAYASAMUDRAM",
        "KOTHACHERUVU",
        "HINDUPUR",
        "RAPTHADU",
        "SOMANDEPALLI",
        "GARLADENNE",
        "GORANTLA",
        "BUKKAPATNAM",
        "VAJRAKARUR",
        "CHILAMATHURU",
        "VIDAPANAKAL",
        "CHENNEKOTHAPALLI",
        "DHARMAVARAMU",
        "KUDERU",
        "LEPAKSHI",
        "KANAGANIPALLE",
        "PUTTAPARTHY",
        "SINGANAMALA",
        "RAJAVOMMANGI",
        "PHIRANGIPURAM",
        "PEDAKURAPADU",
        "VEMURU",
        "THULLUR",
        "SATTENAPALLE",
        "BHATTIPROLU",
        "PEDAKAKANI",
        "TSUNDUR",
        "AMARAVATHI",
        "ATCHAMPET",
        "AMRUTHALUR",
        "KROSURU",
        "KOLLUR",
        "VATTICHERUKURU",
        "TENALI",
        "KOLLIPARA",
        "PONNUR",
        "MANGALAGIRI",
        "TADIKONDA",
        "CHEBROLU",
        "DUGGIRALA",
        "TADEPALLE",
        "MEDIKONDURU",
        "EDLAPADU",
        "PRATHIPADU",
        "PEDANANDIPADU",
        "MUPPALLA",
        "NADENDLA",
        "TADEPALLI",
        "BAPULAPADU",
        "PAMARRU",
        "AGIRIPALLE",
        "NANDIGAMA",
        "PAMIDIMUKKALA",
        "GANNAVARAM",
        "VUYYURU",
        "GUDIVADA",
        "VEERULLAPADU",
        "VATSAVAI",
        "VIJAYAWADA (RURAL)",
        "UNGUTURU",
        "NANDIVADA",
        "GUDLAVALLERU",
        "PENUGANCHIPROLU",
        "JAGGAYYAPETA",
        "NUZVID",
        "MOPIDEVI",
        "PEDAPARUPUDI",
        "G.KONDURU",
        "MOVVA",
        "KANCHIKACHERLA",
        "GHANTASALA",
        "CHANDARLAPADU",
        "THOTLAVALLURU",
        "KANKIPADU",
        "CHALLAPALLE",
        "MYLAVARAM",
        "IBRAHIMPATNAM",
        "PENAMALURU",
        "MOPIDEVI",
        "VIJAYAWADA RURAL",
        "SARAVAKOTA",
        "VEERAGHATTAM",
        "CHEEDIKADA",
        "ARAKU VALLEY",
        "G.MADUGULA",
        "GANTYADA",
        "KURUPAM",
        "CHINTALAPUDI",
        "THONDANGI",
        "RAMACHANDRAPURAM",
        "TUNI",
        "KARAPA",
        "RAVULAPALEM",
        "THALLAREVU",
        "PITHAPURAM",
        "ANAPARTHI",
        "ATREYAPURAM",
        "PEDDAPURAM",
        "KARAPA",
        "PEDAPUDI",
        "JAGGAMPETA",
        "BIKKAVOLU",
        "THONDANGI",
        "KIRLAMPUDI",
        "RAJANAGARAM",
        "SEETHANAGARAM",
        "SAMALKOT",
        "GANDEPALLI",
        "KORUKONDA",
        "GOLLAPROLU",
        "KAKINADA",
        "MANDAPETA",
        "TALLAREVU",
        "KADIAM",
        "RAJAMAHENDRAVARAM  RURAL",
        "RANGAMPETA",
        "U.KOTHAPALLI",
        "SANKAVARAM",
        "YELESWARAM",
        "VINUKONDA",
        "NUZENDLA",
        "RAYACHOTI (PART)",
        "PORUMAMILLA (PART)",
        "CHAPAD (FULL)",
        "JAMMALAMADUGU (PART)",
        "PULLAMPETA (PART)",
        "LAKKIREDDIPALLE (PART)",
        "KODUR (FULL)",
        "RAJAMPETA (PART)",
        "VALLUR (PART)",
        "S.MYDUKUR (PART)",
        "DUVVUR (PART)",
        "CHINTAKOMMADINNE (FULL)",
        "RAMAPURAM ( FULL)",
        "CHENNUR (FULL)",
        "KHAJIPET (FULL)",
        "MUDDANUR (PART)",
        "KONDAPURAM (PART)",
        "KAMALAPURAM (PART)",
        "B.KODUR (PART)",
        "YERRAGUNTLA (PART)",
        "RAJUPALEM (PART)",
        "OBULAVARIPALLE (PART)",
        "VONTIMITTA (PART)",
        "PRODDATUR (PART)",
        "BRAHMAMGARIMATTAM (PART)",
        "SAMBEPALLI (FULL)",
        "MYLAVARAM (PART)",
        "BUDWEL (PART)",
        "GOPAVARAM (PART)",
        "THONDUR (PART)",
        "SIDHOUT (PART)",
        "CHITVEL (PART)",
        "KALASAPADU (PART)",
        "NANDALUR (PART)",
        "PULIVENDULA (PART)",
        "SRI AVADHUTA KASINAYANA  (PART)",
        "VEMULA (PART)",
        "KALLUR",
        "PANYAM",
        "BETAMCHERLA",
        "NANDYAL",
        "VELDURTHI",
        "ORVAKAL",
        "GUDUR",
        "DHONE",
        "VELDURTHI",
        "MACHILLIPATNAM",
        "PEDANA",
        "SATYAVADU",
        "VARADIAH PALEM",
        "SULLURPET",
        "NELLORE",
        "TADA",
        "DORAVARISATRAM",
        "BOGOLE",
        "KODAVALURU",
        "MUTHUKUR",
        "DAGADARTHI",
        "KAVALI",
        "VENKATACHALAM",
        "MANUGOLU",
        "NAIDUPETA",
        "ALLURU",
        "CHILAKUR",
        "T.P.GUDUR",
        "KOVURU",
        "JALADANKI",
        "OJILI",
        "THONDAGI",
        "U KOTHAPALLI",
        "KAKINADA RURAL",
        "ATCHUTAPURAM",
        "RAMBILLI",
        "NAKKAPALLI",
        "PARAWADA",
        "S RAYAVARAM",
        "PAYAKARAOPETA",
        "DARSI",
        "ADDANKI",
        "PODILI",
        "JANAKAVARAM PANGULURU",
        "KOMAROLU",
        "KOTHAPATNAM",
        "KURICHEDU",
        "KONAKANAMITLA",
        "GIDDALURU",
        "NAGULUPPALAPADU",
        "TANGUTURU",
        "CUMBUM",
        "MADDIPADU",
        "RACHERLA",
        "DONAKONDA",
        "ULAVAPADU",
        "ARDHAVEEDU",
        "KANIGIRI",
        "BALLIKURAVA",
        "BESTHAVARIPETA",
        "SINGARAYAKONDA",
        "KORISAPADU",
        "MARTUR",
        "MARKAPUR",
        "CHIMAKURTHI",
        "ONGOLE",
        "TARLUPADU",
        "GUDLURU",
        "PAMURU",
        "CHINAGANJAM",
        "CHIRALA",
        "SANTHANUTALAPADU",
        "SANTHAMAGULURU",
        "ZARUGUMALLI",
        "VETAPALEM",
        "KANDUKURU",
        "VELIGANDLA",
        "PUTTAPARTHI",
        "RENIGUNTA",
        "CHANDRAGIRI",
        "TIRUPATHI( U )",
        "VADAMALAPETA",
        "SRI KALAHASTI",
        "YERPEDU",
        "TIRUPATHI RURAL",
        "PUTTUR",
        "ETCHERLA",
        "G.SIGADAM",
        "LAVERU",
        "RAJAM",
        "RANASTALAM",
        "AMUDALAVALASA",
        "PONDURU",
        "GARA",
        "POLAKI",
        "NARASANNAPETA",
        "KASIMKOTA",
        "RAMBILI",
        "PADMANABHAM",
        "YELAMANCHILI",
        "S RAYAVARAM",
        "ANANDAPAURAM",
        "MUNAGAPAKA",
        "BHOGAPURAM",
        "DENKADA",
        "CHEEPURUPALI",
        "JAMI",
        "PUSAPATIREGA",
        "NELLIMARLA",
        "S.KOTA",
        "VEPADA",
        "LAKKAVARAPUKOTA",
        "S.KOTA.",
        "KOTHAVALASA",
        "VIZIAYANAGRAM",
        "ANAKAPALLE",
        "BHEEMUNIPATNAM",
        "SABBAVARAM",
        "ANANDAPURAM",
        "PARAVADA",
        "PENDURTHI",
        "RAMBILLI",
        "BONDAPALLE",
        "GURLA",
        "GARIVIDI",
        "GAJAPATHINAGARAM",
        "CHEEPURUPALLE",
        "UNGUTURU",
        "AKIVIDU (PART)",
        "ACHANTA",
        "BHIMADOLE",
        "PALACOLE",
        "GANAPAVARAM",
        "PERAVALI",
        "DENDULURU",
        "PENTAPADU",
        "PENUMANTRA",
        "PEDAVEGI",
        "JANGAREDDYGUDEM (PART)",
        "PEDAPADU",
        "VEERAVASARAM",
        "BHIMAVARAM(PART)",
        "ATTILI",
        "KOVVUR(PART)",
        "T P GUDEM",
        "NIDADAVOLE(PART)",
        "CHAGALLU(PART)",
        "ELURU",
        "UNDI(PART)",
        "PENUGONDA",
        "UNDRAJAVARAM",
        "NARASAPUR",
        "DWARAKATIRUMALA",
        "TANUKU",
        "IRAGAVARAM",
        "PALACODERU",
        "PODURU",
        "MOGALTHUR (PART)",
        "KAMAVARAPUKOTA",
        "KALLA(PART)",
        "T.NARASAPURAM",
    ]

    states = {"andhra pradesh": ap, "karnataka": None}

    if state in states:
        print("State available")
        return states[state]
    else:
        print("State Not Found")
        return False
