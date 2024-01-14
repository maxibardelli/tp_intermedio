from re import *
# metos para usar en el modulo modelo, pero que no pertenecen al modulo en si
class validar():
    @staticmethod
    def validar_producto(producto):
        patron="^[A-Za-záéíóú1-9Ññ0.,\s\*]*$"
        if match(patron,producto):
            return True
        
        else:
            return False

class Vaciar():
    @staticmethod
    def vaciar(producto,precio,stock):
        producto.set("")
        precio.set(0)
        stock.set(0)