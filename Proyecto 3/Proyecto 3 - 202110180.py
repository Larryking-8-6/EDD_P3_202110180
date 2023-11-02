import sys
import csv
import json
import os
import bcrypt
import subprocess
from graphviz import Digraph
from PyQt5.QtWidgets import (
    QApplication, QMessageBox, QPushButton, QMainWindow, QWidget, QLabel, QLineEdit,
    QVBoxLayout, QAction, QMenuBar, QMenu, QFileDialog, QTextBrowser, QComboBox, QDialog, QInputDialog
)


class Employee:
    employees = []

    def __init__(self, employee_id, name, password, position, balance=0):
        self.employee_id = employee_id
        self.name = name
        self.password = password
        self.position = position
        self.balance = balance
        Employee.employees.append(self)

    @classmethod
    def find_employee_by_id(cls, employee_id):
        for employee in cls.employees:
            if employee.employee_id == employee_id:
                return employee
        return None

    @classmethod
    def make_payment(cls, employee_id, amount):
        employee = cls.find_employee_by_id(employee_id)
        if employee:
            employee.balance += amount

    @classmethod
    def find_employee_by_username(cls, username):
        for employee in cls.employees:
            if employee.name == username:
                return employee
        return None

    @classmethod
    def login(cls, username, password):
        employee = cls.find_employee_by_username(username)
        if employee and bcrypt.checkpw(password.encode('utf-8'), employee.password):
            return True
        return False

    @classmethod
    def display_encrypted_passwords(cls):
        for employee in cls.employees:
            print(f'Employee ID: {employee.employee_id}, Encrypted Password: {employee.password}')


class Project:
    project_counter = 0

    def __init__(self, project_id, name, priority):
        self.project_id = project_id
        self.name = name
        self.priority = priority
        self.tasks = []
        self.current_task = None

    @classmethod
    def generate_project_id(cls):
        cls.project_counter += 1
        return f"P-{str(cls.project_counter).zfill(3)}"


class Task:
    task_counter = 0

    def __init__(self, name, employee_id, project_id, status="Pendiente", dependencies=None):
        Task.task_counter += 1
        self.task_id = f"T-{str(Task.task_counter).zfill(3)}"
        self.name = name
        self.employee_id = employee_id
        self.project_id = project_id
        self.status = status
        self.completed = False
        self.dependencies = dependencies if dependencies else []

    def __str__(self):
        return f"Tarea ID: {self.task_id}, Nombre: {self.name}, Empleado a cargo: {self.employee_id}, Proyecto: {self.project_id}, Estado: {self.status}, Completada: {self.completed}"

    def mark_completed(self):
        self.completed = True


class Grafo:
    def __init__(self):
        self.principal = None
        self.nodo_origen = None  # Nuevo atributo para el nodo origen

    def inicio(self, proyecto):
        self.nodo_origen = NodoGrafo(proyecto)  # Crear el nodo origen
        self.principal = self.nodo_origen

    def insertarFila(self, u):
        nuevo = NodoGrafo(u)
        if self.principal is None:
            self.principal = nuevo
        else:
            aux = self.principal
            while aux is not None:
                if aux.valor == nuevo.valor:
                    return
                if aux.abajo is None:
                    break
                aux = aux.abajo
            aux.abajo = nuevo

    def insertarColumna(self, u, v):
        nuevo = NodoGrafo(v)
        if self.principal is not None and self.principal.valor == u:
            aux = self.principal
            while aux.siguiente is not None:
                aux = aux.siguiente
            aux.siguiente = nuevo
        else:
            aux = self.principal
            while aux is not None:
                if aux.valor == u:
                    break
                aux = aux.abajo
            if aux is not None:
                while aux.siguiente is not None:
                    aux = aux.siguiente
                aux.siguiente = nuevo

    def verMatriz(self):
        aux = self.principal
        while aux is not None:
            temp = aux.siguiente
            if temp is None:
                print("\nNodo {} No tiene conexion".format(aux.valor), end='')
            else:
                print("\nNodo {} tiene conexion con ".format(aux.valor), end='')
                while temp is not None:
                    print(" {} ".format(temp.valor), end='')
                    temp = temp.siguiente
            aux = aux.abajo

    def agregarNodo(self, u, v):
        self.insertarColumna(u, v)
        return

    def generar_grafo_dot(self):
        cadena = "digraph finite_state_machine { \n rankdir=LR;\n node [shape = circle];\n"
        
        aux = self.principal
        while aux is not None:
            temp = aux.siguiente
            while temp is not None:
                if aux.estado == 3:  # Cambia esto según tus criterios de estado para tareas completadas
                    # Agrega una relación de flecha desde una tarea completada a la siguiente tarea
                    cadena += "\"{}\" -> \"{}\" [label=\"Tarea\"];\n".format(aux.valor, temp.valor)
                temp = temp.siguiente
            aux = aux.abajo
        
        cadena += "}"
        with open("grafo.dot", "w") as file:
            file.write(cadena)

    def renderizar_grafo(self):
        self.generar_grafo_dot()
        os.system("dot -Tpdf grafo.dot -o grafo.pdf")  # Cambia el formato de salida si lo deseas

    def CambiarEstadoTarea(self, tarea, estado):
        aux = self.principal
        while aux is not None:
            if aux.valor == tarea:
                if aux.siguiente is None:
                    aux.estado = estado
                    self.CambiarEstado(tarea, estado)
                    print("Estado Cambiado")
                else:
                    terminado = self.VerificarEstado(tarea)
                    if terminado == True:
                        aux.estado = estado
                        self.CambiarEstado(tarea, estado)
                        print("Estado Cambiado")
                    else:
                        print("Una tarea no se ha comenzado o está en proceso")
            aux = aux.abajo

    def CambiarEstado(self, tarea, estado):
        aux = self.principal
        while aux is not None:
            temp = aux.siguiente
            if temp is not None:
                while temp is not None:
                    if temp.valor == tarea:
                        temp.estado = estado
                    temp = temp.siguiente
            aux = aux.abajo

    def VerificarEstado(self, tarea):
        aux = self.principal
        arregloBool = []
        while aux is not None:
            if aux.valor == tarea:
                temp = aux.siguiente
                while temp is not None:
                    if temp.estado == 3:
                        arregloBool.append(True)
                    else:
                        arregloBool.append(False)
                    temp = temp.siguiente
            aux = aux.abajo
        if False in arregloBool:
            return False
        else:
            return True

