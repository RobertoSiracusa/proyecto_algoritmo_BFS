# Visualizador de Algoritmo BFS

Una aplicación interactiva desarrollada en Python con Tkinter para visualizar el algoritmo de Búsqueda en Anchura (Breadth-First Search) en grafos.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)

## Descripción

Esta aplicación permite crear grafos de forma interactiva y visualizar paso a paso cómo funciona el algoritmo BFS. Ideal para estudiantes que desean comprender el funcionamiento de este algoritmo de búsqueda fundamental en teoría de grafos.

### Características principales:
- ✅ Crear nodos haciendo clic en el canvas
- ✅ Conectar nodos con aristas
- ✅ Eliminar nodos y aristas
- ✅ Visualización animada del algoritmo BFS
- ✅ Control de velocidad de animación
- ✅ Pausar/Reanudar la ejecución
- ✅ Visualización de la cola BFS en tiempo real

---

## Estructura del Proyecto

```
proyecto_algoritmo_BFS/
│
├── main.py                 # Punto de entrada de la aplicación
├── bfs_visualizer.py       # Versión monolítica (legacy)
├── readme.md               # Este archivo
│
├── algorithms/             # Módulo de algoritmos
│   ├── __init__.py
│   └── bfs.py              # Implementación del algoritmo BFS
│
├── config/                 # Configuración de la aplicación
│   ├── __init__.py
│   ├── colors.py           # Paleta de colores (UI y estados)
│   └── styles.py           # Estilos de widgets (botones)
│
├── models/                 # Estructuras de datos
│   ├── __init__.py
│   └── graph.py            # Clase Graph (nodos, aristas, adyacencias)
│
└── ui/                     # Componentes de interfaz
    ├── __init__.py
    ├── app.py              # Aplicación principal (BFSVisualizerApp)
    ├── control_panel.py    # Panel de control lateral
    └── graph_canvas.py     # Canvas para dibujar el grafo
```

### Descripción de módulos:

| Módulo | Archivo | Descripción |
|--------|---------|-------------|
| **algorithms** | `bfs.py` | Contiene la lógica pura del algoritmo BFS |
| **config** | `colors.py` | Define todos los colores de la interfaz |
| **config** | `styles.py` | Define estilos para botones y widgets |
| **models** | `graph.py` | Estructura de datos del grafo |
| **ui** | `app.py` | Clase principal que coordina toda la app |
| **ui** | `control_panel.py` | Panel con botones y controles |
| **ui** | `graph_canvas.py` | Área de dibujo del grafo |

---

## Cómo Ejecutar

### Requisitos
- Python 3.x
- Tkinter (incluido en la mayoría de instalaciones de Python)

### Ejecución

```bash
cd proyecto_algoritmo_BFS
python main.py
```

---

## Cómo Cambiar los Colores de la UI

Todos los colores de la aplicación están centralizados en el archivo `config/colors.py`. Puedes modificarlos fácilmente:

### Colores de los estados de nodos (durante BFS)

```python
# Archivo: config/colors.py

COLORS = {
    'unvisited': '#E8E8E8',      # Color del nodo sin visitar (gris claro)
    'queued': '#FFD700',          # Color del nodo en cola (amarillo/dorado)
    'current': '#FF4444',         # Color del nodo actual (rojo)
    'visited': '#4CAF50',         # Color del nodo visitado (verde)
    'edge': '#666666',            # Color de arista normal (gris)
    'edge_traversed': '#2196F3',  # Color de arista recorrida (azul)
}
```

### Colores de la interfaz de usuario

```python
UI_COLORS = {
    # Fondos
    'bg_main': '#FAF9F6',         # Fondo principal de la ventana
    'bg_canvas': '#FFFFFF',       # Fondo del canvas donde se dibuja
    'bg_separator': '#D0D0D0',    # Color del separador

    # Texto
    'text_primary': '#333333',    # Texto principal
    'text_secondary': '#555555',  # Texto secundario
    'text_muted': '#666666',      # Texto atenuado

    # Botones
    'btn_primary': '#1976D2',     # Botón primario (azul)
    'btn_danger': '#C62828',      # Botón de peligro (rojo)
    'btn_success': '#4CAF50',     # Botón de éxito (verde)
    'btn_info': '#2196F3',        # Botón informativo (azul claro)
    'btn_warning': '#E65100',     # Botón de advertencia (naranja)

    # Otros
    'title': '#2E7D32',           # Color del título
    'queue_text': '#B8860B',      # Color del texto de la cola
}
```

