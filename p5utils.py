import mwapi
import geoip2
import pandas as pd
from bs4 import BeautifulSoup

#  partially stolen from revscoring/languages/english.py
badwords = [
    # r"https?",
    # r"[A-Z]{4,}\b",
    r"wiki\w*",
    #badwords from revscoring
    r"chug",
    r"dishonest\w*",
    r"fraud",
    r"liar",
    #informal words from revscoring
    r"ain'?t", r"a+we?some?(r|st)?",
    r"(b+l+a+h*)+",
    r"bro",
    r"(bye)+",
    r"can'?t",
    r"[ck](oo+|e+w+)l+\w*",
    r"[ck]+r+a+p+(s|ier|iest)?",
    r"chu+g+",
    r"dad+(y|a)?",
    r"don'?t", r"dum+b*(y|ies|er|est)?(ass)?",
    r"d+?u+?d+?e+?\w*",
    r"good[-_]?bye",
    r"h+[aiou]+(h[aeiou]*)*",
    r"mw?[au]+h+[aiou]+(h[aeiou]*)*",
    r"h+[e]+(h[aeiou]*)+",
    r"hel+?o+", r"h(aa+?|e+?)y+?",
    r"h+?m+?",
    r"i", r"i+?d+?i+?o+?t+?",
    r"(la)+",
    r"loser",
    r"l+[uo][uol]*l",
    r"l+?m+?a+?o+?",
    r"l[ou]+?ve?",
    r"m+?e+?o+?w+?",
    r"munch\w*",
    r"mom+(y|a)?",
    r"moron",
    r"nerds?",
    r"noo+b(y|ie|s)?\w*",
    r"no+?pe",
    r"o+?k+?(a+?y+?)?",
    r"o+?m+?g+?\w*",
    r"poo+?p\w*",
    r"retard\w*", r"tard",
    r"r+?o+?f+?l+?(mao)?",
    r"s+?e+?x+?y+?",
    r"so+?rry",
    r"shove",
    r"smelly",
    r"soo+?",
    r"stink(s|y)?",
    r"s+?t+?[uo]+?p+?i+?d+?\w*",
    r"suck(s|ing|er)?", r"sux",
    r"shouldn'?t",
    r"test +edit", r"t+?u+?r+?d+?s?\w*",
    r"wasn'?t",
    r"w+[oua]+t+", r"wtf\w*", r"wh?[ua]+?t?[sz]+[ua]+p", "s+?u+?p+?",
    r"wu+?z+?",
    r"won'?t",
    r"w+?o+?o+?f+?",
    r"ya'?ll", r"y+?a+?y+?", r"y+?e+?a+?h?", r"you('?(ve|re|ll))?",
    r"y+?o+?l+?o+?"
]

