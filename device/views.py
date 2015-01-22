from django.shortcuts import render

from .models import Device

def device_home(request):
    devicess = Device.objects.filter(device__title__isnull=False).distinct().order_by('title')

    #Check various session values for user details and show appropriate info
    if request.session.get('no_title', False):
        messages.info(request, 'Please fill in your profile details by going to your account settings.')
        request.session['no_name'] = False

    if request.session.get('no_device', False):
        messages.warning(request, 'It seems you are having any device.')
        request.session['no_device'] = False

    ctx = {
            'devicess': devices,
        }
    return render_to_response('device/device_home.html', ctx, context_instance=RequestContext(request))
