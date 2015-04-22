from TwitterAPI import TwitterAPI
api = TwitterAPI('K9WyKRZkSv1piH99YGa1r8v7E','bnoWuT5segvhCb64MX1rXyHXr6d5NKThp0wfIqiYEVLVN4dDT1', '69908245-bh8asTTeVVFxJM7isoPasVatElUmvSQjK78NIz79u', 'Qa4wd9U8wSIhJccqtNo5sB9GuoyqxmNGc1SPuZqu6hQvY')

#r = api.request('search/tweets', {'q':'pizza'})
r = api.request('statuses/home_timeline')

for item in r:
        print item['text'][:63]
        exit()