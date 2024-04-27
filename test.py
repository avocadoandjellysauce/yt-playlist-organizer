import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')

video_description = '''Trace the 7,000 year old history of alcohol, from its first known origins in China to cultures all over the world fermenting their own drinks.

--

Nobody knows exactly when humans began to create fermented beverages. The earliest known evidence comes from 7,000 BCE in China, where residue in clay pots has revealed that people were making an alcoholic beverage from fermented rice, millet, grapes, and honey. So how did alcohol come to fuel global trade and exploration? Rod Phillips explores the evolution of alcohol.

Lesson by Rod Phillips, directed by Anton Bogaty.

Animator's website:  

 / anton_bogaty  
Sign up for our newsletter: http://bit.ly/TEDEdNewsletter
Support us on Patreon: http://bit.ly/TEDEdPatreon
Follow us on Facebook: http://bit.ly/TEDEdFacebook
Find us on Twitter: http://bit.ly/TEDEdTwitter
Peep us on Instagram: http://bit.ly/TEDEdInstagram
View full lesson: https://ed.ted.com/lessons/a-brief-hi...

Thank you so much to our patrons for your support! Without you this video would not be possible! Mauricio Basso, Athena Grace Franco, Tirath Singh Pandher, Melvin Williams, Tsz Hin Edmund Chan, Nicolas Silva, Raymond Lee, Kurt Almendras, Denise A Pitts, Abdallah Absi, Dee Wei, Richard A Berkley, Tim Armstrong, Daniel Nester, Hashem Al, denison martins fernandes, Doug Henry, Arlene Spiegelman, Michał Friedrich, Joshua Wasniewski, Maryam Dadkhah, Kristiyan Bonev, Keven Webb, Mihai Sandu, Deepak Iyer, Javid Gozalov, Emilia Alvarado, Jaime Arriola, Mirzat Tulafu, Lewis Westbury, Felipe Hoff, Rebecca Reineke, Cyrus Garay, Victoria Veretilo, Michael Aquilina, William Biersdorf, Patricia Alves Panagides, Valeria Sloan Vasquez, Mike Azarkman, Yvette Mocete, Pavel Maksimov, Victoria Soler-Roig, Betsy Feathers, Samuel Barbas, Therapist Gus, Sai Krishna Koyoda, Elizabeth Parker, William Bravante, Irindany Sandoval and Mark wisdom.'''

pattern = r"^(.*?)(?=http|shoutout|shout out|check out|sign up|newsletter|sponsor)"
match = re.search(pattern, video_description, re.IGNORECASE | re.DOTALL)
if match:
  # Extract the relevant description
  video_description = match.group(1).strip()

#print(video_description.replace('\n', ''))

def language_processing(pl_data):
    '''processes keywords from pl_data dictionary'''
    # to begin processing the pl_data, we will need to tokenize (seperating title/description into words)
    # then we will remove the common stopwords, words that will not help in filtering the videos.

    filtered_pl_data = {}
    stop_words = set(stopwords.words('english'))  # set of common english stopwords from nltk
    for video_title in pl_data:
        token_title = word_tokenize(video_title)
        token_description = word_tokenize(pl_data[video_title])

        filtered_title = [word for word in token_title if word.casefold() not in stop_words]
        filtered_description = [word for word in token_description if word.casefold() not in stop_words]
        filtered_pl_data[filtered_title] = filtered_description
    
    return filtered_pl_data

pl_data = {'A brief history of alcohol - Rod Phillips':''.join(video_description)}
print(language_processing(pl_data))