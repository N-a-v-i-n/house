from .models import property_details,images
import random
def adding_rents_house():
    list_of_amount=[8723,8281,1723,2676,7362,5273,8723,18789,8638,12493,2372,9249,3234]
    list_of_images=['1.jpeg',
                    '2.jpeg',
                    '6.jpeg',
                    '3.jpeg',
                    '4.jpeg',
                    '5.jpeg',
                    '7.jpeg',
                    '8.jpeg',
                    '9.jpeg',
                    '10.jpeg',
                    '11.jpeg',
                    ]
    list_of_city=[
        "parvathipuram",
        "srikakulam",
        "Paderu",
        "Visakhapatnam",
        "Anakapalli",
        "Kakinada",
        "Amalapuram",
        "Rajamahendrava,ra"
        "Bheemavaram",
        "Eluru",
        "Machilipatnam",
        "Vijayawada",
        "Guntur",
        "Bapatla",
        "Narsaraopeta",
        "Ongole",
        "Nellore",
        "Kurnool",
        "Nandyal",
        "Ananthapuram",
        "Puttaparthy",
        "Kadapa",
        "Rayachoty",
        "Chittoor",
        "Tirupati",
        "Vizianagaram",
    ]
    list_of_states=[
        "andhra pradesh",
        "tamil nadu",
        "goa",
        "jammu & kashmir",
        "himachal pradesh",
        "karnataka",
        "bihar",
        "gujarat"
    ]
    list_emails=[
        'navintamilan31@gmail.com',
        'gnanen.007@gmail.com',
        'navintamil31@gmail.com',
        'scn.libra8@gmail.com'
    ]
    list_rooms=[
        '1room',
        '1rk',
        '1bhk',
        '2bhk',
        '3bhk'
    ]
    for x in range(10):

        temp=property_details.objects.create(
            # user_emailid_via_login_token="Infinate.alien@007.com",        
            user_emailid_via_login_token=random.choice(list_emails),        
            property_name="scn",
            property_type="Apartment",
            property_city=(random.choice(list_of_city)).lower(),
            property_state=random.choice(list_of_states),
            property_pincode="010101",
            property_floor="1202",
            monthly_rent=random.choice(list_of_amount),
            house_area="20000 Sqft",
            furnished_or_semi="Kuch nhi h",
            parking="Since, Property is in middle of sea, so parking on ur own risk",
            rooms=random.choice(list_rooms),
            




        )
        temp.save()
        temp2=images.objects.create(
            property_name=temp.id,
            user_email_id="Infinate.alien@007.com",
            image=random.choice(list_of_images),
        )
        temp2.save()
    
