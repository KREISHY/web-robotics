from django.shortcuts import render

def admin_main(request):
    return render(request, 'admin_panel/index.html', {'user': request.user})