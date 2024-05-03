from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
import hashlib
import sqlite3
import re
from os import path
from tkinter import BooleanVar
from subprocess import Popen

                #hash_object = hashlib.sha3_512(password.encode())
				#hex_digest = hash_object.hexdigest()
				# Connect to the database
				#sqliteConnection = sqlite3.connect('../DataBase/connect.db')
				#cursor = sqliteConnection.cursor()
				# Check if the provided credentials exist in the database
				#query = '''Select * From Id WHERE Pseudo=? AND Password=?;'''
				#cursor.execute(query,(id, hex_digest))
				#output = cursor.fetchall()

# Initialize database connection
dataManager = sqlite3.connect('./DTB/Tower_Defense.db')
cursor = dataManager.cursor()

# Set Tkinter appearance
def apply_theme():
     ctk.set_appearance_mode("dark")
     ctk.set_default_color_theme("dark-blue")

def register_user(nickname, password, verify_password, register_window):
    try:
        #Check if password meets requirments
        if not (re.search("[a-z]", password) and re.search("[A-Z]", password) and re.search("[!@#$%^&*(),.?\":{}|<>]", password) and len(password) >= 8):
            messagebox.showerror("Error", "Le mot de passe doit contenir au moins 1 majuscule, 1 minuscule, 1 caractère spécial et doit avoir une longueur d'au moins 10 caractères.")
            return
        
        # Check si mot de passe correspond
        if password != verify_password:
            messagebox.showerror("Error", "Les mot de passe ne correspond pas.")
            return        
        
        hash_object = hashlib.sha3_512(password.encode())
        hashed_password = hash_object.hexdigest()
        
        # Insert user into the database
        insert_query = "INSERT INTO player (nickname, password) VALUES (?, ?);"
        cursor.execute(insert_query, (nickname, hashed_password))
        dataManager.commit()
        messagebox.showinfo("Success", "Registration Successful!")
        
        # Close the registration window
        register_window.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Registration Failed: {str(e)}")


def register_window():

    def toggle_password_visibility():
        if show_password.get():
            # Show password
            champVerifyMdp.configure(show="")
            champMdp.configure(show="")
        else:
            # Hide password
            champVerifyMdp.configure(show="*")
            champMdp.configure(show="*")


    register_window = Toplevel()
    register_window.geometry("600x400")
    register_window.title("Pixel Defender Inscription")
    #apply_theme(register_window)

    frame = ctk.CTkFrame(master=register_window)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = ctk.CTkLabel(master=frame, text="S'inscrire")
    label.pack(pady=12, padx=10)

    champnickname = ctk.CTkEntry(master=frame, placeholder_text="Nom d'utilisateur")
    champnickname.pack(pady=12)

    champMdp = ctk.CTkEntry(master=frame, placeholder_text="Mot de passe", show="*")
    champMdp.pack(pady=12)

    champVerifyMdp = ctk.CTkEntry(master=frame, placeholder_text="Vérifier le mot de passe", show="*")
    champVerifyMdp.pack(pady=12)

    show_password = BooleanVar()
    show_checkbox = ctk.CTkCheckBox(master=frame, text="Afficher le mot de passe", variable=show_password, command=toggle_password_visibility )
    show_checkbox.pack(pady=12, padx=10)


    ButtonInscrip = ctk.CTkButton(master=frame, text="Inscription", command=lambda: register_user(champnickname.get(), champMdp.get(), champVerifyMdp.get(), register_window))
    ButtonInscrip.pack(pady=12, padx=10)

    annulerInsc = ctk.CTkButton(master=frame, text="Annuler", command=register_window.destroy)
    annulerInsc.pack(pady=12, padx=10)


def login():
    nickname = champ1.get()
    userPassword = champ2.get()

    try:
        hash_object = hashlib.sha3_512(userPassword.encode())
        userPassword = hash_object.hexdigest()
        # Check si l'utilisateur exite
        query = "SELECT * FROM player WHERE nickname=? AND password=?;"
        cursor.execute(query,(nickname,userPassword))
        result = cursor.fetchall()
        
        if result:
            messagebox.showinfo("Success", "Login Successful!")
               
            home_page(nickname)  # Ouvrir la page d'accueil
            main_window.withdraw() # Cacher la fenêtre de connexion
        else:
            messagebox.showerror("Error", "Invalid nickname or password!")
    except Exception as e:
        messagebox.showerror("Error", f"Login Failed: {str(e)}")

def show_password():
    if checkbox_var.get():
        champ2.configure(show="")
    else:
        champ2.configure(show="*")


# Create main login window
main_window = ctk.CTk()
main_window.geometry("600x400")
main_window.title("Pixel Defender Connexion")
#apply_theme(main_window)

