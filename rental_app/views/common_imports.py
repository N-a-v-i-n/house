from django.shortcuts import render,HttpResponseRedirect
from rental_app import templates
from rental_app.models import user_otp,users,property_details,images,user_liked,users_credentials_IPs,issues_raised,user_id_for_product,Deleted_post_details,user_free_limits,send_text_to_owner,razorpay_payment_order_details,ad_posting_payments_details,user_collections,unsafe_images,failure_response,super_Admin_users,ad_posted_logs

from django.shortcuts import HttpResponse
import random,datetime
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils import timezone
import re,math
import json
import secrets
import socket
from django.contrib.auth.tokens import default_token_generator
from rental_app.automate_sell import adding_rents_house
from rental_app.images_validations import images_validate
from .common_method import *
from django.http import HttpResponseBadRequest

from PIL import Image , ImageDraw,ImageFont
import os,sys
import random,datetime,base64
from django.utils import timezone
from django.shortcuts import HttpResponse
