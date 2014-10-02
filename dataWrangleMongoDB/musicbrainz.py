# To experiment with this code freely you will have to run this code locally.
# We have provided an example json output here for you to look at,
# but you will not be able to run any queries through our UI.
import json
import requests


BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

query_type = {  "simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"}}


def query_site(url, params, uid="", fmt="json"):
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print "requesting", r.url

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    if type(data) == dict:
        print json.dumps(data, indent=indent, sort_keys=True)
    else:
        print data


def main():
    results = query_by_name(ARTIST_URL, query_type["simple"], "Nirvana")
    pretty_print(results)

    artist_id = results["artist"][1]["id"]
    print "\nARTIST:"
    pretty_print(results["artist"][1])

    artist_data = query_site(ARTIST_URL, query_type["releases"], artist_id)
    releases = artist_data["releases"]
    print "\nONE RELEASE:"
    pretty_print(releases[0], indent=2)
    release_titles = [r["title"] for r in releases]

    print "\nALL TITLES:"
    for t in release_titles:
        print t


def questions():
    #how many bands with name "First Aid Kit"
    q1 = query_by_name(ARTIST_URL, query_type["simple"], '"First AID KIT"')
    print len([a for a in q1["artist"]])
    count=0
    for artist in q1["artist"]:
        print artist['name'],'  : ', artist["disambiguation"]
        count +=1
    print count    
 
    #Begin_area name for QUEEN 
    q2 = query_by_name(ARTIST_URL, query_type["simple"], '"QUEEN"')
    print q2["artist"][0]["begin-area"]

    #Spanish alias for BEATLES
    q3 = query_by_name(ARTIST_URL, query_type["simple"], '"BEATLES"')
    print [a["name"] for a in q3["artist"][0]["aliases"] if a["locale"]=="es"]

    #NIRVANA disambiguation
    q4 = query_by_name(ARTIST_URL, query_type["simple"], "NIRVANA")
    print q4["artist"][0]["disambiguation"]

    #When was ONE DIRECT formed?
    q5 = query_by_name(ARTIST_URL, query_type["simple"], '"ONE DIRECTION"')
    print q5["artist"][0]["life-span"]["begin"]

if __name__ == '__main__':
    main()
