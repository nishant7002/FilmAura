"""
FilmAura — Verified Cinema Dataset Loader & Artifact Manager
Loads curated, high-precision cinephile dataset and handles artifact export/caching.
"""

import os
import json
import pandas as pd
import numpy as np

ARTIFACTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "artifacts")

RAW_MOVIES = [
    {
        "id": "children-of-men-2006",
        "title": "Children of Men",
        "year": 2006,
        "runtime": 109,
        "genres": ["Sci-Fi", "Thriller", "Drama"],
        "rating": 8.0,
        "votes": 520000,
        "director": "Alfonso Cuarón",
        "director_title": "Academy Award Winner & Co-Writer",
        "cinematographer": "Emmanuel Lubezki",
        "cinematographer_title": "Master of Single-Takes",
        "cast": [
            {"name": "Clive Owen", "role": "Theo Faron", "category": "Lead Role"},
            {"name": "Julianne Moore", "role": "Julian Taylor", "category": "Supporting"},
            {"name": "Chiwetel Ejiofor", "role": "Luke", "category": "Fishes Cell Leader"}
        ],
        "synopsis": "In 2027, in a chaotic world in which women have inexplicably become infertile for two decades, a former activist agrees to help transport a miraculously pregnant woman across a heavily fortified, xenophobic United Kingdom to a sanctuary at sea.\n\nFeaturing groundbreaking unbroken sequence shots and intense documentary realism, Cuarón constructs an urgent, harrowing, yet poetically tender meditation on hope, faith, and human preservation amidst absolute societal collapse.",
        "stream_provider": "Prime Video",
        "quality_badge": "4K Remastered",
        "age_rating": "R",
        "trailer_url": "https://www.youtube.com/watch?v=2VT2apoX1zp",
        "similar_ids": ["1917-2019", "snowpiercer-2013", "the-road-2009"],
        "similar_reasons": {
            "1917-2019": "Direct cinematic kin of Cuarón & Lubezki's continuous visual choreography.",
            "snowpiercer-2013": "Bong Joon-ho's unrelenting allegory of dystopian survival and rebellion.",
            "the-road-2009": "Uncompromising parental devotion within a barren earth."
        },
        "moods": {
            "dark": 0.95, "suspenseful": 0.92, "thoughtful": 0.88, "emotional": 0.82,
            "adventurous": 0.65, "motivational": 0.50, "romantic": 0.20, "relaxed": 0.05,
            "happy": 0.05, "funny": 0.02
        },
        "keywords": "dystopian infertility single-take bleak hyper-kinetic survival human-preservation london"
    },
    {
        "id": "blade-runner-2049-2017",
        "title": "Blade Runner 2049",
        "year": 2017,
        "runtime": 164,
        "genres": ["Sci-Fi", "Mystery", "Drama"],
        "rating": 8.0,
        "votes": 620000,
        "director": "Denis Villeneuve",
        "director_title": "Visionary World-Builder",
        "cinematographer": "Roger Deakins",
        "cinematographer_title": "Academy Award Winner for Best Cinematography",
        "cast": [
            {"name": "Ryan Gosling", "role": "Officer K", "category": "Lead Role"},
            {"name": "Harrison Ford", "role": "Rick Deckard", "category": "Legendary Blade Runner"},
            {"name": "Ana de Armas", "role": "Joi", "category": "AI Companion"}
        ],
        "synopsis": "Thirty years after the events of the first film, a new Blade Runner, LAPD Officer K, unearths a long-buried secret that has the potential to plunge what's left of society into chaos. K's discovery leads him on a quest to find Rick Deckard, a former LAPD blade runner who has been missing for three decades.\n\nVilleneuve crafts a monumental, visually transcendent neo-noir masterpiece exploring identity, artificial consciousness, and spiritual longing in a rain-drenched, neon wasteland.",
        "stream_provider": "Max",
        "quality_badge": "4K HDR Dolby Atmos",
        "age_rating": "R",
        "trailer_url": "https://www.youtube.com/watch?v=gCcx85zbxz4",
        "similar_ids": ["dark-city-1998", "ex-machina-2014", "children-of-men-2006"],
        "similar_reasons": {
            "dark-city-1998": "Architectural neon noir drenched in existential identity manipulation.",
            "ex-machina-2014": "Intimate philosophical interrogation of artificial soul and sentience.",
            "children-of-men-2006": "Bleak atmospheric dystopia anchored by profound sensory realism."
        },
        "moods": {
            "dark": 0.90, "thoughtful": 0.96, "suspenseful": 0.85, "emotional": 0.78,
            "romantic": 0.60, "adventurous": 0.50, "motivational": 0.40, "relaxed": 0.30,
            "happy": 0.10, "funny": 0.05
        },
        "keywords": "cyberpunk neo-noir replicant existential memory artificial-intelligence rainy-los-angeles neon"
    },
    {
        "id": "ex-machina-2014",
        "title": "Ex Machina",
        "year": 2014,
        "runtime": 108,
        "genres": ["Sci-Fi", "Psychological Thriller", "Mystery"],
        "rating": 7.7,
        "votes": 580000,
        "director": "Alex Garland",
        "director_title": "Screenwriter & Director",
        "cinematographer": "Rob Hardy",
        "cinematographer_title": "Director of Photography",
        "cast": [
            {"name": "Alicia Vikander", "role": "Ava", "category": "Turing Test Subject"},
            {"name": "Domhnall Gleeson", "role": "Caleb Smith", "category": "Programmer Evaluator"},
            {"name": "Oscar Isaac", "role": "Nathan Bateman", "category": "Eccentric Tech CEO"}
        ],
        "synopsis": "A 26-year-old coder at the world's largest internet company wins a week-long competition to conduct a Turing test at a private mountain retreat belonging to the company's reclusive CEO. But as Caleb interacts with Ava, a breathtaking artificial intelligence, the experiment spirals into a claustrophobic psychological battlefield of deception and manipulation.",
        "stream_provider": "Max",
        "quality_badge": "4K Ultra HD",
        "age_rating": "R",
        "trailer_url": "https://www.youtube.com/watch?v=bggUmGEkgTU",
        "similar_ids": ["blade-runner-2049-2017", "annihilation-2018", "her-2013"],
        "similar_reasons": {
            "blade-runner-2049-2017": "Fascinating examination of whether synthetic consciousness deserves empathy.",
            "annihilation-2018": "Alex Garland's trademark atmospheric dread and scientific curiosity.",
            "her-2013": "Thoughtful, intimate inquiry into digital vulnerability and emotional attachment."
        },
        "moods": {
            "suspenseful": 0.93, "thoughtful": 0.95, "dark": 0.80, "emotional": 0.60,
            "romantic": 0.45, "adventurous": 0.20, "motivational": 0.30, "relaxed": 0.25,
            "happy": 0.05, "funny": 0.10
        },
        "keywords": "ai artificial-intelligence turing-test manipulation claustrophobic isolated-facility android"
    },
    {
        "id": "dark-city-1998",
        "title": "Dark City: Director's Cut",
        "year": 1998,
        "runtime": 111,
        "genres": ["Neo-Noir", "Mystery", "Sci-Fi"],
        "rating": 7.6,
        "votes": 210000,
        "director": "Alex Proyas",
        "director_title": "Cult Visionary",
        "cinematographer": "Dariusz Wolski",
        "cinematographer_title": "Director of Photography",
        "cast": [
            {"name": "Rufus Sewell", "role": "John Murdoch", "category": "Awakened Protagonist"},
            {"name": "William Hurt", "role": "Inspector Frank Bumstead", "category": "Investigator"},
            {"name": "Jennifer Connelly", "role": "Emma Murdoch", "category": "Lounge Singer & Wife"}
        ],
        "synopsis": "A man awakes alone in a strange hotel with no memory of his past, only to discover that he is wanted for a series of brutal murders. While seeking to piece together his identity, he discovers a bizarre underworld run by mysterious beings known as The Strangers who alter the city and residents' memories each midnight.",
        "stream_provider": "Rent on Apple TV / Vudu",
        "quality_badge": "Director's Cut Remastered",
        "age_rating": "R",
        "trailer_url": "https://www.youtube.com/watch?v=gt9HkO-cGGo",
        "similar_ids": ["blade-runner-2049-2017", "children-of-men-2006", "the-lighthouse-2019"],
        "similar_reasons": {
            "blade-runner-2049-2017": "Shared visual lineage of rain-slicked existential neo-noir architecture.",
            "children-of-men-2006": "Unflinching journey through an alienating urban labyrinth.",
            "the-lighthouse-2019": "Psychological descent into unreliable perception and nocturnal delirium."
        },
        "moods": {
            "dark": 0.94, "suspenseful": 0.89, "thoughtful": 0.86, "emotional": 0.65,
            "adventurous": 0.45, "romantic": 0.40, "motivational": 0.35, "relaxed": 0.10,
            "happy": 0.05, "funny": 0.02
        },
        "keywords": "memory-loss the-strangers midnight-tuning neo-noir eternal-night identity-manipulation"
    },
    {
        "id": "annihilation-2018",
        "title": "Annihilation",
        "year": 2018,
        "runtime": 115,
        "genres": ["Sci-Fi", "Cosmic Horror", "Mystery"],
        "rating": 6.9,
        "votes": 350000,
        "director": "Alex Garland",
        "director_title": "Director & Adaptor",
        "cinematographer": "Rob Hardy",
        "cinematographer_title": "Director of Photography",
        "cast": [
            {"name": "Natalie Portman", "role": "Lena", "category": "Biologist & Former Soldier"},
            {"name": "Jennifer Jason Leigh", "role": "Dr. Ventress", "category": "Psychologist Expedition Leader"},
            {"name": "Oscar Isaac", "role": "Kane", "category": "Sole Returning Soldier"}
        ],
        "synopsis": "A biologist signs up for a dangerous, secret expedition into a mysterious quarantined coastal environmental zone known as 'The Shimmer', where the laws of nature do not apply and mutations are spreading uncontrollably. As the all-female scientific team journeys deeper into the kaleidoscopic wilderness, they encounter terror that refracts their own psychological trauma.",
        "stream_provider": "Paramount+",
        "quality_badge": "4K Dolby Vision",
        "age_rating": "R",
        "trailer_url": "https://www.youtube.com/watch?v=89OP78l9oF0",
        "similar_ids": ["ex-machina-2014", "stalker-1979", "arrival-2016"],
        "similar_reasons": {
            "ex-machina-2014": "Garland's cerebral blend of hard biological science and existential terror.",
            "stalker-1979": "The definitive philosophical expedition into an inexplicable, mystical anomaly.",
            "arrival-2016": "Transcendental non-human intelligence reshaping the human consciousness."
        },
        "moods": {
            "dark": 0.92, "suspenseful": 0.90, "thoughtful": 0.88, "emotional": 0.70,
            "adventurous": 0.55, "romantic": 0.30, "motivational": 0.20, "relaxed": 0.10,
            "happy": 0.02, "funny": 0.01
        },
        "keywords": "the-shimmer cellular-mutation cosmic-horror biological-anomaly lighthouse grief refraction"
    },
    {
        "id": "1917-2019",
        "title": "1917",
        "year": 2019,
        "runtime": 119,
        "genres": ["War", "Drama", "Action"],
        "rating": 8.2,
        "votes": 640000,
        "director": "Sam Mendes",
        "director_title": "Academy Award Winner",
        "cinematographer": "Roger Deakins",
        "cinematographer_title": "Academy Award for Best Cinematography",
        "cast": [
            {"name": "George MacKay", "role": "Lance Corporal Schofield", "category": "Lead Dispatch Runner"},
            {"name": "Dean-Charles Chapman", "role": "Lance Corporal Blake", "category": "Messenger Companion"},
            {"name": "Mark Strong", "role": "Captain Smith", "category": "Allied Officer"}
        ],
        "synopsis": "During World War I, two young British soldiers are assigned to deliver an impossible, time-critical message through enemy territory that will save 1,600 of their comrades from walking directly into a deadly ambush. Filmed to appear as one continuous unbroken shot, the journey is an unprecedented feat of visceral immersion.",
        "stream_provider": "Showtime / Paramount+",
        "quality_badge": "4K Ultra HD",
        "age_rating": "R",
        "trailer_url": "https://www.youtube.com/watch?v=YqNYrYUiMfg",
        "similar_ids": ["children-of-men-2006", "dunkirk-2017", "the-road-2009"],
        "similar_reasons": {
            "children-of-men-2006": "Kinetic camera choreography tracking human survival against all odds.",
            "dunkirk-2017": "Ticking-clock tension where sound and pacing mimic pure adrenaline.",
            "the-road-2009": "Devastating landscape traversed by two souls united in duty."
        },
        "moods": {
            "suspenseful": 0.96, "emotional": 0.88, "motivational": 0.85, "dark": 0.75,
            "adventurous": 0.80, "thoughtful": 0.70, "romantic": 0.10, "relaxed": 0.05,
            "happy": 0.15, "funny": 0.05
        },
        "keywords": "world-war-one continuous-take no-mans-land mission-against-time survival trench-warfare"
    },
    {
        "id": "snowpiercer-2013",
        "title": "Snowpiercer",
        "year": 2013,
        "runtime": 126,
        "genres": ["Action", "Sci-Fi", "Drama"],
        "rating": 7.1,
        "votes": 380000,
        "director": "Bong Joon-ho",
        "director_title": "Master of Class Allegory",
        "cinematographer": "Hong Kyung-pyo",
        "cinematographer_title": "Director of Photography",
        "cast": [
            {"name": "Chris Evans", "role": "Curtis Everett", "category": "Tail Section Rebel Leader"},
            {"name": "Song Kang-ho", "role": "Namgoong Minsu", "category": "Security Specialist"},
            {"name": "Tilda Swinton", "role": "Minister Mason", "category": "Front Section Propagandist"}
        ],
        "synopsis": "In a future where a failed climate-change experiment has plunged the Earth into a new ice age, the only human survivors inhabit a perpetually moving globe-spanning train called Snowpiercer. A rigid class system divides the train, until Curtis leads the desperate tail-section passengers in an armed revolution toward the engine.",
        "stream_provider": "Hulu",
        "quality_badge": "1080p HD",
        "age_rating": "R",
        "trailer_url": "https://www.youtube.com/watch?v=nX5PwfEMBM0",
        "similar_ids": ["children-of-men-2006", "parasite-2019", "mad-max-fury-road-2015"],
        "similar_reasons": {
            "children-of-men-2006": "Relentless sociopolitical rebellion through claustrophobic corridors.",
            "parasite-2019": "Bong Joon-ho's cutting razor-sharp dissection of class stratification.",
            "mad-max-fury-road-2015": "Perpetual motion vehicle kinetics driving explosive revolution."
        },
        "moods": {
            "suspenseful": 0.94, "dark": 0.88, "thoughtful": 0.85, "motivational": 0.80,
            "adventurous": 0.82, "emotional": 0.70, "funny": 0.35, "romantic": 0.10,
            "relaxed": 0.05, "happy": 0.05
        },
        "keywords": "perpetual-train ice-age class-revolution engine wilford rebellion dystopian-train"
    },
    {
        "id": "the-road-2009",
        "title": "The Road",
        "year": 2009,
        "runtime": 111,
        "genres": ["Drama", "Survival", "Thriller"],
        "rating": 7.2,
        "votes": 250000,
        "director": "John Hillcoat",
        "director_title": "Director",
        "cinematographer": "Javier Aguirresarobe",
        "cinematographer_title": "Director of Photography",
        "cast": [
            {"name": "Viggo Mortensen", "role": "The Man", "category": "Father & Protector"},
            {"name": "Kodi Smit-McPhee", "role": "The Boy", "category": "Son & Moral Anchor"},
            {"name": "Charlize Theron", "role": "The Woman", "category": "Memory & Flashback"}
        ],
        "synopsis": "In a post-apocalyptic ash-covered world where all flora and fauna have died, an ailing father and his young son walk along a desolate road toward the southern coast, pushing their meager possessions in a shopping cart. Amidst cannibalistic gangs and freezing winds, the father strives to keep the fire of humanity alive in his son.",
        "stream_provider": "Tubi / Prime Video",
        "quality_badge": "1080p HD",
        "age_rating": "R",
        "trailer_url": "https://www.youtube.com/watch?v=94KcI0gLqq1",
        "similar_ids": ["children-of-men-2006", "1917-2019", "arrival-2016"],
        "similar_reasons": {
            "children-of-men-2006": "Uncompromising parental devotion within an ash-covered extinction event.",
            "1917-2019": "A grueling foot journey across treacherous desolation driven by love.",
            "arrival-2016": "Profound melancholy balanced by the sanctity of parenthood."
        },
        "moods": {
            "dark": 0.98, "emotional": 0.95, "suspenseful": 0.88, "thoughtful": 0.85,
            "motivational": 0.60, "adventurous": 0.40, "romantic": 0.20, "relaxed": 0.05,
            "happy": 0.02, "funny": 0.01
        },
        "keywords": "cormac-mccarthy post-apocalyptic ash shopping-cart carrying-the-fire father-son survival"
    },
    {
        "id": "arrival-2016",
        "title": "Arrival",
        "year": 2016,
        "runtime": 116,
        "genres": ["Sci-Fi", "Drama", "Mystery"],
        "rating": 7.9,
        "votes": 730000,
        "director": "Denis Villeneuve",
        "director_title": "Director",
        "cinematographer": "Bradford Young",
        "cinematographer_title": "Director of Photography",
        "cast": [
            {"name": "Amy Adams", "role": "Dr. Louise Banks", "category": "Linguistics Professor"},
            {"name": "Jeremy Renner", "role": "Ian Donnelly", "category": "Theoretical Physicist"},
            {"name": "Forest Whitaker", "role": "Colonel Weber", "category": "Military Liaison"}
        ],
        "synopsis": "Linguistics professor Louise Banks leads an elite team of investigators when twelve mysterious extraterrestrial spacecraft touch down across the globe. As nations teeter on the verge of global war, Banks races against time to learn the language of the alien visitors, uncovering a revelation that shatters linear perception of time, memory, and love.",
        "stream_provider": "Paramount+",
        "quality_badge": "4K Dolby Vision",
        "age_rating": "PG-13",
        "trailer_url": "https://www.youtube.com/watch?v=tFMo3UJ4B4g",
        "similar_ids": ["blade-runner-2049-2017", "interstellar-2014", "annihilation-2018"],
        "similar_reasons": {
            "blade-runner-2049-2017": "Villeneuve's signature contemplative pacing and emotional gravity.",
            "interstellar-2014": "Transcendent cosmic connection bending time and grief.",
            "annihilation-2018": "Encounter with the sublime unknown altering human biology and consciousness."
        },
        "moods": {
            "thoughtful": 0.98, "emotional": 0.92, "cosmic_awe": 0.95, "suspenseful": 0.75,
            "romantic": 0.65, "relaxed": 0.40, "motivational": 0.70, "dark": 0.40,
            "happy": 0.30, "funny": 0.05
        },
        "keywords": "heptapod non-linear-time linguistics alien-contact sapir-whorf memory grief communication"
    },
    {
        "id": "drive-2011",
        "title": "Drive",
        "year": 2011,
        "runtime": 100,
        "genres": ["Neo-Noir", "Crime", "Action"],
        "rating": 7.8,
        "votes": 690000,
        "director": "Nicolas Winding Refn",
        "director_title": "Best Director Cannes Winner",
        "cinematographer": "Newton Thomas Sigel",
        "cinematographer_title": "Director of Photography",
        "cast": [
            {"name": "Ryan Gosling", "role": "The Driver", "category": "Hollywood Stuntman & Getaway Driver"},
            {"name": "Carey Mulligan", "role": "Irene", "category": "Neighbor & Mother"},
            {"name": "Bryan Cranston", "role": "Shannon", "category": "Garage Owner"}
        ],
        "synopsis": "A mysterious Hollywood stunt performer who moonlights as a getaway driver finds himself the target of ruthless crime bosses after he helps his ex-convict neighbor protect her son. Set against a hypnotic synth-wave score and neon Los Angeles shadows, Refn creates an iconic modern fairy tale of chivalry and brutal vengeance.",
        "stream_provider": "Netflix",
        "quality_badge": "1080p HD",
        "age_rating": "R",
        "trailer_url": "https://www.youtube.com/watch?v=KBiOF3y1W0Y",
        "similar_ids": ["blade-runner-2049-2017", "nightcrawler-2014", "dark-city-1998"],
        "similar_reasons": {
            "blade-runner-2049-2017": "Ryan Gosling's stoic, romantic protector archetype in neon twilight.",
            "nightcrawler-2014": "Predatory nocturnal LA streets captured with pulsing synth energy.",
            "dark-city-1998": "Stylized noir shadows masking eruptive violence and tenderness."
        },
        "moods": {
            "dark": 0.88, "romantic": 0.85, "suspenseful": 0.89, "thoughtful": 0.75,
            "motivational": 0.60, "adventurous": 0.70, "relaxed": 0.30, "emotional": 0.70,
            "happy": 0.15, "funny": 0.05
        },
        "keywords": "getaway-driver scorpion-jacket synthwave neon-la elevator-scene chivalry organized-crime"
    },
    {
        "id": "interstellar-2014",
        "title": "Interstellar",
        "year": 2014,
        "runtime": 169,
        "genres": ["Sci-Fi", "Adventure", "Drama"],
        "rating": 8.7,
        "votes": 2100000,
        "director": "Christopher Nolan",
        "director_title": "Director & Co-Writer",
        "cinematographer": "Hoyte van Hoytema",
        "cinematographer_title": "Director of Photography",
        "cast": [
            {"name": "Matthew McConaughey", "role": "Cooper", "category": "Former NASA Pilot"},
            {"name": "Anne Hathaway", "role": "Dr. Amelia Brand", "category": "Astrophysicist"},
            {"name": "Jessica Chastain", "role": "Murph Cooper", "category": "Physicist Daughter"}
        ],
        "synopsis": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Cooper, is tasked to pilot a spacecraft along with a team of researchers through a newly discovered wormhole near Saturn to find a new home for mankind.",
        "stream_provider": "Prime Video",
        "quality_badge": "4K Ultra HD",
        "age_rating": "PG-13",
        "trailer_url": "https://www.youtube.com/watch?v=zSWdZVtXT7E",
        "similar_ids": ["arrival-2016", "inception-2010", "solaris-1972"],
        "similar_reasons": {
            "arrival-2016": "Deep emotional father-daughter bond transcending time and astrophysics.",
            "inception-2010": "Nolan's signature grand intellectual scale and Hans Zimmer score.",
            "solaris-1972": "Cosmic solitude and human consciousness reflected in the void."
        },
        "moods": {
            "thoughtful": 0.95, "emotional": 0.95, "adventurous": 0.92, "motivational": 0.90,
            "suspenseful": 0.88, "dark": 0.60, "romantic": 0.50, "relaxed": 0.20,
            "happy": 0.40, "funny": 0.15
        },
        "keywords": "black-hole wormhole gargantua relativity tesseract hans-zimmer stay-murph"
    },
    {
        "id": "parasite-2019",
        "title": "Parasite",
        "year": 2019,
        "runtime": 132,
        "genres": ["Comedy", "Drama", "Thriller"],
        "rating": 8.5,
        "votes": 920000,
        "director": "Bong Joon-ho",
        "director_title": "4x Academy Award Winner",
        "cinematographer": "Hong Kyung-pyo",
        "cinematographer_title": "Director of Photography",
        "cast": [
            {"name": "Song Kang-ho", "role": "Kim Ki-taek", "category": "Kim Family Patriarch"},
            {"name": "Lee Sun-kyun", "role": "Park Dong-ik", "category": "Tech CEO Father"},
            {"name": "Cho Yeo-jeong", "role": "Park Yeon-gyo", "category": "Wealthy Matriarch"}
        ],
        "synopsis": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan, who systematically scheme to become employed by the Parks one by one.",
        "stream_provider": "Max",
        "quality_badge": "4K UHD",
        "age_rating": "R",
        "trailer_url": "https://www.youtube.com/watch?v=5xH0RZE9jp4",
        "similar_ids": ["snowpiercer-2013", "the-grand-budapest-hotel-2014", "whiplash-2014"],
        "similar_reasons": {
            "snowpiercer-2013": "Bong Joon-ho's razor-sharp social satire and structural class architecture.",
            "the-grand-budapest-hotel-2014": "Immaculate production design and tonal balance of wit and gravity.",
            "whiplash-2014": "Mounting psychological pressure that explodes in an exhilarating climax."
        },
        "moods": {
            "suspenseful": 0.95, "thoughtful": 0.92, "funny": 0.80, "dark": 0.85,
            "emotional": 0.70, "motivational": 0.40, "adventurous": 0.50, "relaxed": 0.15,
            "happy": 0.25, "romantic": 0.10
        },
        "keywords": "palme-dor class-satire architectural-suspense basement ram-don seoul"
    },
    {
        "id": "the-lighthouse-2019",
        "title": "The Lighthouse",
        "year": 2019,
        "runtime": 109,
        "genres": ["Psychological Horror", "Mystery", "Drama"],
        "rating": 7.4,
        "votes": 250000,
        "director": "Robert Eggers",
        "director_title": "Visionary Director",
        "cinematographer": "Jarin Blaschke",
        "cinematographer_title": "Nominated for Best Cinematography",
        "cast": [
            {"name": "Willem Dafoe", "role": "Thomas Wake", "category": "Veteran Lighthouse Keeper"},
            {"name": "Robert Pattinson", "role": "Ephraim Winslow", "category": "New Assistant Keeper"}
        ],
        "synopsis": "In a remote New England island in the 1890s, two lighthouse keepers attempt to maintain their sanity while surviving a raging storm, mounting paranoia, and bizarre hallucinatory visions of mermaids and sirens.",
        "stream_provider": "Max",
        "quality_badge": "1.19:1 35mm B&W",
        "age_rating": "R",
        "trailer_url": "https://www.youtube.com/watch?v=Hyag7lR8CPA",
        "similar_ids": ["dark-city-1998", "annihilation-2018", "solaris-1972"],
        "similar_reasons": {
            "dark-city-1998": "Hallucinatory nocturnal descent into altered states of reality.",
            "annihilation-2018": "Psychological refraction of guilt and madness in an isolated post.",
            "solaris-1972": "Two men isolated against cosmic forces that manifest their subconscious."
        },
        "moods": {
            "dark": 0.98, "suspenseful": 0.91, "funny": 0.65, "thoughtful": 0.85,
            "emotional": 0.50, "adventurous": 0.30, "motivational": 0.10, "relaxed": 0.05,
            "happy": 0.05, "romantic": 0.02
        },
        "keywords": "black-and-white 35mm sea-shanties lobster mermaid insanity isolation"
    },
    {
        "id": "solaris-1972",
        "title": "Solaris",
        "year": 1972,
        "runtime": 167,
        "genres": ["Sci-Fi", "Mystery", "Drama"],
        "rating": 8.0,
        "votes": 100000,
        "director": "Andrei Tarkovsky",
        "director_title": "Master of Poetic Cinema",
        "cinematographer": "Vadim Yusov",
        "cinematographer_title": "Director of Photography",
        "cast": [
            {"name": "Donatas Banionis", "role": "Kris Kelvin", "category": "Psychologist"},
            {"name": "Natalya Bondarchuk", "role": "Hari", "category": "Manifested Wife"}
        ],
        "synopsis": "A psychologist is sent to a space station orbiting a mysterious ocean planet called Solaris to investigate the emotional breakdown of the crew, only to be confronted by the living physical incarnation of his late wife.",
        "stream_provider": "Criterion Channel",
        "quality_badge": "Criterion Collection Restored",
        "age_rating": "PG",
        "trailer_url": "https://www.youtube.com/watch?v=6-4KydP92ss",
        "similar_ids": ["blade-runner-2049-2017", "arrival-2016", "interstellar-2014"],
        "similar_reasons": {
            "blade-runner-2049-2017": "Profound poetic inquiry into human emotion, memory, and love.",
            "arrival-2016": "Transcendental contact with an incomprehensible consciousness.",
            "interstellar-2014": "Existential grief echoing across the silence of deep space."
        },
        "moods": {
            "thoughtful": 0.99, "emotional": 0.90, "dark": 0.75, "relaxed": 0.65,
            "romantic": 0.80, "suspenseful": 0.60, "adventurous": 0.35, "motivational": 0.30,
            "happy": 0.10, "funny": 0.01
        },
        "keywords": "ocean-planet memory grief conscious-planet contemplation stanislaw-lem"
    },
    {
        "id": "nightcrawler-2014",
        "title": "Nightcrawler",
        "year": 2014,
        "runtime": 117,
        "genres": ["Crime", "Drama", "Thriller"],
        "rating": 7.8,
        "votes": 590000,
        "director": "Dan Gilroy",
        "director_title": "Writer & Director",
        "cinematographer": "Robert Elswit",
        "cinematographer_title": "Academy Award Winner",
        "cast": [
            {"name": "Jake Gyllenhaal", "role": "Louis Bloom", "category": "Freelance Stringer"},
            {"name": "Rene Russo", "role": "Nina Romina", "category": "News Director"},
            {"name": "Riz Ahmed", "role": "Rick", "category": "Assistant"}
        ],
        "synopsis": "When Louis Bloom, a driven young man desperate for work, discovers the cutthroat world of freelance crime journalism in nocturnal Los Angeles, he blurs the line between observer and participant to become the star of his own story.",
        "stream_provider": "Netflix",
        "quality_badge": "1080p HD",
        "age_rating": "R",
        "trailer_url": "https://www.youtube.com/watch?v=u1uP_8VJkU8",
        "similar_ids": ["drive-2011", "blade-runner-2049-2017", "dark-city-1998"],
        "similar_reasons": {
            "drive-2011": "Electric nocturnal LA neon and morally ambiguous antihero obsession.",
            "blade-runner-2049-2017": "Sleek metropolitan alienation and cold industrial rhythm.",
            "dark-city-1998": "Dark urban voyeurism and psychological manipulation."
        },
        "moods": {
            "dark": 0.94, "suspenseful": 0.96, "thoughtful": 0.80, "motivational": 0.50,
            "funny": 0.40, "emotional": 0.30, "adventurous": 0.40, "relaxed": 0.05,
            "romantic": 0.05, "happy": 0.02
        },
        "keywords": "stringer freelance-cameraman media-ethics police-scanner dodge-challenger los-angeles"
    }
]

def get_movies_dataframe() -> pd.DataFrame:
    """Returns the film catalogue as a clean Pandas DataFrame."""
    df = pd.DataFrame(RAW_MOVIES)
    return df

def ensure_artifacts_exist():
    """Generates and exports parquet / json cache files if not already present."""
    if not os.path.exists(ARTIFACTS_DIR):
        os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    
    csv_path = os.path.join(ARTIFACTS_DIR, "movies_catalogue.csv")
    if not os.path.exists(csv_path):
        df = get_movies_dataframe()
        # Save a flat version for easy reading
        df.to_csv(csv_path, index=False)
