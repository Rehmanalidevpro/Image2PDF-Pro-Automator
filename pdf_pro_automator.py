import os
import sys
import subprocess
import re
import time

# --- Part 1: Smart Library Manager ---
def manage_libs(action="install"):
    libs = ["colorama", "Pillow"]
    
    if action == "install":
        print("\n[!] Kuch libraries missing hain.")
        print("1. Sab ek sath install karein (Fast)")
        print("2. Ek ek karke install karein (Manual)")
        choice = input("Option select karein (1/2): ")

        if choice == "1":
            for lib in libs:
                subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
        else:
            for lib in libs:
                confirm = input(f"Kya {lib} install karni hai? (y/n): ")
                if confirm.lower() == 'y':
                    subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
        
        print("\n[+] Sab taiyar hai! Script restart ho rahi hai...")
        time.sleep(2)
        os.execl(sys.executable, sys.executable, *sys.argv)

    elif action == "uninstall":
        print("\n[!] Libraries remove ki ja rahi hain...")
        for lib in libs:
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", lib])
        print("[+] Libraries cleaned up!")

# Check if libs are here
try:
    from colorama import Fore, Style, init
    from PIL import Image, ImageDraw, ImageFont
    init(autoreset=True)
except ImportError:
    manage_libs("install")

# --- Part 2: UI & Banner ---
def show_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + Style.BRIGHT + "============================================================")
    print(Fore.YELLOW + Style.BRIGHT + "            REHMAN ALI'S SMART PDF MAKER PRO")
    print(Fore.CYAN + Style.BRIGHT + "============================================================")
    print(Fore.WHITE + " DESCRIPTION:")
    print(" This tool converts numbered images (1.jpg, 2.jpg...) into a")
    print(" single PDF and adds automatic page numbers at the bottom.")
    print(Fore.GREEN + "\n HOW TO USE:")
    print(" 1. Images ka name numbering mein rakho (e.g., 1.jpg, 2.jpg)")
    print(" 2. Folder ka path copy karke yahan paste karo.")
    print(" 3. PDF ka naam rakho aur Output folder check karo.")
    print(Fore.CYAN + "============================================================\n")

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

# --- Part 3: Core Logic ---
def create_pdf():
    show_banner()
    
    # Path mangna
    path = input(Fore.YELLOW + "Step 1: Images folder ka path dein: ").strip('"').strip("'")
    
    if not os.path.exists(path):
        print(Fore.RED + "[Error] Path galat hai yar!")
        return

    # Image files filter karna
    valid_exts = ('.jpg', '.jpeg', '.png', '.bmp')
    files = [f for f in os.listdir(path) if f.lower().endswith(valid_exts)]
    
    if not files:
        print(Fore.RED + "[Error] Is folder mein koi images nahi mili!")
        return

    # Verification of numbering
    files.sort(key=natural_sort_key)
    incorrect = [f for f in files if not re.match(r'^\d+\.', f)]
    
    if incorrect:
        print(Fore.RED + f"\n[!] Warning: {len(incorrect)} images numbering format mein nahi hain!")
        cont = input(Fore.YELLOW + "Kya phir bhi agay barhen? (y/n): ").lower()
        if cont != 'y': return
    else:
        print(Fore.GREEN + "[✔] Sab images theek format mein hain.")

    # PDF Name & Output Folder
    pdf_name = input(Fore.YELLOW + "\nStep 2: PDF ka kya naam rakhna hai? ") or "Rehman_Ali_Output"
    output_folder = os.path.join(path, "PDF_Output_Folder")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    final_pdf_path = os.path.join(output_folder, f"{pdf_name}.pdf")

    # Processing Images and Adding Page Numbers
    print(Fore.MAGENTA + "\n[*] Processing images and adding page numbers...")
    processed_images = []
    
    try:
        for index, filename in enumerate(files, start=1):
            img_path = os.path.join(path, filename)
            img = Image.open(img_path).convert("RGB")
            
            # Draw Page Number
            draw = ImageDraw.Draw(img)
            # Text position (Bottom Center)
            w, h = img.size
            page_text = f"Page {index}"
            
            # Simple text draw (No external font needed for basic use)
            draw.text((w // 2 - 20, h - 50), page_text, fill=(255, 0, 0)) # Red color
            
            processed_images.append(img)
            print(Fore.WHITE + f" -> Processed: {filename} (Added Page {index})")

        # Save to PDF
        if processed_images:
            processed_images[0].save(
                final_pdf_path, 
                save_all=True, 
                append_images=processed_images[1:]
            )
            print(Fore.GREEN + Style.BRIGHT + f"\n[SUCCESS] Mubarak ho! PDF ban gayi.")
            print(Fore.CYAN + f"Saved at: {final_pdf_path}")
    
    except Exception as e:
        print(Fore.RED + f"\n[Error] Masla agaya: {e}")

# --- Part 4: Main Menu ---
while True:
    show_banner()
    print("1. " + Fore.GREEN + "Start PDF Conversion")
    print("2. " + Fore.RED + "Uninstall Tool Libraries")
    print("3. " + Fore.WHITE + "Exit")
    
    choice = input(Fore.YELLOW + "\nOption chuno: ")
    
    if choice == '1':
        create_pdf()
        input(Fore.WHITE + "\nPress Enter to back to menu...")
    elif choice == '2':
        confirm = input(Fore.RED + "Kya waqai sab kuch delete karna hai? (y/n): ")
        if confirm.lower() == 'y':
            manage_libs("uninstall")
            break
    elif choice == '3':
        print(Fore.CYAN + "Allah Hafiz Rehman Ali!")
        time.sleep(1)
        break
    else:
        print(Fore.RED + "Ghalat option!")
        time.sleep(1)
