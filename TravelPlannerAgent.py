import random

ACTIVITIES = {
    "Agartala": {
        "state": "Tripura",
        "sightseeing": [
            {"name": "Neermahal", "cost": 20, "hours": 2},
            {"name": "Ujjayanta Palace", "cost": 10, "hours": 2}
        ],
        "food": [
            {"name": "Momos n More", "cost": 200, "hours": 1}
        ],
        "shopping": [
            {"name": "Battala Market", "cost": 0, "hours": 1}
        ]
    },
    "Agra": {
        "state": "Uttar Pradesh",
        "sightseeing": [
            {"name": "Agra Fort", "cost": 35, "hours": 2},
            {"name": "Mehtab Bagh", "cost": 15, "hours": 1},
            {"name": "Taj Mahal", "cost": 50, "hours": 3}
        ],
        "food": [
            {"name": "Petha Store", "cost": 100, "hours": 0.5},
            {"name": "Pinch of Spice", "cost": 800, "hours": 1.5}
        ],
        "shopping": [
            {"name": "Kinari Bazaar", "cost": 0, "hours": 2},
            {"name": "Sadar Bazaar", "cost": 0, "hours": 2}
        ]
    },
    "Ahmedabad": {
        "state": "Gujarat",
        "sightseeing": [
            {"name": "Adalaj Stepwell", "cost": 0, "hours": 1},
            {"name": "Kankaria Lake", "cost": 25, "hours": 2},
            {"name": "Sabarmati Ashram", "cost": 0, "hours": 2}
        ],
        "food": [
            {"name": "Agashiye", "cost": 1000, "hours": 2},
            {"name": "Manek Chowk", "cost": 200, "hours": 1}
        ],
        "shopping": [
            {"name": "Law Garden", "cost": 0, "hours": 1}
        ]
    },
    "Aizawl": {
        "state": "Mizoram",
        "sightseeing": [
            {"name": "Durtlang Hills", "cost": 0, "hours": 1},
            {"name": "Solomon's Temple", "cost": 0, "hours": 1}
        ],
        "food": [
            {"name": "Red Pepper", "cost": 400, "hours": 1}
        ],
        "shopping": [
            {"name": "Bara Bazar", "cost": 0, "hours": 1}
        ]
    },
    "Amritsar": {
        "state": "Punjab",
        "sightseeing": [
            {"name": "Golden Temple", "cost": 0, "hours": 3},
            {"name": "Jallianwala Bagh", "cost": 0, "hours": 1},
            {"name": "Wagah Border", "cost": 0, "hours": 4},
            {"name": "Partition Museum", "cost": 10, "hours": 2},
            {"name": "Gobindgarh Fort", "cost": 200, "hours": 3},
            {"name": "Durgiana Temple", "cost": 0, "hours": 1},
            {"name": "Sadda Pind", "cost": 750, "hours": 3}
        ],
        "food": [
            {"name": "Kesar Da Dhaba", "cost": 400, "hours": 1},
            {"name": "Kulcha Land", "cost": 200, "hours": 1}
        ],
        "shopping": [
            {"name": "Hall Bazaar", "cost": 0, "hours": 2},
            {"name": "Katra Jaimal Singh", "cost": 0, "hours": 2}
        ]
    },
    "Bangalore": {
        "state": "Karnataka",
        "sightseeing": [
            {"name": "Bangalore Palace", "cost": 230, "hours": 2},
            {"name": "Bannerghatta Biological Park", "cost": 260, "hours": 4},
            {"name": "Cubbon Park", "cost": 0, "hours": 1},
            {"name": "ISKCON Temple", "cost": 0, "hours": 1},
            {"name": "Lalbagh Botanical Garden", "cost": 20, "hours": 2},
            {"name": "Tipu Sultan's Summer Palace", "cost": 15, "hours": 1}
        ],
        "food": [
            {"name": "CTR (Shri Sagar)", "cost": 100, "hours": 1},
            {"name": "Corner House Ice Cream", "cost": 200, "hours": 0.5},
            {"name": "MTR (Mavalli Tiffin Room)", "cost": 250, "hours": 1},
            {"name": "Vidyarthi Bhavan", "cost": 150, "hours": 1}
        ],
        "shopping": [
            {"name": "Brigade Road", "cost": 500, "hours": 2},
            {"name": "Commercial Street", "cost": 500, "hours": 2},
            {"name": "UB City", "cost": 0, "hours": 2}
        ]
    },
    "Bodh Gaya": {
        "state": "Bihar",
        "sightseeing": [
            {"name": "Great Buddha Statue", "cost": 0, "hours": 0.5},
            {"name": "Mahabodhi Temple", "cost": 0, "hours": 2}
        ],
        "food": [
            {"name": "Be Happy Cafe", "cost": 300, "hours": 1}
        ],
        "shopping": [
            {"name": "Tibetan Refugee Market", "cost": 0, "hours": 1}
        ]
    },
    "Chandigarh": {
        "state": "Chandigarh",
        "sightseeing": [
            {"name": "Rock Garden", "cost": 30, "hours": 2},
            {"name": "Rose Garden", "cost": 0, "hours": 1},
            {"name": "Sukhna Lake", "cost": 0, "hours": 1}
        ],
        "food": [
            {"name": "Pal Dhaba", "cost": 500, "hours": 1}
        ],
        "shopping": [
            {"name": "Sector 17 Market", "cost": 0, "hours": 2}
        ]
    },
    "Chennai": {
        "state": "Tamil Nadu",
        "sightseeing": [
            {"name": "Fort St. George", "cost": 15, "hours": 2},
            {"name": "Kapaleeshwarar Temple", "cost": 0, "hours": 1},
            {"name": "Marina Beach", "cost": 0, "hours": 2}
        ],
        "food": [
            {"name": "Murugan Idli Shop", "cost": 200, "hours": 1},
            {"name": "Saravana Bhavan", "cost": 300, "hours": 1}
        ],
        "shopping": [
            {"name": "Pondy Bazaar", "cost": 0, "hours": 2},
            {"name": "T. Nagar", "cost": 0, "hours": 3}
        ]
    },
    "Daman": {
        "state": "Dadra and Nagar Haveli and Daman and Diu",
        "sightseeing": [
            {"name": "Jampore Beach", "cost": 0, "hours": 2},
            {"name": "Moti Daman Fort", "cost": 0, "hours": 1}
        ],
        "food": [
            {"name": "Veera Da Dhaba", "cost": 500, "hours": 1}
        ],
        "shopping": [
            {"name": "Nani Daman Market", "cost": 0, "hours": 1}
        ]
    },
    "Darjeeling": {
        "state": "West Bengal",
        "sightseeing": [
            {"name": "Batasia Loop", "cost": 15, "hours": 0.5},
            {"name": "Tiger Hill", "cost": 0, "hours": 2}
        ],
        "food": [
            {"name": "Glenary's", "cost": 500, "hours": 1}
        ],
        "shopping": [
            {"name": "Mall Road", "cost": 0, "hours": 2}
        ]
    },
    "Delhi": {
        "state": "Delhi",
        "sightseeing": [
            {"name": "Akshardham Temple", "cost": 0, "hours": 3},
            {"name": "Humayun's Tomb", "cost": 35, "hours": 2},
            {"name": "India Gate", "cost": 0, "hours": 1},
            {"name": "Lodhi Gardens", "cost": 0, "hours": 1},
            {"name": "Lotus Temple", "cost": 0, "hours": 1},
            {"name": "Qutub Minar", "cost": 40, "hours": 2},
            {"name": "Red Fort", "cost": 50, "hours": 2}
        ],
        "food": [
            {"name": "Bukhara", "cost": 2500, "hours": 2},
            {"name": "Karim's", "cost": 800, "hours": 2},
            {"name": "Local Dhaba", "cost": 150, "hours": 1},
            {"name": "Paranthe Wali Gali", "cost": 200, "hours": 1},
            {"name": "Street Food Tour", "cost": 300, "hours": 2}
        ],
        "shopping": [
            {"name": "Chandni Chowk", "cost": 0, "hours": 3},
            {"name": "Dilli Haat", "cost": 100, "hours": 3},
            {"name": "Khan Market", "cost": 0, "hours": 2},
            {"name": "Sarojini Market", "cost": 500, "hours": 2}
        ]
    },
    "Gangtok": {
        "state": "Sikkim",
        "sightseeing": [
            {"name": "MG Marg", "cost": 0, "hours": 2},
            {"name": "Rumtek Monastery", "cost": 10, "hours": 2},
            {"name": "Tsomgo Lake", "cost": 0, "hours": 4}
        ],
        "food": [
            {"name": "Roll House", "cost": 100, "hours": 0.5},
            {"name": "Taste of Tibet", "cost": 400, "hours": 1}
        ],
        "shopping": [
            {"name": "MG Marg", "cost": 0, "hours": 2}
        ]
    },
    "Goa": {
        "state": "Goa",
        "sightseeing": [
            {"name": "Basilica of Bom Jesus", "cost": 0, "hours": 1},
            {"name": "Calangute Beach", "cost": 0, "hours": 3},
            {"name": "Dudhsagar Falls", "cost": 400, "hours": 5},
            {"name": "Fort Aguada", "cost": 0, "hours": 2}
        ],
        "food": [
            {"name": "Britto's", "cost": 800, "hours": 2},
            {"name": "Fisherman's Wharf", "cost": 1000, "hours": 2},
            {"name": "Infantaria", "cost": 400, "hours": 1}
        ],
        "shopping": [
            {"name": "Anjuna Flea Market", "cost": 0, "hours": 3},
            {"name": "Mapusa Market", "cost": 0, "hours": 2}
        ]
    },
    "Guwahati": {
        "state": "Assam",
        "sightseeing": [
            {"name": "Brahmaputra River Cruise", "cost": 300, "hours": 1.5},
            {"name": "Kamakhya Temple", "cost": 0, "hours": 2}
        ],
        "food": [
            {"name": "Paradise Restaurant", "cost": 600, "hours": 1}
        ],
        "shopping": [
            {"name": "Fancy Bazaar", "cost": 0, "hours": 2}
        ]
    },
    "Hyderabad": {
        "state": "Telangana",
        "sightseeing": [
            {"name": "Charminar", "cost": 25, "hours": 1},
            {"name": "Golconda Fort", "cost": 25, "hours": 3},
            {"name": "Hussain Sagar Lake", "cost": 0, "hours": 1},
            {"name": "Ramoji Film City", "cost": 1150, "hours": 6}
        ],
        "food": [
            {"name": "Bawarchi", "cost": 300, "hours": 1},
            {"name": "Paradise Biryani", "cost": 400, "hours": 1}
        ],
        "shopping": [
            {"name": "Begum Bazaar", "cost": 0, "hours": 2},
            {"name": "Laad Bazaar", "cost": 0, "hours": 2}
        ]
    },
    "Imphal": {
        "state": "Manipur",
        "sightseeing": [
            {"name": "Kangla Fort", "cost": 20, "hours": 2},
            {"name": "Loktak Lake", "cost": 0, "hours": 3}
        ],
        "food": [
            {"name": "Luxmi Kitchen", "cost": 300, "hours": 1}
        ],
        "shopping": [
            {"name": "Ima Keithel", "cost": 0, "hours": 1}
        ]
    },
    "Indore": {
        "state": "Madhya Pradesh",
        "sightseeing": [
            {"name": "Lal Bagh Palace", "cost": 0, "hours": 2},
            {"name": "Rajwada Palace", "cost": 0, "hours": 1}
        ],
        "food": [
            {"name": "Chappan Dukan", "cost": 200, "hours": 1},
            {"name": "Sarafa Bazaar", "cost": 200, "hours": 1}
        ],
        "shopping": [
            {"name": "MT Cloth Market", "cost": 0, "hours": 1}
        ]
    },
    "Itanagar": {
        "state": "Arunachal Pradesh",
        "sightseeing": [
            {"name": "Ganga Lake", "cost": 0, "hours": 1},
            {"name": "Ita Fort", "cost": 10, "hours": 1}
        ],
        "food": [
            {"name": "Zero Point", "cost": 300, "hours": 1}
        ],
        "shopping": [
            {"name": "Legi Complex", "cost": 0, "hours": 1}
        ]
    },
    "Jaipur": {
        "state": "Rajasthan",
        "sightseeing": [
            {"name": "Amber Fort", "cost": 100, "hours": 3},
            {"name": "City Palace", "cost": 200, "hours": 2},
            {"name": "Hawa Mahal", "cost": 50, "hours": 1},
            {"name": "Jal Mahal", "cost": 0, "hours": 0.5},
            {"name": "Jantar Mantar", "cost": 50, "hours": 1},
            {"name": "Nahargarh Fort", "cost": 50, "hours": 2}
        ],
        "food": [
            {"name": "Chokhi Dhani", "cost": 800, "hours": 4},
            {"name": "Lassiwala", "cost": 60, "hours": 0.5},
            {"name": "Rawat Mishthan Bhandar", "cost": 150, "hours": 1},
            {"name": "Tapri Central", "cost": 400, "hours": 1}
        ],
        "shopping": [
            {"name": "Bapu Bazaar", "cost": 0, "hours": 2},
            {"name": "Johari Bazaar", "cost": 0, "hours": 2},
            {"name": "Tripolia Bazaar", "cost": 0, "hours": 1}
        ]
    },
    "Jaisalmer": {
        "state": "Rajasthan",
        "sightseeing": [
            {"name": "Jaisalmer Fort", "cost": 50, "hours": 2},
            {"name": "Sam Sand Dunes", "cost": 0, "hours": 3}
        ],
        "food": [
            {"name": "Trio", "cost": 800, "hours": 1}
        ],
        "shopping": [
            {"name": "Sadar Bazaar", "cost": 0, "hours": 1}
        ]
    },
    "Kochi": {
        "state": "Kerala",
        "sightseeing": [
            {"name": "Chinese Fishing Nets", "cost": 0, "hours": 0.5},
            {"name": "Fort Kochi", "cost": 0, "hours": 2},
            {"name": "Mattancherry Palace", "cost": 5, "hours": 1}
        ],
        "food": [
            {"name": "Kashi Art Cafe", "cost": 500, "hours": 1.5},
            {"name": "Oceanos", "cost": 600, "hours": 1}
        ],
        "shopping": [
            {"name": "Broadway", "cost": 0, "hours": 2},
            {"name": "Jew Town", "cost": 0, "hours": 2}
        ]
    },
    "Kohima": {
        "state": "Nagaland",
        "sightseeing": [
            {"name": "Kisama Heritage Village", "cost": 20, "hours": 2},
            {"name": "Kohima War Cemetery", "cost": 0, "hours": 1}
        ],
        "food": [
            {"name": "Dream Cafe", "cost": 400, "hours": 1}
        ],
        "shopping": [
            {"name": "Mao Market", "cost": 0, "hours": 1}
        ]
    },
    "Kolkata": {
        "state": "West Bengal",
        "sightseeing": [
            {"name": "Dakshineswar Kali Temple", "cost": 0, "hours": 2},
            {"name": "Howrah Bridge", "cost": 0, "hours": 0.5},
            {"name": "Indian Museum", "cost": 20, "hours": 2},
            {"name": "Victoria Memorial", "cost": 30, "hours": 2}
        ],
        "food": [
            {"name": "Arsalan Biryani", "cost": 400, "hours": 1},
            {"name": "Flurys", "cost": 500, "hours": 1},
            {"name": "Peter Cat", "cost": 800, "hours": 1.5}
        ],
        "shopping": [
            {"name": "College Street", "cost": 0, "hours": 2},
            {"name": "New Market", "cost": 0, "hours": 3}
        ]
    },
    "Kurukshetra": {
        "state": "Haryana",
        "sightseeing": [
            {"name": "Brahma Sarovar", "cost": 0, "hours": 1},
            {"name": "Jyotisar", "cost": 0, "hours": 1}
        ],
        "food": [
            {"name": "Local Dhabas", "cost": 200, "hours": 1}
        ],
        "shopping": [
            {"name": "Sector 17 Market", "cost": 0, "hours": 1}
        ]
    },
    "Lakshadweep": {
        "state": "Lakshadweep",
        "sightseeing": [
            {"name": "Agatti Beach", "cost": 0, "hours": 2},
            {"name": "Lagoon", "cost": 0, "hours": 2}
        ],
        "food": [
            {"name": "Island Cafe", "cost": 400, "hours": 1}
        ],
        "shopping": [
            {"name": "Local Souvenir Shops", "cost": 0, "hours": 0.5}
        ]
    },
    "Leh": {
        "state": "Ladakh",
        "sightseeing": [
            {"name": "Leh Palace", "cost": 250, "hours": 1},
            {"name": "Pangong Lake", "cost": 0, "hours": 5},
            {"name": "Shanti Stupa", "cost": 0, "hours": 1}
        ],
        "food": [
            {"name": "Bon Appetit", "cost": 600, "hours": 1},
            {"name": "The Tibetan Kitchen", "cost": 500, "hours": 1}
        ],
        "shopping": [
            {"name": "Leh Main Bazaar", "cost": 0, "hours": 2}
        ]
    },
    "Lucknow": {
        "state": "Uttar Pradesh",
        "sightseeing": [
            {"name": "Bara Imambara", "cost": 50, "hours": 2},
            {"name": "Rumi Darwaza", "cost": 0, "hours": 0.5}
        ],
        "food": [
            {"name": "Tunday Kababi", "cost": 300, "hours": 1}
        ],
        "shopping": [
            {"name": "Hazratganj", "cost": 0, "hours": 2}
        ]
    },
    "Madurai": {
        "state": "Tamil Nadu",
        "sightseeing": [
            {"name": "Meenakshi Amman Temple", "cost": 0, "hours": 2},
            {"name": "Thirumalai Nayakkar Mahal", "cost": 10, "hours": 1}
        ],
        "food": [
            {"name": "Murugan Idli Shop", "cost": 200, "hours": 1}
        ],
        "shopping": [
            {"name": "Puthu Mandapam", "cost": 0, "hours": 1}
        ]
    },
    "Mumbai": {
        "state": "Maharashtra",
        "sightseeing": [
            {"name": "Chhatrapati Shivaji Terminus", "cost": 0, "hours": 1},
            {"name": "Elephanta Caves", "cost": 250, "hours": 4},
            {"name": "Gateway of India", "cost": 0, "hours": 1},
            {"name": "Haji Ali Dargah", "cost": 0, "hours": 1},
            {"name": "Juhu Beach", "cost": 0, "hours": 2},
            {"name": "Marine Drive", "cost": 0, "hours": 1}
        ],
        "food": [
            {"name": "Bademiya", "cost": 600, "hours": 1},
            {"name": "Britannia & Co.", "cost": 800, "hours": 1},
            {"name": "Leopold Cafe", "cost": 1200, "hours": 2},
            {"name": "Vada Pav Stall", "cost": 50, "hours": 0.5}
        ],
        "shopping": [
            {"name": "Colaba Causeway", "cost": 500, "hours": 2},
            {"name": "Crawford Market", "cost": 0, "hours": 2},
            {"name": "Linking Road", "cost": 500, "hours": 2}
        ]
    },
    "Munnar": {
        "state": "Kerala",
        "sightseeing": [
            {"name": "Eravikulam National Park", "cost": 120, "hours": 3},
            {"name": "Tea Gardens", "cost": 0, "hours": 2}
        ],
        "food": [
            {"name": "Rapsy Restaurant", "cost": 300, "hours": 1}
        ],
        "shopping": [
            {"name": "Munnar Market", "cost": 0, "hours": 1}
        ]
    },
    "Mysore": {
        "state": "Karnataka",
        "sightseeing": [
            {"name": "Chamundi Hill", "cost": 0, "hours": 2},
            {"name": "Mysore Palace", "cost": 70, "hours": 2}
        ],
        "food": [
            {"name": "Vinayaka Mylari", "cost": 150, "hours": 1}
        ],
        "shopping": [
            {"name": "Devaraja Market", "cost": 0, "hours": 1}
        ]
    },
    "Pondicherry": {
        "state": "Puducherry",
        "sightseeing": [
            {"name": "Auroville", "cost": 0, "hours": 3},
            {"name": "Promenade Beach", "cost": 0, "hours": 1},
            {"name": "Sri Aurobindo Ashram", "cost": 0, "hours": 1}
        ],
        "food": [
            {"name": "Cafe des Arts", "cost": 500, "hours": 1},
            {"name": "Villa Shanti", "cost": 1000, "hours": 1.5}
        ],
        "shopping": [
            {"name": "Mission Street", "cost": 0, "hours": 1}
        ]
    },
    "Port Blair": {
        "state": "Andaman and Nicobar Islands",
        "sightseeing": [
            {"name": "Cellular Jail", "cost": 30, "hours": 2},
            {"name": "Corbyn's Cove", "cost": 0, "hours": 1}
        ],
        "food": [
            {"name": "New Lighthouse Restaurant", "cost": 600, "hours": 1}
        ],
        "shopping": [
            {"name": "Aberdeen Bazaar", "cost": 0, "hours": 1}
        ]
    },
    "Pune": {
        "state": "Maharashtra",
        "sightseeing": [
            {"name": "Aga Khan Palace", "cost": 25, "hours": 2},
            {"name": "Shaniwar Wada", "cost": 25, "hours": 2},
            {"name": "Sinhagad Fort", "cost": 50, "hours": 4}
        ],
        "food": [
            {"name": "Goodluck Cafe", "cost": 300, "hours": 1},
            {"name": "Kayani Bakery", "cost": 200, "hours": 0.5}
        ],
        "shopping": [
            {"name": "FC Road", "cost": 0, "hours": 2},
            {"name": "Tulsi Baug", "cost": 0, "hours": 2}
        ]
    },
    "Puri": {
        "state": "Odisha",
        "sightseeing": [
            {"name": "Golden Beach", "cost": 0, "hours": 2},
            {"name": "Jagannath Temple", "cost": 0, "hours": 1.5},
            {"name": "Konark Sun Temple", "cost": 40, "hours": 2}
        ],
        "food": [
            {"name": "Wildgrass Restaurant", "cost": 600, "hours": 1}
        ],
        "shopping": [
            {"name": "Swargadwar Market", "cost": 0, "hours": 1}
        ]
    },
    "Raipur": {
        "state": "Chhattisgarh",
        "sightseeing": [
            {"name": "Ghatarani Waterfalls", "cost": 0, "hours": 3},
            {"name": "Nandan Van Zoo", "cost": 50, "hours": 2}
        ],
        "food": [
            {"name": "Manju Mamta", "cost": 300, "hours": 1}
        ],
        "shopping": [
            {"name": "Pandri Market", "cost": 0, "hours": 1}
        ]
    },
    "Ranchi": {
        "state": "Jharkhand",
        "sightseeing": [
            {"name": "Dassam Falls", "cost": 0, "hours": 2},
            {"name": "Patratu Valley", "cost": 0, "hours": 2}
        ],
        "food": [
            {"name": "Kaveri Restaurant", "cost": 500, "hours": 1}
        ],
        "shopping": [
            {"name": "Main Road", "cost": 0, "hours": 1}
        ]
    },
    "Rann of Kutch": {
        "state": "Gujarat",
        "sightseeing": [
            {"name": "Kalo Dungar", "cost": 0, "hours": 2},
            {"name": "White Desert", "cost": 100, "hours": 3}
        ],
        "food": [
            {"name": "Local Kutchi Food", "cost": 300, "hours": 1}
        ],
        "shopping": [
            {"name": "Bhujodi", "cost": 0, "hours": 2}
        ]
    },
    "Rishikesh": {
        "state": "Uttarakhand",
        "sightseeing": [
            {"name": "Beatles Ashram", "cost": 600, "hours": 2},
            {"name": "Laxman Jhula", "cost": 0, "hours": 1},
            {"name": "Ram Jhula", "cost": 0, "hours": 1},
            {"name": "Triveni Ghat Aarti", "cost": 0, "hours": 1.5},
            {"name": "Parmarth Niketan Aarti", "cost": 0, "hours": 1.5},
            {"name": "River Rafting", "cost": 1500, "hours": 3},
            {"name": "Bungee Jumping", "cost": 3500, "hours": 2},
            {"name": "Paragliding", "cost": 4000, "hours": 2}
        ],
        "food": [
            {"name": "Chotiwala", "cost": 300, "hours": 1},
            {"name": "Freedom Cafe", "cost": 400, "hours": 1}
        ],
        "shopping": [
            {"name": "Laxman Jhula Market", "cost": 0, "hours": 1}
        ]
    },
    "Shillong": {
        "state": "Meghalaya",
        "sightseeing": [
            {"name": "Elephant Falls", "cost": 20, "hours": 1},
            {"name": "Shillong Peak", "cost": 30, "hours": 1},
            {"name": "Umiam Lake", "cost": 0, "hours": 1}
        ],
        "food": [
            {"name": "Cafe Shillong", "cost": 500, "hours": 1}
        ],
        "shopping": [
            {"name": "Police Bazar", "cost": 0, "hours": 2}
        ]
    },
    "Shimla": {
        "state": "Himachal Pradesh",
        "sightseeing": [
            {"name": "Jakhu Temple", "cost": 0, "hours": 1.5},
            {"name": "Mall Road", "cost": 0, "hours": 2},
            {"name": "The Ridge", "cost": 0, "hours": 1}
        ],
        "food": [
            {"name": "Cafe Simla Times", "cost": 500, "hours": 1},
            {"name": "Sita Ram and Sons", "cost": 100, "hours": 0.5}
        ],
        "shopping": [
            {"name": "Lakkar Bazaar", "cost": 0, "hours": 1}
        ]
    },
    "Srinagar": {
        "state": "Jammu and Kashmir",
        "sightseeing": [
            {"name": "Dal Lake", "cost": 0, "hours": 2},
            {"name": "Mughal Gardens", "cost": 50, "hours": 2},
            {"name": "Shankaracharya Temple", "cost": 0, "hours": 1}
        ],
        "food": [
            {"name": "Mughal Darbar", "cost": 800, "hours": 1.5},
            {"name": "Stream Restaurant", "cost": 600, "hours": 1}
        ],
        "shopping": [
            {"name": "Floating Market", "cost": 0, "hours": 1},
            {"name": "Lal Chowk", "cost": 0, "hours": 2}
        ]
    },
    "Tirupati": {
        "state": "Andhra Pradesh",
        "sightseeing": [
            {"name": "Silathoranam", "cost": 0, "hours": 0.5},
            {"name": "Tirumala Venkateswara Temple", "cost": 0, "hours": 4}
        ],
        "food": [
            {"name": "Andhra Spice", "cost": 400, "hours": 1}
        ],
        "shopping": [
            {"name": "Bazaar Street", "cost": 0, "hours": 1}
        ]
    },
    "Udaipur": {
        "state": "Rajasthan",
        "sightseeing": [
            {"name": "City Palace", "cost": 300, "hours": 3},
            {"name": "Jag Mandir", "cost": 0, "hours": 1},
            {"name": "Lake Pichola Boat Ride", "cost": 400, "hours": 1},
            {"name": "Saheliyon Ki Bari", "cost": 10, "hours": 1}
        ],
        "food": [
            {"name": "Ambrai", "cost": 1200, "hours": 2},
            {"name": "Millets of Mewar", "cost": 500, "hours": 1}
        ],
        "shopping": [
            {"name": "Bada Bazaar", "cost": 0, "hours": 2},
            {"name": "Hathi Pol", "cost": 0, "hours": 2}
        ]
    },
    "Varanasi": {
        "state": "Uttar Pradesh",
        "sightseeing": [
            {"name": "Assi Ghat", "cost": 0, "hours": 1},
            {"name": "Dashashwamedh Ghat", "cost": 0, "hours": 2},
            {"name": "Kashi Vishwanath Temple", "cost": 0, "hours": 2},
            {"name": "Sarnath", "cost": 20, "hours": 3}
        ],
        "food": [
            {"name": "Blue Lassi", "cost": 100, "hours": 0.5},
            {"name": "Kashi Chat Bhandar", "cost": 150, "hours": 0.5}
        ],
        "shopping": [
            {"name": "Godowlia Market", "cost": 0, "hours": 2},
            {"name": "Thatheri Bazaar", "cost": 0, "hours": 2}
        ]
    },
    "Visakhapatnam": {
        "state": "Andhra Pradesh",
        "sightseeing": [
            {"name": "Kailasagiri", "cost": 100, "hours": 2},
            {"name": "RK Beach", "cost": 0, "hours": 1},
            {"name": "Submarine Museum", "cost": 40, "hours": 1}
        ],
        "food": [
            {"name": "The Eatery", "cost": 800, "hours": 1}
        ],
        "shopping": [
            {"name": "Jagadamba Centre", "cost": 0, "hours": 2}
        ]
    }
}