verybadwords = [
    r"a+[sr]+s+e*([-_ ]?butt|clown|face|hole|hat|e?s)?",
    r"(fat|stupid|lazy)a+[sr]+s+e*([-_ ]?butt|clown|face|hole|hat|e?s)?",
    r"autofel+at(e|io|ing|ion)s?",
    r"b+i+o?t+c+h+\w*",
    r"bootlip",
    r"blow(job|me)\w*",
    r"bollock\w*",
    r"boo+ger\w*",
    r"b+u+t+t+([-_ ]?clown|face|hole|hat|es)?",
    r"(ass|arse)b+u+t+t+([-_ ]?clown|face|hole|hat|es)?",
    r"bugg(er|ing)\w*",
    r"butthead", r"buttface", r"buttsex", r"buttf+u+c*k+\w*",
    r"chlamydia",
    r"cholo",
    r"clunge\w*",
    r"cock\w*",
    r"coo+n\w*",
    r"[ck]racker\w*",
    r"c+?u+?n+?t\w*",
    r"crack[-_ ]?head\w*",
    r"crooks?",
    r"defraud",
    r"limpdick\w*",
    r"dick\w*",
    r"d+?i+?l+?d+?o+?\w*",
    r"dot[-_ ]?head\w*",
    r"dyk(e|ing)\w*",
    r"(f|ph)a+g+(ot)?\w*",
    r"fart\w*",
    r"f+u+c*k+\w*",
    r"gh?[ea]+y+\w*",
    r"g[yi]p+(o|y|ie?)?", r"gyppie",
    r"goo+k",
    r"gringo",
    r"hooker\w*",
    r"injun\w*",
    r"j+a+p+o?",
    r"k[iy]+ke",
    r"kwash(i|ee)",
    r"lick(er)?s?",
    r"meth",
    r"meth[-_ ]?head\w*",
    r"naz+i(sm?)?",
    r"nig", r"n+?i+?gg+?[aeious]+?\w*", r"niglet", r"nigor", r"nigr", r"nigra",
    r"nonc(e|ing)\w*",
    r"overdose[sd]",
    r"peckerwood\w*",
    r"p(a?e|æ)do((f|ph)[iy]le)?s?",
    r"peni(s)?\w*",
    r"piss\w*",
    r"prostitute\w*",
    r"pot[-_ ]?head\w*",
    r"q(w|u)ash(i|ee)",
    r"rag[-_ ]?head",
    r"red[-_ ]?(neck|skin)",
    r"round[-_ ]?eye",
    r"satan(ic|ism|ist)s?",
    r"scabies",
    r"s+h+[ia]+t+\w*",
    r"s+?l+?u+?t+?\w*",
    r"spi(g|c|k)+",
    r"spigotty",
    r"spik",
    r"spook",
    r"squarehead",
    r"stupid(s+h+[ia]+t+|c+u+n+t+|f+u+c*k+|t+w+a+t+|w+h+o+r+e+)\w*",
    r"subnormal",
    r"su+c*k+(er|iest|a)",
    r"syphil+is",
    r"terror(ist|ism|i[zs](e|ing|ed))s?",
    r"thei[fv](e?s)?",
    r"tran(ny|sexual)",
    r"t+?w+?a+?t+?\w*",
    r"ti+t+((s|ies|y)[\w]*)?",
    r"v+?a+?g+?(i+n+a+)?", r"vajay?jay?\w*",
    r"wank\w*", r"wetback\w*", r"w+h+o+r+(e+|ing)\w*", r"w+o+g+", r"w+o+p+",
    r"yank(e+)?", r"yid",
    r"zipperhead"
    r"he+rpe+s",
    r"hill-?billy",
    r"hom(a|o|er)(sexual)?\w*",
    r"l+?e+?s+?b+?(o+?|i+?a+?n+?)\w*",
    r"b+?o+?n+?e+?r+?",
    r"boobs?",
    r"bullshit",
    r"\w*([a-zA-Z])\1\1\1\w*",
]

def show_changed_text(rev_id):
    """
    Helper function that prints deleted and added text
    for inspection. Not to be used for large numbers of revisions.

    Parameters: revision ID (int or str).

    Returns nothing.
    """
    session = mwapi.Session('https://en.wikipedia.org', user_agent='aaron')
    response = session.get(action='compare', fromrev=str(rev_id), torelative='prev')
    soup = BeautifulSoup(response['compare']['*'], 'lxml')
    
    additions = []
    deletions = []
    
    for addedline in soup.find_all(class_='diff-addedline'):
        if 'diffchange diffchange-inline' in str(addedline):
            for addition in addedline.find_all(class_='diffchange diffchange-inline'):
                additions.append(addition.text)
        else:
            additions.append(addedline.text)
            
    for deletedline in soup.find_all(class_='diff-deletedline'):
        if 'diffchange diffchange-inline' in str(deletedline):
            for deletion in deletedline.find_all(class_='diffchange diffchange-inline'):
                deletions.append(deletion.text)
        else:
            deletions.append(deletedline.text)

    print("Deleted:\n",deletions)
    print("Added:\n",additions)

def get_added_text(rev_id, session):
    """
    Get processed added text from the HTML diff through
    the MediaWiki API.

    Parameters: revision ID (int or str), MWAPI session.

    Returns list of strings.
    """
    try:
        response = session.get(action='compare', fromrev=str(rev_id), torelative='prev', prop='diff')
    except:
        return None
    soup = BeautifulSoup(response['compare']['*'], 'lxml')
    
    additions = []
    
    for addedline in soup.find_all(class_='diff-addedline'):
        if 'diffchange diffchange-inline' in str(addedline):
            for addition in addedline.find_all(class_='diffchange diffchange-inline'):
                additions.append(addition.text)
        else:
            additions.append(addedline.text)

    return additions

