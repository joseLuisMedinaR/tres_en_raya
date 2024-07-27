import flet as ft

# Variables globales para el estado del juego
jugador = "X"
tablero = [""] * 9
botones = []

def items(page):
    global botones
    botones = []  # Reiniciar la lista de botones
    items = []
    for i in range(9):
        boton = ft.Container(
            content=ft.Text("", weight="bold"),
            alignment=ft.alignment.center,
            width=50,
            height=50,
            bgcolor=ft.colors.BLUE_400,
            border_radius=ft.border_radius.all(5),
            on_click=lambda e, i=i: marcar_jugada(page, i)
        )
        botones.append(boton)
        items.append(boton)
    return items

def marcar_jugada(page, indice):
    global jugador, tablero, botones
    if tablero[indice] == "" and not verificar_jugada():
        tablero[indice] = jugador
        color = ft.colors.PURPLE_ACCENT_200 if jugador == "X" else ft.colors.PINK_500
        botones[indice].content = ft.Text(jugador, color=color, weight="bold")
        botones[indice].update()
        if verificar_jugada():
            mostrar_mensaje(page, f"Gano: Jugador {jugador}")
        elif "" not in tablero:
            mostrar_mensaje(page, "Empatan")
        else:
            jugador = "O" if jugador == "X" else "X"

def verificar_jugada():
    jugadas_ganadoras = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for a, b, c in jugadas_ganadoras:
        if tablero[a] == tablero[b] == tablero[c] != "":
            return True
    return False

def mostrar_mensaje(page, mensaje):
    dlg = ft.AlertDialog(
        title=ft.Text("Fin del juego", color=ft.colors.LIGHT_BLUE_300),
        content=ft.Text(mensaje, color=ft.colors.LIGHT_BLUE_400),
        actions=[
            ft.TextButton("Aceptar", on_click=lambda e: cerrar_dialogo(page, dlg))
        ],
    )
    page.overlay.append(dlg)
    dlg.open = True
    page.update()

def cerrar_dialogo(page, dlg):
    dlg.open = False
    page.update()

# Inicializar la interfaz del juego
def main(page: ft.Page):
    page.title = "Tres en Raya"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 300
    page.window.height = 300
    page.window.maximized = False
    page.window.minimizable = False
    
    page.add(
        ft.Column(
            [
                ft.Row(
                    wrap=True,
                    spacing=5,
                    run_spacing=5,
                    controls=items(page),
                    width=192,
                    alignment=ft.MainAxisAlignment.CENTER,  # Centramos los botones horizontalmente
                ),
                ft.CupertinoButton(
                    content=ft.Text("Volver a Jugar"),
                    bgcolor=ft.colors.BLUE_200,
                    opacity_on_click=0.5,
                    on_click=lambda e: page.open(confirmar_reinicio),
                ),
                ft.CupertinoButton(
                    content=ft.Text("Salir"),
                    bgcolor=ft.colors.BLUE_200,
                    opacity_on_click=0.5,
                    on_click=lambda e: page.open(confirmar_salida),
                ),
            ],
            alignment="center",  # Centra la columna verticalmente
            horizontal_alignment=ft.CrossAxisAlignment.CENTER  # Centra el contenido horizontalmente
        )
    )
    page.update()

    def reiniciar_juego(page):
        global jugador, tablero
        jugador = "X"
        tablero = [""] * 9
        # Actualizar la interfaz para reflejar el estado reiniciado
        for boton in botones:
            boton.content = ft.Text("", weight="bold")
            boton.update()
        page.close(confirmar_reinicio)

    def salir_juego(e):
        page.close(confirmar_salida)

    confirmar_salida = ft.AlertDialog(
        modal=True,
        title=ft.Text("Salir"),
        content=ft.Text("¿Desea salir del juego?"),
        actions=[
            ft.TextButton("Si", on_click=lambda e: page.window.close(),),
            ft.TextButton("No", on_click=salir_juego),
        ],
    )

    def reinico_juego(e):
        page.close(confirmar_reinicio)

    confirmar_reinicio = ft.AlertDialog(
        modal=True,
        title=ft.Text("Reiniciar"),
        content=ft.Text("¿Desea reiniciar el juego?"),
        actions=[
            ft.TextButton("Si", on_click=lambda e: reiniciar_juego(page)),
            ft.TextButton("No", on_click=reinico_juego),
        ],
    )

ft.app(target=main)