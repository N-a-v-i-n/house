from .common_imports import *

def help_support(request):
    if request.method == 'POST':
        subject=request.POST.get('issues')
        brief=request.POST.get('breif_issue')
        reference_img=request.FILES.get('reference_image')
        new_data=issues_raised.objects.create(
            subject=subject,
            breif_details=brief,
            reference_img=reference_img
        )
        new_data.save()

        print(new_data)

    return render(request,'help_support.html')

