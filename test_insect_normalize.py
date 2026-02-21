import pytest
from engine.kashrut_engine import KashrutEngine


def test_normalize_missing_insect_scanner():
    inp = {"resultado": "Kosher"}
    out = KashrutEngine.normalize_insect_scanner(inp)
    assert 'insect_scanner' in out
    assert isinstance(out['insect_scanner']['detecciones'], list)
    assert out['insect_scanner']['confianza_global'] == '0%'


def test_normalize_deteccion_basic():
    inp = {
        'insect_scanner': {
            'detecciones': [
                {
                    'bbox': [12.7, 34.2, 50.9, 60.1],
                    'descripcion': 'whole_insect',
                    'especie_aproximada': 'polilla',
                    'confianza': '92',
                    'severidad': 'alta',
                    # accion_recomendada omitted to test inference
                }
            ],
            'resumen': 'Posible polilla',
        }
    }
    out = KashrutEngine.normalize_insect_scanner(inp)
    isc = out['insect_scanner']
    assert isc['confianza_global'] == '92%'
    assert len(isc['detecciones']) == 1
    d = isc['detecciones'][0]
    assert d['bbox'] == [13, 34, 51, 60]
    assert d['confianza'] == '92%'
    assert d['severidad'] == 'Alta'
    assert d['accion_recomendada'] == 'Desechar'
import pytest
from engine.kashrut_engine import KashrutEngine


def test_normalize_missing_insect_scanner():
    inp = {"resultado": "Kosher"}
    out = KashrutEngine.normalize_insect_scanner(inp)
    assert 'insect_scanner' in out
    assert isinstance(out['insect_scanner']['detecciones'], list)
    assert out['insect_scanner']['confianza_global'] == '0%'


def test_normalize_deteccion_basic():
    inp = {
        'insect_scanner': {
            'detecciones': [
                {
                    'bbox': [12.7, 34.2, 50.9, 60.1],
                    'descripcion': 'whole_insect',
                    'especie_aproximada': 'polilla',
                    'confianza': '92',
                    'severidad': 'alta',
                    # accion_recomendada omitted to test inference
                }
            ],
            'resumen': 'Posible polilla',
        }
    }
    out = KashrutEngine.normalize_insect_scanner(inp)
    isc = out['insect_scanner']
    assert isc['confianza_global'] == '92%'
    assert len(isc['detecciones']) == 1
    d = isc['detecciones'][0]
    assert d['bbox'] == [13, 34, 51, 60]
    assert d['confianza'] == '92%'
    assert d['severidad'] == 'Alta'
    assert d['accion_recomendada'] == 'Desechar'