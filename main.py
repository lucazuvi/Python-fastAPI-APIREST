#  API = INTERFAZ DE PROGRAMACION DE APLICACIONES (Conjunto de reglas que sirven para que
# los progrmas puedan comunicarse entre si).
#  REST = Transferencia de estado representacional
# API REST: Interfaz de Programacion de Aplicaciones para compartir recursos.



from typing import List, Optional
import uuid
from fastapi import FastAPI, HTTPException

from pydantic import BaseModel


app = FastAPI()


class Curso(BaseModel):
    id: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int


# Simulacion base de datos
cursos_db = []

# crud: Read(lectura) GET ALL: Leeremos todos los cursos que haya en la db


@app.get("/cursos", response_model=List[Curso])
def obtener_cursos():
    return cursos_db


# crud: Create(Crear) POST: Agregaremos un nuevo recurso a nuestra base de datos
@app.post("/cursos", response_model=Curso)
def crear_curso(curso: Curso):
    curso.id = str(uuid.uuid4())  # UUID para generar un id unico e irrepetible
    cursos_db.append(curso)
    return curso


# crud: Read(lectura) GET (individual): Leeremos el curso que coincida con el ID que pidamos
@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id: str):
    curso = next(
        (curso for curso in cursos_db if curso.id == curso_id), None
    )  # Con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso


# crud: UPDATE(Actualizar) PUT: Modificaremos un recurso que coincida con el ID que mandamos
@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id: str, curso_actualizado: Curso):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    curso_actualizado.id = curso_id
    index = cursos_db.index(
        curso
    )  # Buscamos el indice exacto donde esta el curso en nuestra lista (Database)
    cursos_db[index] = curso_actualizado
    return curso_actualizado


# crud: Delete(borrado): Eliminamos un recurso que coincida con el ID que mandemos
@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id: str):
    curso = next(
        (curso for curso in cursos_db if curso.id == curso_id), None
    )  # Con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    cursos_db.remove(curso)
    return curso
