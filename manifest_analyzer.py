from rich.console import Console
from rich.table import Table
from time import sleep
import sys
import os
import xml.etree.ElementTree as ET

console = Console()

xmlFile = ""
x_symbol = ":x:"
check_symbol = ":white_check_mark:"
page_symbol = ":page_with_curl:"
label_symbol = ":label:"
attention_symbol = ":zap:"

tree = ""
root = ""
app = ""
namespace = "http://schemas.android.com/apk/res/android"

# root tag -> manifest
# root attr -> xmlns

def print_KeyValue(
        key: str,
        value: str,
        symbol: str,
        extra_style = "",
        key_style = "bold magenta",
        value_style = "cyan",
):
    # style_prefix = f"[{extra_style}]" if extra_style else ""
    # style_suffix = f"[/{extra_style}]" if extra_style else ""
    console.print(
        f"{symbol} [{key_style}]{key}:[/{key_style}] [{value_style}]{value}[/{value_style}]",
        style=extra_style
    )

#=============== Main Start ===============
def main():
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
            print_KeyValue(key="Parsing file", value=xmlFile, symbol="\n" + check_symbol)
            with console.status("Parsing file...", spinner="clock"):
                try:
                    tree = ET.parse(xmlFile)
                    root = tree.getroot()

                    if root.get("package") and root.tag == "manifest":
                        print_KeyValue(key= " Package name", value= root.get("package"), symbol= label_symbol, extra_style="blink")
                            
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
    print_KeyValue(key= " app name", value= app_name + "\n", symbol= label_symbol)

    while True:
        console.print("\nOptions \n", style="bold green")
        console.print("[1] Show All Activities", style="cyan", markup= False)
        console.print("[2] Show Exported Activities", style="cyan", markup= False)
        console.print("[3] Show Broadcast Receivers", style="cyan", markup= False)
        console.print("[4] Show Exported Broadcast Receivers", style="cyan", markup= False)
        console.print("[5] Show Content Providers", style="cyan", markup= False)
        console.print("[6] Show Exported Content Providers", style="cyan", markup= False)
        console.print("[7] Show Services", style="cyan", markup= False)
        console.print("[8] Show Exported Services", style="cyan", markup= False)
        console.print("[0] Exit \n", style="bold red")

        choice = input("Please select a field: ").strip()

        if choice == "0":
            console.print("Exiting...", style="bold red")
            break
        elif choice == "1":
            show_all_activities(app)
        elif choice == "2":
            show_exported_activities(app)
        else:
            console.print("Invalid Choice. Try Again!", style="bold red")

#=============== Main End ===============

#=============== Show Exported Activities Start ===============  
def show_exported_activities(app):
    # find exported activities in applications
    activities = app.findall("activity")
    console.print(f"\n{attention_symbol} Exported Activities", style='green')

    for activity in activities:
        if activity.get(f"{{{namespace}}}exported") == "true":
            console.print(f"\n{page_symbol} {activity.get(f"{{{namespace}}}name")}", style='blue')

            # find all intent filters
            intent_filters = activity.findall("intent-filter")

            console.print(f"No. of intent filters for this activity: {len(intent_filters)}")

            # find action-category-data for each intent filter
            for intent_filter in intent_filters:

                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Action", justify="center")
                table.add_column("Category", justify="center")
                table.add_column("Data", justify="left")

                actions = intent_filter.findall("action")
                categories = intent_filter.findall("category")
                data = intent_filter.findall("data")

                aNames = []
                cNames = []
                dNames = []

                for action in actions:
                    aNames.append(action.get(f"{{{namespace}}}name"))

                for category in categories:
                    cNames.append(category.get(f"{{{namespace}}}name"))

                for dt in data:
                    if dt.get(f"{{{namespace}}}scheme"):
                        dNames.append(f"scheme: {dt.get(f'{{{namespace}}}scheme')}")
                    elif dt.get(f"{{{namespace}}}host"):
                        dNames.append(f"host: {dt.get(f'{{{namespace}}}host')}")
                    elif dt.get(f"{{{namespace}}}port"):
                        dNames.append(f"port: {dt.get(f'{{{namespace}}}port')}")
                    elif dt.get(f"{{{namespace}}}path"):
                        dNames.append(f"path: {dt.get(f'{{{namespace}}}path')}")
                    elif dt.get(f"{{{namespace}}}pathPrefix"):
                        dNames.append(f"pathPrefix: {dt.get(f'{{{namespace}}}pathPrefix')}")
                    elif dt.get(f"{{{namespace}}}pathPattern"):
                        dNames.append(f"pathPattern: {dt.get(f'{{{namespace}}}pathPattern')}")
                    elif dt.get(f"{{{namespace}}}mimeType"):
                        dNames.append(f"mimeType: {dt.get(f'{{{namespace}}}mimeType')}")
                              
                # Normalize length
                max_len = max(len(aNames), len(cNames), len(dNames))
                aNames += [""] * (max_len - len(aNames))
                cNames += [""] * (max_len - len(cNames))
                dNames += [""] * (max_len - len(dNames))
               

                for i in range(max_len):
                    table.add_row(aNames[i], cNames[i], dNames[i])

                console.print(table)
#=============== Show Exported Activities End ===============

#=============== Show All Activities Start ===============
def show_all_activities(app):
    # find exported activities in applications
    activities = app.findall("activity")
    console.print(f"\n{attention_symbol} All Activities", style='green')
    console.print(f"Total no. of Activities: {len(activities)}", style='green blink')

    for activity in activities:
        console.print(f"{page_symbol} {activity.get(f"{{{namespace}}}name")}", style='blue')
#=============== Show All Activities End ===============

if __name__ == "__main__":
    main()