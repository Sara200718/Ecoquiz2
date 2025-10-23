import flet as ft
import time


# Você deve ter as imagens correspondentes em assets/images/
QUIZ_DATA = [
    {
        "phase": "Fase 1/6",
        "instruction": "Dica: A vida está tendo que começar do zero. O local é novo e estéril (rocha nua), por exemplo, após uma erupção vulcânica.",
        "question": "Pergunta: Este cenário é um exemplo de qual tipo de sucessão ecológica?",
        "image_path": "assets/images/volcano_scene_1.jpg", 
        "options": [
            "Sucessão Primária",
            "Sucessão Secundária",
        ],
        "correct_answer": "Sucessão Primária",
    },
    {
        "phase": "Fase 2/6",
        "instruction": "Dica: São os primeiros organismos a se estabelecerem na rocha nua, quebrando-a e formando o primeiro solo.",
        "question": "Pergunta: Qual grupo de organismos faz parte da primeira Comunidade Pioneira em uma Sucessão Primária?",
        "image_path": "assets/images/lichen_scene_2.jpg",
        "options": [
            "Árvores de grande porte e herbáceas",
            "Líquens e Musgos (Briófitas)",
        ],
        "correct_answer": "Líquens e Musgos (Briófitas)",
    },
    {
        "phase": "Fase 3/6",
        "instruction": "Dica: Essas plantas têm raízes curtas e crescem em um solo ainda fino. Elas vêm depois dos líquens.",
        "question": "Pergunta: Após o estabelecimento dos líquens, o solo fino permite o surgimento de qual tipo de planta?",
        "image_path": "assets/images/grass_scene_3.jpg",
        "options": [
            "Gramíneas e Ervas Daninhas (Herbáceas)",
            "Grandes arbustos lenhosos",
        ],
        "correct_answer": "Gramíneas e Ervas Daninhas (Herbáceas)",
    },
    {
        "phase": "Fase 4/6",
        "instruction": "Dica: O solo já está mais profundo e consegue reter mais água e nutrientes. A luz ainda é abundante.",
        "question": "Pergunta: Que tipo de organismos passa a dominar o ambiente após as gramíneas, competindo por espaço e água?",
        "image_path": "assets/images/shrub_scene_4.jpg",
        "options": [
            "Árvores de dossel",
            "Arbustos e pequenas árvores (Sementes trazidas pelo vento)",
        ],
        "correct_answer": "Arbustos e pequenas árvores (Sementes trazidas pelo vento)",
    },
    {
        "phase": "Fase 5/6",
        "instruction": "Dica: A comunidade está ficando mais complexa e as espécies tolerantes à sombra começam a dominar.",
        "question": "Pergunta: Qual processo faz com que as espécies pioneiras sejam substituídas pelas arbustivas?",
        "image_path": "assets/images/forest_growth_scene_5.jpg",
        "options": [
            "Invasão (Arrival)",
            "Substituição ou Ecese (Successional Change)",
        ],
        "correct_answer": "Substituição ou Ecese (Successional Change)",
    },
    {
        "phase": "Fase 6/6",
        "instruction": "Dica: A comunidade alcançou um estado de relativa estabilidade, com alta biodiversidade e biomassa.",
        "question": "Pergunta: Como é chamada a última etapa da sucessão ecológica, onde o ecossistema está 'maduro'?",
        "image_path": "assets/images/climax_scene_6.jpg",
        "options": [
            "Comunidade Clímax",
            "Estágio Intermediário",
        ],
        "correct_answer": "Comunidade Clímax",
    },
]

# --- 2. TELA DO QUIZ (Fase) - [A LÓGICA PERMANECE A MESMA] ---

