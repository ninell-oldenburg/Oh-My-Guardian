# Oh My Guardian!
This is an example of an Alexa Amazon® Skill. It is able to search the Guardian Website for a keyword and to send the results via mail to the user. 

## Background

The project was created as a semester project for the course "Dialogue Systems" at the University of Potsdam, Germany. If you 
are interested in the planning and evaluation of the skill, text me. I wrote a project documentation which is (for now) 
available in German.

## Content

The JSON-file was created and is computable via the Alexa Developer Console. It includes all the intent and slot values, user 
utterances and Alexa prompts. To compute it, paste it in the "Edit JSON-file" section in your Alexa Developer Console.

The lambda-function is hosted by the Amazon Web Services. You can download the Zip-file and upload it to your personal lambda 
service, save it and paste the URL to the endpoint in the Alexa Developer Console. 

Everything has been created on line with the Alexa-Tutorial (see https://github.com/alexa for details). They also explain how 
to create such functions in order to get a working skill.

## Use

Invoce the skill in the Alexa-Simulator with "Oh my Guardian". Alexa will, once the skill started successfully, tell you 
what to do. You can also ask for help to get more information about the skill's functions. 

The skill is able to send you a mail via a private mail adress, hosted by the provider GMX, which is free and easy to handle.

## Expansions

Feel free to expand the skill's functions. Possible features I was thinking about are:

1. a datetime filter
2. a relevance filter
3. a filter for the user's interest
4. a feature to safe the user's mail adress
5. a feature to send a message via Telegram/WhatsApp
6. a feature to summarize the article's content
7. different search modes (see documentation of The Guardian API: https://open-platform.theguardian.com/documentation/

## Thanks

Thanks to the initiator, Prof. Dr. David Schlangen, who directed the course at the University of Potsdam.
