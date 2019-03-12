""""Software design MP3 by Anthony Krichevskiy"""

from bs4 import BeautifulSoup
from urllib import request
import requests
import re
import pycountry


def slice_transcript(url):
    """Takes a URL of a Miller Center speech and returns only the transcript of the presidential speech."""
    html = BeautifulSoup(requests.get(url).text, 'lxml')
    input = re.sub(r'<.+?>', '', str(html.get_text()))
    #Speech starts at "Transcript", cut everything before that
    index_start = input.find("Transcript")
    if index_start != -1:
        intro_removed = input[(index_start + 10):]
    else:
        raise Exception('Slicer indexing failed')
    #Speech ends at "Previous", but not all speeches have the "Previous" or "Next" buttons, so end at
    #"View all." This means that every transcript will have "Previous" and the name of the previous speech,
    #as well as "Next" and the name of the next speech at the end. That's fine.
    index_end = intro_removed.rfind("More")
    if index_end != -1:
        intro_and_end_removed = intro_removed[:index_end]
    else:
        raise Exception('Slicer indexing failed')
    return intro_and_end_removed

def next_speech(input_speech):
    """Takes the url of a presidential speech as an input, opens the page source, locates the next
    speech, and returns the URL of the next speech.
    >>> next_speech('https://millercenter.org/the-presidency/presidential-speeches/april-30-1789-first-inaugural-address')
    'https://millercenter.org/the-presidency/presidential-speeches/october-3-1789-thanksgiving-proclamation'
    """
    #Make string of page source
    page = request.urlopen(input_speech)
    soup = BeautifulSoup(page, "lxml")
    page_source = soup.prettify()
    #Remove all white space
    no_white_page_source = "".join(page_source.split())
    #Find the URL of the next speech
    start = (no_white_page_source.find("""Next</header><divclass="rows-wrapper"><divclass="views-row"><divclass="views-fieldviews-field-title"><spanclass="field-content"><ahref=""") + 136)
    end = no_white_page_source[start:].find("hreflang=")
    return "https://millercenter.org" + no_white_page_source[start:(start + end - 1)]

def create_president_txt(file_name, num_of_speeches, url_of_first_speech):
    """Takes the number of speeches a president has on the Miller Center website and the url of the
    first speech then creates a .txt file of name file_name with the text of all of that president's
    speeches."""
    file = open(file_name + '.txt', 'w')
    url = url_of_first_speech
    for index in range(0, num_of_speeches):
        file.write(slice_transcript(url))
        url = next_speech(url)
    file.close()

