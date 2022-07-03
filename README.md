# Instrucciones para Windows:

	1)	Descargar y extraer el repositorio


	2)	Segundo click al archivo 'Docker File.rar' > Extraer aquí
			
			Contraseña:
				(Pedir por email a nsuepaint@gmail.com)


	3)	Abrir CMD o PowerShell


	4)	Utilizando el comando cd, ubicarse en la carpeta donde se extrajo el repositorio:
		
			Comando:
				cd "C:\Ejemplo\De\Carpetas\google_drive_permissions_controller"


	5)	Iniciar las imágenes y el contenedor utilizando docker-compose:
		
			Comando:
				docker-compose up
				
	
	6)	Abra un navegador de internet y dirígase a http://localhost:1453/
	
	
	7)	Inicie sesión con su cuenta de Google y otorgue los permisos requeridos.
		
			La aplicación no está oficialmente aprobada por Google, por lo cual
			aparecerá como aplicación no segura.
			
			La checkbox de permisos a Google Drive viene por defecto destildada,
			asegúrese de tildarla antes de continuar. De lo contrario la aplicación
			no funcionará correctamente.
			


Requisitos:

	1)	Docker Desktop (https://www.docker.com/products/docker-desktop/)
