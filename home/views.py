from django.shortcuts import render

visitor_count = 0


# This is where the request for '/' comes in
def home(request):
    global visitor_count
    visitor_count += 1
    context = {"message": "Hello, you are visitor number {}".
        format(visitor_count)}
    return render(request, 'home.html', context)
