import streamlit as st
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import pandas as pd
import difflib
import speech_recognition as sr

def speak(audio):
    """Function to convert text to speech"""
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """Function to wish the user based on the time of the day"""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("I am HAM your personal assistant. Hello! How can I assist you today?")

def takeCommand():
    """Function to capture voice command from the user"""
    r = sr.Recognizer()

    with sr.Microphone() as source:
        st.write("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        st.write("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        st.write(f"User said: {query}\n")
    except Exception as e:
        st.error(e)
        st.write("Say that again please...")
        return "None"

    return query
    
def main():

    st.title("HAM: Your Personal Assistant")
    listen_button = False
    listen_button = st.button("Listen 🎙️")
    wishMe()

    if listen_button:
        while True:
            query = takeCommand().lower()

            if 'wikipedia' in query:
                query = query.replace("wikipedia", "")
                try:
                    speak('Searching Wikipedia...')
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia")
                    st.write(results)
                    speak(results)
                except wikipedia.exceptions.WikipediaException as e:
                    st.error("Sorry, I encountered an error while searching Wikipedia. Please try again.")

            elif 'open youtube' in query:
                webbrowser.open("https://www.youtube.com")

            elif 'open google' in query:
                webbrowser.open("https://www.google.com")

            elif 'play music' in query:
                music_dir = 'C:\\Users\\mujta\\Downloads\\naats'  # Enter your music directory path here
                songs = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir, songs[0]))

            elif 'the time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir, the time is {strTime}")

            elif 'open my github' in query:
                webbrowser.open("https://github.com/hilalaziz32")

            elif 'imdb' in query:

                # Read the IMDb dataset
                df = pd.read_csv("C:\\Users\\mujta\\Downloads\\Movie-System-Project-Using-AI-Algorithms-main\\Movie-System-Project-Using-AI-Algorithms-main\\IMDB top 1000.csv")

                # Split 'Info' column into 'Votes' and 'Gross' columns
                df[['Votes', 'Gross']] = df['Info'].str.split('|', expand=True)

                # Split 'Cast' column into 'Director' and 'Stars' columns
                df[['Director', 'Stars']] = df['Cast'].str.split('|', expand=True)

                # Strip leading and trailing whitespaces from all string columns
                df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

                # Remove prefixes like "Director:", "Votes:", "Gross:", and "Stars:"
                df['Director'] = df['Director'].str.replace('Director: ', '')
                df['Votes'] = df['Votes'].str.replace('Votes: ','')
                df['Gross'] = df['Gross'].str.replace('Gross: ','')
                df['Stars'] = df['Stars'].str.replace('Stars: ', '')

                # Create additional columns with lowercase letters
                df['Director_lower'] = df['Director'].str.lower()
                df['Stars_lower'] = df['Stars'].str.lower()

                # Extract duration as an integer
                df['duration_int'] = df['Duration'].str.extract('(\d+)').astype(int)

                # Save the cleaned dataset to a new CSV file
                df.to_csv("C:\\Users\\mujta\\Downloads\\Movie-System-Project-Using-AI-Algorithms-main\\Movie-System-Project-Using-AI-Algorithms-main\\IMDB top 1000_cleaned.csv", index=False)
                
                while True:
                    try:
                        st.write("1.Search Movie according to Title or Rate\n2.Search Movie according to Genre\n3.Exit\n")
                        speak(" 1.Search Movie according to Title or Rate\n 2.Search Movie according to Genre \n 3.Exit")
                        
                        choice=takeCommand().lower()
                    
                        if choice == "search movie":
                            st.write("Title or rate")
                            cho = takeCommand().lower()
                            def correct_choice(user_input):
                                closest_match = None
                                max_similarity = 0.0
                                for ch in choice:
                                    similarity = difflib.SequenceMatcher(None, user_input.lower(), ch.lower()).ratio()
                                    if similarity > max_similarity:
                                        closest_match = ch
                                        max_similarity = similarity
                                if max_similarity >= 0.6:
                                    return closest_match
                                return user_input

                        
                            corrected_choice = correct_choice(cho)

                            if "rate" == corrected_choice:
                                st.write("Enter your rating from 1 to 10 about the movie you want to search")
                                rat=int(takeCommand())

                                df1 = df[df['Rate'] >= rat]
                                st.write(df1)

                            elif "title" == corrected_choice:
                                def correct_movie_title(user_input):
                                    closest_match = difflib.get_close_matches(user_input, df["Title"], n=1, cutoff=0.6)
                                    if closest_match:
                                        return closest_match[0]
                                    else:
                                        return user_input
                                st.write("Enter the movie title: ")
                                speak("Enter the movie title: ")
                                user_input = takeCommand().lower() 
                                corrected_title = correct_movie_title(user_input)
                                matching_rows = df[df["Title"].apply(lambda x: corrected_title.lower() in x.lower())]
                                st.write("Corrected Title:", corrected_title)
                                speak("Corrected Title:")
                                st.write("Matching Rows:")
                                speak("Matching Rows:")
                                st.write(matching_rows)

                        elif choice == "theme":
                            genre_synonyms = {
                                "Drama": ["Drama", "Melodrama", "Tragedy", "Theater", "Play"],
                                "Crime": ["Crime", "Criminal", "Illegal", "Lawlessness", "Offense"],
                                "Action": ["Action", "Adventure", "Excitement", "Thrill", "Stunt"],
                                "Adventure": ["Adventure", "Exploration", "Journey", "Quest", "Expedition"],
                                "Biography": ["Biography", "Life story", "Autobiography", "Memoir", "Life history"],
                                "History": ["History", "Historical", "Past", "Antiquity", "Chronicle"],
                                "Sci-Fi": ["Sci-Fi", "Science Fiction", "Futuristic", "Space Opera", "Speculative fiction"],
                                "Romance": ["Romance", "Love story", "Affection", "Passion", "Heartfelt"],
                                "Western": ["Western", "Wild West", "Cowboy", "Frontier", "Outlaw"],
                                "Fantasy": ["Fantasy", "Imaginary", "Enchantment", "Magic", "Mythical"],
                                "Thriller": ["Thriller", "Suspense", "Intense", "Exciting", "Tension"],
                                "Animation": ["Animation", "Cartoon", "Animated", "Toon", "Anime"],
                                "Family": ["Family", "Relatives", "Kin", "Household", "Lineage"],
                                "War": ["War", "Conflict", "Battle", "Combat", "Hostility"],
                                "Comedy": ["Comedy", "Humor", "Funny", "Amusing", "Lighthearted"],
                                "Mystery": ["Mystery", "Enigma", "Puzzle", "Conundrum", "Secret"],
                                "Music": ["Music", "Musical", "Melody", "Harmony", "Tune"],
                                "Horror": ["Horror", "Terrifying", "Frightening", "Scary", "Spooky"],
                                "Sport": ["Sport", "Athletics", "Physical activity", "Exercise", "Game"]
                            }
                            def correct_genre(user_input):
                                closest_match = None
                                max_similarity = 0.0
                                for genres_list in df["Genre"].apply(lambda x: x.split(',')):
                                    for genre in genres_list:
                                        for key, values in genre_synonyms.items():
                                            if user_input.lower() in [synonym.lower() for synonym in values]:
                                                return key
                                        similarity = difflib.SequenceMatcher(None, user_input.lower(), genre.lower()).ratio()
                                        if similarity > max_similarity:
                                            closest_match = genre
                                            max_similarity = similarity

                                if max_similarity >= 0.6:
                                    return closest_match
                                return user_input

                            st.write("Enter the movie genre: ")
                            speak("Enter the movie genre: ")
                            user_input = takeCommand().lower()
                            corrected_genre = correct_genre(user_input)
                            matching_rows = df[df["Genre"].apply(lambda x: user_input.lower() in [genre.lower() for genre in x.split(',')])]
                            st.write("Matching Rows:")
                            speak("Matching Rows:")
                            st.write(matching_rows)

                        elif choice == "exit":
                            st.write("Exit\n")
                            speak("EXIT")
                            break
                        else:
                            st.write("Invalid Choice, Speak Again\n")
                            speak("Invalid Choice, Speak Again")

                    except ValueError:
                        st.write("Invalid input.")
                        speak("Invalid input.")

            elif 'close' in query:
                st.success("Bye Boss!")
                speak("Bye Boss")
                break

if __name__ == "__main__":
    main()
