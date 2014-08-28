#__author__ = "Siddhartha Dutta"
#__date__ = "August 23, 2014"

import os
import sys
import shutil
from stemming.porter2 import stem

def stem_lyrics(lyrics):
    # remove end of lines
    altered_lyrics = lyrics.replace('\r', '\n').lower()
    # custom replacements
    altered_lyrics = altered_lyrics.replace(" don't ", " do not ")
    altered_lyrics = altered_lyrics.replace(" won't ", " will not ")
    altered_lyrics = altered_lyrics.replace(" wouldn't ", " would not ")
    altered_lyrics = altered_lyrics.replace(" hadn't ", " had not ")
    altered_lyrics = altered_lyrics.replace(" he's ", " he is ")
    altered_lyrics = altered_lyrics.replace(" she's ", " she is ")
    altered_lyrics = altered_lyrics.replace(" it's ", " it is ")
    altered_lyrics = altered_lyrics.replace("'ld ", " would ")
    altered_lyrics = altered_lyrics.replace("'ll ", " will ")
    altered_lyrics = altered_lyrics.replace("'m ", " am ")
    altered_lyrics = altered_lyrics.replace("'re ", " are ")
    altered_lyrics = altered_lyrics.replace("'ve ", " have ")
    altered_lyrics = altered_lyrics.replace("'d ", " would ")
    altered_lyrics = altered_lyrics.replace(" ain't ", " is not ")
    altered_lyrics = altered_lyrics.replace("n't ", "n not ")
    altered_lyrics = altered_lyrics.replace("'s ", " ")
    #removing symbols
    symbols = (',', "'", '"', ",", ';', ':', '.', '?', '!', '(', ')', '[', ']'
                   '{', '}', '/', '\\', '_', '|', '-', '@', '#', '*', '<', '>', '//')
    for p in symbols:
        altered_lyrics = altered_lyrics.replace(p, '')
    # replacing each word by its stem
    stemmed_lyrics = ''
    for word in altered_lyrics:
        # stemmed_lyrics += stem(word)
        stemmed_lyrics += word
    
    return stemmed_lyrics


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print 'Error: Enter path of directory'    
        sys.exit(0)

    path = sys.argv[1]
    input_path = path + '/LyricsCorpus'
    output_path = path + '/testing'
    if not os.path.exists(output_path): os.makedirs(output_path)
    else: 
        shutil.rmtree(output_path) 
        os.makedirs(output_path)
    for folder in os.listdir(input_path):
        # .DS_Store is a Mac System file
        if(folder!='.DS_Store'):
            os.makedirs(output_path+'/'+folder)       
            for textfile in os.listdir(input_path+'/'+folder):
                if(textfile!='.DS_Store'):
                    read_file = open(input_path+'/'+folder+'/'+textfile, 'r')
                    lyrics = read_file.read()
                    lyrics = lyrics.strip()
                    stemmed_lyrics = stem_lyrics(lyrics)
                    if stemmed_lyrics is None:
                        print 'Error: File is empty'
                        sys.exit(0)
                    #print stemmed_lyrics
                    write_file = open(output_path+'/'+folder+'/'+textfile, 'w')
                    write_file.write(stemmed_lyrics)
                    write_file.close()
                    read_file.close()
    sys.exit(0)
