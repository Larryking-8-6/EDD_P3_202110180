# Proyecto2-EDD

## 202110180 - Juan Carlos Gonzalez Valdez - seccion C

Librerias y importaciones de la parte grafica:

| Funciones y Bibliotecas Utilizadas | Descripción                           |
|-----------------------------------|---------------------------------------|
| `import sys`                      | Módulo del sistema Python.            |
| `import csv`                      | Módulo para leer/escribir archivos CSV.|
| `import json`                     | Módulo para trabajar con JSON.        |
| `import os`                       | Módulo para interactuar con el sistema de archivos.|
| `import random`                   | Módulo para generación de números aleatorios.|
| `import subprocess`               | Módulo para ejecutar procesos externos.|
| `import graphviz`                 | Módulo para trabajar con gráficos y visualización de datos.|
| `from PyQt5.QtWidgets import ...`  | Importación de clases y widgets para construir interfaces gráficas.|
| `QMessageBox`                     | Clase para mostrar cuadros de diálogo de mensaje.|
| `QPushButton`                     | Clase para crear botones en una interfaz gráfica.|
| `QMainWindow`                     | Clase principal de una ventana de la interfaz gráfica.|


### Funciones de las clases en el programa:

![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/584937b0-8899-4212-a5ed-716ee65dcfa5)

![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/4ff0808e-2e0a-43db-99d5-7ae02ee100dc)

![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/d135c039-bf88-49a6-86ec-926c3cb0a311)

![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/17c69b20-c910-43ef-8a63-28a7e890e637)

![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/2c9f41cf-b8a2-4941-ae1a-20e3a75e8934)


Clase Employee:

Esta clase representa a un empleado y almacena información como el ID del empleado, el nombre, la contraseña y el puesto. También puede tener asignado un ID de proyecto.

Clase Project:

La clase Project representa un proyecto y almacena información como el ID del proyecto, el nombre y la prioridad del proyecto. Además, tiene una lista de tareas relacionadas con el proyecto.

Clase Task:

La clase Task representa una tarea y almacena información como el ID de la tarea, el nombre de la tarea, el ID del empleado asignado y el ID del proyecto al que pertenece.

Clase AVLNode:

AVLNode es una clase utilizada en la implementación del árbol AVL. Cada nodo almacena información sobre un proyecto y su altura. También tiene referencias a sus hijos izquierdo y derecho.

Clase AVLTree:

La clase AVLTree representa un árbol AVL y se utiliza para almacenar proyectos. Ofrece operaciones de inserción y recuperación de proyectos, así como la generación de un archivo DOT para visualizar el árbol.

Clase BTreeNode:

BTreeNode es una clase utilizada en la implementación del árbol B. Cada nodo almacena una lista de claves, referencias a sus hijos y si es una hoja o no. También tiene una referencia a su padre.

Clase BTree:

La clase BTree representa un árbol B y se utiliza para almacenar pares de IDs de tarea y proyecto. Ofrece operaciones de inserción y búsqueda de pares de IDs, así como la generación de un archivo DOT para visualizar el árbol B.

Clase HashTable:

La clase HashTable representa una tabla hash y se utiliza para almacenar y gestionar información relacionada con empleados. Proporciona métodos para la inserción, recuperación y eliminación de empleados utilizando una estructura de tabla hash.

Clase EmployeeInfoDialog:

EmployeeInfoDialog es una clase que representa un cuadro de diálogo utilizado para mostrar información detallada sobre un empleado. Este cuadro de diálogo se utiliza en la interfaz de usuario para ver y editar la información de un empleado específico.

Clase MenuPrincipal:

MenuPrincipal es una clase que representa la ventana principal de la aplicación. Es la interfaz de usuario principal desde la cual los usuarios pueden acceder a diversas funcionalidades de la aplicación, como la gestión de empleados y proyectos. Esta clase maneja la interacción principal con el usuario y la navegación entre diferentes vistas o funcionalidades.


## Metodos y funcionamientos del programa:

