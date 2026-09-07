from pathlib import Path
from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante import RestauranteServicio
import os
os.system("cls")

OPCIONES_MENU = (
    ("1", "Registrar producto"),
    ("2", "Buscar producto"),
    ("3", "Actualizar producto"),
    ("4", "Eliminar producto"),
    ("5", "Listar productos"),
    ("6", "Registrar usuario"),
    ("7", "Buscar usuario"),
    ("8", "Actualizar usuario"),
    ("9", "Eliminar usuario"),
    ("10", "Listar usuarios"),
    ("11", "Realizar venta"),
    ("12", "Consultar ventas por usuario"),
    ("13", "Listar todas las ventas"),
    ("0", "Salir"),
)


def pedir_texto(mensaje: str) -> str:
    return input(mensaje).strip()


def pedir_entero(mensaje: str, defecto=None) -> int:
    texto = pedir_texto(mensaje)
    return defecto if texto == "" and defecto is not None else int(texto)


def pedir_float(mensaje: str) -> float:
    return float(pedir_texto(mensaje))


def mostrar_menu() -> None:
    print("\n===== RESTAURANTE APP =====")
    print("\nGESTIÓN DE PRODUCTOS")
    for n, desc in OPCIONES_MENU[:5]:
        print(f"{n}. {desc}")
    print("\nGESTIÓN DE USUARIOS")
    for n, desc in OPCIONES_MENU[5:10]:
        print(f"{n}. {desc}")
    print("\nVENTAS")
    for n, desc in OPCIONES_MENU[10:]:
        print(f"{n}. {desc}")


def guardar_productos(archivo: ArchivoServicio, servicio: RestauranteServicio) -> None:
    if not archivo.guardar_productos(servicio.listar_productos()):
        print("No se pudieron guardar los productos.")


def guardar_usuarios(archivo: ArchivoServicio, servicio: RestauranteServicio) -> None:
    if not archivo.guardar_usuarios(servicio.listar_usuarios()):
        print("No se pudieron guardar los usuarios.")


def guardar_ventas(archivo: ArchivoServicio, servicio: RestauranteServicio) -> None:
    if not archivo.guardar_ventas(servicio.listar_ventas()):
        print("No se pudieron guardar las ventas.")


def registrar_producto(servicio: RestauranteServicio, archivo: ArchivoServicio) -> None:
    print("\n--- Registrar Producto ---")
    codigo = pedir_texto("Código: ")
    nombre = pedir_texto("Nombre: ")
    precio = pedir_float("Precio: ")
    stock = pedir_entero("Stock: ")
    try:
        registrado = servicio.registrar_producto(Producto(codigo, nombre, precio, stock))
        print("Producto registrado." if registrado else "El código ya existe.")
        if registrado: guardar_productos(archivo, servicio)
    except ValueError as e:
        print(e)


def buscar_producto(servicio: RestauranteServicio) -> None:
    print("\n--- Buscar Producto ---")
    p = servicio.buscar_producto(pedir_texto("Código: "))
    print(p if p else "Producto no encontrado.")


def actualizar_producto(servicio: RestauranteServicio, archivo: ArchivoServicio) -> None:
    print("\n--- Actualizar Producto ---")
    codigo = pedir_texto("Código: ")
    if not servicio.buscar_producto(codigo):
        print("Producto no encontrado.")
        return
    nombre = pedir_texto("Nuevo nombre: ")
    precio = pedir_float("Nuevo precio: ")
    stock = pedir_entero("Nuevo stock: ")
    if servicio.actualizar_producto(codigo, nombre, precio, stock):
        print("Producto actualizado.")
        guardar_productos(archivo, servicio)
    else:
        print("No se pudo actualizar.")


def eliminar_producto(servicio: RestauranteServicio, archivo: ArchivoServicio) -> None:
    print("\n--- Eliminar Producto ---")
    if servicio.eliminar_producto(pedir_texto("Código: ")):
        print("Producto eliminado.")
        guardar_productos(archivo, servicio)
    else:
        print("Producto no encontrado.")


def listar_productos(servicio: RestauranteServicio) -> None:
    print("\n--- Lista de Productos ---")
    productos = servicio.listar_productos()
    if not productos:
        print("Sin productos registrados.")
        return
    for i, p in enumerate(productos, 1):
        print(f"{i}. {p}")


def registrar_usuario(servicio: RestauranteServicio, archivo: ArchivoServicio) -> None:
    print("\n--- Registrar Usuario ---")
    try:
        registrado = servicio.registrar_usuario(Usuario(pedir_texto("Identificación: "), pedir_texto("Nombre: ")))
        print("Usuario registrado." if registrado else "La identificación ya existe.")
        if registrado: guardar_usuarios(archivo, servicio)
    except ValueError as e:
        print(e)


