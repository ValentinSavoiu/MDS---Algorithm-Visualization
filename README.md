**Instalare**

Vedeti 'Releases'

**Utilizare**

In meniul initial, selectati algoritmul dorit si introduceti un nume de fisier. Fisierul ar trebui sa existe in folderul inputs si sa fie generat de programul nostru. Daca lasati gol campul Filename, se va genera un vector/graf aleator
    
Fisierele predefinite sunt prefixate cu v pentru vectori, bfs si dijkstra.

-- Modificarea vectorilor

Pentru a modifica vectorul, dati click pe un element. Vi se vor da optiunile de a sterge elementul, a adauga un element in stanga sau in dreapta lui, sau de a inversa ordinea elementelor din vector
    
-- Modificarea grafurilor

Pentru a modifica un graf, puteti da click pe ecran pentru a adauga un element, sau puteti folosi meniul pentru a adauga / sterge muchii intre noduri si pentru a sterge noduri sau a selecta nodul de start pentru algoritmii de parcurgere.


**Pentru notare:**

backlog and user stories: https://trello.com/b/4lV36J6Y/algorithm-visualization
    
uml: https://drive.google.com/file/d/1TVnSt9vql4WTHPDxLxlgl-OTj3LIhNyh/view?usp=sharing
    
bugfixing/issues: https://github.com/ValentinSavoiu/MDS---Algorithm-Visualization/issues?q=is%3Aissue+is%3Aclosed 
    
refactoring: https://github.com/ValentinSavoiu/MDS---Algorithm-Visualization/commit/af4a86e994d9b9be4b89e645747cfcebfc1e9152
[Context]: Initial, print_array albea intreg ecranul pentru a desena iconitele si vectorul doar pe 20% din el
[Refactoring]: Am impartit ecranul in 4 zone. 2 zone pentru array-uri, o zona pentru iconite si o zona pentru graf. Am creat functiile print_icons, clear_array, clear_graph, clear_icons si am modificat functia print_array care se ocupa, fiecare, de bucatile lor din ecran. In plus, zona din ecran care ar trebui ocupata de aceste elemente este calculata acum la initializarea viewer-ului si doar citita de aceste functii, ceea ce distruge orice posibilitate de coliziune. 
Functionalitatea viewerului a ramas identica (este apelat identic de controller), dar am deschis portile pentru adaugarea unor features fundamentale, precum vizualizarea simultana a unui vector si un graf,


build tool: https://github.com/ValentinSavoiu/MDS---Algorithm-Visualization/releases/tag/v1.3

design pattern: model-view-controller(MVC)
