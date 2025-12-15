import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from main import ADFGVXCipher
from string import ascii_uppercase, digits


class CipherGUI:
    
    def __init__(self):
        self.cipher = ADFGVXCipher()
        self.root = tk.Tk()
        self.root.title("ADFG(V)X Šifra")
        self.root.geometry("1000x800")
        self.root.configure(bg='white')
        
        self.setup_ui()
    
    def setup_ui(self):
        # Hlavni frame
        main_frame = tk.Frame(self.root, bg='white', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ===== HORNI CAST - Nastaveni =====
        settings_frame = tk.LabelFrame(main_frame, text="Nastavení", bg='white', font=('Arial', 10, 'bold'))
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Prepinac ADFGX / ADFGVX
        cipher_frame = tk.Frame(settings_frame, bg='white')
        cipher_frame.pack(pady=5)
        
        tk.Label(cipher_frame, text="Typ šifry:", bg='white', font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        self.cipher_type_var = tk.StringVar(value="ADFGX")
        tk.Radiobutton(cipher_frame, text="ADFGX (5x5)", variable=self.cipher_type_var, value="ADFGX", 
                      bg='white', command=self.on_cipher_type_change).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(cipher_frame, text="ADFGVX (6x6)", variable=self.cipher_type_var, value="ADFGVX", 
                      bg='white', command=self.on_cipher_type_change).pack(side=tk.LEFT, padx=5)
        
        # Prepinac Nahodna / Rucni matice
        matrix_frame = tk.Frame(settings_frame, bg='white')
        matrix_frame.pack(pady=5)
        
        tk.Label(matrix_frame, text="Matice:", bg='white', font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        self.matrix_mode_var = tk.StringVar(value="random")
        tk.Radiobutton(matrix_frame, text="Náhodná", variable=self.matrix_mode_var, value="random", 
                      bg='white', command=self.on_matrix_mode_change).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(matrix_frame, text="Ruční zadání", variable=self.matrix_mode_var, value="manual", 
                      bg='white', command=self.on_matrix_mode_change).pack(side=tk.LEFT, padx=5)
        
        # Tlacitko pro generovani matice
        btn_frame = tk.Frame(settings_frame, bg='white')
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Generovat novou matici", command=self.generate_matrix, 
                 bg='white', relief=tk.RAISED, bd=2).pack()
        
        # ===== PROSTREDNI CAST - Matice a vstupy =====
        middle_frame = tk.Frame(main_frame, bg='white')
        middle_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Leva strana - Matice
        left_frame = tk.LabelFrame(middle_frame, text="Šifrovací matice", bg='white', font=('Arial', 10, 'bold'))
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Rucni zadani matice
        self.manual_frame = tk.Frame(left_frame, bg='white')
        self.manual_frame.pack(pady=10)
        
        self.matrix_entries = []
        self.create_matrix_entries()
        
        # Zbyvajici znaky
        self.remaining_label = tk.Label(left_frame, text="Zbývající znaky: ", bg='white', 
                                       font=('Arial', 9), wraplength=300, justify=tk.LEFT)
        self.remaining_label.pack(pady=5)
        
        # Zobrazeni matice
        self.matrix_display = tk.Text(left_frame, height=8, width=25, bg='white', 
                                     font=('Courier', 12), relief=tk.SUNKEN, bd=2)
        self.matrix_display.pack(pady=10)
        
        # Prava strana - Vstupy
        right_frame = tk.Frame(middle_frame, bg='white')
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Klic
        key_frame = tk.LabelFrame(right_frame, text="Klíčové slovo", bg='white', font=('Arial', 10, 'bold'))
        key_frame.pack(fill=tk.X, pady=(0, 10))
        self.key_entry = tk.Entry(key_frame, font=('Arial', 11), relief=tk.SUNKEN, bd=2)
        self.key_entry.pack(fill=tk.X, padx=10, pady=10)
        
        # Vstupni text
        input_frame = tk.LabelFrame(right_frame, text="Vstupní text", bg='white', font=('Arial', 10, 'bold'))
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.input_text = scrolledtext.ScrolledText(input_frame, height=6, font=('Arial', 10), 
                                                    relief=tk.SUNKEN, bd=2, wrap=tk.WORD)
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tlacitka
        button_frame = tk.Frame(right_frame, bg='white')
        button_frame.pack(fill=tk.X)
        tk.Button(button_frame, text="ŠIFROVAT", command=self.encrypt_text, 
                 bg='white', font=('Arial', 10, 'bold'), relief=tk.RAISED, bd=3, 
                 width=15).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(button_frame, text="DEŠIFROVAT", command=self.decrypt_text, 
                 bg='white', font=('Arial', 10, 'bold'), relief=tk.RAISED, bd=3, 
                 width=15).pack(side=tk.LEFT, padx=5, pady=5)
        
        # ===== DOLNI CAST - Vystupy =====
        output_frame = tk.LabelFrame(main_frame, text="Výstup", bg='white', font=('Arial', 10, 'bold'))
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        # Filtrovany text
        filtered_text_frame = tk.Frame(output_frame, bg='white')
        filtered_text_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(filtered_text_frame, text="Filtrovaný text:", bg='white', 
                font=('Arial', 9, 'bold')).pack(anchor=tk.W)
        self.filtered_text_display = tk.Text(filtered_text_frame, height=2, font=('Courier', 10), 
                                           relief=tk.SUNKEN, bd=2, wrap=tk.WORD)
        self.filtered_text_display.pack(fill=tk.X, pady=2)
        
        # Vysledny text
        result_frame = tk.Frame(output_frame, bg='white')
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        tk.Label(result_frame, text="Výsledný text:", bg='white', 
                font=('Arial', 9, 'bold')).pack(anchor=tk.W)
        self.output_text = scrolledtext.ScrolledText(result_frame, height=6, font=('Arial', 10), 
                                                     relief=tk.SUNKEN, bd=2, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=2)
        
        # Inicializace
        self.on_matrix_mode_change()
        self.generate_matrix()
    
    def create_matrix_entries(self):
        """Vytvori vstupni pole pro rucni zadani matice"""
        # Smazani starych entries
        for widget in self.manual_frame.winfo_children():
            widget.destroy()
        self.matrix_entries = []
        
        size = 5 if self.cipher_type_var.get() == "ADFGX" else 6
        chars = "ADFGX" if size == 5 else "ADFGVX"
        
        # Hlavicka sloupcu
        tk.Label(self.manual_frame, text="  ", bg='white', font=('Arial', 9)).grid(row=0, column=0)
        for i in range(size):
            tk.Label(self.manual_frame, text=chars[i], bg='white', 
                    font=('Arial', 9, 'bold')).grid(row=0, column=i+1, padx=2)
        
        # Radky s entries
        for i in range(size):
            tk.Label(self.manual_frame, text=chars[i], bg='white', 
                    font=('Arial', 9, 'bold')).grid(row=i+1, column=0, padx=5)
            row_entries = []
            for j in range(size):
                entry = tk.Entry(self.manual_frame, width=3, font=('Arial', 11), 
                               justify=tk.CENTER, relief=tk.SUNKEN, bd=2)
                entry.grid(row=i+1, column=j+1, padx=2, pady=2)
                entry.bind('<KeyRelease>', self.on_manual_entry_change)
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)
    
    def on_cipher_type_change(self):
        """Zmena typu sifry"""
        self.create_matrix_entries()
        self.generate_matrix()
    
    def on_matrix_mode_change(self):
        """Zmena rezimu matice"""
        if self.matrix_mode_var.get() == "manual":
            # Zobrazit rucni zadani
            self.manual_frame.pack(pady=10)
            self.update_remaining_chars()
        else:
            # Skryt rucni zadani
            self.manual_frame.pack_forget()
            self.remaining_label.config(text="Zbývající znaky: ")
    
    def on_manual_entry_change(self, event=None):
        """Zmena v rucnim zadani matice"""
        self.update_remaining_chars()
        self.update_matrix_from_entries()
    
    def update_remaining_chars(self):
        """Aktualizace zbyvajicich znaku"""
        used_chars = []
        for row in self.matrix_entries:
            for entry in row:
                char = entry.get().upper()
                if char:
                    used_chars.append(char)
        
        size = 5 if self.cipher_type_var.get() == "ADFGX" else 6
        self.cipher.cipher_type = self.cipher_type_var.get()
        remaining = self.cipher.get_remaining_chars(used_chars)
        
        self.remaining_label.config(text=f"Zbývající znaky: {' '.join(remaining)}")
    
    def update_matrix_from_entries(self):
        """Aktualizace matice z rucniho zadani"""
        size = len(self.matrix_entries)
        matrix = []
        for row in self.matrix_entries:
            matrix_row = []
            for entry in row:
                char = entry.get().upper()
                if char:
                    matrix_row.append(char)
                else:
                    matrix_row.append(' ')
            matrix.append(matrix_row)
        
        self.cipher.grid = matrix
        self.cipher.cipher_type = self.cipher_type_var.get()
        self.display_matrix()
    
    def generate_matrix(self):
        """Generuje novou matici"""
        cipher_type = self.cipher_type_var.get()
        
        if self.matrix_mode_var.get() == "random":
            # Nahodna matice
            if cipher_type == "ADFGX":
                self.cipher.gen_grid_adfgx()
            else:
                self.cipher.gen_grid_adfgvx()
            
            self.display_matrix()
        else:
            # Rucni matice - generujeme a vyplnime entries
            if cipher_type == "ADFGX":
                self.cipher.gen_grid_adfgx()
            else:
                self.cipher.gen_grid_adfgvx()
            
            # Vyplnime entries
            for i, row in enumerate(self.cipher.grid):
                for j, char in enumerate(row):
                    self.matrix_entries[i][j].delete(0, tk.END)
                    self.matrix_entries[i][j].insert(0, char)
            
            self.display_matrix()
            self.update_remaining_chars()
    
    def display_matrix(self):
        """Zobrazi matici"""
        self.matrix_display.delete(1.0, tk.END)
        matrix_text = self.cipher.format_grid()
        self.matrix_display.insert(1.0, matrix_text)
        self.matrix_display.config(state=tk.NORMAL)
    
    def encrypt_text(self):
        """Sifrovani textu"""
        text = self.input_text.get(1.0, tk.END).strip()
        key = self.key_entry.get().strip()
        
        if not text:
            messagebox.showwarning("Varování", "Zadejte text pro šifrování!")
            return
        
        if not key:
            messagebox.showwarning("Varování", "Zadejte klíčové slovo!")
            return
        
        if not self.cipher.grid:
            messagebox.showwarning("Varování", "Vygenerujte nejprve matici!")
            return
        
        # Kontrola kompletnosti matice pri rucnim zadani
        if self.matrix_mode_var.get() == "manual":
            alphabet = self.cipher.get_grid_as_string()
            if ' ' in alphabet:
                messagebox.showwarning("Varování", "Matice není kompletně vyplněná!")
                return
        
        try:
            cipher_type = self.cipher_type_var.get()
            alphabet = self.cipher.get_grid_as_string()
            
            if cipher_type == "ADFGX":
                encrypted = self.cipher.encrypt_adfgx(text, key, alphabet)
            else:
                encrypted = self.cipher.encrypt_adfgvx(text, key, alphabet)
            
            # Zobrazeni filtrovaneho textu
            self.filtered_text_display.delete(1.0, tk.END)
            filtered_text = self.cipher.filter_text(text)
            self.filtered_text_display.insert(1.0, filtered_text)
            
            # Zobrazeni vysledku
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, encrypted)
            
        except Exception as e:
            messagebox.showerror("Chyba", f"Chyba při šifrování: {str(e)}")
    
    def decrypt_text(self):
        """Desifrovani textu"""
        text = self.input_text.get(1.0, tk.END).strip()
        key = self.key_entry.get().strip()
        
        if not text:
            messagebox.showwarning("Varování", "Zadejte text pro dešifrování!")
            return
        
        if not key:
            messagebox.showwarning("Varování", "Zadejte klíčové slovo!")
            return
        
        if not self.cipher.grid:
            messagebox.showwarning("Varování", "Vygenerujte nejprve matici!")
            return
        
        try:
            cipher_type = self.cipher_type_var.get()
            alphabet = self.cipher.get_grid_as_string()
            
            if cipher_type == "ADFGX":
                decrypted = self.cipher.decrypt_adfgx(text, key, alphabet)
            else:
                decrypted = self.cipher.decrypt_adfgvx(text, key, alphabet)
            
            # Zobrazeni vysledku
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, decrypted)
            
            # Vymazani filtrovaneho textu pri desifrovani
            self.filtered_text_display.delete(1.0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Chyba", f"Chyba při dešifrování: {str(e)}")
    
    def run(self):
        """Spusti GUI"""
        self.root.mainloop()