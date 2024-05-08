# import sqlite3

# conn = sqlite3.connect("DTB/Pixel_Defender.db")
# cur = conn.cursor()

# cur.execute("SELECT * FROM tower_level")

# turret_data = cur.fetchall()  # Récupérer toutes les lignes de résultats

# print(turret_data)
# # Fermer la connexion à la base de données
# cur.close()
# conn.close()

TURRET = {
    "CANNON" : [
        {
            "range": 120,
            "cooldown": 1500,
            "damage": 2,
        },
        {
            "range": 140,
            "cooldown": 1250,
            "damage": 4,
        },
        {
            "range": 155,
            "cooldown": 1000,
            "damage": 8,
        },
        {
            "range": 180,
            "cooldown": 750,
            "damage": 10,
        }
    ],
    
    "SNIPER" : [
        {
            #1
            "range": 200,
            "cooldown": 3000,
            "damage": 8,
        },
        {
            #2
            "range": 300,
            "cooldown": 2750,
            "damage": 12,
        },
        {
            #3
            "range": 350,
            "cooldown": 2500,
            "damage": 15,
        },
        {
            #4
            "range": 400,
            "cooldown": 2000,
            "damage": 25,
        }
    ],
        
    "MACHINE_GUN" : [
        {
            #1
            "range": 150,
            "cooldown": 700,
            "damage": 1,
        },
        {
            #2
            "range": 150,
            "cooldown": 600,
            "damage": 1,
        },
        {
            #3
            "range": 200,
            "cooldown": 450,
            "damage": 2,
        },
        {
            #4
            "range": 250,
            "cooldown": 250,
            "damage": 4,
        }
    ]
}