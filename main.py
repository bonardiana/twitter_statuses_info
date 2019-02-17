import urllib.request
import urllib.parse
import urllib.error
import twurl
import json
import ssl


def _input():
    while True:
        print('')
        acct = input('Enter Twitter Account: ')
        if (len(acct) > 1):
            break
    return acct


def js_read(acct):
    TWITTER_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '2000'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)
    headers = dict(connection.getheaders())
    return js


def info_print(js):
    language_dct = dict()
    hashtag_dct = dict()
    loc_info = ""
    posts_info = " has " + \
        str(js[0]['user']['statuses_count']) + " posts"

    if 'location' in js[0]['user']:
        loc_info = " from " + js[0]['user']['location']

    print("User " + js[0]['user']
          ['screen_name'] + loc_info + posts_info)

    print("")
    print("Here " + str(len(js))+" of them are")
    print("")

    for el in js:
        try:
            if el['lang'] not in language_dct:
                language_dct[el['lang']] = 0
            language_dct[el['lang']] += 1

            if el["entities"]["hashtags"]:
                for hashtags in el["entities"]["hashtags"]:
                    if hashtags['text'] not in hashtag_dct:
                        hashtag_dct[hashtags['text']] = 0
                    hashtag_dct[hashtags['text']] += 1
            print(el['text'][:75]+"...")
        except Exception as err:
            pass

    print("")
    print("Info about language "+str(len(js))+" latest posts:")
    print("")

    for lang in language_dct:
        print(str(language_dct[lang])+" posts " + lang)

    hashtag_dct = sorted(list(hashtag_dct.items()),
                         key=lambda x: x[1], reverse=True)

    print("")
    print("Top 5 hashtegs:")
    print("")
    try:
        for i in range(5):

            print("`"+hashtag_dct[i][0]+"` occurs " +
                  str(hashtag_dct[i][1])+" times")
    except:
        print("")
        print("OOOOps no more hashtags :(")


if __name__ == "__main__":
    acct = _input()
    js = js_read(acct)
    info_print(js)