def buscar_usuario(servicio: RestauranteServicio) -> None:
    print("\n--- Buscar Usuario ---")
    u = servicio.buscar_usuario(pedir_texto("Identificación: "))
    print(u if u else "Usuario no encontrado.")


def actualizar_usuario(servicio: RestauranteServicio, archivo: ArchivoServicio) -> None:
    print("\n--- Actualizar Usuario ---")
    iden = pedir_texto("Identificación: ")
    if not servicio.buscar_usuario(iden):
        print("Usuario no encontrado.")
        return
    if servicio.actualizar_usuario(iden, pedir_texto("Nuevo nombre: ")):
        print("Usuario actualizado.")
        guardar_usuarios(archivo, servicio)
    else:
        print("No se pudo actualizar.")


def eliminar_usuario(servicio: RestauranteServicio, archivo: ArchivoServicio) -> None:
    print("\n--- Eliminar Usuario ---")
    if servicio.eliminar_usuario(pedir_texto("Identificación: ")):
        print("Usuario eliminado.")
        guardar_usuarios(archivo, servicio)
    else:
        print("Usuario no encontrado.")


def listar_usuarios(servicio: RestauranteServicio) -> None:
    print("\n--- Lista de Usuarios ---")
    usuarios = servicio.listar_usuarios()
    if not usuarios:
        print("Sin usuarios registrados.")
        return
    for i, u in enumerate(usuarios, 1):
        print(f"{i}. {u}")


def realizar_venta(servicio: RestauranteServicio, archivo: ArchivoServicio) -> None:
    print("\n--- Realizar Venta ---")
    id_usuario = pedir_texto("Identificación del usuario: ")
    cod_producto = pedir_texto("Código del producto: ")
    cantidad = pedir_entero("Cantidad (Enter para 1): ", 1)
    exito = servicio.realizar_venta(id_usuario, cod_producto, cantidad)
    if exito:
        print("Venta registrada correctamente.")
        guardar_ventas(archivo, servicio)
        guardar_productos(archivo, servicio)
    else:
        print("Venta fallida. Verifique usuario, producto y stock.")


def consultar_ventas_usuario(servicio: RestauranteServicio) -> None:
    print("\n--- Ventas por Usuario ---")
    id_usuario = pedir_texto("Identificación del usuario: ")
    ventas = servicio.consultar_ventas_usuario(id_usuario)
    if not ventas:
        print("Sin ventas para este usuario.")
        return
    print(f"\nTotal de ventas: {len(ventas)}")
    for v in ventas:
        print(v)


def listar_todas_ventas(servicio: RestauranteServicio) -> None:
    print("\n--- Todas las Ventas ---")
    ventas = servicio.listar_ventas()
    if not ventas:
        print("Sin ventas registradas.")
        return
    for i, v in enumerate(ventas, 1):
        print(f"{i}. {v}")


def ejecutar_menu() -> None:
    ruta_datos = Path(__file__).resolve().parent / "datos"
    archivo_servicio = ArchivoServicio(str(ruta_datos))
    servicio = RestauranteServicio(
        archivo_servicio.cargar_productos(),
        archivo_servicio.cargar_usuarios(),
        archivo_servicio.cargar_ventas(),
    )

    opciones = {
        "1": lambda: registrar_producto(servicio, archivo_servicio),
        "2": lambda: buscar_producto(servicio),
        "3": lambda: actualizar_producto(servicio, archivo_servicio),
        "4": lambda: eliminar_producto(servicio, archivo_servicio),
        "5": lambda: listar_productos(servicio),
        "6": lambda: registrar_usuario(servicio, archivo_servicio),
        "7": lambda: buscar_usuario(servicio),
        "8": lambda: actualizar_usuario(servicio, archivo_servicio),
        "9": lambda: eliminar_usuario(servicio, archivo_servicio),
        "10": lambda: listar_usuarios(servicio),
        "11": lambda: realizar_venta(servicio, archivo_servicio),
        "12": lambda: consultar_ventas_usuario(servicio),
        "13": lambda: listar_todas_ventas(servicio),
    }

    while True:
        mostrar_menu()
        op = pedir_texto("Seleccione una opción: ")
        if op == "0":
            print("Gracias por usar Restaurante App.")
            break
        accion = opciones.get(op)
        if accion:
            accion()
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    ejecutar_menu()