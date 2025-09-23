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
            with console.status("Parsing file...", spinner="clock"):
                try:
                    tree = ET.parse(xmlFile)
                    root = tree.getroot()

                    if root.get("package") and root.tag == "manifest":
                        u.print_KeyValue(key= " Package name", value= root.get("package"), symbol= label_symbol, extra_style="blink")
                            
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
    
    # Find application tag
    app = root.find('application')
    app_name = app.get(f"{{{namespace}}}name")
    u.print_KeyValue(key= " app name", value= app_name + "\n", symbol= label_symbol)

    show_main_menu(app)
#=============== Main End ===============

#=============== Show Main Menu Starts ===============
def show_main_menu(app):
    while True:
        console.print(f"\n{hamburger_symbol} Main Menu", style="bold green")
        console.print("[1] Show All Activities", style="cyan", markup= False)
        console.print("[2] Show Exported Activities", style="cyan", markup= False)
        console.print("[3] Show All Broadcast Receivers", style="cyan", markup= False)
        console.print("[4] Show Exported Broadcast Receivers", style="cyan", markup= False)
        console.print("[5] Show All Content Providers", style="cyan", markup= False)
        console.print("[6] Show Exported Content Providers", style="cyan", markup= False)
        console.print("[7] Show All Services", style="cyan", markup= False)
        console.print("[8] Show Exported Services", style="cyan", markup= False)
        console.print("[0] Exit \n", style="bold red")

        choice = input("Please select a field: ").strip()

        if choice == "0":
            console.print("Exiting...", style="bold red")
            break
        elif choice == "1":
            u.show_all_items(app, 'activity')
        elif choice == "2":
            u.show_exported_items(app, 'activity')
            break
        elif choice == "3":
            u.show_all_items(app, 'receiver')
        elif choice == "4":
            u.show_exported_items(app, 'receiver')
            break
        elif choice == "5":
            u.show_all_items(app, 'provider')
        elif choice == "6":
            u.show_exported_items(app, 'provider')
            break
        elif choice == "7":
            u.show_all_items(app, 'service')
        elif choice == "8":
            u.show_exported_items(app, 'service')
            break
        else:
            console.print("Invalid Choice. Try Again!", style="bold red")

if __name__ == "__main__":
    main()