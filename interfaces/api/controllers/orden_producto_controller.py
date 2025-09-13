from fastapi import APIRouter, HTTPException, status
from application.use_cases.orden_producto_cases.crear_orden_producto import CrearOrdenProductoUseCase
from application.use_cases.orden_producto_cases.obtener_orden_producto import ObtenerOrdenProductoUseCase
from application.use_cases.orden_producto_cases.listar_orden_producto import ListarOrdenProductosPorOrdenUseCase
from application.use_cases.orden_producto_cases.listar_todos_orden_producto import ListarTodosOrdenProductoUseCase
from application.use_cases.orden_producto_cases.actualizar_orden_producto import ActualizarOrdenProductoUseCase
from application.use_cases.orden_producto_cases.eliminar_orden_producto import EliminarOrdenProductoUseCase
from infrastructure.repositories.postgres_orden_producto_repository import PostgresOrdenProductoRepository
from interfaces.api.dtos.orden_producto_dto import OrdenProductoCreateDTO, OrdenProductoResponseDTO
from domain.entities.orden_producto import OrdenProducto

router = APIRouter(prefix="/orden-producto", tags=["orden-producto"])

orden_producto_repository = PostgresOrdenProductoRepository()

@router.get("/", response_model=list[OrdenProductoResponseDTO])
async def listar_todos_orden_producto():
	use_case = ListarTodosOrdenProductoUseCase(orden_producto_repository)
	return use_case.execute()

@router.post("/", response_model=OrdenProductoResponseDTO, status_code=status.HTTP_201_CREATED)
async def crear_orden_producto(dto: OrdenProductoCreateDTO):
	try:
		use_case = CrearOrdenProductoUseCase(orden_producto_repository)
		orden_producto = use_case.execute(
			dto.id_producto,
			dto.cantidad,
			dto.precio_unitario,
			dto.id_orden
		)
		return orden_producto
	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=f"Error al crear orden-producto: {str(e)}"
		)

@router.get("/{id_ordenProd}", response_model=OrdenProductoResponseDTO)
async def obtener_orden_producto(id_ordenProd: int):
	use_case = ObtenerOrdenProductoUseCase(orden_producto_repository)
	orden_producto = use_case.execute(id_ordenProd)
	if not orden_producto:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="OrdenProducto no encontrado"
		)
	return orden_producto

@router.get("/orden/{id_orden}", response_model=list[OrdenProductoResponseDTO])
async def listar_orden_productos(id_orden: int):
	use_case = ListarOrdenProductosPorOrdenUseCase(orden_producto_repository)
	return use_case.execute(id_orden)

@router.put("/{id_ordenProd}", response_model=OrdenProductoResponseDTO)
async def actualizar_orden_producto(id_ordenProd: int, dto: OrdenProductoCreateDTO):
	use_case = ActualizarOrdenProductoUseCase(orden_producto_repository)
	orden_producto = OrdenProducto(
		id_ordenProd=id_ordenProd,
		id_producto=dto.id_producto,
		cantidad=dto.cantidad,
		precio_unitario=dto.precio_unitario,
		id_orden=dto.id_orden
	)
	actualizado = use_case.execute(id_ordenProd, orden_producto)
	if not actualizado:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="OrdenProducto no encontrado"
		)
	return actualizado

@router.delete("/{id_ordenProd}", status_code=status.HTTP_200_OK)
async def eliminar_orden_producto(id_ordenProd: int):
	use_case = EliminarOrdenProductoUseCase(orden_producto_repository)
	eliminado = use_case.execute(id_ordenProd)
	if not eliminado:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="OrdenProducto no encontrado"
		)
	return {"mensaje": "OrdenProducto eliminado exitosamente"}
