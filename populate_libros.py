from datetime import datetime
from app import app, db, Libro

libros_data = [
    {"nombre": "Cien años de soledad", "autor": "Gabriel García Márquez", "fecha_publicacion": "1967-05-30"},
    {"nombre": "El amor en los tiempos del cólera", "autor": "Gabriel García Márquez", "fecha_publicacion": "1985-09-05"},
    {"nombre": "Crónica de una muerte anunciada", "autor": "Gabriel García Márquez", "fecha_publicacion": "1981-04-05"},
    {"nombre": "La casa de los espíritus", "autor": "Isabel Allende", "fecha_publicacion": "1982-01-01"},
    {"nombre": "De amor y de sombra", "autor": "Isabel Allende", "fecha_publicacion": "1984-03-01"},
    {"nombre": "Harry Potter y la piedra filosofal", "autor": "J.K. Rowling", "fecha_publicacion": "1997-06-26"},
    {"nombre": "Harry Potter y la cámara secreta", "autor": "J.K. Rowling", "fecha_publicacion": "1998-07-02"},
    {"nombre": "Harry Potter y el prisionero de Azkaban", "autor": "J.K. Rowling", "fecha_publicacion": "1999-07-08"},
    {"nombre": "Harry Potter y el cáliz de fuego", "autor": "J.K. Rowling", "fecha_publicacion": "2000-07-08"},
    {"nombre": "El señor de los anillos: La comunidad del anillo", "autor": "J.R.R. Tolkien", "fecha_publicacion": "1954-07-29"},
    {"nombre": "El señor de los anillos: Las dos torres", "autor": "J.R.R. Tolkien", "fecha_publicacion": "1954-11-11"},
    {"nombre": "El señor de los anillos: El retorno del rey", "autor": "J.R.R. Tolkien", "fecha_publicacion": "1955-10-20"},
    {"nombre": "1984", "autor": "George Orwell", "fecha_publicacion": "1949-06-08"},
    {"nombre": "Rebelión en la granja", "autor": "George Orwell", "fecha_publicacion": "1945-08-17"},
    {"nombre": "Matar a un ruiseñor", "autor": "Harper Lee", "fecha_publicacion": "1960-07-11"},
    {"nombre": "El gran Gatsby", "autor": "F. Scott Fitzgerald", "fecha_publicacion": "1925-04-10"},
    {"nombre": "Orgullo y prejuicio", "autor": "Jane Austen", "fecha_publicacion": "1813-01-28"},
    {"nombre": "El guardián entre el centeno", "autor": "J.D. Salinger", "fecha_publicacion": "1951-07-16"},
    {"nombre": "Rayuela", "autor": "Julio Cortázar", "fecha_publicacion": "1963-06-28"},
    {"nombre": "Ficciones", "autor": "Jorge Luis Borges", "fecha_publicacion": "1944-01-01"},
    {"nombre": "El Aleph", "autor": "Jorge Luis Borges", "fecha_publicacion": "1949-01-01"},
    {"nombre": "La sombra del viento", "autor": "Carlos Ruiz Zafón", "fecha_publicacion": "2001-04-15"},
    {"nombre": "El juego del ángel", "autor": "Carlos Ruiz Zafón", "fecha_publicacion": "2008-01-01"},
    {"nombre": "El laberinto de los espíritus", "autor": "Carlos Ruiz Zafón", "fecha_publicacion": "2016-01-01"},
    {"nombre": "El nombre de la rosa", "autor": "Umberto Eco", "fecha_publicacion": "1980-01-01"},
    {"nombre": "El perfume", "autor": "Patrick Süskind", "fecha_publicacion": "1985-03-01"},
    {"nombre": "El Código Da Vinci", "autor": "Dan Brown", "fecha_publicacion": "2003-03-18"},
    {"nombre": "Ángeles y demonios", "autor": "Dan Brown", "fecha_publicacion": "2000-05-01"},
    {"nombre": "Los pilares de la tierra", "autor": "Ken Follett", "fecha_publicacion": "1989-01-01"},
    {"nombre": "La chica del tren", "autor": "Paula Hawkins", "fecha_publicacion": "2015-01-13"}
]

with app.app_context():
    for libro in libros_data:
        fecha_pub = datetime.strptime(libro["fecha_publicacion"], "%Y-%m-%d").date()
        nuevo_libro = Libro(
            nombre=libro["nombre"],
            autor=libro["autor"],
            fecha_publicacion=fecha_pub,
            estado="disponible"  
        )
        db.session.add(nuevo_libro)
    
    db.session.commit()
    print(f"Se han insertado {len(libros_data)} libros en la base de datos.")