#Create files: uncomment all of the following lines to create 44 text files with each president's speeches (Remember: Grover Cleveland was #22 and #24 so there are only 44 of them!).
#create_president_txt('Washington', 21, 'https://millercenter.org/the-presidency/presidential-speeches/april-30-1789-first-inaugural-address')
#create_president_txt('Adams', 9, 'https://millercenter.org/the-presidency/presidential-speeches/march-4-1797-inaugural-address')
#create_president_txt('Jefferson', 24, 'https://millercenter.org/the-presidency/presidential-speeches/march-4-1801-first-inaugural-address')
#create_president_txt('Madison', 22, 'https://millercenter.org/the-presidency/presidential-speeches/march-4-1809-first-inaugural-address')
#create_president_txt('Monroe', 10, 'https://millercenter.org/the-presidency/presidential-speeches/march-4-1817-first-inaugural-address')
#create_president_txt('Quincy Adams', 9, 'https://millercenter.org/the-presidency/presidential-speeches/july-4-1821-speech-us-house-representatives-foreign-policy')
#create_president_txt('Jackson', 26, 'https://millercenter.org/the-presidency/presidential-speeches/march-4-1829-first-inaugural-address')
#create_president_txt('Van Buren', 10, 'https://millercenter.org/the-presidency/presidential-speeches/march-4-1837-inaugural-address')
#create_president_txt('Harrison', 1, 'https://millercenter.org/the-presidency/presidential-speeches/march-4-1841-inaugural-address')
#create_president_txt('Tyler', 18, 'https://millercenter.org/the-presidency/presidential-speeches/april-9-1841-address-upon-assuming-office-president-united')
#create_president_txt('Polk', 25, 'https://millercenter.org/the-presidency/presidential-speeches/march-4-1845-inaugural-address')
#create_president_txt('Taylor', 4, 'https://millercenter.org/the-presidency/presidential-speeches/march-5-1849-inaugural-address')
#create_president_txt('Fillmore', 7, 'https://millercenter.org/the-presidency/presidential-speeches/august-6-1850-message-regarding-compromise-texas')
#create_president_txt('Pierce', 15, 'https://millercenter.org/the-presidency/presidential-speeches/march-4-1853-inaugural-address')
#create_president_txt('Buchanan', 14, 'https://millercenter.org/the-presidency/presidential-speeches/march-4-1857-inaugural-address')
#create_president_txt('Lincoln', 15, 'https://millercenter.org/the-presidency/presidential-speeches/july-6-1852-eulogy-henry-clay')
#create_president_txt('Johnson', 31, 'https://millercenter.org/the-presidency/presidential-speeches/april-17-1865-message-following-death-abraham-lincoln')
#create_president_txt('Grant', 32, 'https://millercenter.org/the-presidency/presidential-speeches/march-4-1869-first-inaugural-address')
#create_president_txt('Hayes', 16, 'https://millercenter.org/the-presidency/presidential-speeches/march-5-1877-inaugural-address')
#create_president_txt('Garfield', 1, 'https://millercenter.org/the-presidency/presidential-speeches/march-4-1881-inaugural-address')
#create_president_txt('Arthur', 11, 'https://millercenter.org/the-presidency/presidential-speeches/september-22-1881-address-upon-assuming-office-president')
#create_president_txt('Cleveland', 29, 'https://millercenter.org/the-presidency/presidential-speeches/march-4-1885-first-inaugural-address')
#create_president_txt('Harrison', 23, 'https://millercenter.org/the-presidency/presidential-speeches/march-4-1889-inaugural-address')
#create_president_txt('McKinley', 14, 'https://millercenter.org/the-presidency/presidential-speeches/march-4-1897-first-inaugural-address')
#create_president_txt('Teddy Roosevelt', 22, 'https://millercenter.org/the-presidency/presidential-speeches/september-14-1901-announcement-death-president-mckinley')
#create_president_txt('Taft', 12, 'https://millercenter.org/the-presidency/presidential-speeches/march-4-1909-inaugural-address')
#create_president_txt('Wilson', 33, 'https://millercenter.org/the-presidency/presidential-speeches/march-4-1913-first-inaugural-address')
#create_president_txt('Harding', 17, 'https://millercenter.org/the-presidency/presidential-speeches/april-4-1917-republic-must-awaken')
#create_president_txt('Coolidge', 12, 'https://millercenter.org/the-presidency/presidential-speeches/december-6-1923-first-annual-message')
#create_president_txt('Hoover', 30, 'https://millercenter.org/the-presidency/presidential-speeches/october-22-1928-principles-and-ideals-united-states-government')
#create_president_txt('FDR', 49, 'https://millercenter.org/the-presidency/presidential-speeches/march-4-1933-first-inaugural-address')
#create_president_txt('Truman', 19, 'https://millercenter.org/the-presidency/presidential-speeches/april-16-1945-first-speech-congress')
#create_president_txt('Eisenhower', 6, 'https://millercenter.org/the-presidency/presidential-speeches/january-20-1953-first-inaugural-address')
#create_president_txt('Kennedy', 44, 'https://millercenter.org/the-presidency/presidential-speeches/july-15-1960-acceptance-democratic-party-nomination')
#create_president_txt('LBJ', 70, 'https://millercenter.org/the-presidency/presidential-speeches/may-30-1963-remarks-gettysburg-civil-rights')
#create_president_txt('Nixon', 23, 'https://millercenter.org/the-presidency/presidential-speeches/september-23-1952-checkers-speech')
#create_president_txt('Ford', 14, 'https://millercenter.org/the-presidency/presidential-speeches/august-9-1974-remarks-taking-oath-office')
#create_president_txt('Carter', 22, 'https://millercenter.org/the-presidency/presidential-speeches/september-23-1976-debate-president-gerald-ford-domestic-issues')
#create_president_txt('Reagan', 59, 'https://millercenter.org/the-presidency/presidential-speeches/october-27-1964-time-choosing')
#create_president_txt('HW.Bush', 12, 'https://millercenter.org/the-presidency/presidential-speeches/october-2-1990-address-nation-budget')
#create_president_txt('Clinton', 39, 'https://millercenter.org/the-presidency/presidential-speeches/january-20-1993-first-inaugural')
#create_president_txt('W.Bush', 39, 'https://millercenter.org/the-presidency/presidential-speeches/january-20-2001-first-inaugural-address')
#create_president_txt('Obama', 50, 'https://millercenter.org/the-presidency/presidential-speeches/august-28-2008-acceptance-speech-democratic-national')
#create_president_txt('Trump', 16, 'https://millercenter.org/the-presidency/presidential-speeches/january-20-2017-inaugural-address')

