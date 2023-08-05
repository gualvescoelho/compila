import sys
import ply.lex as lex
import ply.yacc as yacc
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QPushButton, QLabel, QStackedWidget

# Etapa 1: Definindo a gramática da linguagem
tokens = ('NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'VARIABLE', 'EQUALS', 'SEMICOLON')

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_SEMICOLON = r';'
t_ignore = ' \t\n'

def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Error handling
def t_error(t):
    print(f"Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)

# Etapa 2: Implementando o analisador léxico
lexer = lex.lex()

# Etapa 3: Implementando o analisador sintático
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

variables = {}

def p_statements(p):
    '''statements : statements statement
                  | statement'''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

def p_statement_assignment(p):
    'statement : VARIABLE EQUALS expression SEMICOLON'
    variables[p[1]] = p[3]
    p[0] = [(p[1], p[3])]

def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | term'''

    if len(p) == 4:
        if p[2] == '+':
            p[0] = p[1] + p[3]
        else:
            p[0] = p[1] - p[3]
    else:
        p[0] = p[1]

def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''

    if len(p) == 4:
        if p[2] == '*':
            p[0] = p[1] * p[3]
        else:
            p[0] = p[1] / p[3]
    else:
        p[0] = p[1]

def p_factor(p):
    '''factor : NUMBER
              | VARIABLE'''

    if isinstance(p[1], str):
        p[0] = variables.get(p[1], 0)
    else:
        p[0] = p[1]

# Error handling
def p_error(p):
    if p:
        print(f"Erro de sintaxe em '{p.value}'")
    else:
        print("Erro de sintaxe no final da entrada")

parser = yacc.yacc()

# Etapa 4: Gerando o código intermediário
def compile_expr(expression):
    variables.clear()
    return parser.parse(expression)

class InputWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.input_text = QTextEdit()
        layout.addWidget(self.input_text)

        self.result_text = QLabel()
        layout.addWidget(self.result_text)

        self.confirm_button = QPushButton("Compilar")
        self.confirm_button.clicked.connect(self.on_confirm_button_clicked)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def on_confirm_button_clicked(self):
        input_text = self.input_text.toPlainText()
        try:
            result = compile_expr(input_text)
            self.result_text.setText(f"Resultado: {str(result)}")
        except Exception as e:
            self.result_text.setText(f"Erro: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Compilador com Interface Gráfica")
        self.setGeometry(100, 100, 600, 400)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.input_window = InputWindow()
        self.input_window.confirm_button.clicked.connect(self.on_input_confirm)

        self.stacked_widget.addWidget(self.input_window)

    def on_input_confirm(self):
        self.input_window.on_confirm_button_clicked()

    def show_input_window(self):
        self.stacked_widget.setCurrentWidget(self.input_window)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show_input_window()
    window.show()
    sys.exit(app.exec())