class QuizScreen(ft.View):
    def __init__(self, page: ft.Page, question_index: int):
        super().__init__(
            route=f"/quiz/{question_index}", # Garante a rota correta para o pop
            padding=0
        )
        self.page = page
        self.question_index = question_index
        self.question_data = QUIZ_DATA[question_index]
        self.selected_option = ft.Text(value="", visible=False) 
        
        # Cores
        self.GREEN_MAIN = "#558B2F"
        self.YELLOW_ACCENT = "#FBC02D"
        
        # Componentes do Quiz Screen (o corpo da tela de perguntas)
        self.controls = [
            ft.Container(
                expand=True,
                content=ft.Stack(
                    controls=[
                        # 1. Imagem de Fundo
                        ft.Image(
                            src=self.question_data["image_path"],
                            fit=ft.ImageFit.COVER,
                            expand=True,
                        ),
                        # 2. Sobreposição para escurecer
                        ft.Container(bgcolor=ft.colors.BLACK54),

                        # 3. Conteúdo (Topo, Dica, Card de Perguntas)
                        ft.Column(
                            controls=[
                                self._build_top_header(),
                                # Área da Dica
                                ft.Container(
                                    content=ft.Text(self.question_data["instruction"], size=14, color=ft.colors.BLACK87),
                                    bgcolor=ft.colors.GREEN_50,
                                    padding=12,
                                    border=ft.border.all(2, self.GREEN_MAIN),
                                    border_radius=10,
                                    width=300,
                                    alignment=ft.alignment.top_right,
                                    margin=ft.margin.only(top=20, right=20)
                                ),
                                ft.Spacer(),
                                self._build_question_card(),
                            ],
                            expand=True,
                        ),
                    ]
                )
            )
        ]

    def _build_top_header(self):
        # ... (Mantido o mesmo código do header)
        return ft.Container(
            padding=ft.padding.only(left=20, right=20, top=10),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    # Fase (Eco e Texto)
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.icons.ECO, color=self.GREEN_MAIN, size=24),
                                ft.Text(self.question_data["phase"], color=ft.colors.BLACK, weight=ft.FontWeight.BOLD),
                            ]
                        ),
                        padding=ft.padding.symmetric(horizontal=15, vertical=5),
                        bgcolor=ft.colors.WHITE,
                        border=ft.border.all(3, self.GREEN_MAIN),
                        border_radius=20,
                    ),
                    # Ícone de Dica
                    ft.Container(
                        content=ft.Icon(ft.icons.LIGHTBULB_OUTLINE, color=self.YELLOW_ACCENT, size=24),
                        padding=8,
                        bgcolor=ft.colors.WHITE,
                        shape=ft.BoxShape.CIRCLE,
                        border=ft.border.all(3, self.YELLOW_ACCENT),
                    ),
                ]
            )
        )

    def check_answer(self, e):
        """Lógica para verificar a resposta e avançar."""
        if self.selected_option.value != "":
             # Impede múltiplos cliques
             return
        
        option = e.control.data
        self.selected_option.value = option

        is_correct = option == self.question_data["correct_answer"]
        
        # Feedback visual imediato
        e.control.bgcolor = ft.colors.GREEN_400 if is_correct else ft.colors.RED_400
        e.control.border = ft.border.all(4, ft.colors.GREEN_900 if is_correct else ft.colors.RED_900)
        
        # Adiciona a pontuação à sessão
        self.page.session.set("score", self.page.session.get("score", 0) + (1 if is_correct else 0))
        
        self.page.update()
        
        # Feedback e Navegação
        if is_correct:
            message = "CORRETO! Próxima fase em 2 segundos."
        else:
            message = "ERRADO! Avançando para a próxima fase."

        self.page.snack_bar = ft.SnackBar(
            ft.Text(message),
            duration=2000
        )
        self.page.snack_bar.open = True
        self.page.update()
        
        # Espera 2 segundos antes de navegar
        time.sleep(2) 
        
        if self.question_index + 1 < len(QUIZ_DATA):
            # Próxima fase
            self.page.go(f"/quiz/{self.question_index + 1}")
        else:
            # Fim do Quiz
            self.page.go("/results")


    def _build_question_card(self):
        # Cria os botões de opção
        option_buttons = [
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.icons.CHEVRON_RIGHT_ROUNDED, color=self.GREEN_MAIN),
                        ft.Text(option, size=16, weight=ft.FontWeight.W600),
                    ]
                ),
                padding=10,
                margin=ft.margin.symmetric(vertical=8),
                border_radius=8,
                on_click=self.check_answer,
                data=option, # Passa a opção como dado para o evento
            )
            for option in self.question_data["options"]
        ]

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(self.question_data["question"], size=18, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    *option_buttons,
                ],
                tight=True,
                scroll=ft.ScrollMode.ADAPTIVE,
            ),
            width=500,
            padding=15,
            margin=ft.margin.all(20),
            bgcolor=ft.colors.WHITE,
            border_radius=15,
            border=ft.border.all(5, self.GREEN_MAIN),
            shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.BLACK54),
        )


