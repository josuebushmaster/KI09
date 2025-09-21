from domain.entities.cliente import Cliente
from domain.repositories.cliente_repository import ClienteRepository

class CrearClienteUseCase:
    def __init__(self, cliente_repository: ClienteRepository):
        self.cliente_repository = cliente_repository

    def execute(self, nombre: str, apellido: str, edad: int, email: str = "", telefono: str = "", direccion: str = "") -> Cliente:
        if not nombre or not apellido:
            raise ValueError("nombre y apellido son obligatorios")
        cliente = Cliente(nombre=nombre, apellido=apellido, edad=edad, email=email, telefono=telefono, direccion=direccion)
        return self.cliente_repository.crear(cliente)