class Block:
    def __init__(self, index, timestamp, data, previous_hash, hash, password):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = hash
        self.password = password 

class NodoGrafo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None
        self.abajo = None
        self.estado = 1



class AVLNode:
    def __init__(self, project):
        self.project = project
        self.height = 1
        self.left = None
        self.right = None


def height(node):
    if node is None:
        return 0
    return node.height


def balance_factor(node):
    if node is None:
        return 0
    return height(node.left) - height(node.right)


def rotate_left(y):
    x = y.right
    T2 = x.left

    x.left = y
    y.right = T2

    y.height = 1 + max(height(y.left), height(y.right))
    x.height = 1 + max(height(x.left), height(x.right))

    return x


def rotate_right(x):
    y = x.left
    T2 = y.right

    y.right = x
    x.left = T2

    x.height = 1 + max(height(x.left), height(x.right))
    y.height = 1 + max(height(y.left), height(y.right))

    return y


def insert(root, project):
    if root is None:
        return AVLNode(project)

    if project.project_id < root.project.project_id:
        root.left = insert(root.left, project)
    else:
        root.right = insert(root.right, project)

    root.height = 1 + max(height(root.left), height(root.right))

    balance = balance_factor(root)

    if balance > 1:
        if project.project_id < root.left.project.project_id:
            return rotate_right(root)
        else:
            root.left = rotate_left(root.left)
            return rotate_right(root)

    if balance < -1:
        if project.project_id > root.right.project.project_id:
            return rotate_left(root)
        else:
            root.right = rotate_right(root.right)
            return rotate_left(root)

    return root


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, project):
        self.root = self._insert(self.root, project)

    def _insert(self, node, project):
        if node is None:
            return AVLNode(project)

        if project.project_id < node.project.project_id:
            node.left = self._insert(node.left, project)
        else:
            node.right = self._insert(node.right, project)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        balance = self._get_balance(node)

        if balance > 1:
            if project.project_id < node.left.project.project_id:
                return self._rotate_right(node)
            else:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)
        if balance < -1:
            if project.project_id > node.right.project.project_id:
                return self._rotate_left(node)
            else:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

        return node

    def get_sorted_projects(self):
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, node, result):
        if node:
            self._inorder_traversal(node.left, result)
            result.append(node.project)
            self._inorder_traversal(node.right, result)

    def _get_height(self, node):
        if node is None:
            return 0
        return node.height

    def _get_balance(self, node):
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _rotate_left(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _rotate_right(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))

        return x


class BTreeNode:
    def __init__(self, leaf=True):
        self.keys = []
        self.children = []
        self.leaf = leaf
        self.parent = None

    def insert(self, key):
        if not self.keys:
            self.keys.append(key)
        else:
            i = 0
            while i < len(self.keys) and key > self.keys[i]:
                i += 1
            self.keys.insert(i, key)

    def split_child(self, child_index):
        middle = len(self.children[child_index].keys) // 2
        new_node = BTreeNode(self.children[child_index].leaf)

        new_node.keys = self.children[child_index].keys[middle + 1:]
        self.children[child_index].keys = self.children[child_index].keys[:middle]

        if not self.children[child_index].leaf:
            new_node.children = self.children[child_index].children[middle + 1:]
            self.children[child_index].children = self.children[child_index].children[:middle + 1]

        self.children.insert(child_index + 1, new_node)
        new_node.parent = self

    def is_root(self):
        return self.parent is None


class BTree:
    def __init__(self, degree=2):
        self.root = BTreeNode()
        self.degree = degree

    def insert(self, key):
        root = self.root

        if len(root.keys) == (2 * self.degree) - 1:
            new_root = BTreeNode(leaf=False)
            new_root.children.append(root)
            new_root.split_child(0)
            self.root = new_root
            self.insert_non_full(key, new_root)
        else:
            self.insert_non_full(key, root)

    def insert_non_full(self, key, node):
        i = len(node.keys) - 1

        if node.leaf:
            node.insert(key)
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1

            if len(node.children[i].keys) == (2 * self.degree) - 1:
                node.split_child(i)
                if key > node.keys[i]:
                    i += 1
            self.insert_non_full(key, node.children[i])

    def search(self, key, node=None):
        if node is None:
            node = self.root

        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            return True
        elif node.leaf:
            return False
        else:
            return self.search(key, node.children[i])

    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root
        print("Level", level, ": ", end="")

        for key in node.keys:
            print(key, end=", ")

        if not node.leaf:
            print()
            level += 1
            for child in node.children:
                self.print_tree(child, level)

    def generate_b_dot(self):
        dot_file_path = "arbolB.dot"
        dot_file = open(dot_file_path, "w")
        dot_file.write("digraph G {\n")
        dot_file.write("  graph [rankdir=TB];\n")
        dot_file.write("  node [shape=record];\n")

        self._generate_b_dot_recursive(dot_file, self.root)

        dot_file.write("}\n")
        dot_file.close()

        print("Archivo DOT generado como 'arbolB.dot'.")

    def _generate_b_dot_recursive(self, dot_file, node):
        if node:
            if node.keys:
                for key in node.keys:
                    task_id, project_id = key
                    dot_file.write(f'  "{task_id}_{project_id}" [label="{{Tarea ID: {task_id} | Proyecto ID: {project_id}}}"];\n')

                if not node.is_root():
                    parent_id = node.parent.keys[0][0]  # Obtener el ID del padre
                    dot_file.write(f'  "{parent_id}_{node.keys[0][1]}" -> "{node.keys[0][0]}_{node.keys[0][1]}";\n')

                for child in node.children:
                    self._generate_b_dot_recursive(dot_file, child)


