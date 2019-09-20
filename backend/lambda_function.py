# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.

# Additional Editing:
# Ninell Oldenburg
# University of Potsdam
# 09/12/2019
# Project: Oh my Guardian Skill

import logging

from ask_sdk_core.skill_builder import SkillBuilder

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.handler_input import HandlerInput

from mail.make_mailfile import Write
from mail.send_mail import Mail
from mail.api_request import API
from mail.cut_mail import Cut

import json

from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to the Guardian Skill. I help you finding articles from the Guardian website. Tell me what you are looking for. Say for example: 'What is there about Johnson?"
        
        
        reprompt_text = "If you say 'help' I can tell you all my functions."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )

class KeywordSearchIntentHandler(AbstractRequestHandler):
    """Handler for the search Keyword Search"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("KeywordSearchIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        current_intent = handler_input.request_envelope.request.intent
        confirmed = str(current_intent.confirmation_status)
        # content as default-mode, possible: tag, section, edition
        mode = "content"
        keyword = ""
        for slot_name, current_slot in current_intent.slots.items():
            #if slot_name == 'mode':
            #   mode = current_slot.resolutions.resolutions_per_authority[0].values[0].value.name
            if slot_name == 'keyword':
                keyword = current_slot.value
    
        # make API-request via API module
        request = API(keyword,mode)
        json_response = request.read_properly(request.get_data())
        json_file = json.loads(json_response)
        # write proper mail file and save in global variable
        mail = Write(json_response)
        global mail_text
        mail_text = mail.make_mail()
        
        # count number of articles and sections for output
        article_counter = 0
        section_counter = 0
        for name,content in json_file.items():
            if not (name == 'mode' or name == 'keyword'):
                section_counter += 1
                article_counter += len(content)

        # define output sentences according to confirmation status and outcome of API-request
        if (confirmed == "IntentConfirmationStatus.CONFIRMED"):
            if article_counter == 0:
                speak_output = "Sorry, I couldn't find anything about {}. Do you want to search for another keyword or say goodbye?".format(keyword)
            else:
                speak_output = "For {} I found {} entries in {} sections. Do you want me to send it via mail to you?".format(keyword,article_counter,section_counter)
        else:
            speak_output = "Let's have another try. What are you looking for?"

        handler_input.response_builder.speak(speak_output).set_should_end_session(False)
        return handler_input.response_builder.response

class SendMailIntentHandler(AbstractRequestHandler):
    """Handler for Sending Mail Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SendMailIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        current_intent = handler_input.request_envelope.request.intent
        confirmed = str(current_intent.confirmation_status)
        mail = ""
        client = ""
        country = ""
        for slot_name, current_slot in current_intent.slots.items():
            if slot_name == 'ending':
                client = current_slot.value
            if slot_name == 'country':
                country = current_slot.resolutions.resolutions_per_authority[0].values[0].value.name
            if slot_name == 'mail':
                mail = current_slot.value
        
        # parser for special signs
        cut_instance = Cut()
        mail = cut_instance.cut_mail(mail.replace(' ','+'))
        client = cut_instance.cut_mail(client.replace(' ','+'))

        mailadress = "{}@{}.{}".format(mail,client,country)

        # send mail according to confirmation status of mail adress
        if (confirmed == "IntentConfirmationStatus.CONFIRMED"):
            sending = Mail(mail_text,mailadress)
            sending.send_mail()
            
            speak_output = "I'll send the mail to {}. Is there another keyword you want me to look up or should we say good bye?".format(mailadress)
        else:
            speak_output = "Alright. What is the correct adress?"
        
        handler_input.response_builder.speak(speak_output).set_should_end_session(False)
        return handler_input.response_builder.response

class GoodbyeIntentHandler(AbstractRequestHandler):
    """Handler for Goodbye Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GoodbyeIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"
        
        handler_input.response_builder.speak(speak_output).set_should_end_session(True)
        return handler_input.response_builder.response

class YesIntentHandler(AbstractRequestHandler):
    """Handler for Yes Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("YesIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Alright. So I need your mail adress. Say for example 'my mail is john point doe at mail dot com'."
        
        handler_input.response_builder.speak(speak_output).set_should_end_session(False)
        return handler_input.response_builder.response


class NoIntentHandler(AbstractRequestHandler):
    """Handler for No Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("NoIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Alright. Do you want me to search for another keyword then or say good bye?"
        
        handler_input.response_builder.speak(speak_output).set_should_end_session(False)
        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can search the Guardian Website for articles. If you tell me your keyword, I'll ask the Website an give you the number of articles and number of different sections they're in. Afterwards I can send the findings via mail to you. Please speak in complete sentences and do not spell your mailadress. If there is a point in the head of the adress say 'point'. For the dot dividing mailprovider and countrycode say dot."

        handler_input.response_builder.speak(speak_output).set_should_end_session(False)
        return handler_input.response_builder.response

class RepeatIntentHandler(AbstractRequestHandler):
    """Handler for repeating"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("AMAZON.RepeatIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        speak_output = "Unfortunately the developer wasn't able to implement this correctly. But you can still search for a keyword or say goodbye. Or call help."
        
        handler_input.response_builder.speak(speak_output).set_should_end_session(False)
        return handler_input.response_builder.response

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        handler_input.response_builder.speak(speak_output).set_should_end_session(True)
        return handler_input.response_builder.response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        speak_output = "Goodbye!"
        
        handler_input.response_builder.speak(speak_output).set_should_end_session(True)
        return handler_input.response_builder.response


class FallBackIntentHanlder(AbstractRequestHandler):
    """Handler for Fallback"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "I cannot help you with that. You can tell me what you are looking for or say goodbye."
        
        handler_input.response_builder.speak(speak_output).set_should_end_session(False)
        return handler_input.response_builder.response


""" class IntentReflectorHandler(AbstractRequestHandler):
    # Debugger
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        handler_input.response_builder.speak(speak_output).set_should_end_session(True)
        return handler_input.response_builder.response """


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry I had trouble doing what you asked. Please try again saying what you wanted to say in a proper sentence."
        
        reprompt_text = "Ok still no success. Keyword or goodbye?"

        handler_input.response_builder.speak(speak_output).ask(reprompt_text).set_should_end_session(False)
        return handler_input.response_builder.response

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(KeywordSearchIntentHandler())
sb.add_request_handler(FallBackIntentHanlder())
sb.add_request_handler(RepeatIntentHandler())
sb.add_request_handler(SendMailIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(GoodbyeIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
# sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