Método __init__(self):
Este es el constructor de la clase MenuPrincipal. Se encarga de inicializar la ventana principal de la aplicación y configurar su interfaz de usuario, incluyendo la barra de menú y la disposición de elementos en la ventana.

Método create_actions(self):

Este método crea las acciones (botones y elementos de menú) que se pueden realizar en la ventana principal. Cada acción está asociada a una función específica que se ejecutará cuando el usuario interactúe con el elemento.

Método create_new_project(self):

Este método se utiliza para crear un nuevo proyecto. Abre un cuadro de diálogo donde el usuario puede ingresar el nombre y la prioridad del proyecto. Luego, crea una instancia de la clase Project y la inserta en un árbol AVL llamado project_table.

Método create_new_task(self):

Este método permite al usuario crear una nueva tarea. Comienza mostrando un cuadro de diálogo para ingresar el nombre de la tarea y seleccionar un empleado para asignarle la tarea. Luego, el usuario selecciona un proyecto al que se asignará la tarea. La tarea se crea como una instancia de la clase Task y se agrega a una lista llamada created_tasks.

Método assign_employee_to_task(self):

Este método permite asignar un empleado existente a una tarea. El usuario selecciona una tarea de la lista y proporciona el ID del empleado que desea asignar a esa tarea.

Método assign_task_to_project(self):

Este método permite asignar una tarea existente a un proyecto. El usuario selecciona una tarea de la lista de tareas creadas previamente y asigna un proyecto existente a esa tarea.

Método get_tasks_by_project(self, project_id):

Este método devuelve una lista de tareas que pertenecen al proyecto con el ID especificado.

Método create_filter_dropdown(self):

Este método crea un menú desplegable que permite al usuario filtrar las tareas por proyecto. Los proyectos activos se obtienen de la función get_active_projects_for_employee() y se agregan al menú desplegable.

Método filter_tasks(self):

Este método se llama cuando se hace clic en el botón de filtro. Filtra las tareas según la opción seleccionada en el menú desplegable y muestra las tareas filtradas en la ventana.

Método get_active_projects_for_employee(self):

Este método debería devolver una lista de proyectos activos para un empleado, pero está vacío en el código proporcionado.

Método get_project_id_by_name(self, project_name):

Este método debería devolver el ID de un proyecto dado su nombre, pero está vacío en el código proporcionado.

Método view_all_tasks(self):

Este método debería mostrar todas las tareas, pero actualmente está vacío en el código proporcionado.

Método view_tasks_by_project(self, project_id):

Este método muestra las tareas para un proyecto específico en la ventana principal.

Método view_employees(self):

Este método muestra una lista de empleados en la ventana principal, incluyendo su nombre, código y puesto.

Método view_projects(self):

Este método muestra una lista de proyectos en la ventana principal, incluyendo su nombre, ID y prioridad.

Método _inorder_traversal(self, node):

Este método realiza un recorrido en orden en un árbol binario AVL y muestra información sobre los proyectos en la ventana principal.

Método view_tasks(self):

Este método muestra una lista de tareas en la ventana principal, incluyendo su nombre, ID de empleado y ID de proyecto.

Método assign_project_to_employee(self):

Este método permite asignar un proyecto existente a un empleado. El usuario selecciona un empleado y un proyecto existentes.

Método assign_task_to_selected_project(self):

Este método permite asignar una tarea a un proyecto asignado previamente a un empleado. El usuario selecciona un empleado y una tarea existentes.

Método generate_avl_report(self):

Este método genera un informe visual del árbol AVL de proyectos y lo guarda como un archivo PDF.

Método generate_b_report(self):

Este método genera un informe visual del árbol B de tareas y lo guarda como un archivo PDF (este método está vacío y parece haber un error de indentación en el código proporcionado).

Método generate_hash_table_report(self):

Este método genera un informe en texto plano de la tabla hash de empleados y lo guarda en un archivo de texto.

Método load_csv_employees(self):

