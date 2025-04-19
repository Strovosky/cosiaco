error_data = {
            "correo o contraseña faltantes":{"estado":False, "mensaje":"No se proveyó el el correo o la contraseña"},
            "usuario desactivado":{"estado":False, "mensaje":"El usuario se encuentra desactivado. Activelo primero."},
            "usuario no existe":{"estado":True, "mensaje":"No existe un usuario con ese correo"},
            "credenciales_incorrectas":{"estado":False, "mensaje":"La contraseña es incorrecta"}
        }


for error_key, error_value in error_data.items():
    if error_value["estado"]:
        print(f"We got it, it's {error_key}")





