import datetime

GENRES = [
    ("Alternative", "Alternative"),
    ("Blues", "Blues"),
    ("Classical", "Classical"),
    ("Country", "Country"),
    ("Electronic", "Electronic"),
    ("Folk", "Folk"),
    ("Funk", "Funk"),
    ("Hip-Hop", "Hip-Hop"),
    ("Heavy Metal", "Heavy Metal"),
    ("Instrumental", "Instrumental"),
    ("Jazz", "Jazz"),
    ("Musical Theatre", "Musical Theatre"),
    ("Pop", "Pop"),
    ("Punk", "Punk"),
    ("R&B", "R&B"),
    ("Reggae", "Reggae"),
    ("Rock n Roll", "Rock n Roll"),
    ("Soul", "Soul"),
    ("Swing", "Swing"),
    ("Other", "Other"),
]
STATES = [
    ("AL", "AL"),
    ("AK", "AK"),
    ("AZ", "AZ"),
    ("AR", "AR"),
    ("CA", "CA"),
    ("CO", "CO"),
    ("CT", "CT"),
    ("DE", "DE"),
    ("DC", "DC"),
    ("FL", "FL"),
    ("GA", "GA"),
    ("HI", "HI"),
    ("ID", "ID"),
    ("IL", "IL"),
    ("IN", "IN"),
    ("IA", "IA"),
    ("KS", "KS"),
    ("KY", "KY"),
    ("LA", "LA"),
    ("ME", "ME"),
    ("MT", "MT"),
    ("NE", "NE"),
    ("NV", "NV"),
    ("NH", "NH"),
    ("NJ", "NJ"),
    ("NM", "NM"),
    ("NY", "NY"),
    ("NC", "NC"),
    ("ND", "ND"),
    ("OH", "OH"),
    ("OK", "OK"),
    ("OR", "OR"),
    ("MD", "MD"),
    ("MA", "MA"),
    ("MI", "MI"),
    ("MN", "MN"),
    ("MS", "MS"),
    ("MO", "MO"),
    ("PA", "PA"),
    ("RI", "RI"),
    ("SC", "SC"),
    ("SD", "SD"),
    ("TN", "TN"),
    ("TX", "TX"),
    ("UT", "UT"),
    ("VT", "VT"),
    ("VA", "VA"),
    ("WA", "WA"),
    ("WV", "WV"),
    ("WI", "WI"),
    ("WY", "WY"),
]
GENRE_CHECK = [
    "Alternative",
    "Blues",
    "Classical",
    "Country",
    "Electronic",
    "Folk",
    "Funk",
    "Hip-Hop",
    "Heavy Metal",
    "Instrumental",
    "Jazz",
    "Musical Theatre",
    "Pop",
    "Punk",
    "R&B",
    "Reggae",
    "Rock n Roll",
    "Soul",
    "Swing",
    "Other",
]
ARTISTS = [
    {
        "id": 1004,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San "
        "Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c"
        "4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format"
        "&fit=crop&w=300&q=80",
        "date_created": datetime.date(2017, 4, 1)
    },
    {
        "id": 1005,
        "name": "Matt Quevedo",
        "genres": ["Jazz"],
        "city": "New York",
        "state": "NY",
        "phone": "300-400-5000",
        "facebook_link": "https://www.facebook.com/mattquevedo923251523",
        "seeking_venue": False,
        "image_link": "https://images.unsplash.com/photo-1495223153807-b"
        "916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMD"
        "d9&auto=format&fit=crop&w=334&q=80",
        "date_created": datetime.date(2018, 1, 28)
    },
    {
        "id": 1006,
        "name": "The Wild Sax Band",
        "genres": ["Jazz", "Classical"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "432-325-5432",
        "seeking_venue": False,
        "image_link": "https://images.unsplash.com/photo-1558369981-f9ca7846"
        "2e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=fo"
        "rmat&fit=crop&w=794&q=80",
        "date_created": datetime.date(2016, 5, 12)
    },
]
VENUES = [
    {
        "id": 1001,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to "
        "play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37ab"
        "aaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto="
        "format&fit=crop&w=400&q=60",
        "date_created": datetime.date(2019, 1, 6)
    },
    {
        "id": 1002,
        "name": "The Dueling Pianos Bar",
        "genres": ["Classical", "R&B", "Hip-Hop"],
        "address": "335 Delancey Street",
        "city": "New York",
        "state": "NY",
        "phone": "914-003-1132",
        "website": "https://www.theduelingpianos.com",
        "facebook_link": "https://www.facebook.com/theduelingpianos",
        "seeking_talent": False,
        "image_link": "https://images.unsplash.com/photo-1497032205916-a"
        "c775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyM"
        "Dd9&auto=format&fit=crop&w=750&q=80",
        "date_created": datetime.date(2018, 9, 11)
    },
    {
        "id": 1003,
        "name": "Park Square Live Music & Coffee",
        "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
        "address": "34 Whiskey Moore Ave",
        "city": "San Francisco",
        "state": "CA",
        "phone": "415-000-1234",
        "website": "https://www.parksquarelivemusicandcoffee.com",
        "facebook_link": "https://www.facebook.com/ParkSquareLiveMusic"
        "AndCoffee",
        "seeking_talent": False,
        "image_link": "https://images.unsplash.com/photo-1485686531765-ba63"
        "b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&"
        "auto=format&fit=crop&w=747&q=80",
        "date_created": datetime.date(2017, 6, 21)
    },
]
SHOWS = [
    {
        "id": 1001,
        "start_time": "2019-05-21T21:30:00.000Z",
        "artist_id": 1004,
        "venue_id": 1001,
    },
    {
        "id": 1002,
        "start_time": "2019-06-15T23:00:00.000Z",
        "artist_id": 1005,
        "venue_id": 1003,
    },
    {
        "id": 1003,
        "start_time": "2035-04-01T20:00:00.000Z",
        "artist_id": 1006,
        "venue_id": 1003,
    },
    {
        "id": 1004,
        "start_time": "2035-04-08T20:00:00.000Z",
        "artist_id": 1006,
        "venue_id": 1003,
    },
    {
        "id": 1005,
        "start_time": "2035-04-15T20:00:00.000Z",
        "artist_id": 1006,
        "venue_id": 1003,
    },
]
