import customtkinter as ctk
from tkinter import messagebox
from services.inventario import InventarioService
from ui.productos import FormularioProducto

ctk.set_appearance_mode('light')
ctk.set_default_color_theme('blue')

NAVY = '#172B4D'
BLUE = '#2563EB'
BG = '#F3F6FB'
WHITE = '#FFFFFF'
TEXT = '#172B4D'
MUTED = '#64748B'
BORDER = '#E2E8F0'


class VentanaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Sistema de Inventario | Panel de gestión')
        self.geometry('1280x760')
        self.minsize(1050, 650)
        self.configure(fg_color=BG)
        self.servicio = InventarioService()
        self.tarjetas = {}
        self.producto_seleccionado = None
        self.filas = {}
        self.vista_actual = 'Panel principal'

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.crear_menu()
        self.contenido = ctk.CTkFrame(self, fg_color='transparent', corner_radius=0)
        self.contenido.grid(row=0, column=1, sticky='nsew', padx=30, pady=26)
        self.contenido.grid_columnconfigure(0, weight=1)
        self.contenido.grid_rowconfigure(0, weight=1)
        self.mostrar_vista('Panel principal')

    def crear_menu(self):
        menu = ctk.CTkFrame(self, width=218, fg_color=NAVY, corner_radius=0)
        menu.grid(row=0, column=0, sticky='nsew')
        menu.grid_propagate(False)
        ctk.CTkLabel(menu, text='◈  INVENTARIO', font=('Segoe UI', 21, 'bold'),
                     text_color=WHITE).pack(anchor='w', padx=23, pady=(36, 8))
        ctk.CTkLabel(menu, text='GESTIÓN EMPRESARIAL', font=('Segoe UI', 10, 'bold'),
                     text_color='#A7B8D2').pack(anchor='w', padx=26, pady=(0, 35))
        self.botones_menu = {}
        for nombre, icono in [('Panel principal', '▦'), ('Productos', '▤'), ('Movimientos', '⇄')]:
            boton = ctk.CTkButton(
                menu, text=f'  {icono}    {nombre}', height=46, anchor='w',
                fg_color='transparent', hover_color='#29456E', corner_radius=9,
                text_color='#E8EEF7', font=('Segoe UI', 13),
                command=lambda n=nombre: self.mostrar_vista(n)
            )
            boton.pack(fill='x', padx=13, pady=5)
            self.botones_menu[nombre] = boton
        ctk.CTkLabel(menu, text='Sistema de Inventario  •  v1.0',
                     text_color='#A7B8D2', font=('Segoe UI', 10)).pack(side='bottom', pady=25)

    def limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def mostrar_vista(self, nombre):
        self.vista_actual = nombre
        self.producto_seleccionado = None
        self.limpiar_contenido()
        for titulo, boton in self.botones_menu.items():
            boton.configure(fg_color='#315483' if titulo == nombre else 'transparent')
        if nombre == 'Movimientos':
            self.crear_movimientos()
        else:
            self.crear_panel(nombre)

    def crear_panel(self, vista='Panel principal'):
        principal = ctk.CTkFrame(self.contenido, fg_color='transparent')
        principal.grid(row=0, column=0, sticky='nsew')
        principal.grid_columnconfigure(0, weight=1)
        principal.grid_rowconfigure(3, weight=1)

        titulo = 'Panel de Inventario' if vista == 'Panel principal' else 'Gestión de Productos'
        ctk.CTkLabel(principal, text=titulo, font=('Segoe UI', 28, 'bold'),
                     text_color=TEXT).grid(row=0, column=0, sticky='w')
        ctk.CTkLabel(principal, text='Control y administración de tu inventario',
                     font=('Segoe UI', 13), text_color=MUTED).grid(
                         row=1, column=0, sticky='w', pady=(4, 20))

        tarjetas = ctk.CTkFrame(principal, fg_color='transparent')
        tarjetas.grid(row=2, column=0, sticky='ew', pady=(0, 20))
        for i in range(4):
            tarjetas.grid_columnconfigure(i, weight=1, uniform='cards')
        for i, (nombre, icono) in enumerate([
            ('Total de productos', '▤'), ('Unidades disponibles', '▦'),
            ('Valor del inventario', '$'), ('Stock bajo', '!')
        ]):
            tarjeta = ctk.CTkFrame(tarjetas, fg_color=WHITE, corner_radius=13,
                                   border_width=1, border_color=BORDER, height=112)
            tarjeta.grid(row=0, column=i, sticky='ew', padx=(0, 10) if i < 3 else 0)
            tarjeta.grid_propagate(False)
            ctk.CTkLabel(tarjeta, text=nombre, font=('Segoe UI', 12),
                         text_color=MUTED).pack(anchor='w', padx=20, pady=(18, 4))
            valor = ctk.CTkLabel(tarjeta, text='0', font=('Segoe UI', 24, 'bold'),
                                 text_color=TEXT)
            valor.pack(anchor='w', padx=20)
            self.tarjetas[nombre] = valor

        tarjeta_tabla = ctk.CTkFrame(principal, fg_color=WHITE, corner_radius=14,
                                     border_width=1, border_color=BORDER)
        tarjeta_tabla.grid(row=3, column=0, sticky='nsew')
        tarjeta_tabla.grid_columnconfigure(0, weight=1)
        tarjeta_tabla.grid_rowconfigure(2, weight=1)

        barra = ctk.CTkFrame(tarjeta_tabla, fg_color='transparent')
        barra.grid(row=0, column=0, sticky='ew', padx=22, pady=(20, 15))
        barra.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(barra, text='Productos registrados', font=('Segoe UI', 19, 'bold'),
                     text_color=TEXT).grid(row=0, column=0, sticky='w')
        ctk.CTkButton(barra, text='+  Nuevo producto', height=38, width=160,
                      fg_color=BLUE, hover_color='#1D4ED8', corner_radius=8,
                      font=('Segoe UI', 12, 'bold'), command=self.abrir_formulario).grid(
                          row=0, column=1, sticky='e')

        herramientas = ctk.CTkFrame(tarjeta_tabla, fg_color='transparent')
        herramientas.grid(row=1, column=0, sticky='ew', padx=22, pady=(0, 14))
        herramientas.grid_columnconfigure(0, weight=1)
        self.buscador = ctk.CTkEntry(
            herramientas, placeholder_text='Buscar por código, nombre o categoría...',
            height=39, corner_radius=8, border_color=BORDER, fg_color='#FAFCFF',
            text_color=TEXT, font=('Segoe UI', 12))
        self.buscador.grid(row=0, column=0, sticky='ew', padx=(0, 12))
        self.buscador.bind('<KeyRelease>', lambda _evento: self.buscar_productos())
        ctk.CTkButton(herramientas, text='Editar', width=92, height=38,
                      fg_color='#EDF3FC', hover_color='#DCE9FC', text_color=TEXT,
                      command=self.editar_producto).grid(row=0, column=1, padx=(0, 8))
        ctk.CTkButton(herramientas, text='Eliminar', width=92, height=38,
                      fg_color='#EDF3FC', hover_color='#DCE9FC', text_color=TEXT,
                      command=self.eliminar_producto).grid(row=0, column=2)

        # Tabla hecha con CustomTkinter: sin separadores arrastrables.
        tabla = ctk.CTkFrame(tarjeta_tabla, fg_color=WHITE, corner_radius=0)
        tabla.grid(row=2, column=0, sticky='nsew', padx=22)
        tabla.grid_columnconfigure(0, weight=1)
        tabla.grid_rowconfigure(1, weight=1)
        encabezado = ctk.CTkFrame(tabla, fg_color='#EDF3FA', corner_radius=7, height=43)
        encabezado.grid(row=0, column=0, sticky='ew')
        encabezado.grid_propagate(False)
        self.configurar_columnas(encabezado)
        for i, titulo_col in enumerate(('Código', 'Producto', 'Categoría', 'Precio', 'Cantidad')):
            ctk.CTkLabel(encabezado, text=titulo_col, font=('Segoe UI', 12, 'bold'),
                         text_color=TEXT, anchor='w').grid(row=0, column=i, sticky='nsew', padx=12)
        self.tabla_contenido = ctk.CTkScrollableFrame(
            tabla, fg_color=WHITE, corner_radius=0,
            scrollbar_button_color='#CBD5E1', scrollbar_button_hover_color='#94A3B8')
        self.tabla_contenido.grid(row=1, column=0, sticky='nsew', pady=(4, 0))
        self.configurar_columnas(self.tabla_contenido)

        pie = ctk.CTkFrame(tarjeta_tabla, fg_color='transparent')
        pie.grid(row=3, column=0, sticky='ew', padx=22, pady=(10, 16))
        self.contador = ctk.CTkLabel(pie, text='0 productos', font=('Segoe UI', 11),
                                     text_color=MUTED)
        self.contador.pack(side='left')
        ctk.CTkLabel(pie, text='Selecciona una fila para editar o eliminar',
                     font=('Segoe UI', 11), text_color=MUTED).pack(side='right')
        self.actualizar_productos()

    @staticmethod
    def configurar_columnas(frame):
        for indice, peso in enumerate((2, 4, 3, 2, 2)):
            frame.grid_columnconfigure(indice, weight=peso, uniform='tabla')

    def dibujar_productos(self, productos):
        for widget in self.tabla_contenido.winfo_children():
            widget.destroy()
        self.filas = {}
        self.producto_seleccionado = None
        self.contador.configure(text=f'{len(productos)} producto(s)')
        if not productos:
            ctk.CTkLabel(self.tabla_contenido, text='No se encontraron productos.',
                         font=('Segoe UI', 13), text_color=MUTED).grid(
                             row=0, column=0, columnspan=5, pady=35)
            return
        for indice, producto in enumerate(productos):
            codigo = producto['codigo']
            fondo = WHITE if indice % 2 == 0 else '#F8FAFD'
            valores = (codigo, producto['nombre'], producto['categoria'],
                       f"RD$ {producto['precio']:,.2f}", str(producto['cantidad']))
            etiquetas = []
            for columna, valor in enumerate(valores):
                etiqueta = ctk.CTkLabel(
                    self.tabla_contenido, text=str(valor), anchor='w',
                    font=('Segoe UI', 12), text_color=TEXT, fg_color=fondo,
                    corner_radius=0, height=43)
                etiqueta.grid(row=indice, column=columna, sticky='ew', padx=1, pady=1)
                etiqueta.bind('<Button-1>', lambda _e, p=producto: self.seleccionar_producto(p))
                etiquetas.append(etiqueta)
            self.filas[codigo] = (etiquetas, fondo)

    def seleccionar_producto(self, producto):
        for etiquetas, fondo in self.filas.values():
            for etiqueta in etiquetas:
                etiqueta.configure(fg_color=fondo)
        self.producto_seleccionado = producto
        for etiqueta in self.filas[producto['codigo']][0]:
            etiqueta.configure(fg_color='#DBEAFE')

    def actualizar_productos(self):
        if self.vista_actual == 'Movimientos':
            return
        estadisticas = self.servicio.obtener_estadisticas()
        valores = {
            'Total de productos': estadisticas['productos'],
            'Unidades disponibles': estadisticas['unidades'],
            'Valor del inventario': f"RD$ {estadisticas['valor']:,.2f}",
            'Stock bajo': estadisticas['stock_bajo']
        }
        for titulo, valor in valores.items():
            self.tarjetas[titulo].configure(text=str(valor))
        self.buscar_productos()

    def buscar_productos(self):
        texto = self.buscador.get().strip()
        if texto:
            # Filtro local: también admite categoría, sin depender del SQL del servicio.
            productos = [p for p in self.servicio.listar_productos()
                         if any(texto.casefold() in str(p[c]).casefold()
                                for c in ('codigo', 'nombre', 'categoria'))]
        else:
            productos = self.servicio.listar_productos()
        self.dibujar_productos(productos)

    def abrir_formulario(self):
        FormularioProducto(self, self.actualizar_productos)

    def obtener_producto_seleccionado(self):
        if self.producto_seleccionado is None:
            messagebox.showwarning('Seleccionar producto', 'Primero selecciona un producto de la tabla.')
        return self.producto_seleccionado

    def editar_producto(self):
        producto = self.obtener_producto_seleccionado()
        if producto is not None:
            FormularioProducto(self, self.actualizar_productos, producto=producto)

    def eliminar_producto(self):
        producto = self.obtener_producto_seleccionado()
        if producto is None:
            return
        if not messagebox.askyesno('Confirmar eliminación',
                                   f"¿Seguro que deseas eliminar '{producto['nombre']}'?"):
            return
        if self.servicio.eliminar_producto(producto['id']):
            self.actualizar_productos()
            messagebox.showinfo('Producto eliminado', 'El producto fue eliminado correctamente.')
        else:
            messagebox.showerror('Error', 'No se pudo eliminar el producto.')

    def crear_movimientos(self):
        marco = ctk.CTkFrame(self.contenido, fg_color='transparent')
        marco.grid(row=0, column=0, sticky='nsew')
        marco.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(marco, text='Movimientos de inventario',
                     font=('Segoe UI', 28, 'bold'), text_color=TEXT).grid(
                         row=0, column=0, sticky='w')
        ctk.CTkLabel(marco, text='Registra entradas y salidas de mercancía',
                     font=('Segoe UI', 13), text_color=MUTED).grid(
                         row=1, column=0, sticky='w', pady=(4, 24))
        tarjeta = ctk.CTkFrame(marco, fg_color=WHITE, corner_radius=14,
                               border_width=1, border_color=BORDER)
        tarjeta.grid(row=2, column=0, sticky='ew')
        tarjeta.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(tarjeta, text='Registrar movimiento',
                     font=('Segoe UI', 19, 'bold'), text_color=TEXT).grid(
                         row=0, column=0, sticky='w', padx=25, pady=(24, 18))
        productos = self.servicio.listar_productos()
        self.productos_movimiento = {f"{p['codigo']}  ·  {p['nombre']}": p for p in productos}
        opciones = list(self.productos_movimiento) or ['No hay productos registrados']
        ctk.CTkLabel(tarjeta, text='Producto', text_color=TEXT,
                     font=('Segoe UI', 12)).grid(row=1, column=0, sticky='w', padx=25)
        self.selector_producto = ctk.CTkOptionMenu(tarjeta, values=opciones, height=40,
                                                    fg_color='#EDF3FA', button_color='#DCE8F7',
                                                    button_hover_color='#CBDCF3', text_color=TEXT)
        self.selector_producto.grid(row=2, column=0, sticky='ew', padx=25, pady=(7, 18))
        ctk.CTkLabel(tarjeta, text='Tipo de movimiento', text_color=TEXT,
                     font=('Segoe UI', 12)).grid(row=3, column=0, sticky='w', padx=25)
        self.selector_tipo = ctk.CTkSegmentedButton(tarjeta, values=['Entrada', 'Salida'],
                                                    selected_color=BLUE, selected_hover_color='#1D4ED8')
        self.selector_tipo.set('Entrada')
        self.selector_tipo.grid(row=4, column=0, sticky='w', padx=25, pady=(8, 18))
        ctk.CTkLabel(tarjeta, text='Cantidad', text_color=TEXT,
                     font=('Segoe UI', 12)).grid(row=5, column=0, sticky='w', padx=25)
        self.cantidad_movimiento = ctk.CTkEntry(tarjeta, height=40,
                                                placeholder_text='Ej.: 5', border_color=BORDER)
        self.cantidad_movimiento.grid(row=6, column=0, sticky='ew', padx=25, pady=(7, 20))
        ctk.CTkButton(tarjeta, text='Guardar movimiento', fg_color=BLUE,
                      hover_color='#1D4ED8', height=42, font=('Segoe UI', 12, 'bold'),
                      command=self.guardar_movimiento).grid(row=7, column=0, sticky='e',
                                                             padx=25, pady=(0, 25))
        ctk.CTkLabel(marco, text='Los movimientos actualizan las existencias del producto.',
                     text_color=MUTED, font=('Segoe UI', 12)).grid(
                         row=3, column=0, sticky='w', pady=(16, 0))

    def guardar_movimiento(self):
        producto = self.productos_movimiento.get(self.selector_producto.get())
        if producto is None:
            messagebox.showwarning('Sin productos', 'Primero registra un producto.')
            return
        try:
            cantidad = int(self.cantidad_movimiento.get().strip())
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning('Cantidad inválida', 'Introduce un número entero mayor que cero.')
            return
        tipo = self.selector_tipo.get().lower()
        try:
            resultado = self.servicio.registrar_movimiento(producto['id'], tipo, cantidad)
            if resultado is False:
                messagebox.showerror('Movimiento rechazado', 'No se pudo registrar el movimiento. Verifica las existencias.')
                return
        except Exception as error:
            messagebox.showerror('No se pudo registrar', str(error))
            return
        messagebox.showinfo('Movimiento registrado', 'Las existencias se actualizaron correctamente.')
        self.mostrar_vista('Movimientos')
