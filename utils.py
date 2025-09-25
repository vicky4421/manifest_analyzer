from rich.console import Console
from rich.table import Table
import manifest_analyzer as ma

console = Console()

# symbols
x_symbol = ":x:"
check_symbol = ":white_check_mark:"
page_symbol = ":page_with_curl:"
label_symbol = ":label:"
attention_symbol = ":zap:"
hamburger_symbol = ":hamburger:"
diamond_symbol = ":small_orange_diamond:"

# colors
pri_color = "magenta"
sec_color = "cyan"

namespace = "http://schemas.android.com/apk/res/android"

# function for printing key value in uniform color
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

#=============== Show All Items Start ===============
def show_all_items(app, item):
    items = app.findall(item)
    console.print(f"\n{attention_symbol} All {item}", style='green')
    console.print(f"Total no. of {item}: {len(items)}", style='green blink')

    for i in items:
        console.print(f"{page_symbol} {i.get(f"{{{namespace}}}name")}", style='blue')

    show_item_menu(app, item)
#=============== Show All Items End ===============

#=============== Show Item Menu Start ===============
def show_item_menu(app, item):
    while True:
        console.print(f"\n{hamburger_symbol} {item} Menu", style="bold green")
        console.print(f"[1] Show Exported {item}", style="cyan", markup= False)
        console.print("[0] Exit \n", style="bold red")

        choice = input("Please select a field: ").strip()

        if choice == "0":
            ma.show_main_menu(app)
            break
        elif choice == "1":
            show_exported_items(app, item)
            break
        else:
            console.print("Invalid Choice. Try Again!", style="bold red")
#=============== Show Item Menu End ===============

#=============== Show All Exported Items Start ===============
def show_exported_items(app, item):
    # find exported activities in applications
    items = app.findall(item)
    console.print(f"\n{attention_symbol} Exported {item}\n", style='green')

    total_exported_items = 0

    for i in items:
        if i.get(f"{{{namespace}}}exported") == "true":
            total_exported_items += 1
            console.print(f"{page_symbol} {i.get(f"{{{namespace}}}name")}", style='blue')

    console.print(f"Total no. of Exported {item}: {total_exported_items}", style='green blink')

    show_exported_item_menu(app, item)
#=============== Show All Exported Items End ===============

#=============== Show Exported Items Menu Start ===============
def show_exported_item_menu(app, item):
    while True:
        console.print(f"\n{hamburger_symbol} Exported {item} Menu \n", style="bold green")
        console.print("[1] Show Intent Filters", style="cyan", markup= False)
        console.print("[2] Show Attributes", style="cyan", markup= False)
        console.print("[0] Go Back\n", style="cyan", markup= False)
        choice = input("Please select a field: ").strip()
        print("\n")

        if choice == "0":
            ma.show_main_menu(app)
            break
        elif choice == "1":
            # choose_exp_activity_for_intent(app)
            choose_exp_item_for_intent(app, item)
            break
        elif choice == "2":
            choose_item_for_attributes(app, item)
            break
        else:
            console.print("Invalid Choice. Try Again!", style="bold red")
#=============== Show Exported Items Menu End ===============

#=============== Choose Exported Item for intent filter Menu Start =============== 
def choose_exp_item_for_intent(app, item):

    list_total_exp_items = []

    items = app.findall(item)
    total_exp_items = 0

    for i in items:
        if i.get(f"{{{namespace}}}exported") == "true":
            item_name = i.get(f"{{{namespace}}}name")
            list_total_exp_items.append(item_name)
            total_exp_items += 1
            console.print(f"[{total_exp_items}] {item_name}", style='blue')

    while True:
        console.print(f"\n{hamburger_symbol} Select {item} \n", style="bold green")
        console.print("[0] Go Back\n", style="cyan", markup= False)

        choice = input("Please select a field: ").strip()

        if choice == "0":
            show_exported_items(app, item)
            break
        elif int(choice) > len(list_total_exp_items) or int(choice) < 1:
            console.print("Invalid Choice. Try Again!", style="bold red")
        else:
            show_intent_filters(app, list_total_exp_items[int(choice) - 1], item)
            break
#=============== Choose Exported Activity for intent filter Menu End =============== 

#=============== Show Intent Filters Start ===============  
def show_intent_filters(app, item_name, item):
    items = app.findall(item)

    for i in items:
        if i.get(f"{{{namespace}}}name") == item_name:
            console.print(f"\n{page_symbol} {i.get(f"{{{namespace}}}name")}", style='blue')

            # find all intent filters
            intent_filters = i.findall("intent-filter")

            console.print(f"\nNo. of intent filters for this {item}: {len(intent_filters)}")

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
#=============== Show Intent Filters End ===============

#=============== Show App Attributes Start ===============
def show_app_attr(app):
    for attr, value in app.items():
        attr = attr.split('}', 1)[1]
        print_KeyValue(key=attr, value=value, symbol=diamond_symbol)
#=============== Show App Attributes End ===============

#=============== Choose Item Attributes Menu Start ===============
def choose_item_for_attributes(app, item):

    list_total_items = []

    items = app.findall(item)
    total_items = 0

    for i in items:
        item_name = i.get(f"{{{namespace}}}name")
        list_total_items.append(item_name)
        total_items += 1
        console.print(f"[{total_items}] {item_name}", style='blue')

    while True:
        console.print(f"\n{hamburger_symbol} Select {item} \n", style="bold green")
        console.print("[0] Go Back\n", style="cyan", markup= False)

        choice = input("Please select a field: ").strip()

        if choice == "0":
            show_exported_items(app, item)
            break
        elif int(choice) > len(list_total_items) or int(choice) < 1:
            console.print("Invalid Choice. Try Again!", style="bold red")
        else:
            show_item_attr(app, list_total_items[int(choice) -1], item)
            break
#=============== Choose Item Attributes Menu End ===============

#=============== Show Item Attributes Start ===============
def show_item_attr(app, item_name, item):
    items = app.findall(item)
    for i in items:
        if i.get(f"{{{namespace}}}name") == item_name:
            nickname = item_name.rsplit('.', 1)[-1]
            console.print(f"\n{page_symbol} {nickname}", style='bold green')
            for attr, value in i.items():
                attr = attr.split('}', 1)[1]
                print_KeyValue(key=attr, value=value, symbol=diamond_symbol)
#=============== Show App Attributes End ===============

#=============== Show App Meta Data Start ===============
def show_app_metadata(app):
    count = 0
    list_metadata = app.findall('meta-data')
    for md in list_metadata:
        for value in md.items():
            value = value[1]
            if count == 0:
                console.print(f"{diamond_symbol} {value}: ", style=f"bold {pri_color}", end="")
                count += 1
                continue
            if count == 1:
                console.print(f"{value}", style=sec_color)
                count = 0
#=============== Show App Meta Data End ===============