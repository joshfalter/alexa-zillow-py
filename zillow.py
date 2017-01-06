import logging
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults
from flask import Flask
from flask_ask import Ask, request, session, question, statement

#address='9038 Maple Grove Drive'
#zipcode='29485'
zillow_data=ZillowWrapper('YOUR ZILLOW WEBSERVICES ID')



app = Flask(__name__)
ask = Ask(app, '/')
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

ADDRESS_KEY= "ADDRESS"
ZIP_KEY="ZIPCODE"
DEEP_SEARCH_RESPONSE=object()
RESULT=object()

@ask.launch
def launch():
    speech_text = 'Welcome to Zillow. What address would you like to know more about?'
    reprompt_speech_text = 'What address would you like to know more about?'
    return question(speech_text).reprompt(reprompt_speech_text).simple_card('Launch', speech_text)  


@ask.intent('LookUpAddressIntent', mapping={'location': 'Address'})
def change_address(location):
    address=location
    session.attributes[ADDRESS_KEY] = address
    speech_text = 'Okay. What\'s the zipcode for that address?'
    return question(speech_text).reprompt(speech_text).simple_card('Address changed to:', address)


@ask.intent('ZipcodeIntent', mapping={'zip': 'Zipcode'})
def change_zip(zip):
    zipcode=zip
    session.attributes[ZIP_KEY] = zipcode
    speech_text = 'Great, now what would you like to know? Say help for a list of commands.'
    return question(speech_text).reprompt(speech_text).simple_card('Zip code changed to:', zipcode)
    

def search_results():
    address = session.attributes.get(ADDRESS_KEY)
    zipcode = session.attributes.get(ZIP_KEY)
    #deep_search_response=zillow_data.get_deep_search_results(address, zipcode)
    deep_search_response=zillow_data.get_deep_search_results(address, zipcode)
    result=GetDeepSearchResults(deep_search_response)
    return result
    #search with zillow api
    

#In case they want to stop
@ask.intent('NoIntent')
def no():
    speech_text = 'Goodbye.'
    return statement(speech_text).simple_card('Goodbye.', speech_text)
    
@ask.intent('ValueofHomeIntent')
def value_of_home():
    speech_text = 'The z-estimate value of your house is $' + search_results().zestimate_amount +' What else would you like to know?'
    return question(speech_text).simple_card('Zestimate of Home', speech_text)

@ask.intent('LatitudeIntent')
def latitude_of_home():
    speech_text = 'The latitude of the house is ' + search_results().latitude + ' degrees. What else would you like to know?'
    return question(speech_text).simple_card('Zestimate of Home', speech_text)


@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'I can tell you the following about an address. Latitude, longitude, coordinates, tax value, the year it was built, property size, home size, number of bedrooms and bathrooms, the last year it was sold, the date it was sold, the price it sold for, the z estimate, and the valuation range.'
    return question(speech_text).reprompt(speech_text).simple_card('Help: Commands ', speech_text)


@ask.session_ended
def session_ended():
    return "", 200


if __name__ == '__main__':
    app.run(debug=True)


            


  #  deep_search_response=zillow_data.get_deep_search_results(address, zipcode)
  #  result=GetDeepSearchResults(deep_search_response)
  #  print(address) #This is just for debugging what Alexa hears
  #  speech_text = 'The address has been changed to ' + address + '.' + 'The value of this home is $' +result.zestimate_amount
  #  return statement(speech_text).simple_card('Change Address', speech_text)
