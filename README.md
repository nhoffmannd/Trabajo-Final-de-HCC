En este trabajo, vamos a crear una herramienta usando python para automatizar las evaluaciones de los datos electroquímicos. La herramienta debe contar con una interfase gráfica.

Los datos electroquímicos serán proveídos en formato XLS, generados por un plugin automatizado para Excel 2003.
Para trabajar con los datos, se utilizará el módulo pandas de Python, disponible en:
https://pypi.org/project/pandas/#files
La versión utilizada es la 0.22 de AMD64 cp36, del 31/12/2017.

Para crear la interfase gráfica, se utiliza el módulo PyQt5 de Python, disponible en:
https://pypi.python.org/pypi/PyQt5#downloads
La versión utilizada es la 5.10 de cp35 cp36 cp37 AMD64, con un md5 de fe1f156b3454e414b5fef0c8df6a76e0.

28/02/2018:
Tras muchas vueltas, he encontrado cómo se instalan los módulos en forma .whl.
Python 3.6 viene con pip, que puede accederse desde Windows Powershell. Se usa cd para acceder a la carpeta contenedora, y luego, se usa el comando:

pip install [nombre del archivo .whl]


Estoy siguiendo las instrucciones de http://zetcode.com/gui/pyqt5/firstprograms/ para entender pyQT5.

Quiero armar una pantalla en la cual me permita, a partir de un menú, seleccionar un archivo.