def extract_labels(labels):
    """
    Extracts data from the JSON-formatted "labels" field
    of the WMFLabs tasks file.

    Parameters: JSON-formatted "label" field (as dict).

    Returns six features extracted from the label.
    """
    try:
        automatic = labels['data']['automatic']
    except KeyError:
        automatic = None
    damaging = labels['data']['damaging']
    goodfaith = labels['data']['goodfaith']
    try:
        unsure = labels['data']['unsure']
    except KeyError:
        unsure = None
    timestamp = labels['timestamp']
    user_id = labels['user_id']
    return automatic, damaging, goodfaith, unsure, timestamp, user_id

def get_metadata(rev_id, session):
    """
    Gets various metadata, including the added text, from the
    Wikipedia API.

    Parameters: revision ID (str or int), MWAPI English Wikipedia session.

    Returns namespace, article title, character size of article
    (before and after revision), username, added text.
    """
    try:
        response = session.get(action='compare',
                               fromrev=str(rev_id),
                               torelative='prev',
                               prop='title|user|size|diff')
    except:
        return None, None, None, None, None, None
        
    namespace = response['compare']['tons']
    title = response['compare']['totitle']
    try:
        fromsize = response['compare']['fromsize']
    except KeyError:
        fromsize = 0
    tosize = response['compare']['tosize']
    user = response['compare']['touser']
    
    soup = BeautifulSoup(response['compare']['*'], 'lxml')
    
    additions = []
    
    for addedline in soup.find_all(class_='diff-addedline'):
        if 'diffchange diffchange-inline' in str(addedline):
            for addition in addedline.find_all(class_='diffchange diffchange-inline'):
                additions.append(addition.text)
        else:
            additions.append(addedline.text)

    return namespace, title, fromsize, tosize, user, additions

def get_geoinfo(ip_address, reader):
    """
    Gets geographical information from the MaxMind GeoLite2 database.

    Parameters: IP address (str, v4 or v6 format OK),
    GeoIP2 reader session

    Returns latitude, longitude, and geographic labels
    """
    r = reader.city(ip_address)
    return [r.location.latitude,
            r.location.longitude,
            r.city.name,
            r.subdivisions.most_specific.name,
            r.country.name,
            r.country.iso_code,
            r.postal.code]

def geocode_ips(df, ip_column):
    """
    Takes a dataframe and returns one with geodata columns, using the
    get_geoinfo function.

    Parameters: dataframe, name of columns with IP data (strings).
    Returns a dataframe with additional columns.
    """
    unique_ips = df[ip_column].unique()
    reader = geoip2.database.Reader('./GeoLite2-City_20190604/GeoLite2-City.mmdb')
    
    locs = []
    for ip in unique_ips:
        geodata = get_geoinfo(ip, reader)
        locs.append(geodata)
    
    ip_locations = pd.concat([pd.Series(unique_ips), (pd.DataFrame(locs))], axis=1)
    ip_locations.columns = [
        'user', 'lat', 'lng', 'city', 'state', 'country', 'country_iso', 'postcode'
        ]

    return pd.merge(df, ip_locations, on=ip_column)

def get_ores_data(revision_list, session):
    """
    Get complete ORES data (article quality, draft quality, good faith
    and damaging probabilities, and draft topics) from the ORES API.

    Parameters: batch of revisions (recommended size no more than 50),
    requests session.

    Returns a dataframe of ORES info for the input revisions.
    """
    rev_ids = [str(rev_id) for rev_id in revision_list]
    rev_id_list = "|".join(rev_ids)

    url = "https://ores.wikimedia.org/v3/scores/enwiki/"
    request = session.get(url+"?revids="+rev_id_list)
    data = request.json()

    df = pd.DataFrame()

    for rev_id in rev_ids:
        rev_scores = data['enwiki']['scores'][rev_id]
        try:
            articlequality = rev_scores['articlequality']['score']['prediction']
            draftquality = rev_scores['draftquality']['score']['prediction']
            wp10 = rev_scores['wp10']['score']['prediction']
            damaging = rev_scores['damaging']['score']['probability']['true']
            goodfaith = rev_scores['goodfaith']['score']['probability']['true']
            drafttopic = rev_scores['drafttopic']['score']['prediction']
            row = [rev_id, articlequality, draftquality, wp10, damaging, goodfaith, drafttopic]
        except KeyError:
            row = [None] * 7

        df = df.append([row])

    df.columns = ['rev_id', 'articlequality', 'draftquality',
                  'wp10', 'damaging_prob', 'goodfaith_prob', 'drafttopic']

    return df