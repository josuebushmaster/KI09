import pandas as pd
import types
import json
import os

import pytest

# Asegurar que variables mínimas existen (evitar fallos por .env durante importaciones)
os.environ.setdefault('OLAP_DATABASE_URL', 'postgresql://user:pass@localhost/testdb')

from application.use_cases.ia_cases.analyze_olap_use_case import AnalyzeOlapUseCase


def test_analyze_use_case_builds_filtered_context(monkeypatch):
    # Datos simulados OLAP
    dim_tiempo = pd.DataFrame([
        {"id_tiempo": 101, "anio": 2024, "mes": 1, "dia": 1},
        {"id_tiempo": 102, "anio": 2023, "mes": 12, "dia": 31},
    ])
    hecho_ventas = pd.DataFrame([
        {"id_tiempo": 101, "id_cliente": 1, "id_producto": 10, "monto": 100},
        {"id_tiempo": 102, "id_cliente": 2, "id_producto": 20, "monto": 50},
    ])
    dim_producto = pd.DataFrame([
        {"id_producto": 10, "nombre_producto": "A"},
        {"id_producto": 20, "nombre_producto": "B"},
    ])

    # Parchear el repositorio para devolver los DataFrames simulados
    def fake_get_all_olap_data(self):
        return {
            'hecho_ventas': hecho_ventas,
            'dim_tiempo': dim_tiempo,
            'dim_producto': dim_producto,
            'dim_categoria': pd.DataFrame([]),
            'dim_cliente': pd.DataFrame([]),
        }

    from infrastructure.repositories.olap_data_repository import OlapDataRepository
    monkeypatch.setattr(OlapDataRepository, 'get_all_olap_data', fake_get_all_olap_data)

    uc = AnalyzeOlapUseCase()
    result = uc.run('reporte de enero 2024 por favor')

    assert isinstance(result, dict)
    ctx = result.get('context_text')
    assert ctx and 'Ventas filtradas para 1/2024' in ctx
    assert 'Filas: 1' in ctx  # solo id_tiempo 101
    assert result.get('missing') == [] or isinstance(result.get('missing'), list)


# Pruebas del endpoint FastAPI
from interfaces.api.main import app
from fastapi.testclient import TestClient


def test_ia_endpoint_uses_context(monkeypatch):
    client = TestClient(app)

    # Contexto ficticio que el use case devolverá
    fake_ctx = 'CTX_FROM_OLAP'

    # Parchear el use case para retornar el contexto ficticio
    class FakeUC:
        def run(self, prompt: str):
            return { 'context_text': fake_ctx, 'olap_data': {}, 'missing': [] }

    # Importante: parchear el símbolo usado por el controlador
    monkeypatch.setattr(
        'interfaces.api.controllers.ia_controller.AnalyzeOlapUseCase',
        lambda: FakeUC()
    )

    # Capturar los argumentos con los que se llama al cliente de IA
    captured = {}

    def fake_analyze_prompt(prompt: str, context_text: str = None):
        captured['prompt'] = prompt
        captured['context_text'] = context_text
        return { 'ok': True }

    monkeypatch.setattr('scripts.grok_client.analyze_prompt', fake_analyze_prompt)

    resp = client.post('/ia/analizar', json={ 'prompt': 'haz un resumen' })
    assert resp.status_code == 200

    body = resp.json()
    assert body['result'] == { 'ok': True }
    assert body['context_size'] == len(fake_ctx)
    assert captured['context_text'] == fake_ctx


def test_get_context_endpoint(monkeypatch):
    client = TestClient(app)

    # Simular resultado del use case
    fake_ctx = 'MUESTRA_CTX_OLAP'
    fake_olap = {
        'hecho_ventas': pd.DataFrame({ 'id_tiempo': [1, 2], 'monto': [100, 50] }),
        'dim_tiempo': pd.DataFrame({ 'id_tiempo': [1, 2], 'anio': [2024, 2024], 'mes': [1, 2] })
    }

    class FakeUC:
        def run(self, prompt: str):
            return { 'context_text': fake_ctx, 'olap_data': fake_olap, 'missing': [] }

    # Importante: parchear el símbolo usado por el controlador
    monkeypatch.setattr(
        'interfaces.api.controllers.ia_controller.AnalyzeOlapUseCase',
        lambda: FakeUC()
    )

    resp = client.get('/ia/context', params={ 'prompt': 'diagnostico' })
    assert resp.status_code == 200
    body = resp.json()
    assert body['context_size'] == len(fake_ctx)
    assert 'tables' in body
    assert 'hecho_ventas' in body['tables']
    assert body['tables']['hecho_ventas']['rows'] == 2
