from .common_imports import *

def signup(request):
    if request.method=='POST':
        print()
        print()
        print()
        print()
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email_id=request.POST['email_id']
        mobile_no=request.POST['mobile_no']
        Bio=request.POST['Bio']
        password=request.POST.get('user_password')
        new_data=users(
            first_name=first_name,
            last_name=last_name,
            email_id=email_id,
            mobile_no=mobile_no,
            user_password=password,
            Bio=Bio,
            )
        new_data.save()
        print()
        print()
        print("signup success for : ",email_id)
        # print("User data : ",users.objects.all())
        return render(request,'signup.html')
    return render(request,'signup.html')
