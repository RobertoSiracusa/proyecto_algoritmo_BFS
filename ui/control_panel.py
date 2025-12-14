"""Panel de controles para la aplicación BFS Visualizer."""

import tkinter as tk
from tkinter import ttk

from config.colors import COLORS, UI_COLORS
from config.styles import BUTTON_STYLE, BUTTON_STYLE_SMALL


class ControlPanel:
    """Panel lateral con todos los controles de la aplicación."""
    
    def __init__(self, parent, callbacks):
        """
        Inicializa el panel de controles.
        
        Args:
            parent: Widget padre de tkinter
            callbacks: Diccionario con funciones callback:
                - 'set_mode': función para cambiar modo
                - 'clear_all': función para limpiar grafo
                - 'start_bfs': función para iniciar BFS
                - 'reset_colors': función para reiniciar colores
                - 'toggle_pause': función para pausar/reanudar
                - 'update_speed': función para actualizar velocidad
        """
        self.callbacks = callbacks
        self.mode_buttons = {}
        
        # Frame exterior para scroll
        self.frame = tk.Frame(parent, bg=UI_COLORS['bg_main'])
        
        # Canvas para scroll
        self.control_canvas = tk.Canvas(
            self.frame, 
            bg=UI_COLORS['bg_main'], 
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            self.frame, 
            orient='vertical', 
            command=self.control_canvas.yview
        )
        self.control_frame = tk.Frame(self.control_canvas, bg=UI_COLORS['bg_main'])
        
        self.control_frame.bind(
            '<Configure>', 
            lambda e: self.control_canvas.configure(scrollregion=self.control_canvas.bbox('all'))
        )
        self.control_window = self.control_canvas.create_window(
            (0, 0), 
            window=self.control_frame, 
            anchor='nw'
        )
        self.control_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Hacer que el frame interno se adapte al ancho del canvas
        def on_canvas_configure(event):
            self.control_canvas.itemconfig(self.control_window, width=event.width)
        self.control_canvas.bind('<Configure>', on_canvas_configure)
        
        self.control_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configurar scroll con rueda del mouse
        self._setup_mousewheel()
        
        # Crear widgets
        self._create_widgets()
    
    def _setup_mousewheel(self):
        """Configura el scroll con la rueda del mouse."""
        def _on_mousewheel(event):
            self.control_canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
        
        def _on_mousewheel_linux(event):
            if event.num == 4:
                self.control_canvas.yview_scroll(-1, 'units')
            elif event.num == 5:
                self.control_canvas.yview_scroll(1, 'units')
        
        self.control_canvas.bind_all('<MouseWheel>', _on_mousewheel)
        self.control_canvas.bind_all('<Button-4>', _on_mousewheel_linux)
        self.control_canvas.bind_all('<Button-5>', _on_mousewheel_linux)
    
    def _create_widgets(self):
        """Crea todos los widgets del panel."""
        # Título
        title_label = tk.Label(
            self.control_frame,
            text="BFS Visualizer",
            font=('Helvetica', 18, 'bold'),
            fg=UI_COLORS['title'],
            bg=UI_COLORS['bg_main']
        )
        title_label.pack(pady=15)
        
        # === Sección: Crear Grafo ===
        self._create_graph_section()
        
        # Separador
        ttk.Separator(self.control_frame, orient='horizontal').pack(
            fill=tk.X, pady=15, padx=10
        )
        
        # === Sección: Algoritmo BFS ===
        self._create_bfs_section()
        
        # Separador
        ttk.Separator(self.control_frame, orient='horizontal').pack(
            fill=tk.X, pady=10, padx=10
        )
        
        # === Sección: Estado ===
        self._create_status_section()
        
        # Separador
        ttk.Separator(self.control_frame, orient='horizontal').pack(
            fill=tk.X, pady=10, padx=10
        )
        
        # === Sección: Leyenda ===
        self._create_legend_section()
        
        # === Sección: Cola BFS ===
        ttk.Separator(self.control_frame, orient='horizontal').pack(
            fill=tk.X, pady=10, padx=10
        )
        self._create_queue_section()
    
    def _create_graph_section(self):
        """Crea la sección de crear grafo."""
        section_label = tk.Label(
            self.control_frame,
            text="Crear Grafo",
            font=('Helvetica', 8, 'bold'),
            fg=UI_COLORS['text_primary'],
            bg=UI_COLORS['bg_main']
        )
        section_label.pack(pady=(10, 5))
        
        create_frame = tk.Frame(self.control_frame, bg=UI_COLORS['bg_main'])
        create_frame.pack(pady=5)
        
        # Botón Agregar Nodo
        self.add_node_btn = tk.Button(
            create_frame,
            text="Agregar Nodo",
            bg=UI_COLORS['btn_primary'],
            fg=UI_COLORS['text_white'],
            command=lambda: self.callbacks['set_mode']('add_node'),
            **BUTTON_STYLE_SMALL
        )
        self.add_node_btn.grid(row=0, column=0, padx=3, pady=3)
        self.mode_buttons['add_node'] = self.add_node_btn
        
        # Botón Agregar Arista
        self.add_edge_btn = tk.Button(
            create_frame,
            text="Agregar Arista",
            bg=UI_COLORS['btn_primary'],
            fg=UI_COLORS['text_white'],
            command=lambda: self.callbacks['set_mode']('add_edge'),
            **BUTTON_STYLE_SMALL
        )
        self.add_edge_btn.grid(row=0, column=1, padx=3, pady=3)
        self.mode_buttons['add_edge'] = self.add_edge_btn
        
        # Botón Eliminar
        self.delete_btn = tk.Button(
            create_frame,
            text="Eliminar",
            bg=UI_COLORS['btn_danger'],
            fg=UI_COLORS['text_white'],
            command=lambda: self.callbacks['set_mode']('delete'),
            **BUTTON_STYLE_SMALL
        )
        self.delete_btn.grid(row=1, column=0, padx=3, pady=3)
        self.mode_buttons['delete'] = self.delete_btn
        
        # Botón Limpiar Todo
        self.clear_btn = tk.Button(
            create_frame,
            text="Limpiar Todo",
            bg=UI_COLORS['btn_danger'],
            fg=UI_COLORS['text_white'],
            command=self.callbacks['clear_all'],
            **BUTTON_STYLE_SMALL
        )
        self.clear_btn.grid(row=1, column=1, padx=3, pady=3)
    
    def _create_bfs_section(self):
        """Crea la sección del algoritmo BFS."""
        section_label = tk.Label(
            self.control_frame,
            text="Algoritmo BFS",
            font=('Helvetica', 8, 'bold'),
            fg=UI_COLORS['text_primary'],
            bg=UI_COLORS['bg_main']
        )
        section_label.pack(pady=(5, 5))
        
        # Botón Iniciar BFS
        self.start_btn = tk.Button(
            self.control_frame,
            text="Iniciar BFS",
            bg=UI_COLORS['btn_success'],
            fg=UI_COLORS['text_white'],
            command=self.callbacks['start_bfs'],
            **BUTTON_STYLE
        )
        self.start_btn.pack(pady=5)
        
        # Botón Reiniciar Colores
        self.reset_btn = tk.Button(
            self.control_frame,
            text="Reiniciar Colores",
            bg=UI_COLORS['btn_info'],
            fg=UI_COLORS['text_white'],
            command=self.callbacks['reset_colors'],
            **BUTTON_STYLE
        )
        self.reset_btn.pack(pady=5)
        
        # Botón Pausar
        self.pause_btn = tk.Button(
            self.control_frame,
            text="Pausar",
            bg=UI_COLORS['btn_warning'],
            fg=UI_COLORS['text_white'],
            disabledforeground=UI_COLORS['text_white'],
            command=self.callbacks['toggle_pause'],
            state=tk.DISABLED,
            **BUTTON_STYLE
        )
        self.pause_btn.pack(pady=5)
        
        # Control de velocidad
        speed_frame = tk.Frame(self.control_frame, bg=UI_COLORS['bg_main'])
        speed_frame.pack(pady=10)
        
        speed_label = tk.Label(
            speed_frame,
            text="Velocidad (ms):",
            font=('Helvetica', 8),
            fg=UI_COLORS['text_primary'],
            bg=UI_COLORS['bg_main']
        )
        speed_label.pack(side=tk.LEFT)
        
        self.speed_var = tk.StringVar(value="500")
        self.speed_entry = tk.Entry(
            speed_frame,
            textvariable=self.speed_var,
            width=6,
            font=('Helvetica', 8),
            bg=UI_COLORS['bg_canvas'],
            fg=UI_COLORS['text_primary'],
            insertbackground=UI_COLORS['text_primary'],
            justify=tk.CENTER,
            relief='solid',
            bd=1
        )
        self.speed_entry.pack(side=tk.LEFT, padx=5)
        self.speed_entry.bind('<Return>', self.callbacks['update_speed'])
        self.speed_entry.bind('<FocusOut>', self.callbacks['update_speed'])
    
    def _create_status_section(self):
        """Crea la sección de estado."""
        self.status_label = tk.Label(
            self.control_frame,
            text="Estado: Selecciona una acción",
            font=('Helvetica', 8, 'bold'),
            fg=UI_COLORS['text_muted'],
            bg=UI_COLORS['bg_main'],
            wraplength=250
        )
        self.status_label.pack(pady=10)
        
        self.instruction_label = tk.Label(
            self.control_frame,
            text="Usa los botones de arriba\npara crear tu grafo",
            font=('Helvetica', 8),
            fg=UI_COLORS['text_secondary'],
            bg=UI_COLORS['bg_main'],
            justify=tk.CENTER
        )
        self.instruction_label.pack(pady=5)
    
    def _create_legend_section(self):
        """Crea la sección de leyenda."""
        legend_label = tk.Label(
            self.control_frame,
            text="Leyenda BFS:",
            font=('Helvetica', 8, 'bold'),
            fg=UI_COLORS['text_primary'],
            bg=UI_COLORS['bg_main']
        )
        legend_label.pack(pady=5)
        
        legend_items = [
            ('Sin visitar', COLORS['unvisited']),
            ('En cola', COLORS['queued']),
            ('Actual', COLORS['current']),
            ('Visitado', COLORS['visited']),
        ]
        
        for text, bg_color in legend_items:
            item_frame = tk.Frame(self.control_frame, bg=UI_COLORS['bg_main'])
            item_frame.pack(anchor='w', padx=30, pady=1)
            
            color_box = tk.Label(
                item_frame, 
                width=2, 
                bg=bg_color, 
                relief='solid', 
                bd=1
            )
            color_box.pack(side=tk.LEFT, padx=(0, 8))
            
            text_label = tk.Label(
                item_frame,
                text=text,
                fg=UI_COLORS['text_primary'],
                bg=UI_COLORS['bg_main'],
                font=('Helvetica', 9)
            )
            text_label.pack(side=tk.LEFT)
    
    def _create_queue_section(self):
        """Crea la sección de visualización de cola."""
        queue_title = tk.Label(
            self.control_frame,
            text="Cola BFS:",
            font=('Helvetica', 8, 'bold'),
            fg=UI_COLORS['text_primary'],
            bg=UI_COLORS['bg_main']
        )
        queue_title.pack(pady=3)
        
        self.queue_label = tk.Label(
            self.control_frame,
            text="[ ]",
            font=('Courier', 8),
            fg=UI_COLORS['queue_text'],
            bg=UI_COLORS['bg_main'],
            wraplength=250
        )
        self.queue_label.pack(pady=3)
    
    # === Métodos públicos para actualizar el estado ===
    
    def update_status(self, text, color=None):
        """Actualiza el texto de estado."""
        if color:
            self.status_label.config(text=text, fg=color)
        else:
            self.status_label.config(text=text)
    
    def update_instruction(self, text):
        """Actualiza el texto de instrucción."""
        self.instruction_label.config(text=text)
    
    def update_queue_display(self, labels):
        """Actualiza la visualización de la cola."""
        if labels:
            self.queue_label.config(text="[ " + " → ".join(labels) + " ]")
        else:
            self.queue_label.config(text="[ ]")
    
    def set_button_active(self, mode):
        """Resalta el botón del modo activo."""
        for btn_mode, btn in self.mode_buttons.items():
            if btn_mode == 'delete':
                btn.config(bg=UI_COLORS['btn_danger'])
            else:
                btn.config(bg=UI_COLORS['btn_primary'])
        
        if mode in self.mode_buttons:
            self.mode_buttons[mode].config(bg=UI_COLORS['btn_active'])
    
    def reset_buttons(self):
        """Resetea todos los botones a su estado normal."""
        for btn_mode, btn in self.mode_buttons.items():
            if btn_mode == 'delete':
                btn.config(bg=UI_COLORS['btn_danger'])
            else:
                btn.config(bg=UI_COLORS['btn_primary'])
    
    def set_start_button_state(self, enabled):
        """Habilita/deshabilita el botón de inicio."""
        self.start_btn.config(state=tk.NORMAL if enabled else tk.DISABLED)
    
    def set_pause_button(self, enabled, text="Pausar", is_paused=False):
        """Configura el botón de pausa."""
        state = tk.NORMAL if enabled else tk.DISABLED
        bg_color = UI_COLORS['btn_resume'] if is_paused else UI_COLORS['btn_warning']
        self.pause_btn.config(
            state=state, 
            text=text, 
            bg=bg_color, 
            fg=UI_COLORS['text_white']
        )
    
    def get_speed_value(self):
        """Obtiene el valor de velocidad del entry."""
        return self.speed_var.get()
    
    def set_speed_value(self, value):
        """Establece el valor de velocidad."""
        self.speed_var.set(str(value))
