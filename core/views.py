from django.http import HttpResponse
from .models import Session, Role, User, Story


def index(request):
    s = Session(name="Planning Poker")
    r = Role(name="Admin")
    u = User(username="k-dog", password="password", session_id=s, role_id=r)
    t = Story(name="User Story - 1", story_points=10, session_id=s)

    s.save()
    r.save()
    u.save()
    t.save()

    message = u.username + "(" + r.name + ")" + " is in a session of " + s.name + ", and is looking at " + t.name

    return HttpResponse(message)
