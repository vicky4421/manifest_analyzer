from rich.console import Console
import sys
import os
import xml.etree.ElementTree as ET
import pyfiglet
import utils as u

version = "1.0.0"

xmlFile = ""
namespace = "http://schemas.android.com/apk/res/android"

# symbols
x_symbol = ":x:"
check_symbol = ":white_check_mark:"
page_symbol = ":page_with_curl:"
label_symbol = ":label:"
attention_symbol = ":zap:"
hamburger_symbol = ":hamburger:"

# colors
pri_color = "magenta"
sec_color = "cyan"

console = Console()

#=============== Main Start ===============
def main():

    # Banner
    banner_font = pyfiglet.Figlet(font="slant", width=90)
    console.print(f"{banner_font.renderText("Manifest Analyzer")}", style=pri_color)
    console.print(f"- By Vivek Sawant, Version: {version}")

    # import file from cli 
    if len(sys.argv) == 2:
        xmlFile = sys.argv[1]

        # Check if arg provided is a file
        if not os.path.isfile(xmlFile):
            console.print(f"{x_symbol} Not a file!", style="red", markup=False)
            return

        # Check the file provided is an xml file
        elif not xmlFile.lower().endswith(".xml"):
            console.print(f"{x_symbol} Please provide a XML file", style="red", markup=False)
            return

        # parse file
        else:
            u.print_KeyValue(key="Parsing file", value=xmlFile, symbol="\n\n" + check_symbol)

            try:
                tree = ET.parse(xmlFile)
                root = tree.getroot()
                app = root.find('application')
                if root.get("package") and root.tag == "manifest":
                    u.print_KeyValue(key= " Package name", value= root.get("package"), symbol= label_symbol, extra_style="blink")
                    print("\n")
                    console.print(f"{attention_symbol} App Attributes", style='bold green')
                    u.show_app_attr(app)
                    print("\n")
                    console.print(f"{attention_symbol} App Metadata", style='bold green')
                    u.show_app_metadata(app)
                        
                else:
                    console.print(f"{x_symbol} This is not an Android Manifest file!", style="red")
                    return
            except Exception as e:
                console.print(f"{x_symbol} {e}")
                return
            
    else:
        console.print(f"{x_symbol} Incorrect usage", style="red")
        console.print(f"{check_symbol} Usage: python manifest_analyzer.py [file name]", style='green', markup=False)
        return

    show_main_menu(app)
#=============== Main End ===============

#=============== Show Main Menu Starts ===============
def show_main_menu(app):
    while True:
        console.print(f"\n{hamburger_symbol} Main Menu", style="bold green")
        console.print("[1] Show Activities", style="cyan", markup= False)
        console.print("[2] Show Broadcast Receivers", style="cyan", markup= False)
        console.print("[3] Show Content Providers", style="cyan", markup= False)
        console.print("[4] Show Services", style="cyan", markup= False)
        console.print("[0] Exit \n", style="bold red")

        choice = input("Please select a field: ").strip()

        if choice == "0":
            console.print("Exiting...", style="bold red")
            break
        elif choice == "1":
            u.show_all_items(app, 'activity')
            break
        elif choice == "2":
            u.show_all_items(app, 'receiver')
            break
        elif choice == "3":
            u.show_all_items(app, 'provider')
            break
        elif choice == "4":
            u.show_all_items(app, 'service')
            break
        else:
            console.print("Invalid Choice. Try Again!", style="bold red")

if __name__ == "__main__":
    main()