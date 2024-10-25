#Crear APIs y manejar exepciones
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
#PAquete para trabajar con la estructura de los datos
from pydantic import BaseModel
#Conexion con MongoDB
from motor import motor_asyncio
from bson import ObjectId
from pymongo import MongoClient
from typing import List, Optional
from pydantic import BaseModel, Field
from typing import Optional


# Definir los tags con descripciones
tags_metadata = [
    {
        "name": "Libros",
        "description": "Operaciones con libros: crear, consultar, actualizar y eliminar libros",
    },
    {
        "name": "Autores",
        "description": "Gestión de autores de los libros",
    },
    {
        "name": "Lectores",
        "description": "Operaciones relacionadas con los lectores de la biblioteca",
    },
    {
        "name": "Bibliotecarios",
        "description": "Gestión del personal bibliotecario",
    },
    {
        "name": "Préstamos",
        "description": "Sistema de préstamos y devoluciones de libros",
    }
    
]

# Inicializar la aplicación FastAPI
app = FastAPI(title="Sistema de Biblioteca",
    description="API para gestionar una biblioteca con libros, autores, lectores, bibliotecarios y préstamos",
    version="1.0.0", openapi_tags=tags_metadata)

#Configurar conexion con MongoDB
MONGO_URI="mongodb://localhost:27017" 
#Ejecutar el cliente de base de datos 
cliente=motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db=cliente["Biblioteca"] 
#------------------------------------------------Colecciones-------------------------------------------------------------
autores_collection = db["Autores"]
bibliotecarios_collection = db["Bibliotecarios"]
lectores_collection = db["Lectores"]
libros_collection = db["Libros"]
prestamos_collection = db["Prestamos"]

#----------------------------------------------------CLASS--------------------------------------------------------------
class Autor(BaseModel):
    nombre: str
    apellido: str
    bibliografia:str

class Libro(BaseModel):
    titulo: str
    descripcion: str
    autor: str
    imagen_portada: Optional[str]  # URL de S3
    inventario: bool 

class Prestamo(BaseModel):
    lector: str
    libro_id: str
    bibliotecario: str
    fecha_prestamo: Optional[datetime]
    fecha_devolucion: Optional[datetime]
    foto_credencial: Optional[str]  # URL de S3

class Bibliotecario(BaseModel):
    nombre: str
    apellido: str
    correo:str

class Lector(BaseModel):
    nombre: str
    apellido: str
    correo:str