def get_cities_by_state(state_name):
    """Returns a list of cities in the specified state."""
    return [city for city, details in ACTIVITIES.items() if details.get("state", "").lower() == state_name.lower()]

def calculate_trip_cost(selected_activities):
    """Calculates the total estimated cost for a list of selected activities."""
    return sum(activity.get("cost", 0) for activity in selected_activities)

def generate_itinerary(city, days, budget, preferences):
    """Generates a day-by-day itinerary based on constraints."""
    if city not in ACTIVITIES:
        return None
    
    city_data = ACTIVITIES[city]
    possible_activities = []
    
    # Default to all categories if no preferences provided
    target_categories = preferences if preferences else ["sightseeing", "food", "shopping"]
    
    for category in target_categories:
        if category in city_data:
            possible_activities.extend(city_data[category])
            
    # Shuffle to randomize
    random.shuffle(possible_activities)
    
    itinerary = {}
    current_cost = 0
    activity_idx = 0
    num_activities = len(possible_activities)
    
    for day in range(1, days + 1):
        day_label = f"Day {day}"
        itinerary[day_label] = []
        day_hours = 0
        
        # Fill the day with activities (approx 8 hours max)
        # Loop through available activities
        while day_hours < 8 and activity_idx < num_activities:
            activity = possible_activities[activity_idx]
            
            # Check budget constraint
            if current_cost + activity['cost'] <= budget:
                itinerary[day_label].append({
                    "activity": activity['name'],
                    "cost": activity['cost'],
                    "hours": activity['hours']
                })
                current_cost += activity['cost']
                day_hours += activity['hours']
                activity_idx += 1
            else:
                # Skip expensive activity and try next
                activity_idx += 1
                
    return {
        "city": city,
        "total_budget": budget,
        "total_cost": current_cost,
        "itinerary": itinerary
    }