def home_page(nickname):
    def modify_user():
        def update_user():
            new_nickname = new_nickname_entry.get()
            new_password = new_password_entry.get()

            try:
                # Check if password meets requirements
                if not (re.search("[a-z]", new_password) and re.search("[A-Z]", new_password) and re.search("[!@#$%^&*(),.?\":{}|<>]", new_password) and len(new_password) >= 8):
                    messagebox.showerror("Error", "Le mot de passe doit contenir au moins 1 majuscule, 1 minuscule, 1 caractère spécial et doit avoir une longueur d'au moins 8 caractères.")
                    return

                # Hash the password
                hash_object = hashlib.sha3_512(new_password.encode())
                hashed_password = hash_object.hexdigest()

                # Update user information in the database
                update_query = "UPDATE tower_defence SET nickname = %s, password = %s WHERE nickname = %s"
                data = (new_nickname, hashed_password, nickname)
                cursor.execute(update_query, data)
                dataManager.connection.commit()

                messagebox.showinfo("Success", "User information updated successfully!")
                modify_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update user information: {str(e)}")

        modify_window = Toplevel()
        modify_window.geometry("400x300")
        modify_window.title("Modifier l'utilisateur")

        # Labels and Entries for username and password
        nickname_label = ctk.CTkLabel(master=modify_window, text="Nouveau nom d'utilisateur:")
        nickname_label.pack(pady=10)
        new_nickname_entry = ctk.CTkEntry(master=modify_window)
        new_nickname_entry.pack(pady=5)

        password_label = ctk.CTkLabel(master=modify_window, text="Nouveau mot de passe:")
        password_label.pack(pady=10)
        new_password_entry = ctk.CTkEntry(master=modify_window, show="*")
        new_password_entry.pack(pady=5)

        # Button to trigger the update_user function
        update_button = ctk.CTkButton(master=modify_window, text="Modifier", command=update_user)
        update_button.pack(pady=20)

    def quit_app():
        home_window.withdraw() # Fermer la fenêtre d'accueil

    # Créer une nouvelle fenêtre pour la page d'accueil
    home_window = Toplevel()
    home_window.geometry("600x400")
    home_window.title("Pixel Defender Accueil")

    
    frame = ctk.CTkFrame(master=home_window)
    frame.pack(pady=20, padx=60, fill="both", expand=True)
    # Ajouter du contenu à la page d'accueil
    label = ctk.CTkLabel(master=frame, text=f"Bienvenue sur Pixel Defender, {nickname}!")
    label.pack(pady=20)

    # Ajouter une image qui permet d'accèder au jeu
    Start_button_image = PhotoImage(file="assets/images/gui/logo.png")
    
    def start_game():
        #specifier le chemin du jeu
        launch_game = "jeu/main.py"

        #utilise subprocess pour démarrer l'auter fichier python
        Popen(["python", launch_game])
    
    button_start = ctk.CTkButton(master=frame, text="", command=start_game, image=Start_button_image)
    button_start.pack(pady=12, padx=10)

    # Créer le menu
    menu = Menu(home_window)
    home_window.config(menu=menu)

    # Menu Utilisateur
    user_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Utilisateur", menu=user_menu)
    user_menu.add_command(label="Modifier l'utilisateur", command=modify_user)
    user_menu.add_separator()
    user_menu.add_command(label="Quitter", command=quit_app)

    # Fermer la fenêtre de connexion
    main_window.withdraw()



#Créer la variable de contrôle pour la case à cocher après la création de la fenêtre principal
checkbox_var = BooleanVar()
#Appeler la fonction pour vérifier si des informations de connexion sont enregistrées
frame = ctk.CTkFrame(master=main_window)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = ctk.CTkLabel(master=frame, text="Se connecter")
label.pack(pady=12, padx=10)

champ1 = ctk.CTkEntry(master=frame, placeholder_text="Identifiant")
champ1.pack(pady=12)
nickname = champ1.get()

champ2 = ctk.CTkEntry(master=frame, placeholder_text="Mot de passe", show="*")
champ2.pack(pady=12)

checkbox = ctk.CTkCheckBox(master=frame, text="Afficher le mot de passe", variable=checkbox_var, command=show_password)
checkbox.pack(pady=12, padx=10)

button = ctk.CTkButton(master=frame, text="Connexion", command=login)
button.pack(pady=12, padx=10)


button2 = ctk.CTkButton(master=frame, text="Vous n'êtes pas inscrit, inscrivez-vous ICI ", command=register_window)
button2.pack(pady=12, padx=10)

main_window.mainloop()
