from .common_imports import *
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)
)
plan_amount = 100


def plans(request):
    cookies_token = request.COOKIES.get(
        "otp_token"
    )  # checking for the cookies if the user is already logged in or not
    cookies_email_id = request.COOKIES.get("email_id")
    if cookies_token:
        print("browser_token : ", cookies_token)
        validate = token_validations(cookies_token)
        print("is token_match : ", validate)

        if validate:
            is_user_logged_in = True
            limit_over_pop_up = False

            fetching_user_id_from_token = users_credentials_IPs.objects.get(
                user_token=cookies_token
            )
            current_user_details = fetching_user_id_from_token.user_id
            print("current_user_details : ")
            print("user_id : ", current_user_details.id)
            print("user_email : ", current_user_details.email_id)

            print("Yes, User Logged_in")

            selected_plan_id = request.POST.get("plan_selected")

            if selected_plan_id:
                # if selected_plan_id:

                get_value = plans_validations(selected_plan_id)
                if get_value:
                    plan_amount = get_value
                    data = {}
                    data["Verified"]: True

                    currency = "INR"

                    amount = plan_amount * 100  # Rs. 200

                    # Create a Razorpay Order
                    razorpay_order = razorpay_client.order.create(
                        dict(amount=amount, currency=currency, payment_capture="0")
                    )

                    # order id of newly created order.
                    razorpay_order_id = razorpay_order["id"]
                    callback_url = "/paymenthandler/"

                    # backup order placing
                    new_order = razorpay_payment_order_details.objects.create(
                        user_detail=current_user_details,
                        razorpay_order_id=razorpay_order_id,
                        plan_amount=amount / 100,
                        plan_id=selected_plan_id,
                        created_At=timezone.now(),
                    )
                    new_order.save()

                    # we need to pass these details to frontend.
                    context = {}
                    context["razorpay_order_id"] = razorpay_order_id
                    context["razorpay_merchant_key"] = settings.RAZOR_KEY_ID
                    context["razorpay_amount"] = amount
                    context["currency"] = currency
                    context["callback_url"] = callback_url
                    context["Verified"] = True

                    return render(request, "plans.html", context=context)

                else:
                    return HttpResponseRedirect("/pageNotFound/")

            else:
                return render(request, "plans.html")

        else:
            # if not Logined in
            return HttpResponseRedirect("/")

    else:
        # if cookie not available in browser
        return HttpResponseRedirect("/")

    # currency = "INR"
    # amount = 20000 # Rs. 200

    # # Create a Razorpay Order
    # razorpay_order = razorpay_client.order.create(dict(amount=amount,
    #                                                 currency=currency,
    #                                                 payment_capture='0'))

    # # order id of newly created order.
    # razorpay_order_id = razorpay_order['id']
    # callback_url = '/paymenthandler/'

    # # we need to pass these details to frontend.
    # context = {}
    # context['razorpay_order_id'] = razorpay_order_id
    # context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    # context['razorpay_amount'] = amount
    # context['currency'] = currency
    # context['callback_url'] = callback_url

    # return render(request, 'plans.html', context=context)


# ----------------------------------------------------------------


def plans_validations(id):
    ad_posting_plan_ids = {
        "plan_500_selected": 500,
        "plan_1000_selected": 1000,
        "plan_1500_selected": 1500,
        "plan_2000_selected": 2000,
    }
    try:
        check_is_exist = ad_posting_plan_ids[id]

    except:
        return False

    if check_is_exist:
        plan_value_match = True

        plan_value = check_is_exist

        print("plan_value_match", plan_value_match)

        return plan_value


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    print("callback entered")
    print("amount is ", plan_amount)
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get("razorpay_payment_id", "")
            razorpay_order_id = request.POST.get("razorpay_order_id", "")
            signature = request.POST.get("razorpay_signature", "")
            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }

            # Fetching order date from razorpay_payment_order_details table
            get_data = razorpay_payment_order_details.objects.get(
                razorpay_order_id=razorpay_order_id
            )

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                amount = get_data.plan_amount * 100  # Rs. 200
                try:
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    print("amount is ", amount)

                    # render success page on successful caputre of payment
                    print("on try block sussee")

                    # store data of payment success
                    new_data = ad_posting_payments_details.objects.create(
                        user_detail=get_data.user_detail,
                        razorpay_payment_id=payment_id,
                        razorpay_order_id=razorpay_order_id,
                        plan_amount=amount / 100,
                        plan_id=get_data.plan_id,
                        created_At=timezone.now(),
                    )

                    new_data.save()

                    # updateing user enrolled + assigning post adding limits
                    user_data = users.objects.get(id=get_data.user_detail.id)
                    user_data.user_ad_posting_enrolled = True
                    user_data.no_of_paid_ad_posted_count = 0
                    user_data.user_ad_posting_enrolled_limit = amount / 10000
                    user_data.user_ad_posting_enrolled_limit_expired_date = (
                        timezone.now() + datetime.timedelta(days=180)
                    )
                    user_data.save()

                    return render(request, "success_page.html")
                except:
                    # if there is an error while capturing payment.
                    print("amount is ", amount)
                    return HttpResponse("failed due to Capturing block")
            else:
                # if signature verification fails.
                print("amount is ", amount)
                return HttpResponse("failed due to signature block")
        except:
            # if we don't find the required parameters in POST data
            return HttpResponse("required parameters")
    else:
        # if other than POST request is made.
        return HttpResponse("failed due to other block")
