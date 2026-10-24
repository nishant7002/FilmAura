"""
Script to create the MovieLens-format development dataset in data/dev/
Generates authentic movies.csv, ratings.csv, tags.csv, and links.csv.
"""

import os
import random
import re
import pandas as pd
import numpy as np

def create_dev_dataset(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    random.seed(42)
    np.random.seed(42)

    movies_data = [
        # Sci-Fi / Cyberpunk / Neo-Noir
        (1, "Blade Runner 2049 (2017)", "Sci-Fi|Mystery|Drama", ["cyberpunk", "neo-noir", "replicant", "existential", "neon", "ai", "dystopian", "rainy", "philosophical"], "01856101", 335984),
        (2, "Children of Men (2006)", "Sci-Fi|Thriller|Drama", ["dystopian", "single-take", "survival", "bleak", "poignant", "hope", "futuristic", "chaos"], "0206634", 9693),
        (3, "Ex Machina (2014)", "Sci-Fi|Mystery|Drama", ["ai", "turing-test", "claustrophobic", "manipulation", "android", "thought-provoking", "tech"], "0470752", 264660),
        (4, "Dark City (1998)", "Film-Noir|Mystery|Sci-Fi", ["neo-noir", "memory-loss", "the-strangers", "nocturnal", "stylized", "dark", "existential"], "0118929", 268),
        (5, "Annihilation (2018)", "Sci-Fi|Horror|Mystery", ["the-shimmer", "cosmic-horror", "mutation", "surreal", "grief", "atmospheric", "eerie"], "2798920", 300668),
        (6, "Arrival (2016)", "Sci-Fi|Drama|Mystery", ["linguistics", "non-linear-time", "alien-contact", "memory", "emotional", "philosophical", "poignant"], "2543164", 329865),
        (7, "Drive (2011)", "Crime|Drama|Action", ["neo-noir", "getaway-driver", "synthwave", "violence", "neon", "minimalist", "cool", "tension"], "0780504", 64690),
        (8, "1917 (2019)", "War|Drama|Action", ["continuous-take", "world-war-one", "no-mans-land", "ticking-clock", "suspenseful", "heroic", "immersive"], "8579674", 530915),
        (9, "Snowpiercer (2013)", "Action|Sci-Fi|Drama", ["class-revolution", "perpetual-train", "ice-age", "dystopia", "allegory", "tense", "dark"], "1706620", 110413),
        (10, "The Road (2009)", "Drama|Adventure|Thriller", ["post-apocalyptic", "cormac-mccarthy", "survival", "father-son", "bleak", "melancholy", "grief"], "0898367", 20766),
        (11, "Interstellar (2014)", "Sci-Fi|Adventure|Drama", ["black-hole", "space-travel", "time-dilation", "relativity", "emotional", "epic", "existential"], "0816692", 157336),
        (12, "Parasite (2019)", "Comedy|Drama|Thriller", ["class-struggle", "social-satire", "twists", "suspense", "black-comedy", "wealth-disparity", "clever"], "6751668", 496243),
        (13, "The Lighthouse (2019)", "Horror|Mystery|Drama", ["black-and-white", "insanity", "isolation", "sea-shanties", "mythology", "disturbing", "hallucinatory"], "8273664", 503919),
        (14, "Solaris (1972)", "Sci-Fi|Mystery|Drama", ["philosophical", "ocean-planet", "grief", "poetic", "tarkovsky", "deep", "memory", "slow-burn"], "0069293", 593),
        (15, "Nightcrawler (2014)", "Crime|Drama|Thriller", ["freelance-journalist", "sociopath", "nocturnal-la", "media-critique", "unethical", "taut"], "2872718", 242582),
        
        # Classics & Masterpieces
        (16, "The Shawshank Redemption (1994)", "Drama|Crime", ["prison", "hope", "friendship", "redemption", "inspirational", "classic", "triumph"], "0111161", 278),
        (17, "The Godfather (1972)", "Crime|Drama", ["mafia", "family", "power", "loyalty", "classic", "tragic", "corruption", "masterpiece"], "0068646", 238),
        (18, "Pulp Fiction (1994)", "Crime|Comedy|Thriller", ["nonlinear", "tarantino", "cult", "dialogue-driven", "hitman", "witty", "pop-culture"], "0110912", 680),
        (19, "The Dark Knight (2008)", "Action|Crime|Drama", ["batman", "joker", "chaos", "heroism", "gritty", "nihilistic", "suspenseful", "epic"], "0468569", 155),
        (20, "Fight Club (1999)", "Action|Crime|Drama", ["anti-consumerism", "twist-ending", "insomnia", "anarchism", "cult", "psychological", "dark"], "0137523", 550),
        (21, "Inception (2010)", "Action|Sci-Fi|Thriller", ["dream-within-a-dream", "heist", "mindfuck", "subconscious", "visuals", "intricate", "pacing"], "1375666", 27205),
        (22, "The Matrix (1999)", "Action|Sci-Fi", ["cyberpunk", "simulation", "dystopia", "bullet-time", "rebellion", "kung-fu", "philosophical"], "0133093", 603),
        (23, "Goodfellas (1990)", "Crime|Drama", ["mob", "organized-crime", "scorsese", "voiceover", "rise-and-fall", "dynamic", "gritty"], "0099685", 769),
        (24, "Se7en (1995)", "Crime|Mystery|Thriller", ["seven-deadly-sins", "serial-killer", "grim", "noir", "twists", "rain", "disturbing", "detective"], "0114388", 807),
        (25, "The Silence of the Lambs (1991)", "Crime|Drama|Thriller", ["hannibal-lecter", "fbi", "psychological", "suspense", "chilling", "iconic", "taut"], "0102926", 274),

        # Uplifting / Romantic / Feel-Good / Animation
        (26, "Spirited Away (2001)", "Animation|Adventure|Fantasy", ["studio-ghibli", "miyazaki", "whimsical", "spirits", "charming", "coming-of-age", "magical"], "0245429", 129),
        (27, "Amélie (2001)", "Comedy|Romance", ["quirky", "paris", "whimsical", "feel-good", "charming", "sweet", "romantic", "colorful"], "0211915", 194),
        (28, "Toy Story (1995)", "Adventure|Animation|Children|Comedy|Fantasy", ["pixar", "toys", "friendship", "nostalgic", "family", "charming", "fun"], "0114709", 862),
        (29, "WALL-E (2008)", "Animation|Adventure|Comedy|Romance|Sci-Fi", ["robot", "earth", "sweet", "environmental", "charming", "silent-film", "hopeful"], "0910970", 10681),
        (30, "La La Land (2016)", "Comedy|Drama|Musical|Romance", ["jazz", "hollywood", "dreamers", "bittersweet", "music", "colorful", "romantic"], "3783958", 313369),
        (31, "Before Sunrise (1995)", "Drama|Romance", ["vienna", "dialogue-driven", "intimate", "connection", "walking", "poetic", "youth"], "0112471", 76),
        (32, "Before Sunset (2004)", "Drama|Romance", ["reunion", "paris", "conversation", "maturity", "poignant", "real-time", "romantic"], "0381681", 80),
        (33, "Paddington 2 (2017)", "Adventure|Children|Comedy", ["feel-good", "whimsical", "gentle", "charming", "marmalade", "kindness", "pure-joy"], "4468740", 346648),
        (34, "Up (2009)", "Animation|Adventure|Children|Drama", ["pixar", "balloons", "adventure", "grief", "heartwarming", "emotional", "uplifting"], "1049413", 14160),
        (35, "Singin' in the Rain (1952)", "Comedy|Musical|Romance", ["classic", "dance", "joyful", "golden-age", "hollywood", "cheerful", "upbeat"], "0045152", 872),

        # Thoughtful / Philosophical / Psychological
        (36, "Eternal Sunshine of the Spotless Mind (2004)", "Drama|Romance|Sci-Fi", ["memory-erasure", "heartbreak", "kaufman", "surreal", "inventive", "poignant"], "0338013", 38),
        (37, "Memento (2000)", "Mystery|Thriller", ["amnesia", "reverse-chronology", "nolan", "intricate", "polaroids", "deception", "clever"], "0209144", 77),
        (38, "Her (2013)", "Drama|Romance|Sci-Fi", ["artificial-intelligence", "loneliness", "future-love", "tender", "melancholy", "intimate"], "1798709", 152601),
        (39, "Whiplash (2014)", "Drama|Musical", ["jazz", "obsession", "drumming", "mentor-student", "perfection", "intense", "electrifying"], "2582802", 244786),
        (40, "Stalker (1979)", "Drama|Sci-Fi", ["the-zone", "tarkovsky", "philosophical", "existential", "contemplative", "mysterious", "meditative"], "0079944", 1398),
        (41, "2001: A Space Odyssey (1968)", "Adventure|Mystery|Sci-Fi", ["hal-9000", "monolith", "evolution", "space", "kubrick", "monumental", "visionary"], "0062622", 62),
        (42, "Blade Runner (1982)", "Film-Noir|Sci-Fi|Thriller", ["cyberpunk", "replicants", "rain", "tears-in-rain", "vangelis", "cult", "neo-noir"], "0083658", 78),
        (43, "Alien (1979)", "Horror|Sci-Fi", ["xenomorph", "isolation", "nostromo", "ripley", "claustrophobic", "terror", "space-truckers"], "0078748", 348),
        (44, "Apocalypse Now (1979)", "Drama|War", ["vietnam", "madness", "journey", "surreal", "river", "horror", "coppola", "hypnotic"], "0078788", 28),
        (45, "Taxi Driver (1976)", "Crime|Drama", ["alienation", "urban-decay", "insomnia", "vigilante", "scorsese", "loneliness", "psychological"], "0075314", 103),

        # Comedy / Satire / Dark Comedy
        (46, "The Grand Budapest Hotel (2014)", "Adventure|Comedy|Drama", ["wes-anderson", "quirky", "symmetrical", "witty", "concierge", "charming", "nostalgic"], "2278388", 120467),
        (47, "Fargo (1996)", "Comedy|Crime|Drama|Thriller", ["coen-brothers", "snow", "minnesota", "dark-comedy", "kidnapping", "pregnant-cop", "quirky"], "0116282", 275),
        (48, "The Big Lebowski (1998)", "Comedy|Crime", ["the-dude", "bowling", "rug", "coen-brothers", "cult", "hilarious", "slacker", "laid-back"], "0118715", 115),
        (49, "Dr. Strangelove (1964)", "Comedy|War", ["satire", "nuclear-war", "cold-war", "kubrick", "black-comedy", "absurd", "iconic"], "0057012", 935),
        (50, "Monty Python and the Holy Grail (1975)", "Adventure|Comedy|Fantasy", ["satire", "arthurian", "absurd", "slapstick", "cult", "hilarious", "british-humour"], "0071853", 762),

        # Action / Thriller / Mystery
        (51, "Mad Max: Fury Road (2015)", "Action|Adventure|Sci-Fi", ["post-apocalyptic", "high-octane", "desert", "practical-effects", "furious", "kinetic"], "1392190", 76341),
        (52, "Zodiac (2007)", "Crime|Drama|Mystery|Thriller", ["obsession", "serial-killer", "journalism", "fincher", "unresolved", "meticulous", "suspense"], "0443706", 1923),
        (53, "Shutter Island (2010)", "Drama|Mystery|Thriller", ["asylum", "paranoia", "twist-ending", "scorsese", "psychological", "storm", "eerie"], "1130884", 11324),
        (54, "No Country for Old Men (2007)", "Crime|Drama|Thriller", ["anton-chigurh", "texas", "fate", "coen-brothers", "tension", "ruthless", "cat-and-mouse"], "0477348", 6977),
        (55, "Prisoners (2013)", "Crime|Drama|Mystery|Thriller", ["abduction", "morality", "rain", "fincher-esque", "villeneuve", "suspenseful", "dark"], "1392214", 146233),

        # Relaxed / Contemplative / Documentaries
        (56, "My Neighbor Totoro (1988)", "Animation|Children|Fantasy", ["studio-ghibli", "totoro", "gentle", "nature", "peaceful", "sweet", "childhood"], "0096283", 8392),
        (57, "Paterson (2016)", "Comedy|Drama|Romance", ["poetry", "daily-routine", "calm", "bus-driver", "gentle", "slice-of-life", "peaceful"], "5247022", 370755),
        (58, "Baraka (1992)", "Documentary", ["non-verbal", "humanity", "nature", "meditative", "hypnotic", "transcendent", "visual-poem"], "0103767", 1230),
        (59, "Samsara (2011)", "Documentary", ["visual-masterpiece", "global", "meditation", "spiritual", "rhythm", "sublime", "nature"], "0770802", 89708),
        (60, "Won't You Be My Neighbor? (2018)", "Documentary", ["mr-rogers", "kindness", "empathy", "heartwarming", "inspiring", "uplifting", "gentle"], "7681902", 490004)
    ]

    # 1. movies.csv
    df_movies = pd.DataFrame([
        {"movieId": m[0], "title": m[1], "genres": m[2]}
        for m in movies_data
    ])
    df_movies.to_csv(os.path.join(output_dir, "movies.csv"), index=False)

    # 2. links.csv
    df_links = pd.DataFrame([
        {"movieId": m[0], "imdbId": m[4], "tmdbId": m[5]}
        for m in movies_data
    ])
    df_links.to_csv(os.path.join(output_dir, "links.csv"), index=False)

    # 3. tags.csv
    tag_records = []
    base_timestamp = 1500000000
    for m in movies_data:
        movie_id = m[0]
        tags = m[3]
        for idx, tag in enumerate(tags):
            user_id = (idx % 20) + 1
            ts = base_timestamp + (movie_id * 1000) + (idx * 60)
            tag_records.append({
                "userId": user_id,
                "movieId": movie_id,
                "tag": tag,
                "timestamp": ts
            })
    df_tags = pd.DataFrame(tag_records)
    df_tags.to_csv(os.path.join(output_dir, "tags.csv"), index=False)

    # 4. ratings.csv
    # Generate ~3,500 realistic ratings from 120 users
    # We assign distinct user taste profiles (e.g., Sci-Fi buffs, Cinephile/Drama lovers, Animation/Family lovers)
    num_users = 120
    ratings_records = []

    for uid in range(1, num_users + 1):
        # Pick 20 to 45 movies rated by this user
        num_rated = random.randint(20, 45)
        # Cluster preference
        user_pref = uid % 4
        # 0: Sci-Fi & Noir fan
        # 1: Classic Drama & Crime fan
        # 2: Animation & Uplifting fan
        # 3: General Cinephile
        
        rated_movie_ids = random.sample(range(1, len(movies_data) + 1), num_rated)
        for mid in rated_movie_ids:
            movie_entry = movies_data[mid - 1]
            genres = movie_entry[2]
            
            # Base rating around 3.5 - 4.0
            base = 3.5 + np.random.normal(0, 0.4)
            if user_pref == 0 and ("Sci-Fi" in genres or "Film-Noir" in genres):
                base += 0.8
            elif user_pref == 1 and ("Drama" in genres or "Crime" in genres):
                base += 0.8
            elif user_pref == 2 and ("Animation" in genres or "Children" in genres or "Romance" in genres):
                base += 0.9
            elif user_pref == 3:
                base += 0.4

            # Snap to valid MovieLens 0.5 increments [0.5, 5.0]
            rating = round(base * 2) / 2
            rating = max(0.5, min(5.0, rating))
            ts = base_timestamp + random.randint(1000, 10000000)
            ratings_records.append({
                "userId": uid,
                "movieId": mid,
                "rating": rating,
                "timestamp": ts
            })

    df_ratings = pd.DataFrame(ratings_records)
    df_ratings.to_csv(os.path.join(output_dir, "ratings.csv"), index=False)

    print(f"Created dev dataset in {output_dir}:")
    print(f"  movies: {len(df_movies)}")
    print(f"  ratings: {len(df_ratings)} across {num_users} users")
    print(f"  tags: {len(df_tags)}")
    print(f"  links: {len(df_links)}")

if __name__ == "__main__":
    out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "dev"))
    create_dev_dataset(out)
