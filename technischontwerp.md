
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
    
-   Naar de verkennenpagina (GET) → explore
    
-   Foto’s liken, disliken of skippen (POST)
    
-   Een account zoeken (GET) → search
    
-   Een account volgen (POST) → follow
    
-   Naar een accountpagina (GET) → account
    
-   Bekijken wat een account volgt (GET) → following
    
-   Bekijken door wie een account gevolgd wordt (GET) → followers
    
-   Naar de trendingpagina (GET) → trending
    
-   Het uploaden van een foto/gif (POST) → upload
    
-   Naar hun eigen pagina → account


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
    Registreert gebruiker in de database
    
-   random_upload()  
    Selecteert een random foto voor de verkenner-pagina.
    
-   upload_photo()  
    Uploadt de gegevens van een foto in de database.
    
-   get_photo()  
    Haalt alle nodige informatie, zoals de gebruikersnaam en de beschrijving, van een foto op in de database voor het laten zien van de post.
    
-   get_followers()  
    Vraagt de volgers op van een account voor op de profielpagina.
    
-   get_following()  
    Vraagt de accounts op die iemand volgt voor op de profielpagina.
    

- add_follower()  
Voegt een volger toe in de database

## Models/helpers
-   Bootstrap (https://getbootstrap.com)
    
-   Flask (http://flask.pocoo.org)


# Update Projectvoorstel

## Samenvatting

  

Eyelike is een webapplicatie met als doel om gebruikers te verbinden die geïnteresseerd zijn in het concept mode. Met behulp van Eyelike kunnen gebruikers foto’s en gifjes plaatsen die gerelateerd zijn aan mode. Gebruikers kunnen op random gegenereerde posts reageren door aan te geven of zij de post liken of disliken. Afhankelijk van deze waarde kan een post op de trending pagina terechtkomen. Eyelike is een uniek online platform, omdat het zich in vergelijking met andere online platforms specialiseert in mode en het aantal volgers op EyeLike geen invloed heeft op de populariteit van een bericht.

  
  

## Schetsen

![Schets1](https://i.imgur.com/UaJmsCJ.png)

![Schets2](https://i.imgur.com/dUzkjZB.jpg)

![Schets3](https://i.imgur.com/f85dBo9.jpg)

  

## Features

  

- gebruikers kunnen een account aanmaken

- gebruikers kunnen inloggen op de website

- gebruikers kunnen een nieuw wachtwoord aanvragen

- gebruikers kunnen foto’s op de random/verkennen pagina liken of disliken

- gebruikers kunnen andere gebruikers volgen

- gebruikers kunnen via een zoekfunctie andere accounts vinden

- gebruikers kunnen het account van andere gebruikers bekijken

- gebruikers kunnen bekijken wie ze allemaal volgen en door wie ze gevolgd worden

- gebruikers kunnen de meest populaire posts bekijken op de trending pagina

- gebruikers kunnen foto’s en gifjes uploaden met een beschrijving

- gebruikers kunnen hun eigen pagina bekijken

  

## Minimum Viable Product

  

Het product moet minimaal voldoen aan een bepaald aantal functies die essentieel zijn voor de website. Zo moet een gebruiker zich kunnen registreren en vervolgens aanmelden op de site. De gebruiker moet verder mensen kunnen volgen, gifs en foto’s kunnen plaatsen met een beschrijving en posts van anderen kunnen liken. Verder moeten gebruikers hun eigen profiel en profielen van anderen kunnen zien. Tot slot moet er een trending pagina zijn waar elke gebruiker bij kan om te zien welke posts het meest geliked worden.

  

## Afhankelijkheden

  
  

**Databronnen:**

  

-  [http://api.giphy.com](http://api.giphy.com/) voor de gif’s

-  [https://unsplash.com](https://unsplash.com/) voor de achtergronden op het inlogscherm

  

  

**Externe componenten:**

  

- Bootstrap voor de opmaak en functionaliteiten van de website

  

  

**Concurrerende websites:**

  

- Tumblr

- Pinterest

- Weheartit

- Tinder

- Instagram

  

Deze websites zijn geen directe concurrentie, aangezien er nog geen grote website is die alleen draait om fashion. Ook werken geen van deze websites met dislikes. Verder onderscheidt onze website zich doordat men alleen foto’s kan beoordelen die op de verkennen pagina staan. Dit voorkomt dat het volgersaantal van een account invloed heeft op de hoogte van de waarde van een post en daarmee dus invloed heeft op het komen van de trendingpagina. Het is namelijk alleen mogelijk om op de verkennen pagina een beoordeling te geven aan een foto.

  

  

**Moeilijkste delen:**

  

- Een moeilijk onderdeel van de website is het “wachtwoord vergeten”, aangezien er bij dit deel een mail moet worden verstuurd met een automatisch gegenereerd wachtwoord. Bij dit deel moet dus een e-mail platform worden aangeroepen en automatisch een e-mail worden verstuurd. Ook moet er kunnen worden ingelogd met het gegenereerde wachtwoord.

- Het maken van de trending pagina is ook een uitdaging. Hierop komen foto’s die een bepaalde waarde behaald hebben binnen een bepaalde tijd. De tijd verbinden aan de waardes is een lastig onderdeel.

  

Verder kunnen wij momenteel geen andere extreme moeilijkheden verzinnen, maar dit zou in de loop van het proces natuurlijk kunnen veranderen.

  

## Sanity Check

  

Ons voorstel voldoet aan de projecteisen. Het is op EyeLike namelijk mogelijk foto’s en gifjes te posten met of zonder beschrijving, andere gebruikers te volgen en uploads van elkaar te liken.
