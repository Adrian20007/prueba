import psutil
import socket
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import paramiko
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage


#----------------------------------------------------------------------------gui1
class TaskManagerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SISTEMA DE MONITORIZACION")
        self.geometry("800x600")

        self.style = ttk.Style(self)
        self.style.configure("TLabel", font=("Arial", 14))
        self.style.configure("TButton", font=("Arial", 12))

        self.main_frame = ttk.Frame(self, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.hostname_label = ttk.Label(self.main_frame, text="Nombre de Host:")
        self.hostname_label.grid(row=0, column=0, sticky=tk.W)

        self.cpu_label = ttk.Label(self.main_frame, text="CPU:")
        self.cpu_label.grid(row=1, column=0, sticky=tk.W)

        self.mem_label = ttk.Label(self.main_frame, text="Memoria:")
        self.mem_label.grid(row=2, column=0, sticky=tk.W)

        self.disk_label = ttk.Label(self.main_frame, text="Disco:")
        self.disk_label.grid(row=3, column=0, sticky=tk.W)

        self.net_label = ttk.Label(self.main_frame, text="Red:")
        self.net_label.grid(row=4, column=0, sticky=tk.W)

        self.add_button = ttk.Button(self.main_frame, text="Añadir otro equipo", command=self.open_add_computer_dialog)
        self.add_button.grid(row=5, column=0, pady=10)
        
        self.enviar_correo_btn = ttk.Button(self.main_frame, text="Enviar correo de prueba",
command=self.enviar_correo_de_prueba)
        self.enviar_correo_btn.grid(row=5, column=1, sticky=tk.E)            

        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=1)
        self.main_frame.rowconfigure(3, weight=1)
        self.main_frame.rowconfigure(4, weight=1)

    def update_info(self, hostname, cpu_percent, mem_percent, disk_percent, net_info):
        self.hostname_label.config(text=f"Nombre de Host: {hostname}")
        self.cpu_label.config(text=f"CPU: {cpu_percent}%")
        self.mem_label.config(text=f"Memoria: {mem_percent}%")
        self.disk_label.config(text=f"Disco: {disk_percent}%")
        self.net_label.config(text="Red:\n" + "\n".join(net_info))

    def open_add_computer_dialog(self):
        dialog = AddComputerDialog(self)
        self.wait_window(dialog)
        
    def enviar_correo_de_prueba(self):
        servidor_smtp = 'smtp.gmail.com'
        puerto_smtp = 587
        remitente = 'servidores146@gmail.com'
        contraseña = 'rpdxdwogotmxmvax'
        destinatario = 'adriansanchezcotillas2000@gmail.com'
        asunto = 'Prueba de correo'
        mensaje = 'Este es un correo de prueba'
        
        email = EmailMessage()
        email['Subject'] = asunto
        email['From'] = remitente
        email['To'] = destinatario
        email.set_content(mensaje)

        try:
            server = smtplib.SMTP(servidor_smtp, puerto_smtp)
            server.starttls()
            server.login(remitente, contraseña)

            server.send_message(email)
            server.quit()

            messagebox.showinfo('Correo enviado', 'El correo de prueba ha sido enviado correctamente.')
        except Exception as e:
            messagebox.showerror('Error al enviar el correo', f"Se produjo un error al enviar el correo de prueba: {str(e)}")

class AddComputerDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Añadir otro equipo")
        self.geometry("400x300")

        ip_label = ttk.Label(self, text="Dirección IP:")
        ip_label.pack(pady=10)
        self.ip_entry = ttk.Entry(self)
        self.ip_entry.pack()

        username_label = ttk.Label(self, text="Usuario:")
        username_label.pack(pady=10)
        self.username_entry = ttk.Entry(self)
        self.username_entry.pack()

        password_label = ttk.Label(self, text="Contraseña:")
        password_label.pack(pady=10)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack()

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)

        connect_button = ttk.Button(button_frame, text="Conectar", command=self.connect)
        connect_button.grid(row=0, column=0, padx=10)

        cancel_button = ttk.Button(button_frame, text="Cancelar", command=self.cancel)
        cancel_button.grid(row=0, column=1, padx=10)

        self.result = None

    def connect(self):
        ip = self.ip_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if ip and username and password:
            self.result = (ip, username, password)
            self.destroy()
            ssh_manager = SSHManager()
            ssh_manager.open_ssh_connection(ip, username, password)

        else:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

    def cancel(self):
        self.destroy()



#---------------------------------------------------gui2


