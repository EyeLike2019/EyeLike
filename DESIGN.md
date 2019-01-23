
# Technisch ontwerp EyeLike
Groep 20:
- Furkan Simsir
- Hannah Visser
- Luuk Tegel
- Joost de Wildt

## Controllers

-   Naar de inlogpagina (GET) → login
    
-   Inloggen in het account (POST) → login
    
-   Naar de registreerpagina (GET) → register
    
-   Een account registreren (POST) → register

-   Naar de eigen accountpagina (GET) → account
    
-   Het uploaden van een foto/gif (POST) → upload

-   Een account zoeken (GET) → search

-   Naar de pagina van een gebruiker (GET) → profile
    
-   Een account (ont)volgen (POST) → (un)follow

-   Bekijken wat een account volgt (GET) → following
    
-   Bekijken door wie een account gevolgd wordt (GET) → followers
    
-   Naar de tijdlijn (GET) → timeline

-   Naar de verkennenpagina (GET) → explore
    
-   Foto’s (dis)liken (POST) → (dis)like

-   Foto’s skippen (POST) → skip

-   Foto's verwijderen (POST) → remove

-   Naar de trendingpagina (GET) → trending

-   Foto's aan favorieten toevoegen (POST) → favourite

-   Naar de pagina met favoriete berichten (GET) → favourites

-   Foto's uit favoriteten verwijderen (POST) → remove favourite


## Schetsen
De eerste pagina die de bezoeker van EyeLike te zien krijgt is de explore/verkennenpagina. Het doel van deze pagina is bezoekers kennis te laten maken met de site. Doordat ze al zonder hoeven in te loggen berichten kunnen liken, disliken of overslaan. Uiteraard is het ook mogelijk om een account aan te maken. Hierna kan men inloggen. Zo kunnen gebruikers van EyeLike ook daadwerkelijk zien welke foto's populair zijn, op de trendingpagina, en accounts bekijken. Dit is niet mogelijk zonder ingelogd te zijn. Als er op een (dis)like knop gedrukt wordt zal er te zien zijn dat de rating van een foto omhoog/omlaag gaat. Hierna zal, of na het klikken van de skipbutton, een nieuwe foto verschijnen. Als men zijn gegevens invult en op de knop registreren klikt wordt diegene doorgestuurd naar de inlogpagina. De knop inloggen zal de gebruiker naar zijn/haar persoonlijke accountpagina brengen. Als er op de knop volgen wordt geklikt, zal de kleur van de volgknop veranderen, "volgen" in "volgend" worden veranderd en dit account zal toegevoegd worden aan de lijst met personen die de ingelogde persoon volgt. Het klikken op een accountnaam brengt de ingelogde gebruiker naar de accountpagina van de aangeklikte naam.
![Explore](https://imgur.com/9t9uvkV.png)
![Register](https://i.imgur.com/gZr1M9Q.png)
![Log in](https://i.imgur.com/f85dBo9.jpg)
![Account](https://imgur.com/yDGV8s5.png)
![Trending](https://i.imgur.com/dUzkjZB.jpg)


## Models/helpers

-   login_required() (CS50 Finance)  
    Zorgt voor een omleiding naar de login pagina voor als er voor een bepaalde functionaliteit moet worden ingelogd.
    
-   check_username(username)  
    Returned een lijst met gebruikers met de gegeven gebruikersnaam. Deze functie wordt vooral gebruikt voor het controleren of de gebruikersnaam bestaat.
    
-   check_email(email)  
    Returned een lijst met gebruikers met het gegeven e-mailadres. Deze functie wordt vooral gebruikt voor het controleren of het e-mailadres bestaat.
    
-   get_username(user_id)  
    Returned een lijst met daarin de gebruikersnaam die hoort bij de gegeven user-id.
    
-   get_user_id(username)  
    Returned een lijst met daarin de user-id die hoort bij de gegeven gebruikersnaam.
    
-   verify_password(username, password)  
    Controleert of het gegeven wachtwoord correct is.
    
-   register_user(username, password, email)  
    Registreert gebruiker in de database.
    
-   random_upload()  
    Selecteert een random foto voor de verkenner-pagina.
    
-   update_score(change, photo_id) 
    Verandert de score van een foto in de database.
    
-   upload_photo(user_id, upload, description, username)  
    Uploadt de gegevens van een foto in de database.
    
-   remove_photo(user_id, photo_id) 
    Verwijdert de foto die een gebruiker geplaatst heeft uit de database. 
    
-   follow_user(user_id, follower_id)  
    Voegt een volger toe in de database. 
    
-   unfollow_user(user_id, follower_id)  
    Verwijdert een volger uit de database.

-   is_following(user_id, follower_id)  
    Controleert of de gebruiker het desbetreffende account volgt, zodat er een mogelijkheid gecreëerd wordt om te ontvolgen.
    
-   get_followers(user_id)  
    Vraagt de volgers op van een account voor op de profielpagina.
    
-   get_following(follower_id)  
    Vraagt de accounts op die iemand volgt voor op de profielpagina.
    
-   get_all_uploads(user_id)  
    Haalt alle nodige informatie op van de uploads van degenen die de gebruiker volgt voor de tijdlijn.
    
-   get_all_trending()
    Haalt foto's op uit de database die de afgelopen week geplaatst zijn.
    
-   get_favourites(user_id)
    Haalt foto's op uit de database die door de gebruiker als favoriet zijn gemarkeerd. 
    
-   add_favourite(user_id)
    Voegt een favoriet van een gebruiker toe aan de database. 
    
-   remove_favourite(user_id, photo_id)
    Verwijdert een favoriet van een gebruiker uit de database.
    
-   get_info(post_id)  
    Haalt alle nodige informatie op van een foto's uit de database voor het laten zien van de post.
    

## Plugins en frameworks
-   Bootstrap (https://getbootstrap.com)
    
-   Flask (http://flask.pocoo.org)



