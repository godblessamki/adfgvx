import re
from random import shuffle
from string import digits, ascii_uppercase


class ADFGVXCipher:
    
    def __init__(self):
        self.adfgx_chars = "ADFGX"
        self.adfgvx_chars = "ADFGVX"
        self.grid = None
        self.key = None
        self.first_cipher = None
        self.cipher_type = None  # 'ADFGX' or 'ADFGVX'
        
        # Diakriticka mapa pro ceske znaky
        self.DIACRITIC_MAP = {
            'Á': 'A', 'á': 'A', 'Č': 'C', 'č': 'C', 'Ď': 'D', 'ď': 'D',
            'É': 'E', 'é': 'E', 'Ě': 'E', 'ě': 'E', 'Í': 'I', 'í': 'I',
            'Ň': 'N', 'ň': 'N', 'Ó': 'O', 'ó': 'O', 'Ř': 'R', 'ř': 'R',
            'Š': 'S', 'š': 'S', 'Ť': 'T', 'ť': 'T', 'Ú': 'U', 'ú': 'U',
            'Ů': 'U', 'ů': 'U', 'Ý': 'Y', 'ý': 'Y', 'Ž': 'Z', 'ž': 'Z',
        }
    
    def filter_text(self, text):
        """
        Filtruje vstupni text (s logikou z Playfair sifry) - 
        prevede diakritiku, odstrani mezery a kompletně vymaze specialni znaky.
        Zachovava pouze PISMENA a CISLICE.
        """
        filtered = []
        
        for char in text:
            # 1. Zpracování mezer (ty se nešifrují a nemají se ani ukládat)
            if char == ' ':
                continue  # Mezera je ignorována (vymazána)
            
            # 2. Vypuštění speciálních znaků
            # Kontroluje, zda se jedná o písmeno nebo číslici, jinak přeskočí.
            if not char.isalnum(): 
                continue # Znak není alfanumerický, je ignorován a smazán
            
            # 3. Převod diakritiky
            if char in self.DIACRITIC_MAP:
                char = self.DIACRITIC_MAP[char]
            
            # 4. Převod na velká písmena
            char = char.upper()
            
            # 5. Nahrazení J -> I (kvůli 5x5 matici ADFGX)
            if char == 'J':
                char = 'I'
            
            # 6. Přidání platného znaku (písmena/číslice)
            filtered.append(char)
        
        return ''.join(filtered)
    def gen_grid_adfgx(self, custom_alphabet=None):
        """Generuje 5x5 mrizku pro ADFGX (bez J)"""
        if custom_alphabet:
            chars = list(custom_alphabet)
        else:
            chars = list(ascii_uppercase.replace('J', ''))
            shuffle(chars)
        
        self.grid = [chars[0:5], chars[5:10], chars[10:15], chars[15:20], chars[20:25]]
        self.cipher_type = 'ADFGX'
        return self.grid
    
    def gen_grid_adfgvx(self, custom_alphabet=None):
        """Generuje 6x6 mrizku pro ADFGVX (A-Z + 0-9)"""
        if custom_alphabet:
            chars = list(custom_alphabet)
        else:
            chars = list(ascii_uppercase + digits)
            shuffle(chars)
        
        self.grid = [chars[0:6], chars[6:12], chars[12:18], chars[18:24], chars[24:30], chars[30:36]]
        self.cipher_type = 'ADFGVX'
        return self.grid
    
    def find_val(self, value):
        """Hleda hodnotu v mrizce a vraci jeji souradnice"""
        for row_num, row in enumerate(self.grid):
            for col_num, element in enumerate(row):
                if element == value:
                    return (row_num, col_num)
        return None
    
    def num_to_char(self, number):
        """Prevadi cislo (souradnice) na odpovidajici pismeno"""
        chars = self.adfgx_chars if self.cipher_type == 'ADFGX' else self.adfgvx_chars
        if 0 <= number < len(chars):
            return chars[number]
        else:
            raise ValueError('Cislo mimo rozsah')
    
    def gen_first_cipher(self, msg):
        """Vytvori prvni sifrovy text z mrizky"""
        # Filtrace textu
        filtered_msg = self.filter_text(msg)
        
        # Odstraneni mezer pro sifrovani
        filtered_msg_no_space = filtered_msg.replace(' ', '')
        
        self.first_cipher = ""
        
        for char in filtered_msg_no_space:
            coords = self.find_val(char)
            if coords:
                row, col = map(self.num_to_char, coords)
                self.first_cipher = self.first_cipher + row + col
        
        return self.first_cipher
    
    def transpose_with_key(self, input_key):
        """Transpozice pomoci klicoveho slova"""
        first_cipher_list = list(self.first_cipher)
        self.key = self.filter_text(input_key).replace(' ', '')
        
        # Vytvoreni keyword mrizky
        keyword_grid = [first_cipher_list[i:i+len(self.key)] for i in range(0, len(first_cipher_list), len(self.key))]
        
        # Doplneni posledniho radku
        if keyword_grid and len(keyword_grid[-1]) < len(self.key):
            keyword_grid[-1].extend(['X'] * (len(self.key) - len(keyword_grid[-1])))
        
        # Serazeni podle klice
        indices = sorted(range(len(self.key)), key=lambda i: self.key[i])
        
        # Serazeni sloupcu
        keyword_grid_sorted = [[row[i] for i in indices] for row in keyword_grid]
        
        # Cteni po sloupcich
        final_cipher_temp = [[row[col] for row in keyword_grid_sorted] for col in range(len(keyword_grid_sorted[0]))]
        
        # Zplošteni a spojeni
        final_cipher = [item for sublist in final_cipher_temp for item in sublist]
        final_cipher = "".join(final_cipher)
        
        return final_cipher
    
    def encrypt_adfgx(self, msg, key, custom_alphabet=None):
        """ADFGX sifrovani"""
        self.gen_grid_adfgx(custom_alphabet)
        self.gen_first_cipher(msg)
        encrypted = self.transpose_with_key(key)
        return encrypted
    
    def encrypt_adfgvx(self, msg, key, custom_alphabet=None):
        """ADFGVX sifrovani"""
        self.gen_grid_adfgvx(custom_alphabet)
        self.gen_first_cipher(msg)
        encrypted = self.transpose_with_key(key)
        return encrypted
    
    def reverse_transpose(self, encrypted_text, key):
        """Inverzni transpozice"""
        key = self.filter_text(key).replace(' ', '')
        key_length = len(key)
        text_length = len(encrypted_text)
        num_rows = (text_length + key_length - 1) // key_length
        
        # Serazeni klice
        indices = sorted(range(len(key)), key=lambda i: key[i])
        
        # Vypocet delky sloupcu
        full_cols = text_length % key_length
        if full_cols == 0:
            full_cols = key_length
        
        # Rekonstrukce sloupcu
        columns = {}
        pos = 0
        for idx in indices:
            if idx < full_cols:
                col_length = num_rows
            else:
                col_length = num_rows - 1
            
            columns[idx] = list(encrypted_text[pos:pos+col_length])
            pos += col_length
        
        # Cteni po radcich
        result = []
        for row in range(num_rows):
            for col in range(key_length):
                if col in columns and row < len(columns[col]):
                    result.append(columns[col][row])
        
        return ''.join(result)
    
    def decode_pairs(self, decoded_text):
        """Prevod dvojic znaku zpet na pismena"""
        chars = self.adfgx_chars if self.cipher_type == 'ADFGX' else self.adfgvx_chars
        result = []
        i = 0
        
        while i < len(decoded_text):
            if i + 1 < len(decoded_text):
                pair = decoded_text[i:i+2]
                if pair[0] in chars and pair[1] in chars:
                    row = chars.index(pair[0])
                    col = chars.index(pair[1])
                    if row < len(self.grid) and col < len(self.grid[row]):
                        result.append(self.grid[row][col])
                i += 2
            else:
                i += 1
        
        return ''.join(result)
    
    def decrypt_adfgx(self, encrypted_text, key, alphabet):
        """ADFGX desifrovani"""
        self.cipher_type = 'ADFGX'
        self.grid = [list(alphabet[i:i+5]) for i in range(0, 25, 5)]
        
        decoded = self.reverse_transpose(encrypted_text, key)
        decrypted = self.decode_pairs(decoded)
        
        return decrypted
    
    def decrypt_adfgvx(self, encrypted_text, key, alphabet):
        """ADFGVX desifrovani"""
        self.cipher_type = 'ADFGVX'
        self.grid = [list(alphabet[i:i+6]) for i in range(0, 36, 6)]
        
        decoded = self.reverse_transpose(encrypted_text, key)
        decrypted = self.decode_pairs(decoded)
        
        return decrypted
    
    def format_grid(self):
        """Vraci mrizku jako string"""
        if not self.grid:
            return ""
        
        chars = self.adfgx_chars if self.cipher_type == 'ADFGX' else self.adfgvx_chars
        size = len(self.grid)
        
        result = "  " + " ".join(chars[:size]) + "\n"
        for i, row in enumerate(self.grid):
            result += chars[i] + " " + " ".join(row) + "\n"
        
        return result
    
    def get_grid(self):
        """Vraci aktualni mrizku"""
        return self.grid
    
    def get_grid_as_string(self):
        """Vraci mrizku jako jeden retezec"""
        if not self.grid:
            return ""
        return ''.join([''.join(row) for row in self.grid])
    
    def get_key(self):
        """Vraci aktualni klic"""
        return self.key
    
    def get_first_cipher(self):
        """Vraci prvni sifrovy text (pred transpozici)"""
        return self.first_cipher
    
    def get_remaining_chars(self, used_chars):
        """Vraci zbyvajici znaky pro rucni vyplnovani mrizky"""
        if self.cipher_type == 'ADFGX':
            all_chars = set(ascii_uppercase.replace('J', ''))
        else:
            all_chars = set(ascii_uppercase + digits)
        
        return sorted(list(all_chars - set(used_chars)))


# Spusteni aplikace
if __name__ == "__main__":
    from gui import CipherGUI
    app = CipherGUI()
    app.run()