#------------------------------------------- Modelo de actualizacion parcial--------------------------------------------
class UpdateAutorModel(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    bibliografia:str | None = None

class UpdateLibroModel(BaseModel):
    titulo: str | None = None
    descripcion: str | None = None
    autor: str | None = None
    imagen_portada: Optional[str] | None = None # URL de S3
    inventario: bool | None = None

class UpdatePrestamoModel(BaseModel):
    lector: str | None = None
    libro_id: str | None = None
    bibliotecario: str | None = None
    fecha_prestamo: Optional[datetime] | None = None
    fecha_devolucion: Optional[datetime] | None = None
    foto_credencial: Optional[str]  | None = None # URL de S3

class UpdateBibliotecarioModel(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    correo:str | None = None

class UpdateLectorModel(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    correo:str | None = None


#-------------------------------------------------METODOS GET------------------------------------------------------------

#Endpoint (ruta de url) para obtener libros DE LA DB 
@app.get("/libros/", tags=["Libros"])
async def get_libros():
    resultados=dict() #tener todos 
    libros=await libros_collection.find().to_list(None) 
    #Iterar todos los elementos de la lista 
    for i, elemento in enumerate(libros): 
        resultados[i]=dict()
        resultados[i]["titulo"]=elemento["titulo"]
        resultados[i]["descripcion"]=elemento["descripcion"]
        resultados[i]["autor"]=elemento["autor"] 
        resultados[i]["imagen_portada"]=elemento["imagen_portada"]
        resultados[i][" inventario"]=elemento["inventario"] 
    return resultados

#Endpoint (ruta de url) para obtener autores DE LA DB 
@app.get("/autores/", tags=["Autores"])
async def get_autores():
    #Obtener de manera asincrona todos los usuarios
    resultados=dict() #tener todos los usuarios 
    autores=await autores_collection.find().to_list(None) 
    #Iterar todos los elementos de la lista users 
    for i, elemento in enumerate(autores): 
        resultados[i]=dict()
        resultados[i]["nombre"]=elemento["nombre"]
        resultados[i]["apellido"]=elemento["apellido"]
        resultados[i]["bibliografia"]=elemento["bibliografia"] 
    return resultados

#Endpoint (ruta de url) para obtener Bibliotecario DE LA DB 
@app.get("/bibliotecarios/", tags=["Bibliotecarios"])
async def get_bibliotecarios():
    #Obtener de manera asincrona todos los usuarios
    resultados=dict() #tener todos los usuarios 
    bibliotecarios=await bibliotecarios_collection.find().to_list(None) 
    #Iterar todos los elementos de la lista users 
    for i, elemento in enumerate(bibliotecarios): 
        resultados[i]=dict()
        resultados[i]["nombre"]=elemento["nombre"]
        resultados[i]["apellido"]=elemento["apellido"]
        resultados[i]["correo"]=elemento["correo"] 
    return resultados

#Endpoint (ruta de url) para obtener Lector DE LA DB 
@app.get("/lectores/", tags=["Lectores"])
async def get_lectores():
    #Obtener de manera asincrona todos los usuarios
    resultados=dict() #tener todos los usuarios 
    lectores=await lectores_collection.find().to_list(None) 
    #Iterar todos los elementos de la lista users 
    for i, elemento in enumerate(lectores): 
        resultados[i]=dict()
        resultados[i]["nombre"]=elemento["nombre"]
        resultados[i]["apellido"]=elemento["apellido"]
        resultados[i]["correo"]=elemento["correo"] 
    return resultados

#Endpoint (ruta de url) para obtener Prestamos DE LA DB 
@app.get("/prestamos/", tags=["Préstamos"])
async def get_prestamos():
    #Obtener de manera asincrona todos los usuarios
    resultados=dict() #tener todos los usuarios 
    prestamos=await prestamos_collection.find().to_list(None) 
    #Iterar todos los elementos de la lista users 
    for i, elemento in enumerate(prestamos): 
        resultados[i]=dict()
        resultados[i]["lector"]=elemento["lector"]
        resultados[i]["libro_id"]=elemento["libro_id"]
        resultados[i]["bibliotecario"]=elemento["bibliotecario"] 
        resultados[i]["fecha_prestamo"]=elemento["fecha_prestamo"]
        resultados[i]["fecha_devolucion"]=elemento["fecha_devolucion"]
        resultados[i]["foto_credencial"]=elemento["foto_credencial"] 
    return resultados



#---------------------------------------------------------GET BY ID-----------------------------------------------------

#GET BY ID LIBROS
@app.get("/libros/{libros_id}", tags=["Libros"])
async def get_libro_by_id(libro_id: str):
    try:
        # Buscar el usuario por ObjectId
        libro = await libros_collection.find_one({"_id": ObjectId(libro_id)})
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
    except Exception:
        raise HTTPException(status_code=400, detail="Formato inválido del ID")

    return {
        "titulo": libro["titulo"],
        "descripcion": libro["descripcion"],
        "autor": libro["autor"],
        "imagen_portada": libro["imagen_portada"],
        "inventario": libro["inventario"],
    }

#GET BY ID AUTOR 
@app.get("/autores/{autor_id}", tags=["Autores"])
async def get_autor_by_id(autor_id: str):
    try:
        # Buscar el usuario por ObjectId
        autor = await autores_collection.find_one({"_id": ObjectId(autor_id)})
        if not autor:
            raise HTTPException(status_code=404, detail="Autor no encontrado")
    except Exception:
        raise HTTPException(status_code=400, detail="Formato inválido del ID")

    return {
        "nombre": autor["nombre"],
        "apellido": autor["apellido"],
        "bibliografia": autor["bibliografia"]
    }

#GET BY ID bibliotecario
@app.get("/bibliotecarios/{bibliotecario_id}", tags=["Bibliotecarios"])
async def get_bibliotecario_by_id(bibliotecario_id: str):
    try:
        # Buscar el usuario por ObjectId
        bibliotecario = await bibliotecarios_collection.find_one({"_id": ObjectId(bibliotecario_id)})
        if not bibliotecario:
            raise HTTPException(status_code=404, detail="Bibliotecario no encontrado")
    except Exception:
        raise HTTPException(status_code=400, detail="Formato inválido del ID")

    return {
        "nombre": bibliotecario["nombre"],
        "apellido": bibliotecario["apellido"],
        "correo": bibliotecario["correo"]
    }

#GET BY ID Lector
@app.get("/lectores/{lector_id}", tags=["Lectores"])
async def get_lector_by_id(lector_id: str):
    try:
        # Buscar el usuario por ObjectId
        lector = await lectores_collection.find_one({"_id": ObjectId(lector_id)})
        if not lector:
            raise HTTPException(status_code=404, detail="Lector no encontrado")
    except Exception:
        raise HTTPException(status_code=400, detail="Formato inválido del ID")

    return {
        "nombre": lector["nombre"],
        "apellido": lector["apellido"],
        "correo": lector["correo"]
    }

#GET BY ID Prestamos
@app.get("/prestamos/{prestamo_id}", tags=["Préstamos"])
async def get_prestamo_by_id(prestamo_id: str):
    try:
        # Buscar el usuario por ObjectId
        prestamo = await prestamos_collection.find_one({"_id": ObjectId(prestamo_id)})
        if not prestamo:
            raise HTTPException(status_code=404, detail="Prestamo no encontrado")
    except Exception:
        raise HTTPException(status_code=400, detail="Formato inválido del ID")

    return {
        "lector": prestamo["lector"],
        "libro_id": prestamo["libro_id"],
        "bibliotecario": prestamo["bibliotecario"],
        "fecha_prestamo": prestamo["fecha_prestamo"],
        "fecha_devolucion": prestamo["fecha_devolucion"],
        "foto_credencial": prestamo["foto_credencial"]
    }


#--------------------------------------------------------------POST-----------------------------------------------------

#METODOS POST
#Metodo para agregar Libros a la DB
@app.post("/libros/", tags=["Libros"])
async def create_libro(libros: Libro): 
    #se agrega un libro a la base de datos
    #Los datos del libro deben estar en diccionario 
    await libros_collection.insert_one(libros.dict()) 
    return{
        "message":"El libro se agrego correctamente"
    }

#Metodo para agregar Autores a la DB
@app.post("/autores/", tags=["Autores"])
async def create_autores(autor: Autor):
    #Se agrega un autor a la DB
    await autores_collection.insert_one(autor.dict())
    return {
        "message": "El autor se agrego correctamente"
    }

#Metodo para agregar lectores a la DB
@app.post("/lectores/", tags=["Lectores"])
async def create_lector(lector: Lector):
    #Agregar lector a pedido a la DB
    await lectores_collection.insert_one(lector.dict())
    return {
        "message":"Se agrego la lector correctamente"
    }

#Metodo para agregar bibliotecario a la DB
@app.post("/bibliotecarios/", tags=["Bibliotecarios"])
async def create_bibliotecario(bibliotecario: Bibliotecario):
    #Agregar bibliotecario a la DB
    await bibliotecarios_collection.insert_one(bibliotecario.dict())
    return {
        "message":"Se agrego el bibliotecario correctamente"
    }
  

# Modificar el método POST de préstamos para incluir la lógica de inventario
@app.post("/prestamos/", tags=["Préstamos"])
async def create_prestamo(prestamo: Prestamo):
    # Verificar si el libro existe y está en inventario
    libro = await libros_collection.find_one({"_id": ObjectId(prestamo.libro_id)})
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    if not libro["inventario"]:
        raise HTTPException(status_code=400, detail="El libro no está disponible en inventario")
    
    # Verificar si el lector existe
    lector = await lectores_collection.find_one({"_id": ObjectId(prestamo.lector)})
    if not lector:
        raise HTTPException(status_code=404, detail="Lector no encontrado")
    
    # Verificar si el bibliotecario existe
    bibliotecario = await bibliotecarios_collection.find_one({"_id": ObjectId(prestamo.bibliotecario)})
    if not bibliotecario:
        raise HTTPException(status_code=404, detail="Bibliotecario no encontrado")
    
    # Establecer las fechas de préstamo y devolución
    prestamo.fecha_prestamo = datetime.now()
    prestamo.fecha_devolucion = prestamo.fecha_prestamo + timedelta(days=3)
    
    # Crear el préstamo
    prestamo_dict = prestamo.dict()
    await prestamos_collection.insert_one(prestamo_dict)
    
    # Actualizar el inventario del libro (marcarlo como no disponible)
    await libros_collection.update_one(
        {"_id": ObjectId(prestamo.libro_id)},
        {"$set": {"inventario": False}}
    )
    
    return {
        "message": "Préstamo registrado correctamente",
        "fecha_devolucion": prestamo.fecha_devolucion
    }


#------------------------------------------------------DELETE------------------------------------------------------------

#Eliminar LIBROS por ID
@app.delete("/libros/{libro_id}", tags=["Libros"])
async def delete_libro_id(libro_id: str):
    try:
        resultado = await libros_collection.delete_one({"_id":ObjectId(libro_id)})

    except Exception as e:
        raise HTTPException(status_code=404, detail="Formato inválido por el ID del libro")
    if resultado.deleted_count==0:
        raise HTTPException(status_code=404,detail="Libro no encontrado")
    return{
        "message": "Libro eliminado correctamente"
        }

#Eliminar autor por ID
@app.delete("/autores/{autor_id}", tags=["Autores"])
async def delete_autor_id(autor_id: str):
    try:
        resultado = await autores_collection.delete_one({"_id":ObjectId(autor_id)})

    except Exception as e:
        raise HTTPException(status_code=404, detail="Formato inválido por el ID del autor")
    if resultado.deleted_count==0:
        raise HTTPException(status_code=404,detail="Autor no encontrado")
    return{
        "message": "Autor eliminado correctamente"
        }

#Eliminar lector por ID
@app.delete("/lectores/{lector_id}", tags=["Lectores"])
async def delete_lector_id(lector_id: str):
    try:
        resultado = await lectores_collection.delete_one({"_id":ObjectId(lector_id)})

    except Exception as e:
        raise HTTPException(status_code=404, detail="Formato inválido por el ID del lector")
    if resultado.deleted_count==0:
        raise HTTPException(status_code=404,detail="Lector no encontrado")
    return{
        "message": "Lector eliminado correctamente"
        }

#Eliminar bibliotecario por ID
@app.delete("/bibliotecarios/{bibliotecario_id}", tags=["Bibliotecarios"])
async def delete_bibliotecario_id(bibliotecario_id: str):
    try:
        resultado = await bibliotecarios_collection.delete_one({"_id":ObjectId(bibliotecario_id)})

    except Exception as e:
        raise HTTPException(status_code=404, detail="Formato inválido por el ID del bibliotecario")
    if resultado.deleted_count==0:
        raise HTTPException(status_code=404,detail="bibliotecario no encontrado")
    return{
        "message": "bibliotecarior eliminado correctamente"
        }


#--------------------------------------------------------------PUT----------------------------------------------------

# Actualizar Libro por ObjectId
@app.put("/libros/{libro_id}", tags=["Libros"])
async def update_libros(libro_id: str, libro_data: UpdateLibroModel):
    try:
        # Crear el filtro con ObjectId
        filtro = {"_id": ObjectId(libro_id)}
        
        # Crear el diccionario de actualización
        actualizacion = {k: v for k, v in libro_data.dict().items() if v is not None}
        
        if not actualizacion:
            raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar")
        
        # Realizar la actualización
        resultado = await libros_collection.update_one(filtro, {"$set": actualizacion})
    except Exception:
        raise HTTPException(status_code=400, detail="Formato inválido del ID")
    
    if resultado.modified_count == 0:
        raise HTTPException(status_code=404, detail="Libro no encontrado o no modificado")
    
    return {"message": "Libro actualizado correctamente"}


# Actualizar autores por ObjectId
@app.put("/autores/{autor_id}", tags=["Autores"])
async def update_autores(autor_id: str, autor_data: UpdateAutorModel):
    try:
        # Crear el filtro con ObjectId
        filtro = {"_id": ObjectId(autor_id)}
        
        # Crear el diccionario de actualización
        actualizacion = {k: v for k, v in autor_data.dict().items() if v is not None}
        
        if not actualizacion:
            raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar")
        
        # Realizar la actualización
        resultado = await autores_collection.update_one(filtro, {"$set": actualizacion})
    except Exception:
        raise HTTPException(status_code=400, detail="Formato inválido del ID")
    
    if resultado.modified_count == 0:
        raise HTTPException(status_code=404, detail="Autor no encontrado o no modificado")
    
    return {"message": "Autor actualizado correctamente"}

# Actualizar lector por ObjectId
@app.put("/lectores/{lector_id}", tags=["Lectores"])
async def update_lectores(lector_id: str, lector_data: UpdateLectorModel):
    try:
        # Crear el filtro con ObjectId
        filtro = {"_id": ObjectId(lector_id)}
        
        # Crear el diccionario de actualización
        actualizacion = {k: v for k, v in lector_data.dict().items() if v is not None}
        
        if not actualizacion:
            raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar")
        
        # Realizar la actualización
        resultado = await lectores_collection.update_one(filtro, {"$set": actualizacion})
    except Exception:
        raise HTTPException(status_code=400, detail="Formato inválido del ID")
    
    if resultado.modified_count == 0:
        raise HTTPException(status_code=404, detail="Lector no encontrado o no modificado")
    
    return {"message": "Lector actualizado correctamente"}

# Actualizar bibliotecario por ObjectId
@app.put("/bibliotecarios/{bibliotecario_id}", tags=["Bibliotecarios"])
async def update_bibliotecarios(bibliotecario_id: str, bibliotecario_data: UpdateBibliotecarioModel):
    try:
        # Crear el filtro con ObjectId
        filtro = {"_id": ObjectId(bibliotecario_id)}
        
        # Crear el diccionario de actualización
        actualizacion = {k: v for k, v in bibliotecario_data.dict().items() if v is not None}
        
        if not actualizacion:
            raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar")
        
        # Realizar la actualización
        resultado = await bibliotecarios_collection.update_one(filtro, {"$set": actualizacion})
    except Exception:
        raise HTTPException(status_code=400, detail="Formato inválido del ID")
    
    if resultado.modified_count == 0:
        raise HTTPException(status_code=404, detail="Bibliotecario no encontrado o no modificado")
    
    return {"message": "Bibliotecario actualizado correctamente"}


# Actualizar prestamo por ObjectId
@app.put("/prestamos/{prestamo_id}", tags=["Préstamos"])
async def update_prestamos(prestamo_id: str,prestamo_data: UpdatePrestamoModel):
    try:
        # Crear el filtro con ObjectId
        filtro = {"_id": ObjectId(prestamo_id)}
        
        # Crear el diccionario de actualización
        actualizacion = {k: v for k, v in prestamo_data.dict().items() if v is not None}
        
        if not actualizacion:
            raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar")
        
        # Realizar la actualización
        resultado = await prestamos_collection.update_one(filtro, {"$set": actualizacion})
    except Exception:
        raise HTTPException(status_code=400, detail="Formato inválido del ID")
    
    if resultado.modified_count == 0:
        raise HTTPException(status_code=404, detail="Prestamo no encontrado o no modificado")
    
    return {"message": "Prestamo actualizado correctamente"}


#------------------------------------------------------VERIFICAR DISPONIBILIDAD-------------------------------------------
# Agregar endpoint para verificar disponibilidad de libro
@app.get("/libros/{libro_id}/disponibilidad", tags=["Libros"])
async def verificar_disponibilidad(libro_id: str):
    libro = await libros_collection.find_one({"_id": ObjectId(libro_id)})
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    return {
        "disponible": libro["inventario"],
        "titulo": libro["titulo"]
    }


#-------------------------------------------------DEVOLUCIONES-----------------------------------------------------------
# Agregar endpoint para devolución de libros
@app.post("/devoluciones/{prestamo_id}", tags=["Préstamos"])
async def devolver_libro(prestamo_id: str):
    # Verificar si el préstamo existe
    prestamo = await prestamos_collection.find_one({"_id": ObjectId(prestamo_id)})
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    
    # Verificar si el libro ya fue devuelto (comparando la fecha actual con la fecha de devolución)
    if datetime.now() > prestamo["fecha_devolucion"]:
        # Aquí podrías implementar lógica para multas por retraso
        pass
    
    # Actualizar el inventario del libro (marcarlo como disponible)
    await libros_collection.update_one(
        {"_id": ObjectId(prestamo["libro_id"])},
        {"$set": {"inventario": True}}
    )
    # Actualizar el estado del préstamo
    await prestamos_collection.update_one(
        {"_id": ObjectId(prestamo_id)},
        {
            "$set": {
                "devuelto": True,
                "fecha_devolucion_real": datetime.now()
            }
        }
    )
    
    return {"message": "Libro devuelto correctamente"}