class HashTable:
    def __init__(self, capacity=5):
        self.capacity = capacity
        self.size = 0
        self.table = [None] * self.capacity

    def hash(self, key):
        return sum(ord(char) for char in key) % self.capacity

    def insert(self, key, employee):
        if self.size >= 0.7 * self.capacity:
            new_capacity = self.get_next_fibonacci_capacity()
            self.resize(new_capacity)

        index = self.hash(key)
        if self.table[index] is None:
            self.table[index] = []
        self.table[index].append(employee)  # Almacena el objeto empleado directamente en la lista
        self.size += 1

    def find(self, key):
        index = self.hash(key)
        if self.table[index] is not None:
            for k, v in self.table[index]:
                if k == key:
                    return v
        return None

    def get_utilization(self):
        return self.size / self.capacity

    def get_next_fibonacci_capacity(self):
        a, b = 0, 1
        while b < self.capacity:
            a, b = b, a + b
        return b

    def resize(self, new_capacity):
        old_table = self.table
        self.capacity = new_capacity
        self.size = 0
        self.table = [None] * self.capacity

        for item in old_table:
            if item is not None:
                for key, value in item:
                    self.insert(key, value)

    def get_all(self):
        all_employees = []
        for index in range(len(self.table)):
            if self.table[index] is not None:
                all_employees.extend(self.table[index])
        return all_employees


class EmployeeInfoDialog(QDialog):
    def __init__(self, employee):
        super().__init__()
        self.setWindowTitle("Información del Empleado")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        employee_id_label = QLabel(f"ID: {employee.employee_id}")
        name_label = QLabel(f"Nombre: {employee.name}")
        position_label = QLabel(f"Puesto: {employee.position}")

        layout.addWidget(employee_id_label)
        layout.addWidget(name_label)
        layout.addWidget(position_label)

        self.setLayout(layout)

class MenuPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.tasks_in_progress = {}
        self.setWindowTitle("Menú principal - ProjectUp")
        self.setGeometry(100, 100, 600, 400)

        main_layout = QVBoxLayout()

        self.menu_bar = QMenuBar(self)
        self.file_menu = self.menu_bar.addMenu("Archivo")
        self.edit_menu = self.menu_bar .addMenu("Cargar Empleados")
        self.view_menu = self.menu_bar.addMenu("Ver Empleados")
        self.projects_menu = self.menu_bar.addMenu("Proyectos")
        self.tasks_menu = self.menu_bar.addMenu("Tareas")

        self.view_tasks_action = QAction("Ver Tareas", self)
        self.view_tasks_action.triggered.connect(self.view_tasks)
        self.tasks_menu.addAction(self.view_tasks_action)

        self.reports_menu = self.menu_bar.addMenu("Generar Reportes")
        self.report_avl_action = QAction("Reporte AVL", self)
        self.report_b_action = QAction("Reporte B", self)
        self.report_hash_table_action = QAction("Reporte Tabla Hash", self)
        self.report_task_action = QAction("Grafo", self)
        self.report_blockchain_action = QAction("Reporte de Blockchain", self)

        self.report_avl_action.triggered.connect(self.generate_avl_report)
        self.report_b_action.triggered.connect(self.generate_b_report)
        self.report_hash_table_action.triggered.connect(self.generate_hash_table_report)
        self.report_task_action.triggered.connect(self.generate_grafo)
        self.report_blockchain_action.triggered.connect(self.generate_blockchain_report)

        self.reports_menu.addAction(self.report_avl_action)
        self.reports_menu.addAction(self.report_b_action)
        self.reports_menu.addAction(self.report_hash_table_action)
        self.reports_menu.addAction(self.report_task_action)  
        self.reports_menu.addAction(self.report_blockchain_action)

        self.employee_table = HashTable()  
        self.project_table = AVLTree()  
        self.task_table = BTree()  

        self.create_actions()

        self.employee_display = QTextBrowser(self)
        self.employee_counter = 1

        main_layout.addWidget(self.menu_bar)
        main_layout.addWidget(self.employee_display)
        self.setLayout(main_layout)

        self.projects = []
        self.employees = []
        self.created_tasks = []
        self.created_projects = []
        self.hash_table = HashTable() 

    def create_actions(self):
        self.new_project_action = QAction("Nuevo Proyecto", self)
        self.new_task_action = QAction("Nueva Tarea", self)
        self.assign_task_to_project_action = QAction("Asignar Tarea a Proyecto", self)
        self.assign_task_to_selected_project_action = QAction("Asignar Tarea al Proyecto Seleccionado", self)
        self.view_employees_action = QAction("Ver Empleados", self)
        self.view_projects_action = QAction("Ver Proyectos", self)
        self.assign_project_action = QAction("Asignar Proyecto", self)
        self.load_csv_employees_action = QAction("Cargar archivo CSV", self)
        self.load_json_action = QAction("Cargar archivo JSON", self)
        self.exit_action = QAction("Salir", self)
        self.new_employee_action = QAction("Nuevo Empleado", self)
        self.complete_task_action = QAction("Completar Tarea", self)

        self.new_project_action.triggered.connect(self.create_new_project)
        self.new_task_action.triggered.connect(self.create_new_task)
        self.assign_task_to_project_action.triggered.connect(self.assign_task_to_project)
        self.assign_task_to_selected_project_action.triggered.connect(self.assign_task_to_selected_project)
        self.view_employees_action.triggered.connect(self.view_employees)
        self.view_projects_action.triggered.connect(self.view_projects)
        self.load_csv_employees_action.triggered.connect(self.load_csv_employees)
        self.load_json_action.triggered.connect(self.load_json)
        self.assign_project_action.triggered.connect(self.assign_project_to_employee)
        self.exit_action.triggered.connect(self.close)
        self.new_employee_action.triggered.connect(self.create_new_employee)
        self.complete_task_action.triggered.connect(self.complete_task)

        self.arbol_avl = None

        self.projects_menu.addAction(self.new_project_action)
        self.projects_menu.addAction(self.assign_project_action)
        self.tasks_menu.addAction(self.new_task_action)
        self.tasks_menu.addAction(self.assign_task_to_project_action)
        self.tasks_menu.addAction(self.assign_task_to_selected_project_action)
        self.tasks_menu.addAction(self.complete_task_action)
        self.view_menu.addAction(self.view_employees_action)
        self.edit_menu.addAction(self.load_csv_employees_action)
        self.edit_menu.addAction(self.load_json_action)
        self.projects_menu.addAction(self.view_projects_action)
        self.edit_menu.addAction(self.new_employee_action)
        self.file_menu.addAction(self.exit_action)


    def create_new_project(self):
        if not hasattr(self, 'project_counter'):
            self.project_counter = 0

        self.project_counter += 1
        project_id = f"PY-{str(self.project_counter).zfill(3)}"
        project_name, ok1 = QInputDialog.getText(self, "Nuevo Proyecto", "Nombre del nuevo proyecto:")

        priority_options = ["A", "B", "C"]

        priority, ok2 = QInputDialog.getItem(self, "Nuevo Proyecto", "Selecciona la prioridad del nuevo proyecto:", priority_options, 0, False)

        if ok1 and ok2:
            project = Project(project_id, project_name, priority)
            self.project_table.insert(project)

            print(f"Proyecto creado - ID: {project_id}, Nombre: {project_name}, Prioridad: {priority}")
        else:
            print("La creación de proyecto se canceló.")

    def create_new_task(self):
        if not Employee.employees:
            QMessageBox.critical(self, "Error", "No hay empleados disponibles para crear una tarea.")
            return

        if not self.project_table.root:
            QMessageBox.critical(self, "Error", "No hay proyectos disponibles para asignar a las tareas.")
            return

        task_name, ok = QInputDialog.getText(self, "Crear Nueva Tarea", "Nombre de la tarea:")
        if ok and task_name:
            employee_names = [f"{employee.name} (ID: {employee.employee_id})" for employee in Employee.employees]

            employee_name, ok = QInputDialog.getItem(self, "Asignar Empleado a Tarea", "Selecciona un empleado:", employee_names, 0, False)

            if ok:
                selected_employee_id = employee_name.split("(ID: ")[1].split(")")[0]

                projects = self.project_table.get_sorted_projects()

                if not projects:
                    QMessageBox.critical(self, "Error", "No hay proyectos disponibles para asignar a las tareas.")
                    return

                project_names = [f"{project.name} (ID: {project.project_id})" for project in projects]

                project_name, ok = QInputDialog.getItem(self, "Asignar Proyecto a Tarea", "Selecciona un proyecto:", project_names, 0, False)

                if ok:
                    selected_project = next(project for project in projects if project_name.endswith(f"(ID: {project.project_id})"))

                    # Verifica si ya hay una tarea "En Proceso" para este proyecto
                    if selected_project.project_id not in self.tasks_in_progress:
                        status = "En Proceso"
                    else:
                        status = "Pendiente"

                    new_task = Task(task_name, selected_employee_id, selected_project.project_id, status)

                    # Agrega la tarea a las tareas en proceso solo si está "En Proceso"
                    if status == "En Proceso":
                        self.tasks_in_progress[selected_project.project_id] = new_task

                    self.created_tasks.append(new_task)

                    QMessageBox.information(self, "Tarea Creada", f"Tarea creada - ID: {new_task.task_id}, Nombre: {new_task.name}, Empleado a cargo: {new_task.employee_id}, Proyecto: {new_task.project_id}, Estado: {new_task.status}")
                else:
                    QMessageBox.information(self, "Creación de Tarea Cancelada", "La creación de tarea se canceló.")
            else:
                print("La creación de tarea se canceló.")


    def assign_employee_to_task(self):
        if not Employee.employees:
            QMessageBox.critical(self, "Error", "No hay empleados disponibles para asignar a tareas.")
            return

        if not Task.tasks:
            QMessageBox.critical(self, "Error", "No hay tareas disponibles para asignar empleados.")
            return

        task_names = [f"{task.name} (ID: {task.task_id})" for task in Task.tasks]

        task_name, ok = QInputDialog.getItem(self, "Asignar Empleado a Tarea", "Selecciona una tarea:", task_names, 0, False)

        if ok:
            selected_task = next(task for task in Task.tasks if task_name.endswith(f"(ID: {task.task_id})"))

            employee_id, ok = QInputDialog.getText(self, "Asignar Empleado a Tarea", "ID del empleado a asignar a la tarea:")

            if ok:
                # Verificar si el empleado existe
                if not Employee.find_employee_by_id(employee_id):
                    QMessageBox.critical(self, "Error", "El empleado especificado no existe.")
                else:
                    selected_task.employee_id = employee_id
                    QMessageBox.information(self, "Empleado Asignado", f"Empleado asignado a la tarea - Tarea ID: {selected_task.task_id}, Empleado ID: {employee_id}")
            else:
                QMessageBox.information(self, "Asignación de Empleado Cancelada", "La asignación de empleado se canceló.")
        else:
            QMessageBox.information(self, "Asignación de Empleado Cancelada", "La asignación de empleado se canceló.")


    
    def assign_task_to_project(self):
        if not self.employees:
            print("No hay empleados disponibles para asignar tareas a proyectos.")
            return

        if not self.created_tasks:
            print("No hay tareas disponibles para asignar a proyectos.")
            return

        task_names = [f"{task.name} (ID: {task.task_id})" for task in self.created_tasks]

        task_name, ok = QInputDialog.getItem(self, "Asignar Tarea a Proyecto", "Selecciona una tarea:", task_names, 0, False)

        if ok:
            selected_task = next(task for task in self.created_tasks if task_name.endswith(f"(ID: {task.task_id})"))

            # Obtener la lista de el arbol AVL
            projects = self.project_table.get_sorted_projects()

            if not projects:
                print("No hay proyectos disponibles para asignar tareas.")
                return

            # Crear una lista
            project_names = [f"{project.name} (ID: {project.project_id})" for project in projects]

            project_name, ok = QInputDialog.getItem(self, "Asignar Tarea a Proyecto", "Selecciona un proyecto:", project_names, 0, False)

            if ok:
                selected_project = next(project for project in projects if project_name.endswith(f"(ID: {project.project_id})"))

                selected_task.project_id = selected_project.project_id

                print(f"Tarea asignada al proyecto - Tarea ID: {selected_task.task_id}, Proyecto ID: {selected_project.project_id}")
            else:
                print("La asignación de tarea a proyecto se canceló.")
        else:
            print("La asignación de tarea a proyecto se canceló.")

    def get_tasks_by_project(self, project_id):
        tasks_by_project = []
        for task in self.created_tasks:
            if task.project_id == project_id:
                tasks_by_project.append(task)
        return tasks_by_project


    def filter_tasks(self):
        selected_option = self.filter_dropdown.currentText()

        if selected_option == "Mostrar todas las tareas":
            self.view_all_tasks()
        else:
            project_id = self.get_project_id_by_name(selected_option)
            self.view_tasks_by_project(project_id)

    def get_active_projects_for_employee(self):
        active_projects = []  
        return active_projects

    def get_project_id_by_name(self, project_name):
        project_id = None  
        return project_id

    def view_all_tasks(self):
        pass

    def view_tasks_by_project(self, project_id):
        self.employee_display.clear()
        self.employee_counter = 1

        tasks = self.get_tasks_by_project(project_id)

        for task in tasks:
            display_text = f"Tarea {self.employee_counter}\n"
            display_text += f"Código de tarea: {task.task_id}\n"
            display_text += f"Nombre de la tarea: {task.name}\n"
            display_text += f"Empleado a cargo: {task.employee_id}\n"
            display_text += f"Nombre del proyecto: {task.project_id}\n"
            self.employee_display.append(display_text)

            self.employee_counter += 1
            
    def view_employees(self):
        self.employee_display.clear()
        self.employee_counter = 1

        for employee in Employee.employees:
            display_text = f"Empleado {self.employee_counter}\n"
            display_text += f"Código: {employee.employee_id}\n"
            display_text += f"Nombre: {employee.name}\n"
            display_text += f"Puesto: {employee.position}\n"
            self.employee_display.append(display_text)

            self.employee_counter += 1


    def view_projects(self):
        self.employee_display.clear()
        self.employee_counter = 1

        self._inorder_traversal(self.project_table.root)
        self.employee_display.append("Proyectos:")
        for project in self.created_projects:
            self.employee_display.append(f"  - ID: {project.project_id}, Nombre: {project.name}, Prioridad: {project.priority}")

    def _inorder_traversal(self, node):
        if node:
            self._inorder_traversal(node.left)

            display_text = f"Proyecto {self.employee_counter}\n"
            display_text += f"ID: {node.project.project_id}\n"
            display_text += f"Nombre: {node.project.name}\n"
            display_text += f"Prioridad: {node.project.priority}\n"
            self.employee_display.append(display_text)

            self.employee_counter += 1

            self._inorder_traversal(node.right)

    def view_tasks(self):
        self.employee_display.clear()
        self.employee_counter = 1

        in_progress_tasks = []
        completed_tasks = []
        pending_tasks = []

        for task in self.created_tasks:
            if task.status == "En Proceso":
                in_progress_tasks.append(task)
            elif task.status == "Pendiente":
                pending_tasks.append(task)
            elif task.status == "Completada":
                completed_tasks.append(task)

        self.employee_display.append("\nTareas Completadas:\n")
        for task in completed_tasks: 
            display_text = f"Tarea {self.employee_counter} (Completada)\n"
            display_text += f"Código de Tarea: {task.task_id}\n"
            display_text += f"Nombre de la Tarea: {task.name}\n"
            display_text += f"ID del Empleado a Cargo: {task.employee_id}\n"
            display_text += f"ID del Proyecto: {task.project_id}\n"
            self.employee_display.append(display_text)
            self.employee_counter += 1

        self.employee_display.append("Tareas en Proceso:\n")
        for task in in_progress_tasks:
            display_text = f"Tarea {self.employee_counter} (En Proceso)\n"
            display_text += f"Código de Tarea: {task.task_id}\n"
            display_text += f"Nombre de la Tarea: {task.name}\n"
            display_text += f"ID del Empleado a Cargo: {task.employee_id}\n"
            display_text += f"ID del Proyecto: {task.project_id}\n"
            self.employee_display.append(display_text)
            self.employee_counter += 1

        self.employee_display.append("\nTareas Pendientes:\n")
        for task in pending_tasks:
            display_text = f"Tarea {self.employee_counter} (Pendiente)\n"
            display_text += f"Código de Tarea: {task.task_id}\n"
            display_text += f"Nombre de la Tarea: {task.name}\n"
            display_text += f"ID del Empleado a Cargo: {task.employee_id}\n"
            display_text += f"ID del Proyecto: {task.project_id}\n"
            self.employee_display.append(display_text)
            self.employee_counter += 1

    def assign_project_to_employee(self):
        if not self.employees:
            print("No hay empleados disponibles para asignar proyectos.")
            return
        employees = [employee for employee in self.employee_table.get_all()]

        if not employees:
            print("No hay empleados disponibles para asignar proyectos.")
            return

        employee_names = [f"{employee.name} (ID: {employee.employee_id})" for employee in employees]

        employee_name, ok = QInputDialog.getItem(self, "Asignar Proyecto", "Selecciona un empleado:", employee_names, 0, False)

        if ok:
            selected_employee = next(employee for employee in employees if employee_name.endswith(f"(ID: {employee.employee_id})"))

            projects = self.project_table.get_sorted_projects()

            if not projects:
                print("No hay proyectos disponibles para asignar a empleados.")
                return

            project_names = [f"{project.name} (ID: {project.project_id})" for project in projects]

            project_name, ok = QInputDialog.getItem(self, "Asignar Proyecto", "Selecciona un proyecto:", project_names, 0, False)

            if ok:
                selected_project = next(project for project in projects if project_name.endswith(f"(ID: {project.project_id})"))

                selected_employee.assigned_project_id = selected_project.project_id

                print(f"Proyecto asignado al empleado - Proyecto ID: {selected_project.project_id}, Empleado ID: {selected_employee.employee_id}")
            else:
                print("La asignación de proyecto se canceló.")
        else:
            print("La asignación de proyecto se canceló.")


    def assign_task_to_selected_project(self):
        if not self.employees:
            print("No hay empleados disponibles para asignar tareas a proyectos.")
            return

        employee_names = [f"{employee.name} (ID: {employee.employee_id})" for employee in self.employees]

        employee_name, ok = QInputDialog.getItem(self, "Asignar Tarea a Empleado", "Selecciona un empleado:", employee_names, 0, False)

        if ok:
            selected_employee = next(employee for employee in self.employees if employee_name.endswith(f"(ID: {employee.employee_id})"))

            if selected_employee.assigned_project_id is not None:
                selected_task = self.get_selected_task() 

                if selected_task:
                    selected_task.project_id = selected_employee.assigned_project_id
                    print(f"Tarea asignada al proyecto - Tarea ID: {selected_task.task_id}, Proyecto ID: {selected_employee.assigned_project_id}")
                else:
                    print("No se seleccionó una tarea válida.")
            else:
                print("El empleado seleccionado no tiene un proyecto asignado.")
        else:
            print("La asignación de tarea a empleado se canceló.")

    def generate_avl_report(self):
        sorted_projects = sorted(self.created_projects, key=lambda project: (project.priority, project.project_id))

        dot_file_path = "arbolAVL.dot"
        dot_file = open(dot_file_path, "w")
        dot_file.write("digraph G {\n")
        dot_file.write("  graph [rankdir=TB];\n")
        dot_file.write("  node [shape=record];\n")

        priority_groups = {"A": [], "B": [], "C": []}
        for project in sorted_projects:
            priority = project.priority
            priority_groups[priority].append(project)

        for priority, projects in priority_groups.items():
            for project in projects:
                dot_file.write(f'  "{project.project_id}" [label="{{ID: {project.project_id} | Nombre: {project.name} | Prioridad: {project.priority}}}"];\n')


            if priority == "A":
                for project_A in projects:
                    for project_B in priority_groups["B"]:
                        dot_file.write(f'  "{project_A.project_id}" -> "{project_B.project_id}";\n')
            elif priority == "B":
                for project_B in projects:
                    for project_C in priority_groups["C"]:
                        dot_file.write(f'  "{project_B.project_id}" -> "{project_C.project_id}";\n')

        dot_file.write("}\n")
        dot_file.close()

        print("Archivo DOT generado como 'arbolAVL.dot'.")

        try:
            subprocess.run(["dot", "-Tpdf", "-o", "arbolAVL.pdf", "arbolAVL.dot"])
            print("Archivo PDF generado como 'arbolAVL.pdf'.")
        except Exception as e:
            print(f"Error al generar el archivo PDF: {str(e)}")



    def generate_b_report(self):
            b_tree = BTree()
            output_folder = r"C:\Users\Rodrigo Gonzalez\Desktop\Cursos U\Estructura de Datos\Proyecto 2"

            b_tree.generate_b_dot()

            pdf_file_path = os.path.join(output_folder, "arbolB.pdf")
            try:
                subprocess.run(["dot", "-Tpdf", "-o", pdf_file_path, "arbolB.dot"])
                print(f"Archivo PDF generado como 'arbolB.pdf' en '{output_folder}'.")
            except Exception as e:
                print(f"Error al generar el archivo PDF: {str(e)}")

    def generate_hash_table_report(self):
        txt_file_path = os.path.expanduser("~/Desktop/Hash_Table_Report.txt")

        with open(txt_file_path, "w", encoding="utf-8") as txt_file:
            txt_file.write("Reporte de Empleados\n")
            txt_file.write("=================================\n\n")

            employees = self.employees 

            if not employees:
                error_message = "No hay datos de empleados para generar el informe."
                txt_file.write(error_message)
                print(error_message)
            else:
                txt_file.write("ID de Empleado | Nombre | Puesto | Contraseña\n")
                txt_file.write("-------------------------------------------------\n")

                for employee in employees:
                    employee_id = employee.employee_id
                    name = employee.name
                    position = employee.position
                    password = bcrypt.hashpw(employee.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                    txt_file.write(f"{employee_id:<14} | {name:<6} | {position:<7} | {password}\n")
                    print(f"ID de Empleado: {employee_id}, Nombre: {name}, Puesto: {position}, Contraseña: {password}")

        print(f"Informe de empleados generado como 'Hash_Table_Report.txt' en el escritorio.")


    def load_csv_employees(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Cargar Empleados CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if file_path:
            try:
                self.employees = []
                with open(file_path, newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        employee_id = row["ID"]
                        name = row["nombre"].strip() 
                        password = row["contrasenia"]
                        position = row["puesto"].strip()

                        valid_positions = ["Frontend Developer", "Backend Developer", "Quality Assurance (QA)", "Project Manager"]
                        if position not in valid_positions:
                            print(f"Error: Puesto inválido para el empleado con ID {employee_id}.")
                            continue

                        employee = Employee(employee_id, name, password, position)
                        self.employees.append(employee)  # Agrega a la lista
                        print(f"Cargando empleado - Código: {employee_id}, Nombre: {name}, Puesto: {position}")

                print("Empleados cargados desde CSV con éxito.")
            except Exception as e:
                print(f"Error al cargar empleados desde el archivo CSV: {e}")


    def find_employee_by_id(self, employee_id):
            for employee in self.employees:
                if employee.employee_id == employee_id:
                    return employee
            return None

    def load_json(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("JSON Files (*.json)")
        file_dialog.setViewMode(QFileDialog.List)

        if file_dialog.exec_():
            file_name = file_dialog.selectedFiles()[0]
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                    self.created_tasks.clear()

                    if "Proyectos" in data:
                        projects_data = data["Proyectos"]
                        print("Proyectos encontrados en el archivo JSON:")
                        for project_data in projects_data:
                            project_id = project_data["id"]
                            project_name = project_data["nombre"]
                            priority = project_data["prioridad"]

                            project = Project(project_id, project_name, priority)
                            self.created_projects.append(project)

                            print(f"  - ID: {project.project_id}, Nombre: {project.name}, Prioridad: {project.priority}")

                            if "tareas" in project_data:
                                tasks_data = project_data["tareas"]
                                print("Tareas encontradas en el proyecto:")
                                tasks_in_process = {}

                                for task_data in tasks_data:
                                    task_name = task_data["nombre"]
                                    employee_id = task_data.get("empleado", "")  # Intenta obtener el ID del empleado

                                    if employee_id:
                                        if project_id not in tasks_in_process:
                                            task = Task(task_name, employee_id, project_id, status="En Proceso")
                                            tasks_in_process[project_id] = task
                                        else:
                                            task = Task(task_name, employee_id, project_id, status="Pendiente")
                                    else:
                                        task = Task(task_name, "", project_id, status="Pendiente")

                                    self.created_tasks.append(task)
                                    print(f"    - Tarea: {task_name}, Empleado ID: {employee_id}, Estado: {task.status}")

                    self.view_projects()
                    self.view_tasks()

                    QMessageBox.information(self, "Éxito", "Los datos se han cargado correctamente desde el archivo JSON.")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar el archivo JSON: {str(e)}")


    def generate_blockchain_report(self):
        data_from_hash_table = [
            (0, "2023-01-01", "Genesis Block", "0", "0000", "password0"),
            (1, "2023-01-02", "Data 1", "0000", "hash1", "password1"),
            (2, "2023-01-03", "Data 2", "hash1", "hash2", "password2"),
            (3, "2023-01-04", "Data 3", "hash2", "hash3", "password3"),
        ]

        blocks = [Block(*data) for data in data_from_hash_table]

        dot = Digraph(comment='Blockchain Report', format='pdf')
        dot.attr(rankdir='LR')

        for index, block in enumerate(blocks):
            label = (
                f'Index: {block.index}\n'
                f'Timestamp: {block.timestamp}\n'
                f'Data: {block.data}\n'
                f'Previous Hash: {block.previous_hash}\n'
                f'Password: {block.password}'  # Usa el atributo password_hash
            )
            dot.node(f'Block{index}', label, shape='box')

            if index > 0:
                dot.edge(f'Block{index - 1}', f'Block{index}')

        pdf_file_path = 'blockchain_report.pdf'

        dot.render(pdf_file_path, view=True)


    def complete_task(self):
        in_progress_tasks = [task for task in self.created_tasks if task.status == "En Proceso"]
        pending_tasks = [task for task in self.created_tasks if task.status == "Pendiente"]

        if not in_progress_tasks:
            QMessageBox.warning(self, "Error", "No hay tareas en proceso para completar.")
            return

        task_names = [str(task) for task in in_progress_tasks]
        selected_task, ok = QInputDialog.getItem(self, "Completar Tarea", "Selecciona una tarea para completar:", task_names, 0, False)

        if ok:
            selected_task = next(task for task in in_progress_tasks if str(task) == selected_task)

            if selected_task:
                project_id = selected_task.project_id

                task_in_progress_for_project = next(
                    (task for task in in_progress_tasks if task.project_id == project_id), None
                )

                if task_in_progress_for_project == selected_task:
                    selected_task.status = "Completada"
                    selected_task.mark_completed()

                    pending_project_tasks = [
                        task for task in pending_tasks if task.project_id == project_id
                    ]

                    first_pending_task = None
                    if pending_project_tasks:
                        first_pending_task = pending_project_tasks[0]

                    if first_pending_task:
                        first_pending_task.status = "En Proceso"
                    self.update_task_display()
                    QMessageBox.information(
                        self,
                        "Tarea Completada",
                        f"Tarea completada - ID: {selected_task.task_id}, Nombre: {selected_task.name}",
                    )
                else:
                    QMessageBox.warning(
                        self, "Error", "Ya hay una tarea en proceso para este proyecto."
                    )
            else:
                QMessageBox.warning(self, "Error", "No se encontró la tarea seleccionada.")


    def update_task_display(self):
        self.employee_display.clear()
        self.employee_counter = 1

        in_progress_tasks = [task for task in self.created_tasks if task.status == "En Proceso"]

        if not in_progress_tasks:
            self.employee_display.append("No hay tareas en proceso.")
            return

        self.employee_display.append("Tareas en Proceso:\n")

        for task in in_progress_tasks:
            display_text = f"Tarea {self.employee_counter} (En Proceso)\n"
            display_text += f"Código de Tarea: {task.task_id}\n"
            display_text += f"Nombre de la Tarea: {task.name}\n"
            display_text += f"ID del Empleado a Cargo: {task.employee_id}\n"
            display_text += f"ID del Proyecto: {task.project_id}\n"
            self.employee_display.append(display_text)
            self.employee_counter += 1

    def create_new_employee(self):
        new_employee_dialog = NewEmployeeDialog(self)
        result = new_employee_dialog.exec_()
        if result == QDialog.Accepted:
            employee = new_employee_dialog.get_employee()
            self.employee_table.insert(employee.employee_id, employee)
            self.employees.append(employee) 
            self.employee_counter += 1
            print(f"Empleado agregado - Código: {employee.employee_id}, Nombre: {employee.name}, Puesto: {employee.position}")

    def generate_grafo(self):
        completed_tasks = [task for task in self.created_tasks if task.status == "Completada"]
        in_progress_tasks = [task for task in self.created_tasks if task.status == "En Proceso"]

        dot = Digraph(comment='Grafo de Tareas', format='pdf')

        for task in completed_tasks:
            dot.node(f"{task.project_id}\n{task.task_id}", style='filled', fillcolor='green')

        for task in in_progress_tasks:
            dot.node(f"{task.project_id}\n{task.task_id}")

        for task in in_progress_tasks:
            for dependency_id in task.dependencies:
                dot.edge(f"{task.project_id}\n{task.task_id}", f"{task.project_id}\n{dependency_id}")

        pdf_file_path = r'C:\Users\Rodrigo Gonzalez\Desktop\grafo'

        dot.render(pdf_file_path, view=True)

class NewEmployeeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo Empleado")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.name_label = QLabel("Nombre:")
        self.name_input = QLineEdit()

        self.position_label = QLabel("Puesto:")
        self.position_combo = QComboBox()
        self.position_combo.addItems(["Frontend Developer", "Backend Developer", "Quality Assurance (QA)", "Project Manager"])

        self.password_label = QLabel("Contraseña:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.create_button = QPushButton("Crear")
        self.create_button.clicked.connect(self.create_employee)

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.position_label)
        layout.addWidget(self.position_combo)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.create_button)

        self.setLayout(layout)

    def create_employee(self):
        name = self.name_input.text()
        position = self.position_combo.currentText()
        password = self.password_input.text()

        if name and position and password:
            position_to_code = {
                "Frontend Developer": "FDEV-",
                "Backend Developer": "BDEV-",
                "Quality Assurance (QA)": "QA-",
                "Project Manager": "PM-"
            }

            code = position_to_code[position]

            correlativo = 1
            while True:
                new_id = f"{code}{correlativo:03d}" 
                if self.parent().employee_table.find(new_id) is None:
                    break
                correlativo += 1

            employee_id = new_id

            self.employee = Employee(employee_id, name, password, position)
            self.accept()
        else:
            print("Por favor, complete todos los campos.")

    def get_employee(self):
        return self.employee

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Iniciar Sesión")
        self.setGeometry(100, 100, 400, 200)

        self.label_username = QLabel("Usuario:")
        self.label_password = QLabel("Contraseña:")
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.login_button = QPushButton("Iniciar Sesión")

        self.username_input.setText("PM-202110180")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setText("12345678")

        self.login_button.clicked.connect(self.on_login)

        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.label_username)
        layout.addWidget(self.username_input)
        layout.addWidget(self.label_password)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        return layout

    def on_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "PM-202110180" and password == "12345678":
            self.open_main_menu()

    def open_main_menu(self):
        self.main_menu = MenuPrincipal()
        self.main_menu.show()
        self.hide()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Proyectos y Tareas")
        self.setGeometry(100, 100, 800, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    main_window = MainWindow()
    
    login_window.show()
    sys.exit(app.exec_())


    # def create_filter_dropdown(self):
    #     active_projects = self.get_active_projects_for_employee()
    #     active_projects.append("Mostrar todas las tareas")

    #     filter_label = QLabel("Filtrar tareas por proyecto:")
    #     self.filter_dropdown = QComboBox()
    #     self.filter_dropdown.addItems(active_projects)

    #     filter_button = QPushButton("Filtrar")
    #     filter_button.clicked.connect(self.filter_tasks)

    #     filter_layout = ()
    #     filter_layout.addWidget(filter_label)
    #     filter_layout.addWidget(self.filter_dropdown)
    #     filter_layout.addWidget(filter_button)

    # return filter_layout