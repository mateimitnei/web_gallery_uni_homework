
# Mițnei Matei - Tema IAP1 (2024)

**Website Log-in:**  
Username: `walt`  
Password: `1`

## Descriere:

>Nu am folosit Bootstrap sau alt framework de css pentru ca am vrut sa am control complet asupra
design-ului. In schimb, le-am dat multor elemente proprietatea de flexbox care a ajutat la
aranjarea in pagina, in special la pozitionarea pozelor din galerie (si rearanjarea acestora
la zoom in).

Ruta default a serverului (`/`) foloseste functia `index` cu care transmite categoriile cu
toate fisierele aferente prin "render_template('gallery.html', files=uploaded_files)".

La ruta `/about` se incarca pagina `about.html`.

In functia de login (ruta `/login`) se preiau username-ul si parola din form-ul html cu
`request.form.get()`. Se verifica daca sunt corecte si in caz afirmativ se redirecteaza la pagina
principala, schimbandu-se session["authenticated"] la "True". Daca nu, se reincarca pagina de
login cu mesajul de eroare corespunzator, session["authenticated"] ramanand "False".

La logout se seteaza session["authenticated"] la "False" si se redirecteaza catre login.

Pentru `/upload`, in primul rand, se verifica daca utilizatorul este logat (pentru a evita
accesarea neautentificata prin linkul `http://localhost:5000/upload`). Daca este, se preiau file,
name si category din form-ul html. Se verifica daca fisierul este compatibil (are o extensie
din lista de extensii permise) si apoi daca utilizatorul a introdus o denumire noua prin "name".
In cazul in care "name" exista se inlocuieste numele de dinainte de .[extensie] cu "name". Dupa
i se da un nume unic (descris la functionalitati extra), se salveaza fisierul in folderul serverului
si se creeaza un thumbnail cu functia `create_thumbnail` (care foloseste pillow), in cadrul careia
se si redenumeste fisierul cu ".thumb". Daca totul a mers bine, se redirecteaza spre pagina
principala. Daca nu, se reincarca pagina de upload cu mesajul de eroare respectiv.

Ruta `/uploads/<path:filename>` este folosita de pagina `gallery.html` pentru a afisa imaginile
full resolution (si implicit full screen) pe o pagina separata.

Fisierul `gallery.html` se foloseste de parametrul Jinja2 primit (`files`) pentru a itera prin
doua for-uri si a afisa pozele pe categorii. Fiecare poza este reprezentata printr-un tag `<img>`
ce are ca sursa fisierul thumbnail si un link `<a>` catre imaginea originala.


### Functionalitati extra:

1. Se poate incarca pe site aceeasi poza de mai multe ori, pentru ca in cadrul functiei
upload_file i se da un nume unic fiecarui fisier transmis (daca nu este un fisier duplicat, se
pastreaza numele original). De exemplu, daca se incarca de doua ori aceeasi imagine "photo.jpg" se
vor salva in sistemul de fisiere al site-ului ca "photo.jpg" si "photo_1.jpg". In acest mod se
poate afisa de mai multe ori aceeasi imagine in galerie.
2. In momentul in care o categorie (de ex "selfies") nu contine nicio poza, pe site va aparea in
dreptul acesteia mesajul "empty". Am implementat asta in fisierul html cu un if-else din Jinja2.
3. Pe pagina cu galeria foto, in dreapta, se afla si un "nav bar" cu titlurile categoriilor,
pe post de link-uri catre inceputul fiecarei categorii. Acestea devin folositoare in momentul in
care sunt incarcate multe poze si ar dura mai mult cautarea categoriile prin scroll.
