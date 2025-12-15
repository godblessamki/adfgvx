import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
# Předpokládáme, že 'from main import ADFGVXCipher' je funkční
from main import ADFGVXCipher  
from string import ascii_uppercase, digits

# Nastavení barev pro Dark Mode (pro konzistentnost, i když ttk je lepší)
BG_MAIN = '#2E2E2E'   # Tmavě šedé pozadí
BG_FRAME = '#3C3C3C'  # Tmavší šedé pozadí pro rámečky
FG_TEXT = '#F0F0F0'   # Světlý text
FG_LABEL = '#FFFFFF'  # Bílý text pro nadpisy
INPUT_BG = '#4A4A4A'  # Tmavé pozadí pro vstupní pole
BUTTON_COLOR = '#5A5A5A' # Tmavší tlačítka


class CipherGUI:
    
    def __init__(self):
        self.cipher = ADFGVXCipher()
        self.root = tk.Tk()
        self.root.title("ADFG(V)X Šifra")
        self.root.geometry("1000x800")
        
        # Nastavení ttk stylu
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')  # 'clam' je dobrý základ pro úpravy
        
        # Definice vlastního stylu pro tmavé pozadí
        self.style.configure('TFrame', background=BG_MAIN)
        self.style.configure('TLabelframe', background=BG_MAIN, foreground=FG_LABEL)
        self.style.configure('TLabelframe.Label', background=BG_MAIN, foreground=FG_LABEL, font=('Arial', 10, 'bold'))
        self.style.configure('TLabel', background=BG_MAIN, foreground=FG_TEXT)
        self.style.configure('TRadiobutton', background=BG_MAIN, foreground=FG_TEXT)
        self.style.map('TRadiobutton', background=[('active', BG_FRAME)])
        self.style.configure('TButton', background=BUTTON_COLOR, foreground=FG_TEXT, font=('Arial', 10, 'bold'))
        self.style.map('TButton', background=[('active', '#6E6E6E')])
        
        # Hlavní okno s tmavým pozadím
        self.root.configure(bg=BG_MAIN)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Hlavni frame
        main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ===== HORNI CAST - Nastaveni =====
        settings_frame = ttk.LabelFrame(main_frame, text="Nastavení")
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Prepinac ADFGX / ADFGVX
        cipher_frame = ttk.Frame(settings_frame)
        cipher_frame.pack(pady=5)
        
        ttk.Label(cipher_frame, text="Typ šifry:").pack(side=tk.LEFT, padx=5)
        self.cipher_type_var = tk.StringVar(value="ADFGX")
        ttk.Radiobutton(cipher_frame, text="ADFGX (5x5)", variable=self.cipher_type_var, value="ADFGX", 
                      command=self.on_cipher_type_change).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(cipher_frame, text="ADFGVX (6x6)", variable=self.cipher_type_var, value="ADFGVX", 
                      command=self.on_cipher_type_change).pack(side=tk.LEFT, padx=5)
        
        # Prepinac Nahodna / Rucni matice
        matrix_mode_frame = ttk.Frame(settings_frame)
        matrix_mode_frame.pack(pady=5)
        
        ttk.Label(matrix_mode_frame, text="Matice:").pack(side=tk.LEFT, padx=5)
        self.matrix_mode_var = tk.StringVar(value="random")
        ttk.Radiobutton(matrix_mode_frame, text="Náhodná", variable=self.matrix_mode_var, value="random", 
                      command=self.on_matrix_mode_change).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(matrix_mode_frame, text="Ruční zadání", variable=self.matrix_mode_var, value="manual", 
                      command=self.on_matrix_mode_change).pack(side=tk.LEFT, padx=5)
        
        # Tlacitko pro generovani matice
        btn_frame = ttk.Frame(settings_frame)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Generovat novou matici", command=self.generate_matrix).pack()
        
        # ===== PROSTREDNI CAST - Matice a vstupy =====
        middle_frame = ttk.Frame(main_frame)
        middle_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Leva strana - Matice
        left_frame = ttk.LabelFrame(middle_frame, text="Šifrovací matice")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Rucni zadani matice
        self.manual_frame = ttk.Frame(left_frame)
        self.manual_frame.pack(pady=10)
        
        self.matrix_entries = []
        self.create_matrix_entries()
        
        # Zbyvajici znaky
        self.remaining_label = ttk.Label(left_frame, text="Zbývající znaky: ", wraplength=300, justify=tk.LEFT)
        self.remaining_label.pack(pady=5)
        
        # Zobrazeni matice
        self.matrix_display = tk.Text(left_frame, height=8, width=25, 
                                     font=('Courier', 12), relief=tk.FLAT, bd=2,
                                     bg=INPUT_BG, fg=FG_TEXT, insertbackground=FG_TEXT) # Nastaveni tmavých barev
        self.matrix_display.pack(pady=10, padx=10)
        
        # Prava strana - Vstupy
        right_frame = ttk.Frame(middle_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Klic
        key_frame = ttk.LabelFrame(right_frame, text="Klíčové slovo")
        key_frame.pack(fill=tk.X, pady=(0, 10))
        self.key_entry = tk.Entry(key_frame, font=('Arial', 11), relief=tk.FLAT, bd=2,
                                 bg=INPUT_BG, fg=FG_TEXT, insertbackground=FG_TEXT) # Nastaveni tmavých barev
        self.key_entry.pack(fill=tk.X, padx=10, pady=10)
        self.key_entry.insert(0, "heslo")
        
        # Vstupni text
        input_frame = ttk.LabelFrame(right_frame, text="Vstupní text")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.input_text = scrolledtext.ScrolledText(input_frame, height=6, font=('Arial', 10), 
                                                    relief=tk.FLAT, bd=2, wrap=tk.WORD,
                                                    bg=INPUT_BG, fg=FG_TEXT, insertbackground=FG_TEXT)
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.input_text.insert("1.0", "útok na čeňka 123! @#$°")
        
        # Tlacitka
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill=tk.X)
        ttk.Button(button_frame, text="ŠIFROVAT", command=self.encrypt_text).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(button_frame, text="DEŠIFROVAT", command=self.decrypt_text).pack(side=tk.LEFT, padx=5, pady=5)
        
        # ===== DOLNI CAST - Vystupy =====
        output_frame = ttk.LabelFrame(main_frame, text="Výstup")
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        # Filtrovany text
        filtered_text_frame = ttk.Frame(output_frame)
        filtered_text_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(filtered_text_frame, text="Filtrovaný text:", font=('Arial', 9, 'bold')).pack(anchor=tk.W)
        self.filtered_text_display = tk.Text(filtered_text_frame, height=2, font=('Courier', 10), 
                                           relief=tk.FLAT, bd=2, wrap=tk.WORD,
                                           bg=INPUT_BG, fg=FG_TEXT, insertbackground=FG_TEXT)
        self.filtered_text_display.pack(fill=tk.X, pady=2)
        
        # Vysledny text
        result_frame = ttk.Frame(output_frame)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        ttk.Label(result_frame, text="Výsledný text:", font=('Arial', 9, 'bold')).pack(anchor=tk.W)
        self.output_text = scrolledtext.ScrolledText(result_frame, height=6, font=('Arial', 10), 
                                                     relief=tk.FLAT, bd=2, wrap=tk.WORD,
                                                     bg=INPUT_BG, fg=FG_TEXT, insertbackground=FG_TEXT)
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
        ttk.Label(self.manual_frame, text="  ", foreground=FG_TEXT).grid(row=0, column=0)
        for i in range(size):
            ttk.Label(self.manual_frame, text=chars[i], font=('Arial', 9, 'bold'), 
                      foreground=FG_TEXT).grid(row=0, column=i+1, padx=2)
        
        # Radky s entries
        for i in range(size):
            ttk.Label(self.manual_frame, text=chars[i], font=('Arial', 9, 'bold'), 
                      foreground=FG_TEXT).grid(row=i+1, column=0, padx=5)
            row_entries = []
            for j in range(size):
                # Použití tk.Entry, protože ttk.Entry je pro 1 znak nepraktické, 
                # ale s nastavením tmavých barev
                entry = tk.Entry(self.manual_frame, width=3, font=('Arial', 11), 
                               justify=tk.CENTER, relief=tk.FLAT, bd=2,
                               bg=INPUT_BG, fg=FG_TEXT, insertbackground=FG_TEXT)
                entry.grid(row=i+1, column=j+1, padx=2, pady=2)
                entry.bind('<KeyRelease>', self.on_manual_entry_change)
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)
    
    # ... zbytek metod je stejný ...
    
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
        # Předpokládáme, že self.cipher má metodu get_remaining_chars
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
        # Předpokládáme, že self.cipher má metodu format_grid()
        matrix_text = self.cipher.format_grid() 
        self.matrix_display.insert(1.0, matrix_text)
        self.matrix_display.config(state=tk.DISABLED) # Změněno na DISABLED, protože by neměla být editovatelná
    
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
            alphabet = self.cipher.get_grid_as_string() # Předpokládáme existenci metody
            if ' ' in alphabet:
                messagebox.showwarning("Varování", "Matice není kompletně vyplněná!")
                return
        
        try:
            cipher_type = self.cipher_type_var.get()
            alphabet = self.cipher.get_grid_as_string()
            
            # Předpokládáme existenci a funkčnost metod
            if cipher_type == "ADFGX":
                encrypted = self.cipher.encrypt_adfgx(text, key, alphabet)
            else:
                encrypted = self.cipher.encrypt_adfgvx(text, key, alphabet)
            
            # Zobrazeni filtrovaneho textu
            self.filtered_text_display.config(state=tk.NORMAL)
            self.filtered_text_display.delete(1.0, tk.END)
            # Předpokládáme existenci metody
            filtered_text = self.cipher.filter_text(text) 
            self.filtered_text_display.insert(1.0, filtered_text)
            self.filtered_text_display.config(state=tk.DISABLED)
            
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
            
            # Předpokládáme existenci a funkčnost metod
            if cipher_type == "ADFGX":
                decrypted = self.cipher.decrypt_adfgx(text, key, alphabet)
            else:
                decrypted = self.cipher.decrypt_adfgvx(text, key, alphabet)
            
            # Zobrazeni vysledku
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, decrypted)
            
            # Vymazani filtrovaneho textu pri desifrovani
            self.filtered_text_display.config(state=tk.NORMAL)
            self.filtered_text_display.delete(1.0, tk.END)
            self.filtered_text_display.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Chyba", f"Chyba při dešifrování: {str(e)}")
    
    def run(self):
        """Spusti GUI"""
        self.root.mainloop()

# Spuštění GUI by vypadalo takto (pokud by byl kód mimo třídu):
# if __name__ == '__main__':
#     # Pro účely testování je potřeba funkční ADFGVXCipher
#     # Příklad:
#     # class DummyCipher:
#     #    ... implementace metod pro testování ...
#     # ADFGVXCipher = DummyCipher 
#     app = CipherGUI()
#     app.run()