#Build country and reference dictionary
foreign_nation_dict = dict()
for country in pycountry.countries:
    foreign_nation_dict[country.name] = 0
for country in pycountry.historic_countries:
    foreign_nation_dict[country.name] = 0
#Add important foreign actors in US history that are not already in dict.
foreign_nation_dict['Great Britain'] = 0
foreign_nation_dict['Cherokee'] = 0
foreign_nation_dict['Lakota'] = 0
foreign_nation_dict['Indian Territories'] = 0
foreign_nation_dict['Soviet Union'] = 0
foreign_nation_dict['Suez'] = 0
foreign_nation_dict['Confederate'] = 0
foreign_nation_dict['Confederacy'] = 0
#Add important international organizations
foreign_nation_dict['United Nations'] = 0
foreign_nation_dict['NATO'] = 0
foreign_nation_dict['European Union'] = 0
foreign_nation_dict['EU'] = 0
foreign_nation_dict['Warsaw Pact'] = 0
foreign_nation_dict['UN'] = 0
#Add the adjective form of important country names, where the country name doesn't
#exist in the adjective form. For example, I am not adding "Colombian" to the list
#because a search for "Colombia" would pick that up, but "Mexican" is important to add
#because a search for "Mexico" won't pick it up.
foreign_nation_dict['Canadian'] = 0
foreign_nation_dict['Chinese'] = 0
foreign_nation_dict['German'] = 0
foreign_nation_dict['Danish'] = 0
foreign_nation_dict['British'] = 0
foreign_nation_dict['Spanish'] = 0
foreign_nation_dict['Finnish'] = 0
foreign_nation_dict['French'] = 0
foreign_nation_dict['Irish'] = 0
foreign_nation_dict['Italian'] = 0
foreign_nation_dict['Mexican'] = 0
foreign_nation_dict['Dutch'] = 0
foreign_nation_dict['Polish'] = 0
foreign_nation_dict['Saudi'] = 0
foreign_nation_dict['Swedish'] = 0
foreign_nation_dict['Turkish'] = 0
foreign_nation_dict['Ukrainian'] = 0
foreign_nation_dict['Czech'] = 0
foreign_nation_dict['Indian'] = 0
#Fix country names to the colloquial name.
foreign_nation_dict['Bolivia'] = foreign_nation_dict.pop('Bolivia, Plurinational State of')
foreign_nation_dict['Democratic Republic of the Congo'] = foreign_nation_dict.pop('Congo, The Democratic Republic of the')
foreign_nation_dict['Iran'] = foreign_nation_dict.pop('Iran, Islamic Republic of')
foreign_nation_dict['Korea'] = foreign_nation_dict.pop('Korea, Republic of')
foreign_nation_dict['Laos'] = foreign_nation_dict.pop("Lao People's Democratic Republic")
foreign_nation_dict['Saint Martin'] = foreign_nation_dict.pop('Saint Martin (French part)')
foreign_nation_dict['Moldova'] = foreign_nation_dict.pop('Moldova, Republic of')
foreign_nation_dict['Macedonia'] = foreign_nation_dict.pop('Macedonia, Republic of')
foreign_nation_dict['North Korea'] = foreign_nation_dict.pop("Korea, Democratic People's Republic of")
foreign_nation_dict['Palestine'] = foreign_nation_dict.pop('Palestine, State of')
foreign_nation_dict['Russia'] = foreign_nation_dict.pop('Russian Federation')
foreign_nation_dict['Syria'] = foreign_nation_dict.pop('Syrian Arab Republic')
foreign_nation_dict['Taiwan'] = foreign_nation_dict.pop('Taiwan, Province of China')
foreign_nation_dict['Tanzania'] = foreign_nation_dict.pop('Tanzania, United Republic of')
foreign_nation_dict['Vatican'] = foreign_nation_dict.pop('Holy See (Vatican City State)')
foreign_nation_dict['Venezuela'] = foreign_nation_dict.pop('Venezuela, Bolivarian Republic of')
foreign_nation_dict['Vietnam'] = foreign_nation_dict.pop('Viet Nam')
foreign_nation_dict['Burma'] = foreign_nation_dict.pop('Burma, Socialist Republic of the Union of')
foreign_nation_dict['Czechoslovakia'] = foreign_nation_dict.pop('Czechoslovakia, Czechoslovak Socialist Republic')
foreign_nation_dict['France'] = foreign_nation_dict.pop('France, Metropolitan')
foreign_nation_dict['Panama Canal'] = foreign_nation_dict.pop('Panama Canal Zone')
foreign_nation_dict['Midway'] = foreign_nation_dict.pop('Midway Islands')
foreign_nation_dict['USSR'] = foreign_nation_dict.pop('USSR, Union of Soviet Socialist Republics')
foreign_nation_dict['Yemen'] = foreign_nation_dict.pop("Yemen, Democratic, People's Democratic Republic of")
foreign_nation_dict['Yugoslavia'] = foreign_nation_dict.pop('Yugoslavia, Socialist Federal Republic of')
#Delete small countries to speed the program.
del foreign_nation_dict['Åland Islands']
del foreign_nation_dict['French Southern Territories']
del foreign_nation_dict['Antigua and Barbuda']
del foreign_nation_dict['Bonaire, Sint Eustatius and Saba']
del foreign_nation_dict['Saint Barthélemy']
del foreign_nation_dict['Brunei Darussalam']
del foreign_nation_dict['Bouvet Island']
del foreign_nation_dict['Cocos (Keeling) Islands']
del foreign_nation_dict["Côte d'Ivoire"]
del foreign_nation_dict['Cook Islands']
del foreign_nation_dict['Comoros']
del foreign_nation_dict['Cabo Verde']
del foreign_nation_dict['Curaçao']
del foreign_nation_dict['Christmas Island']
del foreign_nation_dict['Cayman Islands']
del foreign_nation_dict['Fiji']
del foreign_nation_dict['Falkland Islands (Malvinas)']
del foreign_nation_dict['Faroe Islands']
del foreign_nation_dict['Micronesia, Federated States of']
del foreign_nation_dict['Guernsey']
del foreign_nation_dict['Heard Island and McDonald Islands']
del foreign_nation_dict['Isle of Man']
del foreign_nation_dict['British Indian Ocean Territory']
del foreign_nation_dict['Saint Kitts and Nevis']
del foreign_nation_dict['Saint Lucia']
del foreign_nation_dict['Marshall Islands']
del foreign_nation_dict['Maldives']
del foreign_nation_dict['Northern Mariana Islands']
del foreign_nation_dict['Montserrat']
del foreign_nation_dict['Mauritius']
del foreign_nation_dict['Mayotte']
del foreign_nation_dict['Norfolk Island']
del foreign_nation_dict['Pitcairn']
del foreign_nation_dict['French Polynesia']
del foreign_nation_dict['Réunion']
del foreign_nation_dict['South Georgia and the South Sandwich Islands']
del foreign_nation_dict['Saint Helena, Ascension and Tristan da Cunha']
del foreign_nation_dict['Svalbard and Jan Mayen']
del foreign_nation_dict['Solomon Islands']
del foreign_nation_dict['Saint Pierre and Miquelon']
del foreign_nation_dict['Sao Tome and Principe']
del foreign_nation_dict['Suriname']
del foreign_nation_dict['Sint Maarten (Dutch part)']
del foreign_nation_dict['Seychelles']
del foreign_nation_dict['Turks and Caicos Islands']
del foreign_nation_dict['Tokelau']
del foreign_nation_dict['Togo']
del foreign_nation_dict['Timor-Leste']
del foreign_nation_dict['Tonga']
del foreign_nation_dict['United States Minor Outlying Islands']
del foreign_nation_dict['Saint Vincent and the Grenadines']
del foreign_nation_dict['Virgin Islands, British']
del foreign_nation_dict['Virgin Islands, U.S.']
del foreign_nation_dict['Vanuatu']
del foreign_nation_dict['Wallis and Futuna']
del foreign_nation_dict['French Afars and Issas']
del foreign_nation_dict['Netherlands Antilles']
del foreign_nation_dict['British Antarctic Territory']
del foreign_nation_dict['Byelorussian SSR Soviet Socialist Republic']
del foreign_nation_dict['Canton and Enderbury Islands']
del foreign_nation_dict['Dahomey']
del foreign_nation_dict['French Southern and Antarctic Territories']
del foreign_nation_dict['Gilbert and Ellice Islands']
del foreign_nation_dict['Upper Volta, Republic of']
del foreign_nation_dict['Johnston Island']
del foreign_nation_dict['New Hebrides']
del foreign_nation_dict['Dronning Maud Land']
del foreign_nation_dict['Neutral Zone']
del foreign_nation_dict['Pacific Islands (trust territory)']
del foreign_nation_dict['US Miscellaneous Pacific Islands']
del foreign_nation_dict['Southern Rhodesia']
del foreign_nation_dict['Sikkim']
del foreign_nation_dict['East Timor']
del foreign_nation_dict['Viet-Nam, Democratic Republic of']
del foreign_nation_dict['Wake Island']
del foreign_nation_dict['Zaire, Republic of']
del foreign_nation_dict['United States']

