# Import library yang diperlukan
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import random

# Definisikan kelas TebakanGame
class TebakanGame:
    def __init__(self, master):
        # Inisialisasi objek TebakanGame.
        # Parameters:
        #     master (tk.Tk): Objek utama Tkinter sebagai master window.
        self.master = master
        self.master.title("Guess The Number") # Judul jendela

        # Gaya tombol dan latar belakang
        self.button_color = "#507590" #Warna latar belakang tombol.
        self.hover_color = "#28495c" #Warna latar belakang tombol saat di-hover.
        self.font_style = ('Open Sans', 12) #Gaya font yang digunakan pada elemen GUI.
        
        # Load dan tampilkan gambar latar belakang
        image_path = r"login_bg.png"
        self.load_and_display_image(image_path)

        # Set the background color and style for transparency
        self.master.tk_setPalette(background='#b8d3e1')
        style = ttk.Style(self.master)

        # Create a transparent label style
        style.element_create("Transparent.TLabel", "from", "default")
        style.layout("Transparent.TLabel", [("Transparent.TLabel", {"sticky": "news"})])
        style.configure("Transparent.TLabel", background="#b8d3e1")

        # Menampilkan label dan entry untuk memasukkan batas angka
        tk.Label(self.master, text="Masukkan batas angka", font=('Open Sans', 18),bg='#b8d3e1').pack(pady=20)
        self.entry = tk.Entry(self.master, font=('Open Sans', 15), )
        self.entry.pack(pady=10)
        

        # Menambahkan event binding untuk tombol Enter
        self.entry.bind("<Return>", lambda event: self.start_game())
        
        # Menangani penutupan jendela
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Menampilkan tombol untuk memulai game
        self.start_button = tk.Button(self.master, text="Mulai Game", command=self.start_game, font=('Open Sans', 15), bg=self.button_color)
        self.start_button.pack(pady=15)

        # Membuat Event binding untuk efek hover pada tombol (akan menjadi beda warna)
        self.start_button.bind("<Enter>", lambda event: self.on_hover(event, self.hover_color))  # Set hover background color to a slightly different shade of green
        self.start_button.bind("<Leave>", lambda event: self.on_hover(event, self.button_color))  # Set back to the original background color


        # Inisialisasi variabel untuk permainan
        self.random_number = 0
        self.attempts = 0

    
    # Metode ini digunakan untuk mengubah warna tombol saat di-hover
    def on_hover(self, event, color):
        # Objek event Tkinter yang dipicu.
        # Warna yang akan diatur pada tombol.
        event.widget.config(bg=color)

    
    # Metode untuk memuat dan menampilkan gambar latar belakang.
    def load_and_display_image(self, image_path):
        # memuat gambar dari file lokal menggunakan PIL
        image = Image.open(image_path) #Path gambar latar belakang.
        image = ImageTk.PhotoImage(image)

        # Tampilkan gambar menggunakan Label dan meletakan di latar belakang
        label = tk.Label(self.master, image=image)
        label.image = image  # Keep a reference to avoid garbage collection
        label.place(relwidth=1, relheight=1)

    def start_game(self):
        # Memulai permainan dengan mengambil input batas angka dari pengguna
        # dan melakukan iterasi hingga tebakan benar.
        try:
            # Mengambil batas angka dari input pengguna
            batas_atas = int(self.entry.get())
            if batas_atas < 0:
                messagebox.showerror("Error", "Masukkan bilangan positif.")
                return
            if batas_atas < 2:
                messagebox.showerror("Error", "Masukkan angka batas yang lebih besar dari 1.")
                return

            # Perintah untuk mengacak angka target
            self.random_number = random.randint(1, batas_atas)
            self.attempts = 0

            # Melakukan iterasi hingga tebakan benar
            game_over = False
            while not game_over:
                tebakan = self.get_guess(batas_atas)
                self.attempts += 1
                game_over = self.update_feedback(tebakan)

            self.display_results()



        # Menangani kesalahan jika input tidak valid
        except ValueError:
            messagebox.showerror("Error", "Masukkan karakter yang sesuai.")

    def get_guess(self, batas_atas):
        # Meminta tebakan dari pengguna dengan penanganan kesalahan.
        # Parameters:
        #     batas_atas (int): Batas atas angka yang dapat ditebak.
        # Returns:
        #     int: Tebakan yang valid dari pengguna.
        while True:
            try:
                tebakan = int(simpledialog.askstring("Tebakan", f'Tebak angka antara 1 sampai {batas_atas}'))
                if tebakan <= 0:
                    messagebox.showerror("Error", "Masukkan angka di atas 0.")
                elif tebakan > batas_atas:
                    messagebox.showerror("Error", f'Tebakan anda terlalu besar. Tebak angka antara 1 sampai {batas_atas}.')
                else:
                    return tebakan
            except ValueError:
                # Menangani kesalahan jika input bukan angka
                messagebox.showerror("Error", "Masukkan karakter yang sesuai.")

    def update_feedback(self, tebakan):

        # Menampilkan umpan balik berdasarkan tebakan pengguna.

        # Parameters:
        #     tebakan (int): Tebakan pengguna.
        if tebakan < self.random_number:
            messagebox.showinfo("Coba Lagi!", "Tebakan anda terlalu rendah, Tebak lagi")
        elif tebakan > self.random_number:
            messagebox.showinfo("Coba Lagi!", "Tebakan anda terlalu tinggi, Tebak lagi")  
        else:
            return True  # Game is over because the guess is correct
        return False  # Game is still ongoing
       

    def display_results(self):
        # Menampilkan hasil tebakan setelah permainan selesai
        messagebox.showinfo("Selamat!!", f'Tebakan anda benar!\n Angka yang benar adalah {self.random_number}.\n Jumlah percobaan: {self.attempts}')

        # Mengatur ulang elemen-elemen untuk permainan baru
        self.entry.delete(0, tk.END)
        self.entry.focus_set()

    def on_closing(self):
        if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar?"):
            self.master.destroy()



if __name__ == "__main__":
    # Membuat instance Tkinter
    root = tk.Tk()
    app = TebakanGame(root)

    # Menentukan ukuran jendela
    root.geometry("300x200")

    # # untuk tidak bisa di perbesar atau di perkecil
    root.resizable(False, False)

    # Memulai loop utama Tkinter
    root.mainloop()
