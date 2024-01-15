from tkinter.messagebox import askyesno,showerror,showinfo
from tkinter import *
from metodos_staticos import *
from dato import IntegrityError
from _tkinter import TclError
def mensaje_alta(fun_alta):
    def envoltura(*args):
        if fun_alta(*args):
            print("hola")
        else:
            print("chau")
    return envoltura

class Control():
    def __init__(self) -> None:
        pass
    @mensaje_alta
    def alta(producto,precio,tree,stock,my_base):   
        valor=True
        try:
            if producto.get()!="" and precio.get()!="" and stock.get()!="":
                if validar.validar_producto(producto.get())==True:
                    if askyesno( "ALTA",f"decea dar de alta: {producto.get()} ${precio.get()}"):
                        cursor=my_base.cursor()
                        data=(producto.get(),precio.get(),stock.get())
                        sql="INSERT INTO producto(producto, precio, stock) VALUES(?,?,?)"
                        cursor.execute(sql,data)
                        my_base.commit()
                        
                        showinfo(title="ALTA",message="Alta Exitosa")
                        """
                        ingreso=Tabla()
                        ingreso.descripcion=producto.get()
                        ingreso.precio=precio.get()
                        ingreso.stock=stock.get()
                        ingreso.save()
                        showinfo(title="ALTA",message="Alta Exitosa")
                        """
                        Control.actualizar_treeview(tree,my_base)
                        Vaciar.vaciar(producto,precio,stock)
                    else:
                        showinfo(title="ALTA",message="Alta Cancelada")  
                        valor=False
                else:
                    showerror(title="ERROR AL VALIDAR", message="ERROR EN EL CAMPO DESCIPCION")
                    valor=False
            else:
                showerror(title="ERROR", message="NO SE PUEDEN DAR DE ALTA CAMPOS VACIOS")
                valor=False
        except(IntegrityError):
            showerror(title="ERROR", message="NO SE PUEDEN DAR DE ALTA PRODUCTOS IGUALES")
            Vaciar.vaciar(producto,precio,stock)
        except(TclError):
            showerror(title="ERROR", message="CAMPO PRECIO U STOCK VACIOS, NO ADMITEN LETRAS")
            Vaciar.vaciar(producto,precio,stock)
        return valor
    def baja(tree,producto,precio,stock,boton_modificar,boton_alta,boton_borrar,my_base):
        
        if askyesno("BAJA",f"decea dar de baja: {producto.get()} $ {precio.get()}"):
            select=tree.selection()
            select_i=tree.item(select)
            id=select_i['text']
            cursor=my_base.cursor()
            data=(id,)
            sql= "DELETE FROM producto WHERE id = ?;"
            cursor.execute(sql,data)
            my_base.commit()
            """
            borrar=Tabla.get(Tabla.id==select_i["text"])
            borrar.delete_instance()
            tree.delete(select)"""
            Control.actualizar_treeview(tree,my_base)
            showinfo(title="BAJA",message="Baja Exitosa") 
            Vaciar.vaciar(producto,precio,stock)
        else:
            showerror(title="ERROR",message="BAJA CANCELADA")
            Vaciar.vaciar(producto,precio,stock)
        boton_modificar.configure(state=DISABLED)
        boton_alta.configure(state=NORMAL)
        boton_borrar.configure(state=DISABLED) 

    def modificar(tree,producto,precio,stock,boton_modificar,boton_alta,boton_borrar,my_base):
        try:
            if producto.get()!="" and precio.get()!="" and stock.get()!="":
                if validar.validar_producto(producto.get())==True:
                    if askyesno("MODIFICAR",f"decea modificar: {producto.get()} ${precio.get()} {stock.get()}"):
                        
                        select=tree.selection()
                        select_item=tree.item(select)
                        id_item=select_item["text"]
                        id_item=str(id_item)
                        cursor=my_base.cursor()
                        sql="UPDATE producto SET (producto,precio,stock)=(?,?,?) WHERE id=?;"
                        data=(producto.get(),precio.get(),stock.get(),id_item)
                        cursor.execute(sql,data)
                        my_base.commit()
                        Control.actualizar_treeview(tree,my_base)                        
                        showinfo(title="MODIFICAR",message="Modificacion Exitosa")
                        Vaciar.vaciar(producto,precio,stock)
                    else:
                        showinfo(title="MODIFICAR",message="Modificacion Cancelada")
                        Vaciar.vaciar(producto,precio,stock)
                else:
                    showerror(title="ERROR AL VALIDAR", message="ERROR EN EL CAMPO DESCIPCION")
                    Vaciar.vaciar(producto,precio,stock)
            else:
                showerror(title="ERROR", message="CAMPO DESCRIPCION VACIO")        
                boton_modificar.configure(state=DISABLED)
                boton_alta.configure(state=NORMAL)
                boton_borrar.configure(state=DISABLED)
                Vaciar.vaciar(producto,precio,stock)
        except(TclError):
            showerror(title="ERROR", message="CAMPO PRECIO U STOCK VACIOS, NO ADMITEN LETRAS")
            Vaciar.vaciar(producto,precio,stock)

        boton_modificar.configure(state=DISABLED)
        boton_alta.configure(state=NORMAL)
        boton_borrar.configure(state=DISABLED)
            



    def muestra(tree,producto,precio,stock,boton_modificar,boton_alta,boton_borrar):
        #Para evitar que lance un error, si el usuario no slecciona un valor del Tree
        try:
            select=tree.selection()
            select_item=tree.item(select)
            i=select_item["values"]
            producto.set(i[0])
            precio.set(i[1])
            stock.set(i[2])
            boton_modificar.configure(state=NORMAL)
            boton_alta.configure(state=DISABLED)
            boton_borrar.configure(state=NORMAL)
        except(IndexError):
            showerror(title="ERROR", message="seleccione un objeto")
    """
    def actualizar_treeview(tree):
        records = tree.get_children()
        for element in records:
            tree.delete(element)

        for fila in Tabla.select():
            tree.insert("", 0, text=fila.id, values=(fila.descripcion, fila.precio,fila.stock))
    """
    def actualizar_treeview(tree,my_base):
        records = tree.get_children()
        for element in records:
            tree.delete(element)
        sql = "SELECT * FROM producto ORDER BY id ASC"
        cursor=my_base.cursor()
        datos=cursor.execute(sql)
        resultado = datos.fetchall()
        for fila in resultado:
            tree.insert("", 0, text=fila[0], values=(fila[1], fila[2],fila[3]))