import pyjokes

def get_joke():
    try:
        return pyjokes.get_joke()
    except:
        return "I don't know any jokes right now."