from pydantic import BaseModel, Field, field_validator
# `Optional` se usa para indicar campos que pueden ser None
from typing import Optional
# `datetime` para manejar fechas de orden
from datetime import datetime
# `Enum` para definir los estados posibles de la orden
from enum import Enum

class OrdenEstado(str, Enum):
    # Enum de strings que lista los estados válidos de una orden
    # Hereda de `str` para que los valores sean tratables como cadenas
    PENDIENTE = "pendiente"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"
    ENVIADA = "enviada"

class OrdenCreateDTO(BaseModel):
    # DTO usado para crear una orden (entrada desde el cliente)
    # `id_cliente` es obligatorio y debe ser > 0
    id_cliente: int = Field(..., gt=0, description="ID del cliente")
    # `fecha_orden` opcional; por defecto se asigna la hora actual UTC
    fecha_orden: Optional[datetime] = Field(default_factory=datetime.utcnow)
    # `estado_orden` por defecto es 'pendiente' (tipo OrdenEstado)
    estado_orden: OrdenEstado = Field(default=OrdenEstado.PENDIENTE)

    @field_validator('estado_orden', mode='before')
    @classmethod
    def _coerce_estado_create(cls, v):
        # Este validador se ejecuta antes de la validación del tipo
        # Recibe el valor bruto (v) que vino en la petición y debe
        # devolver un valor válido para que Pydantic lo parsee.

        # Si el cliente omitió el campo o pasó null, usar el valor por defecto
        if v is None:
            return OrdenEstado.PENDIENTE.value

        # Aceptamos números (p. ej. 1) y los mapeamos a los strings
        if isinstance(v, int):
            mapping = {
                1: OrdenEstado.PENDIENTE.value,
                2: OrdenEstado.COMPLETADA.value,
                3: OrdenEstado.CANCELADA.value,
                4: OrdenEstado.ENVIADA.value,
            }
            mapped = mapping.get(v)
            # Si el entero no está en el mapping, lanzamos error claro
            if mapped is None:
                raise ValueError(f"Estado inválido: {v}. Debe ser 1, 2, 3 o 4")
            return mapped

        # Si el cliente envía una cadena, comprobamos que sea uno de los estados válidos
        if isinstance(v, str):
            valid_states = [e.value for e in OrdenEstado]
            if v not in valid_states:
                raise ValueError(f"Estado inválido: {v}. Debe ser uno de: {valid_states}")
            return v

        # Si recibe directamente la instancia del Enum, devolvemos su valor string
        if isinstance(v, OrdenEstado):
            return v.value

        # Cualquier otro tipo no es aceptado
        raise ValueError(f"Tipo de estado inválido: {type(v)}")

class OrdenUpdateDTO(BaseModel):
    # DTO para actualizar una orden: todos los campos son opcionales
    id_cliente: Optional[int] = Field(None, gt=0, description="ID del cliente")
    fecha_orden: Optional[datetime] = None
    estado_orden: Optional[OrdenEstado] = None

    @field_validator('estado_orden', mode='before')
    @classmethod
    def _coerce_estado_update(cls, v):
        # Si el cliente no quiere actualizar el estado, puede enviar null/omit
        if v is None:
            return None

        # Igual que en create: permitir enteros mapeados
        if isinstance(v, int):
            mapping = {
                1: OrdenEstado.PENDIENTE.value,
                2: OrdenEstado.COMPLETADA.value,
                3: OrdenEstado.CANCELADA.value,
                4: OrdenEstado.ENVIADA.value,
            }
            mapped = mapping.get(v)
            if mapped is None:
                raise ValueError(f"Estado inválido: {v}. Debe ser 1, 2, 3 o 4")
            return mapped

        # Aceptar strings válidos
        if isinstance(v, str):
            valid_states = [e.value for e in OrdenEstado]
            if v not in valid_states:
                raise ValueError(f"Estado inválido: {v}. Debe ser uno de: {valid_states}")
            return v

        # Si ya es el Enum, retornar su valor
        if isinstance(v, OrdenEstado):
            return v.value

        # Tipo no soportado
        raise ValueError(f"Tipo de estado inválido: {type(v)}")

class OrdenResponseDTO(BaseModel):
    # DTO usado para serializar la respuesta que envía la API
    id_orden: int
    id_cliente: int
    fecha_orden: datetime
    # Aquí mantenemos `estado_orden` como str para simplificar la salida
    estado_orden: str  # Cambiado a str para simplificar

    @field_validator('estado_orden', mode='before')
    @classmethod
    def _coerce_estado_response(cls, v):
        # Si la capa de infra devuelve un entero, lo mapeamos a string
        if isinstance(v, int):
            mapping = {
                1: "pendiente",
                2: "completada",
                3: "cancelada",
                4: "enviada",
            }
            # Si no encuentra el entero, devolveremos 'pendiente' por defecto
            return mapping.get(v, "pendiente")

        # Si la infra devuelve el Enum, obtener su valor string
        if isinstance(v, OrdenEstado):
            return v.value

        # Para cualquier otro caso, convertir a str (defensa adicional)
        return str(v)