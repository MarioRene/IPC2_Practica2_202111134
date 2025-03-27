import tkinter as tk
from tkinter import messagebox, ttk
from collections import deque
from graphviz import Digraph
import os
import time

class PizzaOrder:
    def __init__(self, order_id, customer_name):
        self.order_id = order_id
        self.customer_name = customer_name
        self.pizzas = []
        self.creation_time = time.time()
    
    def add_pizza(self, specialty, quantity=1):
        for _ in range(quantity):
            self.pizzas.append(specialty)
    
    def remove_pizza(self, specialty):
        if specialty in self.pizzas:
            self.pizzas.remove(specialty)
            return True
        return False
    
    def get_total_time(self):
        specialty_times = {
            "Pepperoni": 12,
            "Hawaiana": 15,
            "Vegetariana": 18,
            "Cuatro Quesos": 20
        }
        return sum(specialty_times[pizza] for pizza in self.pizzas)
    
    def get_queue_time(self, current_time):
        return int((current_time - self.creation_time) / 60)  # Convertir a minutos
    
    def __str__(self):
        pizza_counts = {}
        for pizza in self.pizzas:
            pizza_counts[pizza] = pizza_counts.get(pizza, 0) + 1
        
        pizza_details = []
        for specialty, count in pizza_counts.items():
            time_per_pizza = {
                "Pepperoni": 12,
                "Hawaiana": 15,
                "Vegetariana": 18,
                "Cuatro Quesos": 20
            }[specialty]
            pizza_details.append(f"{count} x {specialty} - {time_per_pizza} min cada una")
        
        return (f"Orden {self.order_id}\n"
                f"Nombre: {self.customer_name}\n"
                f"Cantidad de pizzas: {len(self.pizzas)}\n"
                f"Especialidades: {', '.join(pizza_details)}\n"
                f"Tiempo Total: {self.get_total_time()} min")

class PizzaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Pizzas")
        self.root.geometry("800x600")
        
        # Configuración de estilo
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        
        # Variables de estado
        self.order_queue = deque()
        self.current_order_id = 1
        self.current_order = None
        
        # Crear menú principal
        self.create_main_menu()
    
    def create_main_menu(self):
        """Crea la interfaz del menú principal"""
        self.clear_window()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Sistema de Pizzas", font=('Arial', 16, 'bold')).pack(pady=20)
        
        buttons = [
            ("Nueva Orden", self.create_new_order),
            ("Entregar Orden", self.deliver_order),
            ("Ver Órdenes", self.view_orders),
            ("Salir", self.root.quit)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(main_frame, text=text, command=command, width=20)
            btn.pack(pady=10)
    
    def create_new_order(self):
        """Crea una nueva orden"""
        self.clear_window()
        self.current_order = PizzaOrder(self.current_order_id, "")
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Nueva Orden", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Datos del cliente
        customer_frame = ttk.Frame(main_frame)
        customer_frame.pack(pady=10, fill='x')
        
        ttk.Label(customer_frame, text="Nombre del Cliente:").grid(row=0, column=0, sticky='w')
        self.customer_name_entry = ttk.Entry(customer_frame)
        self.customer_name_entry.grid(row=0, column=1, padx=5, sticky='ew')
        
        # Especialidad y cantidad
        pizza_frame = ttk.Frame(main_frame)
        pizza_frame.pack(pady=10, fill='x')
        
        ttk.Label(pizza_frame, text="Especialidad:").grid(row=0, column=0, sticky='w')
        self.specialty_var = tk.StringVar()
        specialties = ["Pepperoni", "Hawaiana", "Vegetariana", "Cuatro Quesos"]
        self.specialty_combo = ttk.Combobox(pizza_frame, textvariable=self.specialty_var, values=specialties, state="readonly")
        self.specialty_combo.grid(row=0, column=1, padx=5, sticky='ew')
        self.specialty_combo.current(0)
        
        ttk.Label(pizza_frame, text="Cantidad:").grid(row=1, column=0, sticky='w')
        self.quantity_var = tk.IntVar(value=1)
        self.quantity_spin = ttk.Spinbox(pizza_frame, from_=1, to=10, textvariable=self.quantity_var)
        self.quantity_spin.grid(row=1, column=1, padx=5, sticky='ew')
        
        # Botones para agregar/eliminar pizzas
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Agregar Pizza", command=self.add_pizza_to_order).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Eliminar Pizza", command=self.remove_pizza_from_order).pack(side='left', padx=5)
        
        # Lista de pizzas en la orden actual
        self.pizzas_listbox = tk.Listbox(main_frame, height=5)
        self.pizzas_listbox.pack(pady=10, fill='x')
        
        # Botones finales
        final_button_frame = ttk.Frame(main_frame)
        final_button_frame.pack(pady=20)
        
        ttk.Button(final_button_frame, text="Cancelar", command=self.create_main_menu).pack(side='left', padx=5)
        ttk.Button(final_button_frame, text="Finalizar Orden", command=self.finalize_order).pack(side='left', padx=5)
    
    def add_pizza_to_order(self):
        """Agrega una pizza a la orden actual"""
        specialty = self.specialty_var.get()
        quantity = self.quantity_var.get()
        
        if not specialty:
            messagebox.showerror("Error", "Seleccione una especialidad")
            return
        
        self.current_order.add_pizza(specialty, quantity)
        self.update_pizzas_list()
    
    def remove_pizza_from_order(self):
        """Elimina una pizza de la orden actual"""
        selected = self.pizzas_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Seleccione una pizza para eliminar")
            return
        
        pizza_str = self.pizzas_listbox.get(selected[0])
        specialty = pizza_str.split(" x ")[1].split(" - ")[0]
        
        if self.current_order.remove_pizza(specialty):
            self.update_pizzas_list()
        else:
            messagebox.showerror("Error", "No se pudo eliminar la pizza")
    
    def update_pizzas_list(self):
        """Actualiza la lista de pizzas en la interfaz"""
        self.pizzas_listbox.delete(0, tk.END)
        
        pizza_counts = {}
        for pizza in self.current_order.pizzas:
            pizza_counts[pizza] = pizza_counts.get(pizza, 0) + 1
        
        for specialty, count in pizza_counts.items():
            time_per_pizza = {
                "Pepperoni": 12,
                "Hawaiana": 15,
                "Vegetariana": 18,
                "Cuatro Quesos": 20
            }[specialty]
            self.pizzas_listbox.insert(tk.END, f"{count} x {specialty} - {time_per_pizza} min cada una")
    
    def finalize_order(self):
        """Finaliza la orden actual y la agrega a la cola"""
        customer_name = self.customer_name_entry.get().strip()
        if not customer_name:
            messagebox.showerror("Error", "Ingrese el nombre del cliente")
            return
        
        if not self.current_order.pizzas:
            messagebox.showerror("Error", "La orden no tiene pizzas")
            return
        
        self.current_order.customer_name = customer_name
        self.order_queue.append(self.current_order)
        self.current_order_id += 1
        
        messagebox.showinfo("Éxito", f"Orden {self.current_order.order_id} agregada a la cola")
        self.create_main_menu()
        self.visualize_queue()
    
    def deliver_order(self):
        """Entrega la siguiente orden en la cola"""
        self.clear_window()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, padx=20, pady=20)
        
        if not self.order_queue:
            ttk.Label(main_frame, text="No hay pedidos pendientes", font=('Arial', 14)).pack(pady=50)
            ttk.Button(main_frame, text="Regresar", command=self.create_main_menu).pack(pady=20)
            return
        
        delivered_order = self.order_queue.popleft()
        current_time = time.time()
        queue_time = delivered_order.get_queue_time(current_time)
        total_time = delivered_order.get_total_time()
        
        # Mostrar detalles de la orden entregada
        ttk.Label(main_frame, text="ORDEN ENTREGADA", font=('Arial', 16, 'bold')).pack(pady=10)
        
        order_frame = ttk.Frame(main_frame, borderwidth=2, relief="groove")
        order_frame.pack(pady=10, fill='x', padx=50)
        
        ttk.Label(order_frame, text=f"Orden {delivered_order.order_id}", font=('Arial', 12, 'bold')).pack(pady=5)
        ttk.Label(order_frame, text=f"Nombre: {delivered_order.customer_name}").pack(anchor='w', padx=10)
        ttk.Label(order_frame, text=f"Cantidad de pizzas: {len(delivered_order.pizzas)}").pack(anchor='w', padx=10)
        
        # Mostrar especialidades con sus tiempos
        pizza_counts = {}
        for pizza in delivered_order.pizzas:
            pizza_counts[pizza] = pizza_counts.get(pizza, 0) + 1
        
        for specialty, count in pizza_counts.items():
            time_per_pizza = {
                "Pepperoni": 12,
                "Hawaiana": 15,
                "Vegetariana": 18,
                "Cuatro Quesos": 20
            }[specialty]
            ttk.Label(order_frame, text=f"{count} x {specialty} ~ Tiempo: {time_per_pizza} min").pack(anchor='w', padx=10)
        
        ttk.Label(order_frame, text=f"Tiempo Total: {total_time} min", font=('Arial', 10, 'bold')).pack(anchor='w', padx=10, pady=5)
        ttk.Label(order_frame, text=f"Tiempo en cola: {queue_time} minutos", font=('Arial', 10, 'bold')).pack(anchor='w', padx=10)
        
        # Botón para regresar
        ttk.Button(main_frame, text="Regresar", command=self.create_main_menu).pack(pady=20)
        
        # Actualizar visualización de la cola
        self.visualize_queue()
    
    def view_orders(self):
        """Muestra todas las órdenes en la cola"""
        self.clear_window()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        ttk.Label(main_frame, text="ÓRDENES EN COLA", font=('Arial', 16, 'bold')).pack(pady=10)
        
        if not self.order_queue:
            ttk.Label(main_frame, text="No hay órdenes en la cola", font=('Arial', 12)).pack(pady=50)
            ttk.Button(main_frame, text="Regresar", command=self.create_main_menu).pack(pady=20)
            return
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mostrar cada orden en la cola
        current_time = time.time()
        for order in self.order_queue:
            order_frame = ttk.Frame(scrollable_frame, borderwidth=2, relief="groove")
            order_frame.pack(pady=10, fill='x', padx=10)
            
            ttk.Label(order_frame, text=f"Orden {order.order_id}", font=('Arial', 12, 'bold')).pack(pady=5)
            ttk.Label(order_frame, text=f"Nombre: {order.customer_name}").pack(anchor='w', padx=10)
            ttk.Label(order_frame, text=f"Cantidad de pizzas: {len(order.pizzas)}").pack(anchor='w', padx=10)
            
            # Mostrar especialidades con sus tiempos
            pizza_counts = {}
            for pizza in order.pizzas:
                pizza_counts[pizza] = pizza_counts.get(pizza, 0) + 1
            
            for specialty, count in pizza_counts.items():
                time_per_pizza = {
                    "Pepperoni": 12,
                    "Hawaiana": 15,
                    "Vegetariana": 18,
                    "Cuatro Quesos": 20
                }[specialty]
                ttk.Label(order_frame, text=f"{count} x {specialty} ~ Tiempo: {time_per_pizza} min").pack(anchor='w', padx=10)
            
            total_time = order.get_total_time()
            queue_time = order.get_queue_time(current_time)
            
            ttk.Label(order_frame, text=f"Tiempo Total: {total_time} min", font=('Arial', 10, 'bold')).pack(anchor='w', padx=10, pady=5)
            ttk.Label(order_frame, text=f"Tiempo en cola: {queue_time} minutos", font=('Arial', 10, 'bold')).pack(anchor='w', padx=10)
        
        # Botón para regresar
        ttk.Button(main_frame, text="Regresar", command=self.create_main_menu).pack(pady=20)
    
    def visualize_queue(self):
        """Crea una visualización gráfica de la cola usando Graphviz"""
        if not hasattr(self, 'graph_dir'):
            self.graph_dir = "queue_visualizations"
            os.makedirs(self.graph_dir, exist_ok=True)
        
        dot = Digraph(comment='Cola de Pedidos de Pizza')
        dot.attr('node', shape='box', style='rounded')
        dot.attr(rankdir='LR')  # De izquierda a derecha
        
        if not self.order_queue:
            dot.node('0', 'Cola Vacía')
        else:
            for i, order in enumerate(self.order_queue):
                pizza_counts = {}
                for pizza in order.pizzas:
                    pizza_counts[pizza] = pizza_counts.get(pizza, 0) + 1
                
                pizzas_str = "\\n".join([f"{count}x {pizza}" for pizza, count in pizza_counts.items()])
                label = (f"Orden {order.order_id}\\n"
                         f"Cliente: {order.customer_name}\\n"
                         f"Total: {order.get_total_time()} min\\n"
                         f"{pizzas_str}")
                
                dot.node(str(i), label)
                
                if i > 0:
                    dot.edge(str(i-1), str(i))
        
        filename = f"{self.graph_dir}/queue_{int(time.time())}"
        dot.render(filename, format='png', cleanup=True)
    
    def clear_window(self):
        """Limpia la ventana actual"""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PizzaApp(root)
    root.mainloop()
    
