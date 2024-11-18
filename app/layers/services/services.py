# capa de servicio/lógica de negocio
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
from ..transport import transport  # Importamos la capa de transporte que hace la consulta a la API

def getAllImages(input=None):
    # Si se pasa un parámetro 'input', lo usamos para realizar una búsqueda en la API,
    # de lo contrario, obtenemos todas las imágenes disponibles.
    raw_images = transport.getAllImages(input)

    # Ahora transformamos los datos crudos de la API en objetos Card
    images = []
    for img in raw_images:
        card = translator.fromRequestIntoCard(img)
        images.append(card)

    return images

def saveFavourite(request):
    # Transforma un objeto de request en una Card y lo guarda en la base de datos
    fav = translator.fromTemplateIntoCard(request)
    fav.user = get_user(request)  # Asocia al usuario logueado
    return repositories.saveFavourite(fav)

def getAllFavourites(request):
    # Obtiene todos los favoritos de un usuario, si está autenticado
    if not request.user.is_authenticated:
        return []
    
    user = get_user(request)
    favourite_list = repositories.getAllFavourites(user)  # Asumimos que esta función existe en repositories
    
    # Mapeamos los favoritos desde la base de datos en objetos Card
    mapped_favourites = []
    for fav in favourite_list:
        card = translator.fromRepositoryIntoCard(fav)
        mapped_favourites.append(card)
    
    return mapped_favourites

def deleteFavourite(request):
    # Elimina un favorito de la base de datos por su ID
    fav_id = request.POST.get('id')
    return repositories.deleteFavourite(fav_id)
