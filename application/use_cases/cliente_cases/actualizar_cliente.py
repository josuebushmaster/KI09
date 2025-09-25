from typing import Optional
from domain.entities.cliente import Cliente
from domain.repositories.cliente_repository import ClienteRepository


class ActualizarClienteUseCase:
    def __init__(self, cliente_repository: ClienteRepository):
        self.cliente_repository = cliente_repository

    def execute(self, id_cliente: int, nombre: str, apellido: str, edad: int, email: str, telefono: str, direccion: str) -> Optional[Cliente]:
        # Obtener cliente existente
        existente = self.cliente_repository.obtener_por_id(id_cliente)
        if not existente:
            # No existe: no crear uno nuevo desde el path de actualización
            return None

        # Merge: usar el valor nuevo si no es vacío/por defecto, si no usar el actual
        nombre_final = nombre if nombre != "" else existente.nombre
        apellido_final = apellido if apellido != "" else existente.apellido
        edad_final = edad if edad != 0 else existente.edad
        email_final = email if email != "" else existente.email
        telefono_final = telefono if telefono != "" else existente.telefono
        direccion_final = direccion if direccion != "" else existente.direccion

        cliente_actualizado = Cliente(
            id_cliente=id_cliente,
            nombre=nombre_final,
            apellido=apellido_final,
            edad=edad_final,
            email=email_final,
            telefono=telefono_final,
            direccion=direccion_final
        )

        return self.cliente_repository.actualizar(id_cliente, cliente_actualizado)