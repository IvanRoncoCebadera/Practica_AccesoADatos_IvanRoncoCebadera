from models.usuarios.Usuario import Usuario
from IRepository.IRepository import IRepository


class IUsuarioRepo(IRepository[Usuario, str]):
    pass