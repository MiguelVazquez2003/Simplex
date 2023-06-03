import streamlit as st
import pulp
import pandas as pd
from PIL import Image

def solve_linear_programming(objective, constraints, maximize):
    problema = pulp.LpProblem("PROBLEMA_DE_OPTIMIZACION_LINEAL", pulp.LpMaximize if maximize else pulp.LpMinimize)

    variables = {}
    for var_name in objective.keys():
        variables[var_name] = pulp.LpVariable(var_name, lowBound=0)

    objetivo = pulp.lpSum([coeff * variables[var_name] for var_name, coeff in objective.items()])
    problema += objetivo, 'Funcion objetivo'

    for constr_name, constr in constraints.items():
        constraint_expr = pulp.lpSum([coeff * variables[var_name] for var_name, coeff in constr['variables'].items()])
        if constr['operator'] == '<=':
            problema += constraint_expr <= constr['rhs'], constr_name
        elif constr['operator'] == '>=':
            problema += constraint_expr >= constr['rhs'], constr_name
        elif constr['operator'] == '<':
            problema += constraint_expr < constr['rhs'], constr_name
        elif constr['operator'] == '>':
            problema += constraint_expr > constr['rhs'], constr_name
        else:
            raise ValueError(f"Operador no válido en la restricción '{constr_name}'")

    status = problema.solve()

    if status == 1:
        optimal_value = problema.objective.value()
        result = {'Valor óptimo': optimal_value}
        for var in problema.variables():
            result[var.name] = var.value()
        return result, problema
    else:
        return {'status': problema.status, 'message': pulp.LpStatus[problema.status]}, problema

def main():
     # Descripción del método Simplex en español
    st.subheader('Método Simplex')
    st.write('El método Simplex es un algoritmo utilizado para resolver problemas de programación lineal. '
             'Permite encontrar la solución óptima de un problema de maximización o minimización, sujetos a '
             'restricciones lineales. El método se basa en la iteración entre soluciones factibles adyacentes '
             'en el espacio de soluciones, buscando mejorar la función objetivo en cada paso hasta alcanzar '
             'la solución óptima.')

    # Descripción del programa
    st.subheader('Descripción del Programa')
    st.write('Este programa implementa el método Simplex para resolver problemas de programación lineal. '
             'Permite definir la función objetivo, las restricciones y los parámetros del problema, y muestra '
             'el resultado final.')

    # Carga y visualización de la imagen
    image = Image.open('simplex.png')
    st.image(image, caption='Ilustración del método Simplex')
    st.title('Solver del Método Simplex')
    st.sidebar.title('Parámetros')

    # Definir función objetivo
    st.sidebar.subheader('Función Objetivo')
    objective = {}
    num_vars = st.sidebar.number_input('Número de variables', value=2, min_value=1)
    for i in range(num_vars):
        var_name = st.sidebar.text_input(f'Nombre de la variable {i+1}', value=f'X{i+1}', key=f'variable_{i+1}')
        var_coeff = st.sidebar.number_input(f'Coeficiente de {var_name}', value=1)
        objective[var_name] = var_coeff

    # Definir si se maximiza o minimiza
    maximize = st.sidebar.selectbox('Objetivo', ('Maximizar', 'Minimizar')) == 'Maximizar'

    # Definir restricciones
    constraints = {}
    num_constraints = st.sidebar.number_input('Número de restricciones', value=1, min_value=1, max_value=5)

    for i in range(num_constraints):
        st.sidebar.subheader(f'Restricción {i+1}')
        constr = {}
        constr['variables'] = {}
        for j in range(num_vars):
            var_name = st.sidebar.text_input(f'Nombre de la variable {j+1}', value=f'X{j+1}', key=f'restriccion_{i+1}_variable_{j+1}')
            var_coeff = st.sidebar.number_input(f'Coeficiente de {var_name} (restricción {i+1})', value=1)
            constr['variables'][var_name] = var_coeff
        constr['operator'] = st.sidebar.selectbox(f'Operador (restricción {i+1})', ('<=', '>=', '<', '>'))
        constr['rhs'] = st.sidebar.number_input(f'Lado derecho (restricción {i+1})', value=0)
        constraints[f'Restricción {i+1}'] = constr

    if st.button('Resolver'):
        result, problem = solve_linear_programming(objective, constraints, maximize)
        st.subheader('Resultado')
        st.write(pd.DataFrame.from_dict(result, orient='index', columns=['Valor']))

if __name__ == '__main__':
    main()