# --- 3. TELA DE INTRODUÇÃO/MISSÃO - [MANTIDA A MESMA] ---

def IntroScreen(page: ft.Page):
    return ft.View(
        "/intro",
        [
            ft.Container(
                expand=True,
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "MISSÃO DE\nSUCESSÃO",
                            size=36,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.WHITE,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            "Reconstrução de um ecossistema",
                            size=18,
                            color=ft.colors.WHITE70,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(height=50),
                        ft.ElevatedButton(
                            text="iniciar missão",
                            on_click=lambda e: page.go("/quiz/0"), # Inicia a Fase 0
                            style=ft.ButtonStyle(
                                bgcolor={ft.MaterialState.DEFAULT: "#558B2F"},
                                color={ft.MaterialState.DEFAULT: ft.colors.WHITE},
                                padding=ft.padding.symmetric(horizontal=40, vertical=15),
                                shape={ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=30)},
                                elevation={ft.MaterialState.DEFAULT: 10}
                            ),
                            content=ft.Row(
                                [ft.Text("iniciar missão", size=20, weight=ft.FontWeight.BOLD), ft.Icon(ft.icons.ARROW_FORWARD)],
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ),
                        ft.Container(height=80)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    main_alignment=ft.MainAxisAlignment.END 
                ),
                image_src="assets/images/mission_background.jpg", 
                image_fit=ft.ImageFit.COVER,
            )
        ],
        padding=0
    )

# --- 4. TELA DE RESULTADOS (Simplificada) - [MANTIDA A MESMA] ---
def ResultsScreen(page: ft.Page):
    score = page.session.get("score", 0)
    total = len(QUIZ_DATA)
    
    return ft.View(
        "/results",
        [
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    [
                        ft.Text("Fim da Missão!", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_800),
                        ft.Text(f"Sua Pontuação Final: {score} de {total}", size=24),
                        ft.ElevatedButton("Recomeçar Missão", on_click=lambda e: page.go("/intro")),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            )
        ]
    )


# --- 5. FUNÇÃO PRINCIPAL DO FLET - [MANTIDA A MESMA] ---

def main(page: ft.Page):
    page.title = "EcoQuiz: Missão de Sucessão Ecológica"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.session.set("score", 0) # Inicializa a pontuação na sessão

    def route_change(route):
        page.views.clear()
        
        if page.route == "/intro" or page.route == "/":
            page.views.append(IntroScreen(page))
        
        elif page.route.startswith("/quiz/"):
            try:
                index = int(page.route.split("/")[-1])
                # Redireciona para resultados se o índice for maior que o número de fases
                if index >= len(QUIZ_DATA):
                    page.go("/results")
                    return
                page.views.append(QuizScreen(page, index))
            except (ValueError, IndexError):
                page.views.append(IntroScreen(page))

        elif page.route == "/results":
            page.views.append(ResultsScreen(page))

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main, assets_dir=".") 
