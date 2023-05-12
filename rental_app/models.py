from django.db import models
from datetime import timedelta
from django.utils import timezone


currentDatetime=timezone.now()
# Create your models here.
class users(models.Model):
    first_name=models.CharField(max_length=30,default=None)
    last_name=models.CharField(max_length=30)
    email_id=models.CharField(max_length=100)
    mobile_no=models.CharField(max_length=12)
    Bio=models.CharField(max_length=200, default="Never Loose Hope !!")
    user_profile_pic=models.ImageField(upload_to='')
    user_password=models.CharField(max_length=100, default="")
    created_at=models.DateTimeField(default=currentDatetime, null=True)
    no_of_requests_to_view_contact_no=models.IntegerField(default=0)
    no_of_free_ad_posted_count=models.IntegerField(default=0)
    no_of_paid_ad_posted_count=models.IntegerField(default=0)
    user_ad_posting_enrolled=models.BooleanField(default=False)
    user_ad_posting_enrolled_limit=models.IntegerField(default=0)
    user_ad_posting_enrolled_limit_expired_date=models.DateField(null=True)
    user_view_contact_enrolled=models.BooleanField(default=False)
    user_state_by_geo_loc=models.CharField(max_length=100,default="null")
    role=models.CharField(max_length=50,default='user')
    user_added_by_admin=models.CharField(max_length=100,default=None,null=True)

    
    def __str__(self): 
        return self.first_name
    


class send_text_to_owner(models.Model):
    request_user_id=models.IntegerField(default=0)
    receiver_user_id=models.ForeignKey(users,default=0,on_delete=models.CASCADE)
    request_user_time=models.DateTimeField(default=currentDatetime)
    request_property_id=models.IntegerField(default=0)
    request_user_mobile_no=models.CharField(max_length=12,default=0)
    request_user_email_id=models.CharField(max_length=200)

    def __str__(self):
        return self.request_user_email_id

class user_otp(models.Model):
    email_id=models.CharField(max_length=100,default=None)
    otp=models.IntegerField()

    def __str__(self):
        return self.email_id
    
# class user_id_for_product(models.Model):
#     user_id=models.CharField(max_length=100)

#     def __str__(self):
#         return self.user_id

class property_details(models.Model):
    user_emailid_via_login_token=models.CharField(max_length=100, default="")
    property_name=models.CharField(max_length=200,default=None)
    property_type=models.CharField(max_length=200)

    property_city=models.CharField(max_length=30,default=None)
    property_state=models.CharField(max_length=30,default=None)
    property_pincode=models.CharField(max_length=6,default=None)
    # property_located_in_city=models.CharField(max_length=30,default=None)
    property_distict=models.CharField(max_length=100,default="null")

    property_floor=models.IntegerField(default=0)
    # property_conditions=models.CharField(max_length=300,default=None)
    monthly_rent=models.IntegerField()
    # monthly_maintance=models.IntegerField()
    # required_doc=models.CharField(max_length=200)
    # advance_amount=models.IntegerField()
    # contact_no=models.IntegerField()
    house_area=models.CharField(max_length=100)
    furnished_or_semi=models.CharField(max_length=100,default="null",null=True)
    rooms=models.CharField(max_length=100,default="null",null=True)
    

    appliance_TV=models.BooleanField(default=False)
    appliance_Fridge=models.BooleanField(default=False)
    appliance_sofa=models.BooleanField(default=False)
    appliance_bed=models.BooleanField(default=False)
    appliance_dresser=models.BooleanField(default=False)
    appliance_AC=models.BooleanField(default=False)
    appliance_washing_machine=models.BooleanField(default=False)
    appliance_water_heaters=models.BooleanField(default=False)
    appliance_fans=models.BooleanField(default=False)
    appliance_water_purifier=models.BooleanField(default=False)
    appliance_tubelights=models.BooleanField(default=False)
    appliance_Inventers=models.BooleanField(default=False)


    # tenure_period=models.CharField(max_length=100,default=None)
    parking=models.CharField(max_length=20,default=None)
    # variable_or_fixed=models.CharField(max_length=20,default=None)
    created_at=models.DateTimeField(default=timezone.now(), null=True)
    no_of_likes=models.IntegerField(default=0)
    post_expire_date=models.DateTimeField(default=currentDatetime+timedelta(days=30))

    ad_posted_by=models.CharField(max_length=50,default='user')

    def __str__(self):
        return self.user_emailid_via_login_token
    

class user_id_for_product(models.Model):
    user_id=models.CharField(max_length=100)
    product=models.ForeignKey(property_details,on_delete=models.CASCADE,null=True)
    

    def __str__(self):
        return self.user_id
    
class images(models.Model):
    property_name=models.CharField(default="temp",max_length=10000000)
    user_email_id=models.CharField(max_length=30)
    image=models.ImageField(upload_to='')
    Is_image_safe=models.BooleanField(default=False)

    def __str__(self):
        return self.user_email_id
    