Este método permite al usuario cargar datos de empleados desde un archivo CSV. Los datos se leen desde el archivo y se insertan en una tabla hash llamada employee_table.

Método find_employee_by_id(self, employee_id):

Este método busca un empleado por su ID y lo devuelve si se encuentra.

Método load_json(self):

Este método permite al usuario cargar datos desde un archivo JSON. Los datos incluyen información sobre proyectos, tareas y empleados, y se utilizan para actualizar las estructuras de datos en la aplicación.

Método create_new_employee(self):

Este método crea un nuevo empleado utilizando un cuadro de diálogo. El usuario ingresa el nombre, el puesto y la contraseña del empleado, y se crea una instancia de la clase Employee. Luego, se inserta en una tabla hash llamada employee_table.

Clase NewEmployeeDialog:

Esta clase define un cuadro de diálogo para crear un nuevo empleado. Permite al usuario ingresar el nombre, el puesto y la contraseña del empleado.

Clase LoginWindow:

Esta clase representa una ventana de inicio de sesión donde los usuarios pueden ingresar su nombre de usuario y contraseña para acceder a la aplicación.

Clase MainWindow:

Esta clase representa la ventana principal de la aplicación, que es una ventana principal donde se desarrolla la aplicación.

Bloque if __name__ == "__main__"::

Este bloque de código se ejecuta cuando el script se inicia como programa principal. Inicializa la aplicación, crea una instancia de LoginWindow y muestra la ventana de inicio de sesión.

## "Uso de las estructuras"

Árbol AVL (Árbol Binario de Búsqueda Balanceado):

Uso en el Proyecto: El Árbol AVL se utiliza para almacenar y organizar los proyectos. Cada nodo del árbol AVL representa un proyecto con su ID, nombre y prioridad. Los proyectos se almacenan en el árbol AVL de manera que se mantenga siempre balanceado, lo que garantiza un tiempo de búsqueda y recuperación eficiente de proyectos.

Un Árbol AVL es una estructura de datos en la que cada nodo tiene dos hijos, izquierdo y derecho, y la diferencia de alturas entre los subárboles izquierdo y derecho de cualquier nodo (llamada "factor de equilibrio") es como máximo 1. Cuando se insertan o eliminan proyectos en el árbol AVL, este se reorganiza automáticamente para mantener su equilibrio.

![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/b80d666b-9077-47f1-9365-2352a33d3f44)


Árbol B:

Uso en el Proyecto: El Árbol B se utiliza para almacenar las tareas de todos los proyectos. Cada nodo del Árbol B representa una tarea y contiene información sobre el nombre de la tarea, el ID del empleado responsable y el ID del proyecto al que está asignada. El Árbol B permite una búsqueda eficiente de tareas y una gestión eficaz de las asignaciones de tareas.

Un Árbol B es una estructura de datos en la que cada nodo puede tener múltiples hijos (generalmente entre 2 y un número fijo conocido como el "orden" del árbol). Los nodos del Árbol B están organizados de manera jerárquica, y se garantiza que los datos estén ordenados dentro del árbol. Los Árboles B se utilizan comúnmente en bases de datos y sistemas de archivos para gestionar y buscar datos eficientemente.

![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/9528a4f6-e3cc-43d1-87b1-41feab74a275)


Tabla Hash:

Uso en el Proyecto: La Tabla Hash se utiliza para mantener una lista de empleados generales. Cada entrada de la tabla hash contiene información sobre un empleado, incluyendo su nombre, ID, contraseña y puesto. La Tabla Hash permite una búsqueda rápida de empleados por su ID y almacena los datos de manera eficiente.

Una Tabla Hash es una estructura de datos que utiliza una función hash para mapear claves (en este caso, IDs de empleados) a valores (datos de empleado). Esto permite un acceso rápido a los datos utilizando la clave. En el proyecto, se utiliza la Tabla Hash para almacenar y recuperar rápidamente los detalles de los empleados utilizando sus IDs como claves.

![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/f6e16036-0ffe-4a5f-967e-b88d138f3acc)
