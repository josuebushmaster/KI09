from domain.entities.cliente import Cliente
from domain.repositories.cliente_repository import ClienteRepository

class CrearClienteUseCase:
    def __init__(self, cliente_repository):
        self.cliente_repository = cliente_repository

    def execute(self, nombre: str, apellido: str, edad: int, email: str = "", telefono: str = "", direccion: str = "") -> Cliente:
        cliente = Cliente(nombre=nombre, apellido=apellido, edad=edad, email=email, telefono=telefono, direccion=direccion)
        return self.cliente_repository.crear(cliente)