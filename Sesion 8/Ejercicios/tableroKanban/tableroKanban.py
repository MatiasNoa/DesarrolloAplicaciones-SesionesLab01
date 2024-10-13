import reflex as rx

class State(rx.State):
    mostrar_solo_pendientes: bool = False
    
    def mostrar_pendientes(self):
        self.mostrar_solo_pendientes = True

#Tareas
def tarjeta_tarea(tarea):
    return rx.box(
        rx.vstack(
            rx.heading(tarea["titulo"], size="sm", color="teal"),
            rx.text(tarea["estado"], color="gray.600"),
            spacing="2",
            align_items="start",
        ),
        padding="4",
        border="1px solid #e2e8f0",
        border_radius="md",
        background="#f7fafc",
        _hover={"background": "#edf2f7", "cursor": "pointer"},
        box_shadow="sm",
        transition="background-color 0.3s ease, box-shadow 0.3s ease",
        width="90%",
    )

#Columnas que incluyen tarjetas
def columna_kanban(nombre, tareas):
    return rx.box(
        rx.vstack(
            rx.heading(nombre, size="lg", color="blue.600", font_weight="bold"),
            rx.vstack(
                rx.foreach( #Recorre el diccionario
                    tareas,
                    #Si mostrar_solo_pendientes es False o la tarea está en "Pendiente"
                    lambda t: rx.cond(
                        ~State.mostrar_solo_pendientes | (t["estado"] == "Pendiente"),
                        tarjeta_tarea(t) #Si la condición es True, muestra la tarjeta de la tarea
                    )
                ),
                spacing="4",
                align_items="center",
            ),
            spacing="6",
            align_items="stretch",
        ),
        padding="6",
        border="1px solid #e2e8f0",
        border_radius="lg",
        background="white",
        box_shadow="md",
        width="100%",
    )

tareas_pendientes = [
    {"titulo": "Tarea 1", "estado": "Pendiente"},
    {"titulo": "Tarea 2", "estado": "Completada"},
    {"titulo": "Tarea 3", "estado": "En progreso"},
    {"titulo": "Tarea 4", "estado": "Pendiente"},
    {"titulo": "Tarea 5", "estado": "Completada"},
]

tareas_en_progreso = [
    {"titulo": "Tarea 6", "estado": "En progreso"},
    {"titulo": "Tarea 7", "estado": "Pendiente"},
    {"titulo": "Tarea 8", "estado": "Completada"},
    {"titulo": "Tarea 9", "estado": "Pendiente"},
]

tareas_completadas = [
    {"titulo": "Tarea 10", "estado": "Pendiente"},
    {"titulo": "Tarea 11", "estado": "Pendiente"},
    {"titulo": "Tarea 12", "estado": "Completada"},
    {"titulo": "Tarea 13", "estado": "Pendiente"},
    {"titulo": "Tarea 14", "estado": "Pendiente"},
]

def contar_tareas_por_estado(tareas):
    contadores = {}
    for tarea in tareas:
        estado = tarea["estado"]
        if estado in contadores:
            contadores[estado] += 1
        else:
            contadores[estado] = 1
    return contadores

todas_las_tareas = tareas_pendientes + tareas_en_progreso + tareas_completadas
contadores = contar_tareas_por_estado(todas_las_tareas)

def index():
    return rx.container(
        rx.vstack(
            rx.hstack(
                columna_kanban("Pendientes", tareas_pendientes),
                columna_kanban("Haciendo", tareas_en_progreso),
                columna_kanban("Realizado", tareas_completadas),
                spacing="6",
                width="100%",
                justify="space-between",
            ),
            rx.box(f"Pendientes: {contadores.get('Pendiente', 0)}"),
            rx.box(f"En Progreso: {contadores.get('En progreso', 0)}"),
            rx.box(f"Completada: {contadores.get('Completada', 0)}"),
            rx.button(
                "Ver pendientes",
                width="100%",
                on_click=State.mostrar_pendientes,
                color_scheme="teal",
                size="lg",
                border_radius="md",
                box_shadow="sm",
                _hover={"background": "#2b6cb0", "color": "white"},
            ),
            width="100%",
            spacing="8",
        ),
        max_width="1200px",
        padding="6",
        background="#f7fafc",
    )

app = rx.App()
app.add_page(index)
