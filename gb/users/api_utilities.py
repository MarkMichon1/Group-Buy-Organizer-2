from django.contrib.sessions.models import Session

def extract_user_from_session_key():
    try:
        session = Session.objects.get(pk='6bq0jv7zpkoly3ojbzswx0w83tpzpn2l')
        print(session.get_decoded())
    except:
        return False