### Lancement client/serveur

1. **Lancer le serveur (Python) :**
    - Il affichera son adresse IP.

2. **Dans le client (Java), modifier la ligne 106 du fichier `Client.java` :**
    ```java
    monClient.initClient("10.126.5.252", test);
    ```
    - Remplacer `"10.126.5.252"` par l'adresse IP affichée par le serveur.

3. **Lancer le client (Java).**

Pour connaître les commandes utilisables, vous pouvez les trouver dans le fichier `CLI.java` à partir de la ligne 39.