
import requests
import json
import flickrapi
import random
from random import randint
import os
import tweepy
from mastodon import Mastodon
 

def get_keys():
    cred = {}
    with open("/home/pi/bots/imagist/keys") as f:
        lines = f.readlines()
    for line in lines:
        key,value = line.split("\t")
        cred[key] = value.replace("\n","")

    return cred

def get_flickr_image():
    

    api_key = cred['flickr_key']
    api_secret = cred['flickr_secret']

    flickr = flickrapi.FlickrAPI(api_key, api_secret,format="parsed-json")
    photos = flickr.interestingness.getList(license='4,5,9,10',per_page='40')
    photo = random.choice(photos['photos']['photo'])
    fullsize = flickr.photos.getSizes(photo_id=photo['id'])['sizes']['size'][-1]['source']
    return fullsize

def get_description():
    img = get_flickr_image()
    image = "{'url' : '" + img + "'}"
    headers = {
        'Host' : 'eastus.api.cognitive.microsoft.com',
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key' : cred['azure_key']
    }

    r = requests.post('https://eastus.api.cognitive.microsoft.com/vision/v1.0/describe?maxCandidates=5', data = image, headers = headers)

    d = json.loads(str(r.content,'utf-8'))
    if 'description' in d:
        if (len(d['description']['captions']) > 0):
            return d['description']['captions'][0]['text'].replace("a close up of ","")
        else:
            return get_description()
    else:
        return get_description()
    
def format_wheelbarrow(text):
    words = text.split(" ")
    poem = ''
    for i in range(len(words)):
        if (i in [0,1,4,5,8,9,12,13,16,17]):
            poem += words[i] + " "
        elif (i in [2,6,10,14,18]):
            poem += words[i] + "\n"
        elif (i in [3,7,11,15,19]):
            poem += words[i] + "\n\n"
            
    return poem

def format_random_linebreaks(text):
    poem = ''
    for word in text.split(" "):
        poem += word + " " + random.choice(["\n","","","","","","\n\n"])
    return poem

def format_columb(text):
    # found this while looking for something else and I liked the result 
    # https://stackoverflow.com/a/1624988
    width = random.choice([5,6,7,8,9])
    poem = ''
    lines = [ text[i:i+width] for i in range(0, len(text), width) ]
    for line in lines:
        poem += line + "\n"
    return poem

def format_icebox(text):
    poem = ""
    stanza_goals = []
    stanzas = ['','','']
    
    words = text.split(" ")
    stanza,extra = divmod(len(words), 3)
    
    if (extra is 2):
        cut_one = stanza + 1
        cut_two = cut_one + stanza
    elif (extra is 1):
        cut_one = stanza
        cut_two = cut_one + stanza + 1
    else:
        cut_one = stanza
        cut_two = cut_one + stanza
        
    for w in range(len(words)):
        if (w <= cut_one):
            stanzas[0] += words[w] + " "
        elif (cut_one < w <= cut_two):
            stanzas[1] += words[w] + " "
        else: 
            stanzas[2] += words[w] + " "

    for s in stanzas:
        swords = s.split(" ")
        line,extra = divmod(len(swords),4)
        line_lengths = [0,0,0,0]
        for i in range(4):
            line_lengths[i] = line
        for e in range(extra):
            line_lengths[randint(0,3)] += 1
        cc = 0 
        cuts = []
        for ll in line_lengths:
            cc += ll
            cuts.append(cc)       
        lines = [[],[],[],[]]
        lines[0] = swords[0:cuts[0]]
        lines[1] = swords[cuts[0]:cuts[1]]
        lines[2] = swords[cuts[1]:cuts[2]]
        lines[3] = swords[cuts[2]:cuts[3]]

        for l in lines:
            poem += " ".join(l)
            poem += "\n"
        poem += "\n"
    return str(poem)

prepositions = ["above","across from","up against","alongside","behind","below","beneath",
                "beside","beyond","by","in","inside","near","off","on top of","opposite",
                "outside","over","just past","because of","towards","under",
                "underneath","up on top of","upon","with",
                "ahead of","because of","close to",
                "inside of","instead of","just to the left of","next to","for the sake of",
                "in front of","on top of"]

# get some credentials
cred = get_keys()

# compose the text
text = get_description() + " " + random.choice(["like",random.choice(prepositions)]) + " " + get_description()
 
# format the poem
poem = random.choice([
    format_random_linebreaks(text),
    format_icebox(text),
    format_icebox(text),
    format_icebox(text),
    format_wheelbarrow(text),
    format_columb(text)])

# send it to Mastodon

mastodon = Mastodon(
    #access_token = 'autoimagist_usercred.secret',
    client_id = '/home/pi/bots/imagist/autoimagist_clientcred.secret',
    api_base_url = 'https://botsin.space'
)

mastodon.log_in(
    cred['email'],
    cred['pw'],
    to_file = '/home/pi/bots/imagist/autoimagist_usercred.secret'
)

mastodon.toot(poem)

# send it to Twitter
# first authorize
twauth = tweepy.OAuthHandler(cred['twitter_consumer_key'],cred['twitter_consumer_secret'])
twauth.set_access_token(cred['twitter_access_key'],cred['twitter_access_secret'])
twapi = tweepy.API(twauth)

twapi.update_status(status=poem)