class TaskManagerGUI2(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SISTEMA DE MONITORIZACIÓN SSH")
        self.geometry("800x600")

        self.style = ttk.Style(self)
        self.style.configure("TLabel", font=("Arial", 14))
        self.style.configure("TButton", font=("Arial", 12))

        self.main_frame = ttk.Frame(self, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.hostname_label = ttk.Label(self.main_frame, text="Nombre de Host:")
        self.hostname_label.grid(row=0, column=0, sticky=tk.W)

        self.cpu_label = ttk.Label(self.main_frame, text="CPU:")
        self.cpu_label.grid(row=1, column=0, sticky=tk.W)

        self.mem_label = ttk.Label(self.main_frame, text="Memoria:")
        self.mem_label.grid(row=2, column=0, sticky=tk.W)

        self.disk_label = ttk.Label(self.main_frame, text="Disco:")
        self.disk_label.grid(row=3, column=0, sticky=tk.W)

        self.net_label = ttk.Label(self.main_frame, text="Red:")
        self.net_label.grid(row=4, column=0, sticky=tk.W)

        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=1)
        self.main_frame.rowconfigure(3, weight=1)
        self.main_frame.rowconfigure(4, weight=1)


    def update_info(self, hostname, cpu_percent, mem_percent, disk_percent, net_info):
        self.hostname_label.config(text=f"Nombre de Host: {hostname}")
        self.cpu_label.config(text=f"CPU: {cpu_percent}%")
        self.mem_label.config(text=f"Memoria: {mem_percent}%")
        self.disk_label.config(text=f"Disco: {disk_percent}%")
        self.net_label.config(text="Red:\n" + "\n".join(net_info))



#---------------------------------------------------monitor2

class SSHManager:
    def __init__(self):
        self.gui2 = TaskManagerGUI2()
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.gui2.main_frame)
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=6, padx=20, pady=20)
        
        self.cpu_percent = 0
        self.mem_percent = 0
        self.disk_percent = 0
        self.net_info = []

    def open_ssh_connection(self, ip, username, password):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh_client.connect(ip, username=username, password=password)
            self.ssh_client = ssh_client
            self.update_remote_info()
        except paramiko.AuthenticationException:
            messagebox.showerror("Error", "La autenticación ha fallado. Por favor, verifique las credenciales.")
        except paramiko.SSHException:
            messagebox.showerror("Error", "No se pudo establecer la conexión SSH.")
        except socket.error as e:
            messagebox.showerror("Error", f"No se pudo conectar al host remoto: {str(e)}")

    def update_remote_info(self):
        stdin, stdout, stderr = self.ssh_client.exec_command("top -bn1 | grep %Cpu && df -h")
        output = stdout.read().decode()
        lines = output.split('\n')
        self.cpu_percent = float(lines[0].split()[1].replace(',', '.'))

        mem_percent = psutil.virtual_memory().percent
        self.mem_percent = float(mem_percent)

        disk_info = [line.split() for line in lines if line.startswith('/dev/')]
        if disk_info:
            self.disk_percent = float(disk_info[0][4].strip('%'))
        else:
            self.disk_percent = 0

        net_info = self.get_remote_network_info()
        self.net_info = net_info

        self.gui2.update_info(self.get_remote_hostname(), self.cpu_percent, self.mem_percent, self.disk_percent, self.net_info)
        self.plot_usage(self.cpu_percent, self.mem_percent, self.disk_percent)
        self.gui2.after(1000, self.update_remote_info)

    def get_remote_network_info(self):
        net_info = []

        stdin, stdout, stderr = self.ssh_client.exec_command("ip addr show")
        output = stdout.read().decode()
        lines = output.split('\n')
        for line in lines:
            if line.strip().startswith("inet "):
                parts = line.split()
                if len(parts) >= 2:
                    ip_address = parts[1].split('/')[0]
                    net_info.append(ip_address)

        return net_info


    def get_remote_hostname(self):
        stdin, stdout, stderr = self.ssh_client.exec_command("hostname")
        return stdout.read().decode().strip()

    def plot_usage(self, cpu_percent, mem_percent, disk_percent):
        self.ax.clear()
        usage_labels = ['CPU', 'Memoria', 'Disco']
        usage_values = [cpu_percent, mem_percent, disk_percent]
        self.ax.bar(usage_labels, usage_values, color=['red', 'green', 'blue'])
        self.ax.set_ylim(0, 100)
        self.ax.set_ylabel('Porcentaje')
        self.ax.set_title('Uso del sistema')
        self.canvas.draw()


#--------------------------------------------------------GUi 1 actualizar

