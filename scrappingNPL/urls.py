# Look:
# Para que el processed sea True, se debe scrappear el texto de la web,
# traducirlo de N idioma a Español, y luego limpiar el texto de caracteres innecesarios
# y textos repepitivos.
#Keys:
ID, NAME, AUTOR, URL = "id", "name", "autor", "url"
books = [
    {
        "id": 1,
        "name": "El espectro de poder",
        "language": "English",
        "autor": "Charles Egbert Craddock",
        "url": "https://www.gutenberg.org/cache/epub/76105/pg76105-images.html",
        "processed": True
    },
    {
        "id": 2,
        "name": "La Divina Comedia",
        "language": "Spanish",
        "autor": "Dante Alighieri",
        "url": "https://www.gutenberg.org/cache/epub/57303/pg57303-images.html",
        "processed": True
    },
    {
        "id": 3,
        "name": "Volvoreta",
        "language": "Spanish",
        "autor": "Wenceslao Fernández-Flórez",
        "url": "https://www.gutenberg.org/cache/epub/58865/pg58865-images.html",
        "processed": True
    },
    {
        "id": 4,
        "name": "Los Hombres de Pro",
        "language": "Spanish",
        "autor": "José María de Pereda",
        "url": "https://www.gutenberg.org/cache/epub/14995/pg14995-images.html",
        "processed": True
    },
    {
        "id": 5,
        "name": "El libro de las tierras vírgenes",
        "language": "Spanish",
        "autor": "Rudyard Kipling",
        "url": "https://www.gutenberg.org/cache/epub/69552/pg69552-images.html",
        "processed": True
    },
    {
        "id": 6,
        "name": "Belarmino y Apolonio",
        "language": "Spanish",
        "autor": "Ramón Pérez de Ayala",
        "url": "https://www.gutenberg.org/cache/epub/14318/pg14318-images.html",
        "processed": True
    },
    {
        "id": 7,
        "name": "La Casa de los Cuervos",
        "language": "Spanish",
        "autor": "Hugo Wast",
        "url": "https://www.gutenberg.org/cache/epub/59631/pg59631-images.html",
        "processed": True
    },
    {
        "id": 8,
        "name": "Candido, o El Optimismo",
        "language": "Spanish",
        "autor": "Voltaire",
        "url": "https://www.gutenberg.org/cache/epub/7109/pg7109-images.html",
        "processed": True
    },
    {
        "id": 9,
        "name": "Novelas de Voltaire — Tomo Primero",
        "language": "Spanish",
        "autor": "Voltaire",
        "url": "https://www.gutenberg.org/cache/epub/9895/pg9895-images.html",
        "processed": True
    },
    {
        "id": 10,
        "name": "Zadig, ó El Destino, Historia Oriental",
        "language": "Spanish",
        "autor": "Voltaire",
        "url": "https://www.gutenberg.org/cache/epub/5985/pg5985-images.html",
        "processed": True
    },
    {
        "id": 11,
        "name": "Los Apóstoles",
        "language": "Spanish",
        "autor": "Ernest Renan",
        "url": "https://www.gutenberg.org/cache/epub/65410/pg65410-images.html",
        "processed": False
    },
    {
        "id": 12,
        "name": "Vida de Jesús",
        "language": "Spanish",
        "autor": "Ernest Renan",
        "url": "https://www.gutenberg.org/cache/epub/65165/pg65165-images.html",
        "processed": False
    }
]

def searchBook(iD: int, key: str):
    return books[iD - 1][key]


def needProcess():
    print("Libros por procesar: ")
    for book in books:
        if not book["processed"]:
            print(f"\033[31mID = {book.get('id')} - {book.get('name')}")


def isIn(book_name: str):
    for book in books:
        if book_name == book["name"]:
            print("Libro Existente")
            break