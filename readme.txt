Para mejorar la legibilidad del código, dividí las funciones del código en módulos. Tal vez no fue la mejor ni la más práctica idea, pero lo hice con fines puramente estéticos.
Cada módulo tiene funciones cuyas descripciones están agregadas como comentarios previo a la declaración.
Los módulos "main" y "transferencias" tienen varios códigos de error que están descriptos al final de su código.

###MÓDULO MAIN###
Se encarga del ingreso y creación de usuarios, así como de inicializar el módulo de homebanking.

### MÓDULO HOMEBANKING ###
Funciona como interfaz para que el usuario acceda a su información (nombre, dinero en cuenta y saldo), así como inicializar diferentes procesos que serán descriptos a continuación:

	### MÓDULO TRANSFERENCIAS ###
	Permite que un usuario transfiera dinero a otro usuario, siempre y cuando se cumplan las condiciones (existencia y dinero en cuenta)

	### MÓDULO CUENTAS ###
	Permite que un usuario pague sus deudas, siempre y cuando se cumplan las condiciones (dinero en cuenta).

	### MÓDULO PRÉSTAMOS ###
	Permite que un usuario acceda a 3 tipos de préstamo, que varían según cantidad de dinero y tiempo para pagar.

	### MÓDULO HISTORIAL ###
	Permite que un usuario vea su historial y acceda a los detalles de cada operación.


El programa guarda sus datos en un archivo "users.txt" cuyo contenido es una lista con la información de cada usuario. Esta lista se divide en...
# DNI (funciona como identificador para cada usuario)
# Contraseñas 
# Nombre
# Alias
# Dinero
# Deudas (contiene el detalle de la deuda y el dinero a pagar)
# Historial (formato tipo <Fecha: operación>:<lista contenedora de código de operación y detalles>
El archivo tiene un backup por si llega a surgir algún inconveniente o se desea volver a un estado previo

# NOTA: hay una cuenta de rápido acceso, cuyos DNI y contraseña son "1"