### Ejemplo: Cambiar a tema oscuro

Para crear un tema oscuro, modifica los valores en `config/colors.py`:

```python
UI_COLORS = {
    'bg_main': '#1E1E1E',         # Fondo oscuro
    'bg_canvas': '#2D2D2D',       # Canvas oscuro
    'text_primary': '#FFFFFF',    # Texto blanco
    'text_secondary': '#CCCCCC',  # Texto gris claro
    # ... etc
}
```

---

## Implementación del Algoritmo BFS

El algoritmo BFS está implementado en `algorithms/bfs.py`. A continuación se explica su funcionamiento:

### Código del Algoritmo

```python
from collections import deque

def generate_bfs_steps(graph, start_node):
    """
    Genera los pasos del algoritmo BFS para animación.
    
    Args:
        graph: Objeto Graph con los nodos y adyacencias
        start_node: ID del nodo inicial
        
    Returns:
        Lista de tuplas representando cada paso del algoritmo
    """
    steps = []
    bfs_queue = deque([start_node])    # Cola inicializada con nodo inicial
    visited = {start_node}              # Conjunto de nodos visitados
    
    while bfs_queue:                    # Mientras la cola no esté vacía
        current = bfs_queue.popleft()   # Extraer primer elemento
        steps.append(('visit', current, list(bfs_queue)))
        
        # Obtener vecinos ordenados alfabéticamente
        neighbors = sorted(graph.get_neighbors(current))
        
        for neighbor in neighbors:
            if neighbor not in visited:       # Si no ha sido visitado
                visited.add(neighbor)         # Marcar como visitado
                bfs_queue.append(neighbor)    # Agregar a la cola
                steps.append(('enqueue', neighbor, current, list(bfs_queue)))
        
        steps.append(('done', current, list(bfs_queue)))
    
    return steps
```

### Explicación del Algoritmo

1. **Inicialización**:
   - Se crea una cola (`deque`) con el nodo inicial
   - Se crea un conjunto `visited` para rastrear nodos ya visitados

2. **Bucle principal**:
   - Mientras la cola tenga elementos:
     - Extraer el primer nodo de la cola (`popleft`)
     - Obtener los vecinos del nodo actual
     - Para cada vecino no visitado:
       - Marcarlo como visitado
       - Agregarlo al final de la cola

3. **Generación de pasos**:
   - El algoritmo genera una lista de pasos para la animación:
     - `('visit', node_id, queue)`: Indica que un nodo está siendo procesado
     - `('enqueue', node_id, from_node, queue)`: Indica que un nodo fue agregado a la cola
     - `('done', node_id, queue)`: Indica que un nodo terminó de procesarse

### Visualización de Estados

| Estado | Color | Descripción |
|--------|-------|-------------|
| Sin visitar | Gris (#E8E8E8) | Nodo aún no descubierto |
| En cola | Amarillo (#FFD700) | Nodo descubierto, esperando ser procesado |
| Actual | Rojo (#FF4444) | Nodo siendo procesado actualmente |
| Visitado | Verde (#4CAF50) | Nodo completamente procesado |

### Complejidad

- **Tiempo**: O(V + E) donde V = número de vértices, E = número de aristas
- **Espacio**: O(V) para almacenar la cola y el conjunto de visitados

---

## Uso de la Aplicación

### Crear el grafo
1. **Agregar nodos**: Clic en "Agregar Nodo" → Clic en el canvas
2. **Agregar aristas**: Clic en "Agregar Arista" → Clic en nodo 1 → Clic en nodo 2
3. **Eliminar**: Clic en "Eliminar" → Clic en nodo o arista

### Ejecutar BFS
1. Clic en "Iniciar BFS"
2. Selecciona el nodo inicial haciendo clic en él
3. Observa la animación
4. Usa "Pausar/Reanudar" para controlar la ejecución
5. Ajusta la velocidad (50-5000 ms) según necesites

### Controles adicionales
- **Reiniciar Colores**: Restaura los colores originales del grafo
- **Limpiar Todo**: Elimina todos los nodos y aristas

---

## Autor

Proyecto desarrollado para la materia **Estructuras Discretas 2**.