from django.contrib import admin
from .models import users,user_otp,property_details,images,user_liked,users_credentials_IPs,issues_raised,user_id_for_product,user_free_limits,send_text_to_owner,ad_posted_logs,ad_posting_payments_details,razorpay_payment_order_details,user_collections,unsafe_images,failure_response,super_Admin_users
from .models import Deleted_post_details
# Register your models here.
class AdminImages(admin.ModelAdmin):
    list_display=['user_email_id','image']

class Adminusers(admin.ModelAdmin):
    list_display=['email_id','mobile_no']

class Deleted_details(admin.ModelAdmin):
    list_display=['post_id','post_user_email','posted_user_contact_details']

class Proper_details(admin.ModelAdmin):
    list_display=[
        "user_emailid_via_login_token",
        "property_city",
        "monthly_rent",
        "created_at",
        "no_of_likes",
        "post_expire_date",
    ]

class user_unloced(admin.ModelAdmin):
    list_display=[
        'user_id',
        'unlocked_contact_no_for_product_id_is',
        'unlocked_at',
    ]
class send_text_to_owner_on_every_request(admin.ModelAdmin):
    list_display=[
        'request_user_id',
        'receiver_user_id',
        'request_user_time',
        'request_user_email_id',
        'request_user_mobile_no',
        'request_property_id',
    ]

class ad_posting_payment(admin.ModelAdmin):
    list_display=[
        'plan_amount',
        'plan_id',
        'created_At'
    ]

class razorpay_order_details(admin.ModelAdmin):
    list_display=[
        'plan_amount',
        'plan_id',
        'created_At'
    ]

class user_info(admin.ModelAdmin):
    list_display=[
        'user_visited_ip_address',
        'visted_time'
    ]

admin.site.register(users,Adminusers)
admin.site.register(user_otp)
admin.site.register(property_details,Proper_details)
admin.site.register(images,AdminImages)
admin.site.register(user_liked)
admin.site.register(users_credentials_IPs)
admin.site.register(issues_raised)
admin.site.register(user_id_for_product)
admin.site.register(Deleted_post_details,Deleted_details)
admin.site.register(user_free_limits,user_unloced)
admin.site.register(send_text_to_owner,send_text_to_owner_on_every_request)
admin.site.register(ad_posted_logs)
admin.site.register(ad_posting_payments_details,ad_posting_payment)
admin.site.register(razorpay_payment_order_details,razorpay_order_details)
admin.site.register(user_collections,user_info)
admin.site.register(unsafe_images)
admin.site.register(failure_response)
admin.site.register(super_Admin_users)

