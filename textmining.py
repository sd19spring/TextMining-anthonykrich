""""Software design MP3 by Anthony Krichevskiy"""

from bs4 import BeautifulSoup
import requests
html = BeautifulSoup(requests.get('https://millercenter.org/the-presidency/presidential-speeches/september-19-1796-farewell-address').text, 'lxml')
import re
transcript = re.sub(r'<.+?>', '', str(html.get_text()))

def slice_transcript(input):
    """Takes a string of the html webpage from the Miller Center and returns only the transcript of the presidential speech."""
    #Speech starts at "Transcript", cut everything before that
    index_start = input.find("Transcript")
    if index_start != -1:
        intro_removed = input[(index_start + 10):]
    else:
        raise Exception('Slicer indexing failed')
    #Speech ends at "Previous", but there might be multiple instances of "Previous",
    #so cut until "transcript end" then cut until "Previous"
    index_almost_end = intro_removed.find("transcript icon")
    if index_almost_end != -1:
        intro_and_end_removed = intro_removed[:index_almost_end]
    else:
        raise Exception('Slicer indexing failed')
    index_end = intro_and_end_removed.rfind("Previous")
    if index_end != -1:
        final = intro_and_end_removed[:index_end]
    else:
        raise Exception('Slicer indexing failed')
    return final

print(slice_transcript(transcript))