class unsafe_images(models.Model):
    image_id=models.ForeignKey(images,on_delete=models.CASCADE)   
    unsafe_img=models.BooleanField(default=True)
    created_at=models.DateTimeField(default=timezone.now()) 
    unsafe_reason=models.TextField(max_length=500,default="none")
    


class user_liked(models.Model):
    user_id=models.IntegerField(default=0)
    user_email=models.CharField(max_length=50,default="")
    liked_property_ids=models.IntegerField()

    def __str__(self):
        return self.user_email
    

class users_credentials_IPs(models.Model):
    user_id=models.ForeignKey(users,on_delete=models.CASCADE,default=0)
    user_email_id=models.CharField(max_length=50)
    user_ip_address=models.CharField(max_length=100,default=None, null=True)
    user_token=models.CharField(max_length=100)
    createdAt=models.DateTimeField(default=currentDatetime)
    user_state_by_geo_loc=models.CharField(max_length=100,default="null")

    def __str__(self):
        return self.user_email_id
    

class issues_raised(models.Model):
    subject=models.CharField(max_length=100)
    breif_details=models.CharField(max_length=500)
    reference_img=models.ImageField(upload_to='')

    def __str__(self):
        return self.subject
    
class Deleted_post_details(models.Model):
    post_id=models.CharField(max_length=100)
    post_user_email=models.CharField(max_length=100)
    posted_user_contact_details=models.CharField(max_length=30)
    post_address=models.CharField(max_length=200)
    deleted_at=models.DateTimeField(default=currentDatetime, null=True)



    def __str__(self):
        return self.post_user_email
    
class user_free_limits(models.Model):
    user_id=models.ForeignKey(users,on_delete=models.CASCADE)
    product_id=models.ForeignKey(property_details,on_delete=models.CASCADE)
    unlocked_contact_no_for_product_id_is=models.IntegerField(default=0)
    unlocked_at=models.DateTimeField(default=currentDatetime, null=True)


class ad_posted_logs(models.Model):
    user_details=models.ForeignKey(users,on_delete=models.CASCADE)
    user_posted_ad_property_id=models.IntegerField(default=0)
    user_posted_date=models.DateField(default=currentDatetime,null=True)

    def __str__(self):
        return self.user_details.email_id
    

class razorpay_payment_order_details(models.Model):
    user_detail=models.ForeignKey(users,on_delete=models.CASCADE)
    razorpay_order_id=models.CharField(max_length=500)
    plan_amount=models.IntegerField()
    plan_id=models.CharField(max_length=100)
    created_At=models.DateTimeField(default=currentDatetime,null=True)


    def __str__(self):
        return self.user_detail.email_id


class ad_posting_payments_details(models.Model):
    user_detail=models.ForeignKey(users,on_delete=models.CASCADE)
    razorpay_payment_id=models.CharField(max_length=500)
    razorpay_order_id=models.CharField(max_length=500)
    plan_amount=models.IntegerField()
    plan_id=models.CharField(max_length=100)
    created_At=models.DateTimeField(default=currentDatetime,null=True,)

    def __str__(self):
        return self.user_detail.email_id
    

# special data table to get as possible user personal info

class user_collections(models.Model):
    user_visited_ip_address=models.CharField(max_length=100,default=None, null=True)
    visted_count=models.IntegerField(max_length=1000,default=0)
    visited_product_pg=models.BooleanField(default=False)
    visited_profile_pg=models.BooleanField(default=False)
    visited_sell_pg=models.BooleanField(default=False)
    visited_plan_pg=models.BooleanField(default=False)
    visited_liked_pg=models.BooleanField(default=False)
    visited_help_and_support_pg=models.BooleanField(default=False)
    visited_update_property_pg=models.BooleanField(default=False)
    visted_time=models.DateTimeField(default=timezone.now())
    active_time=models.DateTimeField(default=timezone.now())
    user_state_by_geo_loc=models.CharField(max_length=100,default="null")


class failure_response(models.Model):
    failure_message=models.TextField(max_length=2000,default="None")
    failure_user_details=models.ForeignKey(users,default="None",on_delete=models.CASCADE)
    created_At=models.DateTimeField(default=currentDatetime,null=True,)
    other_responses=models.TextField(max_length=2000,default="none")


class super_Admin_users(models.Model):
    user_id=models.ForeignKey(users,on_delete=models.CASCADE)
    created_At=models.DateTimeField(default=currentDatetime,null=True)
    role=models.CharField(max_length=50,default=None)
    last_login_time=models.DateTimeField(default=currentDatetime,null=True)
    user_ip_address=models.CharField(max_length=100,default=None, null=True)
    user_location=models.CharField(max_length=100,default=None,null=True)

    def __str__(self):
        return self.user_id.email_id

    

    
# db=>
# ip + token

# cookie=>
# token
# logged_in 

# when_ever users come check for cookie token, if exist then collect user_ip +  token and match with database if data exist-true then.. user should logged-in 
# or else user should render to login page..
# and if sign-out then user-ip + token should deleted from db & browser cookie