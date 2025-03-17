# -*- coding: utf-8 -*-
import itertools
import argparse

def generate_passwords(org, years):
    org_variants = set([org, org.lower(), org.upper(), org.capitalize()])
    seasons = ["Primavera", "Verano", "Invierno", "Otoño"]
    common_words = ["Admin", "Secure", "Pass", "Password", "Clave", "Administrador", "root"]
    special_chars = ["!", "#", "*", "@"]
    passwords = set()
    
    # Generar variantes de common_words
    common_word_variants = set()
    for word in common_words:
        common_word_variants.update([word, word.lower(), word.upper(), word.capitalize()])
    
    for year in years:
        for org_var in org_variants:
            base_passwords = set([
                f"{org_var}{year}", f"{org_var}-{year}", f"{org_var}_{year}",
                f"{org_var}{year}123", f"{org_var}{year}789",
                f"{year}{org_var}", f"{year}-{org_var}"
            ])
            
            for char in special_chars:
                base_passwords.add(f"{org_var}{year}{char}")
            
            for word in common_word_variants:
                base_passwords.add(f"{org_var}{word}{year}")
            
            passwords.update(base_passwords)
            
            # Agregar combinaciones con caracteres especiales al final
            for pw in base_passwords:
                for i in range(1, len(special_chars) + 1):
                    for comb in itertools.combinations(special_chars, i):
                        passwords.add(f"{pw}{''.join(comb)}")
        
        for season in seasons:
            passwords.add(f"{season}{year}")
            for org_var in org_variants:
                passwords.add(f"{org_var}{season}{year}")
                passwords.add(f"{season}{org_var}{year}")
                
    return list(passwords)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generador de contraseñas basadas en organizaciones y años",
                                     epilog="# Ejemplo: python3 pass_generator.py -o mercadona supermercado -y 2023 2024 2025")
    parser.add_argument("-o", "--orgs", nargs="+", required=True, help="Lista de nombres de organizaciones (mercadona mediamarkt)")
    parser.add_argument("-y", "--years", nargs="+", required=True, help="Lista de años (2023 2024 2025)")
    
    args = parser.parse_args()
    
    for org_name in args.orgs:
        passwords = generate_passwords(org_name, args.years)
        for pw in passwords:
            print(pw)
