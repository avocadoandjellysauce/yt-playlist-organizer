import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
import string


description2 = '''Download a free audiobook and support TED-Ed's nonprofit mission: http://adbl.co/2om4O4Q

Check out Neil Gaiman's "Norse Mythology": http://bit.ly/2opZptA

View full lesson: https://ed.ted.com/lessons/the-myth-o...

Thor – son of Odin, god of thunder, and protector of mankind – struggled mightily against his greatest challenge yet: opening a bag of food. How had the mighty god fallen so far? Scott Mellor tells the myth of Thor's journey to Utgard.

Lesson by Scott A. Mellor, animation by Rune F.B. Hansen.

Thank you so much to our patrons for your support! Without you this video would not be possible! Alejandro Cachoua, Thomas Mungavan, Elena Crescia, Edla Paniguel, Sarah Lundegaard, Charlsey, Anna-Pitschna Kunz, Tim Armstrong, Alessandro, Erika Blanquez, Ricki Daniel Marbun, zjweele13, Judith Benavides, Znosheni Kedy, Caitlin de Falco, Scheherazade Kelii, Errys, James Bruening, Michael Braun-Boghos, Ricardo Diaz, Kack-Kyun Kim, Alexandrina Danifeld, Danny Romard, Yujing Jiang, Stina Boberg, Mariana Ortega, Anthony Wiggins, Hoai Nam Tran, Joe Sims, David Petrovič, Chris Adriaensen, Lowell Fleming, Lorenzo Margiotta, Amir Ghandeharioon, Anuj Tomar, Sunny Patel, Rachel Birenbaum, Vijayalakshmi, Devesh Kumar, Uday Kishore, Aidan Forero, Leen Mshasha, Allan Hayes, Thomas Bahrman, Alexander Baltadzhiev, Vaibhav Mirjolkar, Tony, Michelle, Katie and Josh Pedretti, Erik Biemans, Gaurav Mathur, Sameer Halai, Hans Peng, Tekin Gültekin, Thien Loc Huynh, Bogdan Alexandru Stoica, Hector Quintanilla, PH Chua, Raheem, and Varinia Bohoslavsky.'''

pattern = r"^(.*?)(?=http|shoutout|shout out|check out|sign up|newsletter|sponsor|patron|patrons)"
match = re.search(pattern, description2, re.IGNORECASE | re.DOTALL)
if match:
  # Extract the relevant description
  description2 = match.group(1).strip()

#print(video_description.replace('\n', ''))

def language_processing(pl_data):
    '''processes keywords from pl_data dictionary.'''
    # to begin processing the pl_data, we will need to tokenize (seperating title/description into words)
    # then we will remove the common stopwords, words that will not help in filtering the videos.

    filtered_pl_data = {}
    stop_words = set(stopwords.words('english'))  # set of common english stopwords from nltk
    for video_title in pl_data:
        token_title = word_tokenize(video_title)
        token_description = word_tokenize(pl_data[video_title])

        filtered_title = ' '.join([word for word in token_title if word.casefold() not in stop_words and word not in string.punctuation])
        filtered_description = [word for word in token_description if word.casefold() not in stop_words and word not in string.punctuation]
        filtered_pl_data[filtered_title] = filtered_description
    
    return filtered_pl_data

pl_data = {"The myth of Thor's journey to the land of giants - Scott A. Mellor":''.join(description2)}

print(language_processing(pl_data))