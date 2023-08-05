import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QPushButton, QLabel

from PyCalc import compile_expr
# Importe aqui o compilador desenvolvido anteriormente
# (tokens, lexer, precedence, p_expression, p_term, p_factor, p_error, parser, compile_expr)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Configuração da janela principal
        self.setWindowTitle("Compilador Simples")
        self.setGeometry(100, 100, 600, 400)

        # Configuração do layout
        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Entrada de texto
        self.input_text = QTextEdit()
        layout.addWidget(self.input_text)

        # Botão para executar o compilador
        btn_compile = QPushButton("Executar Compilador")
        btn_compile.clicked.connect(self.execute_compiler)
        layout.addWidget(btn_compile)

        # Saída do compilador
        self.output_label = QLabel()
        layout.addWidget(self.output_label)

    def execute_compiler(self):
        expression = self.input_text.toPlainText()
        try:
            # Remover parênteses da expressão antes de compilar
            expression = expression.replace("(", "").replace(")", "")
            result = compile_expr(expression)
            self.output_label.setText(f"Resultado: {result}")
        except Exception as e:
            self.output_label.setText(f"Erro: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
