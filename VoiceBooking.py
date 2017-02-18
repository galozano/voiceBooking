
from __future__ import print_function

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- Functions that control the skill's behavior ------------------
""" If we wanted to initialize the session to have some attributes we could add those here """
def get_welcome_response():

    session_attributes = {}
    card_title = "Welcome to VoiceBooking"
    speech_output = "Welcome to VoiceBooking. "

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "How can I help you"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():

    card_title = "Session Ended"
    speech_output = "Thank you for using VoiceBooking. " \
                    "Have a nice day! "

    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

"""Books an appointment at a time and date specified by the user"""
def bookAppointmentIntent(intent,session):

    card_title = intent['name']
    session_attributes = {}
    should_end_session = True
    reprompt_text = None

    print("bookAppointmentIntent - Date Requested:"  + intent["slots"]["Date"]["value"])
    print("bookAppointmentIntent - Time Requested:"  + intent["slots"]["Time"]["value"])

    speech_output = "Your appointment was succesfully booked at " + intent["slots"]["Time"]["value"] " on " + intent["slots"]["Date"]["value"]

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

"""Books an appointment at a time and date specified by the user"""
def askTimeIntent(intent,session):

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    reprompt_text = None

    print("getPricesIntent - Price Check")

    speech_output = "The barber shop is open today from 9 AM to 8PM"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

"""Called when the user launches the skill without specifying what they want"""
def on_launch(launch_request, session):

    print("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])

    # Dispatch to your skill's launch
    return get_welcome_response()

"""Called when the user specifies an intent for this skill"""
def on_intent(intent_request, session):

    print("on_intent requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    print("on_intent requestName=" + intent_name)

    # Dispatch to your skill's intent handlers
    if intent_name == "BookAppointmentIntent":
        return bookAppointmentIntent(intent, session)
    elif intent_name == "AskTimeIntent":
        return askTimeIntent(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

"""Called when the user ends the session."""
"""Is not called when the skill returns should_end_session=true"""
def on_session_ended(session_ended_request, session):

    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Main handler ------------------

""" Route the incoming request based on type (LaunchRequest, IntentRequest,
etc.) The JSON body of the request is provided in the event parameter. """
def lambda_handler(event, context):

    print("event.session.application.applicationId=" + event['session']['application']['applicationId'])

    #Verify if application is the right one
    #if (event['session']['application']['applicationId'] != "amzn1.ask.skill.48d59ff4-009c-45e4-a487-a236e0ff4e76"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']}, event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
