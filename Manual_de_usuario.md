# Proyecto2-EDD

## 202110180 - Juan Carlos Gonzalez Valdez - Proyect Up
## Requisitos del sistema:

## Hardware

Procesador: Se recomienda un procesador de al menos 2.0 GHz de velocidad.
Memoria RAM: Se recomienda al menos 4 GB de RAM.
Almacenamiento: Se requiere al menos 100 MB de espacio en disco para la instalación.

## Software

Sistema Operativo: Se recomienda uno de los siguientes sistemas operativos:

Windows 10 o posterior.
macOS 10.12 Sierra o posterior.
Distribuciones Linux compatibles.
Python: Se requiere Python 3.x instalado en el sistema.

Qt Framework: Se debe instalar el framework Qt para la interfaz de usuario.

Librerías y Dependencias: El proyecto puede requerir ciertas librerías y dependencias adicionales en base a lo trabajado.


# Utilizacion del programa

![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/42d4bd69-4f33-40fd-8e8c-fd482b461c74)

Ventana principal al ejecitar, donde se tendra que logiar el administrador.

![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/d0dbe2e0-79d5-46ee-9874-24204975b6c0)

Al iniciar sesion pasamos al menu con mas opciones en base a los requerimentos del programa tales como:

### Archivo
![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/89dc6af5-34eb-479b-bca6-96cc89d8d62c)


### Cargar Empleados
![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/7204e18b-f4ff-4992-af12-e4f7bc1e9794)

En este apartado nos encontramos con la seccion de carga, donde podemos cargarlos tanto en json, csv y manuales. al seleccionar cualquiera de las 3 se abre un menu con opciones.
![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/74225c36-c10d-480a-905c-5ed8279c5549)

al cargar por ejemplo el csv donde estarian los empleados nos llega un mensaje en terminal que se han cargado correctamente tanto ahi como en json.

Al seleccionar nuevo empleado se despliega un menu para agregarlo manualmente:
![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/9ff20594-f4cd-4c26-b079-e43ed26618db)
Con 4 opciones por defecto al ser el administrador y agregar equipo de trabajo.

![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/bc57ad03-9d7d-4887-8778-7f40bf80dfbd)

### Ver empleados

En este apartado podemos los empleados cargados y registrados manualmente:
![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/a8ead9f9-415e-4551-a242-7f916077654e)

### Proyectos

En este apartado podemos crear, asignar y ver los proyectos del sistema:
![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/6cd69476-c194-4221-9190-fe23878a5523)

En este caso se mostratian los cargados por el json previamente
![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/93f783f3-b79b-4f94-ab96-34ac96c9a2ce)

En la parte de crear podemos crear uno nuevo e individual con su nombre y prioridad:
![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/b4366dbf-a306-4c84-94d6-ce98e6ae737d)
![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/b6843f44-9e88-442a-ab88-e1badfdeae9b)
![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/34d63023-c717-4993-b36e-6bb3f85711d9)

Asignar proyectos, la idea es que se pueda asignar un empleado pero cubre solo las tareas.

Y la opcion de ver proyecto que al seleccionarla muestra el listado completo de los proyectos en el sistema:
![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/ba9dc97a-3476-4485-9db9-680f58076f1e)

### Tareas

El apartado de tareas, donde podemos hacer una creacion, visualizacion y configuracion de la misma para cada empleado:

![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/2a202e08-8031-4269-a8b8-b37e1b4ccfc6)

Filtrar proyectos, esto deja filtrat en base a los activos y no activos pero debido a limitantes propias no se hizo una implementacion adecuada:
![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/5dacad7b-916e-4f50-b5ab-4a1a39cdb3a3)


Procesos actuales:
![image](https://github.com/Larryking-8-6/EDD_P3_202110180/assets/125839529/e9548640-a15e-41e8-a0af-ec3eb436f87a)

Aqui es donde definimos que tareas en base al orde se realizan apra seguir con la sigueinte del mismo poryecto.

Nueva tarea:
![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/3e2280a9-2904-47f0-9f80-b596634d95be)
Aqui podemos activar un despliegue de empleados para definir quien la hara:
![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/6bf6f327-60ed-43f3-9f97-823761a20599)

Y tambien definir en que proyecto sera:
![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/074ec3ee-acec-4758-8b8e-0d958e1d73af)

![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/a7d999fc-c8ab-4809-bbec-d09ae1b87162)

Tambien podemos cambiar la aseignacion de tareas y empleados.

## Completar tareas

Como agregado nuevo se implemnto un area para terminar tareas del programa donde se puden tener avances en tiempo real del mismo en base a los poryectos y tareas cargados.

![image](https://github.com/Larryking-8-6/EDD_P3_202110180/assets/125839529/48a6d399-5f75-44d3-b373-285a24ab2641)

![image](https://github.com/Larryking-8-6/EDD_P3_202110180/assets/125839529/c4017c56-361b-43ea-9b5a-740e651ea08b)

![image](https://github.com/Larryking-8-6/EDD_P3_202110180/assets/125839529/f7839efc-f0ed-4d0e-84cd-c3b374f50e50)

Estas mismas al ser completadas actualizan su estado para su finalizacion.

### Generar reportes

Esta es el area mas importante en donde resaltan los tipos de reportes en base a las estructura que se utilizaron:

## Reporte AVL:
Este es en base a los proyectos que hay en el sistema, generando un .dot grafico:

![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/a46afb40-9672-4840-a60f-83da0dc2fa3f)

Se muestra un ejemplo con datos pre cargados del json

## Reporte de B:
Este reporte contiene los datos de ID de proyecto, numero de tarea , empleado y nombre del proyecto:
![image](https://github.com/Larryking-8-6/Proyecto2-EDD/assets/125839529/9d44d2cf-8141-46dc-b714-f63ce6448655)

Debido a un par de inconvenientes los datos se cargan de manera erronea y no genera los nodos.

## Reporte Hash:

En este apartado podemos ver los datos de los empleados junto con la codificacion de los mismos en las contrasenias para uemtnar la seguridad.
![image](https://github.com/Larryking-8-6/EDD_P3_202110180/assets/125839529/85cb6589-701b-4104-95e1-f9f0a820450f)

![image](https://github.com/Larryking-8-6/EDD_P3_202110180/assets/125839529/d42ff542-ac9a-479b-9a00-2d5829af77c1)

## Reporte de Block chain

En este apartado se muestra el cifrado y guardado de datos en un bloque para mayor seguridad.

![image](https://github.com/Larryking-8-6/EDD_P3_202110180/assets/125839529/35d47dc6-0abf-4f06-a431-830d7fe30854)

![image](https://github.com/Larryking-8-6/EDD_P3_202110180/assets/125839529/af48d798-c4fb-47a9-ad93-14dd88dff6d0)


## Reporte Grafo
![image](https://github.com/Larryking-8-6/EDD_P3_202110180/assets/125839529/ebda365e-42d4-4b48-9a4e-a2464f42319f)
![Uploading image.png…]()


En este reporte se pueden obvservar las tareas completadas paso a paso.

