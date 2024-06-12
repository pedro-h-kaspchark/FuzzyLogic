import numpy as np
import skfuzzy as fuzz 
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Definição das variáveis fuzzy
relevancia = ctrl.Antecedent(np.arange(0, 11, 1), 'relevancia')
necessidade = ctrl.Antecedent(np.arange(0, 11, 1), 'necessidade')
pertinencia = ctrl.Consequent(np.arange(0, 11, 1), 'pertinencia')

# Definindo as funções de pertinência para 'relevancia'
relevancia['baixa'] = fuzz.trimf(relevancia.universe, [0, 0, 5])
relevancia['media'] = fuzz.trimf(relevancia.universe, [0, 5, 10])
relevancia['alta'] = fuzz.trimf(relevancia.universe, [5, 10, 10])

# Definindo as funções de pertinência para 'necessidade'
necessidade['baixa'] = fuzz.trimf(necessidade.universe, [0, 0, 5])
necessidade['media'] = fuzz.trimf(necessidade.universe, [0, 5, 10])
necessidade['alta'] = fuzz.trimf(necessidade.universe, [5, 10, 10])

# Definindo as funções de pertinência para 'pertinencia'
pertinencia['baixa'] = fuzz.trimf(pertinencia.universe, [0, 0, 5])
pertinencia['media'] = fuzz.trimf(pertinencia.universe, [0, 5, 10])
pertinencia['alta'] = fuzz.trimf(pertinencia.universe, [5, 10, 10])

# Regras fuzzy
rule1 = ctrl.Rule(relevancia['baixa'] & necessidade['baixa'], pertinencia['baixa'])
rule2 = ctrl.Rule(relevancia['baixa'] & necessidade['media'], pertinencia['baixa'])
rule3 = ctrl.Rule(relevancia['baixa'] & necessidade['alta'], pertinencia['media'])
rule4 = ctrl.Rule(relevancia['media'] & necessidade['baixa'], pertinencia['baixa'])
rule5 = ctrl.Rule(relevancia['media'] & necessidade['media'], pertinencia['media'])
rule6 = ctrl.Rule(relevancia['media'] & necessidade['alta'], pertinencia['alta'])
rule7 = ctrl.Rule(relevancia['alta'] & necessidade['baixa'], pertinencia['media'])
rule8 = ctrl.Rule(relevancia['alta'] & necessidade['media'], pertinencia['alta'])
rule9 = ctrl.Rule(relevancia['alta'] & necessidade['alta'], pertinencia['alta'])

# Sistema de controle fuzzy
pertinencia_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
pertinencia_sim = ctrl.ControlSystemSimulation(pertinencia_ctrl)

# Função para calcular a pertinência
def calcular_pertinencia(relevancia_valor, necessidade_valor):
    pertinencia_sim.input['relevancia'] = relevancia_valor
    pertinencia_sim.input['necessidade'] = necessidade_valor
    pertinencia_sim.compute()
    return pertinencia_sim.output['pertinencia']

# Testando a função
relevancia_valor = 6.5  # Relevância dada ao documento
necessidade_valor = 8.0  # Necessidade de informação do usuário

pertinencia_resultado = calcular_pertinencia(relevancia_valor, necessidade_valor)
print(f'A pertinência desse dado é: {pertinencia_resultado:.2f}')

# Plotando as funções de pertinência
relevancia.view()
necessidade.view()
pertinencia.view()

# Gerar gráficos de superfície
relevancia_values = np.arange(0, 11, 1)
necessidade_values = np.arange(0, 11, 1)

# Preparar a matriz para os resultados
x, y = np.meshgrid(relevancia_values, necessidade_values)
z = np.zeros_like(x)

# Avaliar o sistema para cada ponto do grid
for i in range(11):
    for j in range(11):
        pertinencia_sim.input['relevancia'] = x[i, j]
        pertinencia_sim.input['necessidade'] = y[i, j]
        pertinencia_sim.compute()
        z[i, j] = pertinencia_sim.output['pertinencia']

# Plotar a superfície
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(x, y, z, cmap='viridis')

ax.set_xlabel('Relevância')
ax.set_ylabel('Necessidade')
ax.set_zlabel('Pertinência')

plt.show()
