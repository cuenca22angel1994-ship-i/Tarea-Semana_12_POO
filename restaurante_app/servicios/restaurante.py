from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class RestauranteServicio:
    def __init__(
        self,
        productos_iniciales: list[Producto] | None = None,
        usuarios_iniciales: list[Usuario] | None = None,
        ventas_iniciales: list[Venta] | None = None,
    ) -> None:
        # === COLECCIONES PRINCIPALES (se mantienen para listar y persistir) ===
        self._productos: list[Producto] = productos_iniciales.copy() if productos_iniciales else []
        self._usuarios: list[Usuario] = usuarios_iniciales.copy() if usuarios_iniciales else []
        self._ventas: list[Venta] = ventas_iniciales.copy() if ventas_iniciales else []

        # === ÍNDICES AUXILIARES (Semana 12 — para búsquedas O(1)) ===
        self._productos_por_codigo: dict[str, Producto] = {}
        self._usuarios_por_identificacion: dict[str, Usuario] = {}
        self._ventas_por_usuario: dict[str, list[Venta]] = {}

        # Reconstruir índices al iniciar
        self._reconstruir_indices()

    def _reconstruir_indices(self) -> None:
        """Reconstruye todos los índices desde las listas principales al cargar desde JSON."""
        self._productos_por_codigo = {p.codigo: p for p in self._productos}
        self._usuarios_por_identificacion = {u.identificacion: u for u in self._usuarios}
        self._ventas_por_usuario.clear()
        for venta in self._ventas:
            self._ventas_por_usuario.setdefault(venta.usuario_id, []).append(venta)

    # ---------- PRODUCTOS ----------
    def registrar_producto(self, producto: Producto) -> bool:
        if self.buscar_producto(producto.codigo) is not None:
            return False
        self._productos.append(producto)
        self._productos_por_codigo[producto.codigo] = producto
        return True

    def buscar_producto(self, codigo: str) -> Producto | None:
        """Búsqueda O(1) mediante índice por código (Semana 12)."""
        codigo = codigo.strip()
        return self._productos_por_codigo.get(codigo)

    def actualizar_producto(self, codigo: str, nuevo_nombre: str, nuevo_precio: float, nuevo_stock: int) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        producto.nombre = nuevo_nombre
        producto.precio = nuevo_precio
        producto.stock = nuevo_stock
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        self._productos.remove(producto)
        self._productos_por_codigo.pop(codigo, None)
        return True

    def listar_productos(self) -> list[Producto]:
        return self._productos.copy()

    # ---------- USUARIOS ----------
    def registrar_usuario(self, usuario: Usuario) -> bool:
        if self.buscar_usuario(usuario.identificacion) is not None:
            return False
        self._usuarios.append(usuario)
        self._usuarios_por_identificacion[usuario.identificacion] = usuario
        return True

    def buscar_usuario(self, identificacion: str) -> Usuario | None:
        """Búsqueda O(1) mediante índice por identificación (Semana 12)."""
        identificacion = identificacion.strip()
        return self._usuarios_por_identificacion.get(identificacion)

    def actualizar_usuario(self, identificacion: str, nuevo_nombre: str) -> bool:
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False
        usuario.nombre = nuevo_nombre
        return True

    def eliminar_usuario(self, identificacion: str) -> bool:
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False
        self._usuarios.remove(usuario)
        self._usuarios_por_identificacion.pop(identificacion, None)
        return True

    def listar_usuarios(self) -> list[Usuario]:
        return self._usuarios.copy()

    # ---------- VENTAS ----------
    def realizar_venta(self, usuario_id: str, producto_codigo: str, cantidad: int = 1) -> bool:
        """Realiza una venta actualizando stock y registrando la venta."""
        usuario = self.buscar_usuario(usuario_id)
        producto = self.buscar_producto(producto_codigo)

        if usuario is None or producto is None:
            return False
        if cantidad <= 0 or producto.stock < cantidad:
            return False

        # Crear y registrar venta
        venta = Venta(usuario.identificacion, producto.codigo, cantidad)
        self._ventas.append(venta)
        self._ventas_por_usuario.setdefault(usuario.identificacion, []).append(venta)

        # Descontar stock
        producto.vender(cantidad)
        return True

    def listar_ventas(self) -> list[Venta]:
        return self._ventas.copy()

    def consultar_ventas_usuario(self, usuario_id: str) -> list[Venta]:
        """Consulta O(1) — no recorre toda la lista de ventas (Semana 12)."""
        usuario_id = usuario_id.strip()
        return self._ventas_por_usuario.get(usuario_id, []).copy()