class TaskManager:
    def __init__(self):
        self.gui = TaskManagerGUI()
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.gui.main_frame)
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=6, padx=20, pady=20)
        self.gui.after(0, self.update_info)
        self.gui.mainloop()
        
        #correos variables
        self.email_sent = False  # Variable de control para verificar si se ha enviado un correo
        self.last_email_time = None  # Variable para almacenar el tiempo del último envío de correo
        self.timer_interval = 10  # Intervalo de tiempo en segundos para la verificación de recursos
        self.email_interval = 1800  # Intervalo de tiempo en segundos para el envío de correo (30 minutos)
    def update_info(self):
        hostname = socket.gethostname()
        cpu_percent = psutil.cpu_percent()
        mem_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent
        net_info = self.get_network_info()

        self.gui.update_info(hostname, cpu_percent, mem_percent, disk_percent, net_info)
        self.plot_usage(cpu_percent, mem_percent, disk_percent)
        self.gui.after(1000, self.update_info)

    def get_network_info(self):
        net_info = []

        net_if_addrs = psutil.net_if_addrs()
        for interface, addresses in net_if_addrs.items():
            for address in addresses:
                if address.family == socket.AF_INET:
                    net_info.append(f"{interface}: {address.address}")

        return net_info


    def plot_usage(self, cpu_percent, mem_percent, disk_percent):
        self.ax.clear()
        usage_labels = ['CPU', 'Memoria', 'Disco']
        usage_values = [cpu_percent, mem_percent, disk_percent]
        self.ax.bar(usage_labels, usage_values, color=['red', 'green', 'blue'])
        self.ax.set_ylim(0, 100)
        self.ax.set_ylabel('Porcentaje')
        self.ax.set_title('Uso del sistema')
        self.canvas.draw()
        
   
 #-------------------------------------------------------------Correos
    def enviar_correo(self, destinatario, asunto, mensaje):
        servidor_smtp = 'smtp.gmail.com'
        puerto_smtp = 587
        remitente = 'servidores146@gmail.com'
        contraseña = 'rpdxdwogotmxmvax'

        email = EmailMessage()
        email['Subject'] = asunto
        email['From'] = remitente
        email['To'] = destinatario
        email.set_content(mensaje)

        try:
            server = smtplib.SMTP(servidor_smtp, puerto_smtp)
            server.starttls()
            server.login(remitente, contraseña)

            server.send_message(email)
            server.quit()
            
            print("Correo enviado")
        except Exception as e:
            print("Error al enviar el correo:", str(e))


    def verificar_recursos_y_enviar_correos(self):
        self.update()
        # Umbrales
        umbral_cpu = 90
        umbral_memoria = 90
        umbral_disco = 90
        
        hostname = socket.gethostname()
        cpu_percent = psutil.cpu_percent()
        mem_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent


        self.gui.update_info(hostname, cpu_percent, mem_percent, disk_percent)
        self.plot_usage(cpu_percent, mem_percent, disk_percent)
	
        # Verificar si se ha enviado al menos un correo electrónico
        if self.email_sent:
            # Obtener el tiempo actual
            current_time = datetime.datetime.now()

            # Verificar si ha pasado media hora desde el último envío de correo
            if (current_time - self.last_email_time).seconds >= self.email_interval:
                # Realizar las verificaciones y enviar los correos electrónicos
                uso_cpu = self.obtener_uso_cpu()
                uso_memoria = self.obtener_uso_memoria()
                uso_disco = self.obtener_uso_disco()

                if uso_cpu > umbral_cpu:
                    destinatario = 'adriansanchezcotillas2000@gmail.com'
                    asunto = f'Alerta de uso de CPU en {hostname}'
                    mensaje = f'El uso de CPU ha alcanzado el {uso_cpu}%'
                    self.enviar_correo(destinatario, asunto, mensaje)

                if uso_memoria > umbral_memoria:
                    destinatario = 'adriansanchezcotillas2000@gmail.com'
                    asunto = f'Alerta de uso de memoria en {hostname}'
                    mensaje = f'El uso de memoria ha alcanzado el {uso_memoria}%'
                    self.enviar_correo(destinatario, asunto, mensaje)

                if uso_disco > umbral_disco:
                    destinatario = 'adriansanchezcotillas2000@gmail.com'
                    asunto = f'Alerta de uso de disco en {hostname}'
                    mensaje = f'El uso de disco ha alcanzado el {uso_disco}%'
                    self.enviar_correo(destinatario, asunto, mensaje)

                # Actualizar el tiempo del último envío de correo al tiempo actual
                self.last_email_time = current_time
        else:
            # Realizar las verificaciones y enviar el primer correo electrónico
            uso_cpu = self.obtener_uso_cpu()
            uso_memoria = self.obtener_uso_memoria()
            uso_disco = self.obtener_uso_disco()

            if uso_cpu > umbral_cpu:
                destinatario = 'adriansanchezcotillas2000@gmail.com'
                asunto = f'Alerta de uso de CPU en {hostname}'
                mensaje = f'El uso de CPU ha alcanzado el {uso_cpu}%'
                self.enviar_correo(destinatario, asunto, mensaje)

            if uso_memoria > umbral_memoria:
                destinatario = 'adriansanchezcotillas2000@gmail.com'
                asunto = f'Alerta de uso de memoria en {hostname}'
                mensaje = f'El uso de memoria ha alcanzado el {uso_memoria}%'
                self.enviar_correo(destinatario, asunto, mensaje)

            if uso_disco > umbral_disco:
                destinatario = 'adriansanchezcotillas2000@gmail.com'
                asunto = f'Alerta de uso de disco en {hostname}'
                mensaje = f'El uso de disco ha alcanzado el {uso_disco}%'
                self.enviar_correo(destinatario, asunto, mensaje)

            # Establecer la variable de control de correo enviado a True
            self.email_sent = True
            # Establecer el tiempo del último envío de correo al tiempo actual
            self.last_email_time = datetime.datetime.now()
            
    def iniciar_verificacion_recursos(self):
        while True:
            # Verificar recursos y enviar correos
            self.verificar_recursos_y_enviar_correos()

            # Pausar la ejecución por el intervalo de tiempo especificado
            time.sleep(self.timer_interval)
       
        

if __name__ == "__main__":
    TaskManager()

    
    