def foreign_nation_counter(txt_file):
    """Takes a text file as an input and returns a dictionary with a count of all mentions of foreign nations"""
    file = open(txt_file, 'r')
    lines = file.readlines()
    president_dict = {}
    for key, value in foreign_nation_dict.items():
        for line in lines:
            president_dict[key] = president_dict.get(key, 0) + line.count(key)
    for key in list(president_dict.keys()): ##Creates a list of all keys
        if president_dict[key] == 0:
            del president_dict[key]
    return sorted(president_dict.items(), key=lambda x: x[1], reverse=True)

file = open('Results.txt', 'w')
file.write('Washington \n' + str(foreign_nation_counter('Washington.txt')) + '\n')
file.write('Adams \n' + str(foreign_nation_counter('Adams.txt')) + '\n')
file.write('Jefferson \n' + str(foreign_nation_counter('Jefferson.txt')) + '\n')
file.write('Madison \n' + str(foreign_nation_counter('Madison.txt')) + '\n')
file.write('Monroe \n' + str(foreign_nation_counter('Monroe.txt')) + '\n')
file.write('Quincy Adams \n' + str(foreign_nation_counter('Quincy Adams.txt')) + '\n')
file.write('Jackson \n' + str(foreign_nation_counter('Jackson.txt')) + '\n')
file.write('Van Buren \n' + str(foreign_nation_counter('Van Buren.txt')) + '\n')
file.write('Harrison \n' + str(foreign_nation_counter('Harrison.txt')) + '\n')
file.write('Tyler \n' + str(foreign_nation_counter('Tyler.txt')) + '\n')
file.write('Polk \n' + str(foreign_nation_counter('Polk.txt')) + '\n')
file.write('Taylor \n' + str(foreign_nation_counter('Taylor.txt')) + '\n')
file.write('Fillmore \n' + str(foreign_nation_counter('Fillmore.txt')) + '\n')
file.write('Pierce \n' + str(foreign_nation_counter('Pierce.txt')) + '\n')
file.write('Buchanan \n' + str(foreign_nation_counter('Buchanan.txt')) + '\n')
file.write('Lincoln \n' + str(foreign_nation_counter('Lincoln.txt')) + '\n')
file.write('Johnson \n' + str(foreign_nation_counter('Johnson.txt')) + '\n')
file.write('Grant \n' + str(foreign_nation_counter('Grant.txt')) + '\n')
file.write('Hayes \n' + str(foreign_nation_counter('Hayes.txt')) + '\n')
file.write('Garfield \n' + str(foreign_nation_counter('Garfield.txt')) + '\n')
file.write('Arthur \n' + str(foreign_nation_counter('Arthur.txt')) + '\n')
file.write('Cleveland \n' + str(foreign_nation_counter('Cleveland.txt')) + '\n')
file.write('Harrison \n' + str(foreign_nation_counter('Harrison.txt')) + '\n')
file.write('McKinley \n' + str(foreign_nation_counter('McKinley.txt')) + '\n')
file.write('Teddy Roosevelt \n' + str(foreign_nation_counter('Teddy Roosevelt.txt')) + '\n')
file.write('Taft \n' + str(foreign_nation_counter('Taft.txt')) + '\n')
file.write('Wilson \n' + str(foreign_nation_counter('Wilson.txt')) + '\n')
file.write('Harding \n' + str(foreign_nation_counter('Harding.txt')) + '\n')
file.write('Coolidge \n' + str(foreign_nation_counter('Coolidge.txt')) + '\n')
file.write('Hoover \n' + str(foreign_nation_counter('Hoover.txt')) + '\n')
file.write('FDR \n' + str(foreign_nation_counter('FDR.txt')) + '\n')
file.write('Truman \n' + str(foreign_nation_counter('Truman.txt')) + '\n')
file.write('Eisenhower \n' + str(foreign_nation_counter('Eisenhower.txt')) + '\n')
file.write('Kennedy \n' + str(foreign_nation_counter('Kennedy.txt')) + '\n')
file.write('LBJ \n' + str(foreign_nation_counter('LBJ.txt')) + '\n')
file.write('Nixon \n' + str(foreign_nation_counter('Nixon.txt')) + '\n')
file.write('Ford \n' + str(foreign_nation_counter('Ford.txt')) + '\n')
file.write('Carter \n' + str(foreign_nation_counter('Carter.txt')) + '\n')
file.write('Reagan \n' + str(foreign_nation_counter('Reagan.txt')) + '\n')
file.write('HW.Bush \n' + str(foreign_nation_counter('HW.Bush.txt')) + '\n')
file.write('Clinton \n' + str(foreign_nation_counter('Clinton.txt')) + '\n')
file.write('W.Bush \n' + str(foreign_nation_counter('W.Bush.txt')) + '\n')
file.write('Obama \n' + str(foreign_nation_counter('Obama.txt')) + '\n')
file.write('Trump \n' + str(foreign_nation_counter('Trump.txt')) + '\n')
file.close()
