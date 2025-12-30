
call "D:\mega\python\+Modulos\++copiar modulos de onedrive.bat"


set RUTA_ORIGEN="D:\mega\python\edu bolsa web
set RUTA_INSTALACION="D:\programacion\python\edu bolsa web
mkdir %RUTA_INSTALACION%"

copy %RUTA_ORIGEN%\app.py" %RUTA_INSTALACION%"
copy %RUTA_ORIGEN%\database.db" %RUTA_INSTALACION%"
copy %RUTA_ORIGEN%\edu_bolsa_web.bat" %RUTA_INSTALACION%"
copy %RUTA_ORIGEN%\forms.py" %RUTA_INSTALACION%"
copy %RUTA_ORIGEN%\models.py" %RUTA_INSTALACION%"
copy %RUTA_ORIGEN%\requirements.txt" %RUTA_INSTALACION%"
copy %RUTA_ORIGEN%\wsgi.py" %RUTA_INSTALACION%"
copy %RUTA_ORIGEN%\instalar requirements.bat" %RUTA_INSTALACION%"

mkdir %RUTA_INSTALACION%\instance"
Xcopy %RUTA_ORIGEN%\instance" %RUTA_INSTALACION%\instance" /E /H /C /I /Y

mkdir %RUTA_INSTALACION%\Templates"
Xcopy %RUTA_ORIGEN%\Templates" %RUTA_INSTALACION%\Templates" /E /H /C /I /Y



echo pause