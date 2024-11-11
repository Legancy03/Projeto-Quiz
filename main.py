import pygame
import sys
import random
import os


class QuizGame:
    def __init__(self):
        self.background_image = None
        self.font = None
        self.screen = None
        pygame.init()
        pygame.mixer.init()

        # Configurações do jogo
        self.colors = {"WHITE": (255, 255, 255), "BLACK": (0, 0, 0), "BLUE": (0, 0, 255)}
        self.dimensions = {"WIDTH": 800, "HEIGHT": 600}
        self.setup_screen()
        self.load_assets()

        # Variáveis do jogo
        self.question_text = ""
        self.question_index = 0
        self.score = 0
        self.max_questions = 4

    def setup_screen(self):
        # Configurações da tela
        self.screen = pygame.display.set_mode((self.dimensions["WIDTH"], self.dimensions["HEIGHT"]))
        pygame.display.set_caption("Quiz de Matemática")
        self.font = pygame.font.SysFont("Comic Sans", 36)

    def load_assets(self):
        # Carregar imagem de fundo
        background_image_files = [f"battleback{i}.png" for i in range(1, 11)]
        selected_image = random.choice(background_image_files)
        self.background_image = pygame.image.load(os.path.join("Assets", selected_image))
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (self.dimensions["WIDTH"], self.dimensions["HEIGHT"]))
        # Carregar música de fundo
        pygame.mixer.music.load(os.path.join("Assets", "Woodland Fantasy.mp3"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def generate_question(self):
        # Gera uma pergunta aleatória
        num1, num2 = random.randint(1, 15), random.randint(1, 15)
        operation = random.choice(["+", "-", "*"])

        answer = {"+": num1 + num2, "-": num1 - num2, "*": num1 * num2}[operation]
        self.question_text = f"Quanto é {num1} {operation} {num2}?"

        options = [answer, answer + random.randint(1, 10), answer - random.randint(1, 10),
                   answer + random.randint(11, 20)]
        random.shuffle(options)
        return {"question": self.question_text, "options": options, "answer": options.index(answer)}

    def draw_text(self, text, x, y, color):
        # Desenha o texto na posição (x, y) com a cor especificada
        text_surface = self.font.render(text, True, color)
        rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, rect)

    def show_question(self, current_question):
        # Exibe a pergunta e as opções na tela
        self.screen.blit(self.background_image, (0, 0))  # Desenha a imagem de fundo
        self.draw_text(current_question["question"], self.dimensions["WIDTH"] // 2, 50, self.colors["WHITE"])
        y_offset = 150
        for index, option in enumerate(current_question["options"]):
            self.draw_text(f"{chr(65 + index)}. {option}", self.dimensions["WIDTH"] // 2, y_offset,
                           self.colors["BLACK"])
            y_offset += 70
        pygame.display.flip()

    def check_answer(self, current_question, user_answer):
        # Verifica a resposta do usuário e atualiza a pontuação
        if user_answer == current_question["answer"]:
            self.score += 1

    def show_final_score(self):
        # Mostra a pontuação final
        self.screen.blit(self.background_image, (0, 0))  # Desenha a imagem de fundo
        self.draw_text("Quiz Finalizado!", self.dimensions["WIDTH"] // 2, self.dimensions["HEIGHT"] // 4 - 40,
                       self.colors["BLACK"])
        self.draw_text(f"Pontuação: {self.score}/{self.max_questions}", self.dimensions["WIDTH"] // 2,
                       self.dimensions["HEIGHT"] // 3, self.colors["BLUE"])
        self.draw_text("Pressione Enter para reiniciar", self.dimensions["WIDTH"] // 2,
                       self.dimensions["HEIGHT"] // 2 + 40, self.colors["BLACK"])
        pygame.display.flip()

    def run(self):
        # Função principal do jogo
        running = True
        restart = False
        self.score = 0
        self.question_index = 0
        current_question = self.generate_question()

        while running:
            if self.question_index < self.max_questions:
                self.show_question(current_question)
            else:
                self.show_final_score()
                restart = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif self.question_index < self.max_questions:
                        if event.key in [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d]:
                            user_answer = event.key - pygame.K_a
                            self.check_answer(current_question, user_answer)
                            current_question = self.generate_question()
                            self.question_index += 1
                    elif restart and event.key == pygame.K_RETURN:
                        self.score = 0
                        self.question_index = 0
                        current_question = self.generate_question()
                        restart = False

            pygame.display.update()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = QuizGame()
    game.run()
