# Tarea-Semana_12_POO
Utilización de colecciones para la mejora de rendimiento en restaurante_app

**Estudiante:** ANGEL RAFAEL CUENCA TAMAYO
**Asignatura:** Programación Orientada a Objetos

## Descripción del Proyecto
Sistema de gestión de productos, usuarios y ventas con **persistencia JSON** y **optimización de búsquedas mediante colecciones** (Semana 12).
El objetivo es mejorar el rendimiento de las operaciones frecuentes evitando recorrer listas completas.

## Mejoras Implementadas (Semana 12)

### Índices con Diccionarios (O(1) en búsquedas)
| Índice | Estructura | Mejora |
|---|---|---|
| `_productos_por_codigo` | `dict[str, Producto]` | Buscar producto por código → sin recorrer toda la lista |
| `_usuarios_por_identificacion` | `dict[str, Usuario]` | Buscar usuario por identificación → acceso directo |
| `_ventas_por_usuario` | `dict[str, list[Venta]]` | Consultar ventas por usuario → sin recorrer todas las ventas |

###  Conservación de Listas Principales
Las listas `_productos`, `_usuarios` y `_ventas` se mantienen para **listar, iterar y persistir** en JSON. Los diccionarios actúan como **índices auxiliares sincronizados**.

### Sincronización Automática
- Al registrar/modificar/eliminar → se actualizan tanto la lista como el índice correspondiente
- Al iniciar el programa → `_reconstruir_indices()` reconstruye todos los índices desde los objetos cargados de JSON

## Funcionalidades
-  Registro, búsqueda, actualización y eliminación de productos (con stock)
-  Registro, búsqueda, actualización y eliminación de usuarios
-  Realización de ventas con control de stock
-  Consulta de ventas por usuario
-  Persistencia automática en archivos JSON
-  Manejo de excepciones (archivos, formato, permisos)

## ▶️ Ejecución
```bash
python main.py
