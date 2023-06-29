import tkinter
from tkinter import *
from tkinter import ttk
import requests
import json
import datetime


# main search
def main_function(search_parameters: str):
    url = 'https://client.dropcatch.com/Search'
    body_site = {
        "searchTerm": search_parameters,
        "filters": [
            {
                "values": [
                    {
                        "Range": {
                            "Min": "2023-02-06T06:55:17.668Z",
                            "Max": None
                        }
                    }
                ],
                "Name": "ExpirationDate"
            }
        ],
        "page": 1,
        "size": 50,
        "sorts": [
            {
                "field": "highBid",
                "direction": "Descending"
            }
        ]
    }

    x = requests.post(url, json=body_site)

    return x


def day_difference_with_today(date_data):
    date_format = "%d.%m.%Y %H:%M:%S"
    today = datetime.datetime.strptime(datetime.datetime.today().strftime(date_format), date_format)
    ddf = datetime.datetime.strptime(from_iso_date_to_str(date_iso=date_data, date_format=date_format), date_format) - today
    return ddf.days


def from_iso_date_to_str(date_iso, date_format="%d.%m.%Y %H:%M:%S"):
    return datetime.datetime.fromisoformat(date_iso[:-1]).astimezone(datetime.timezone.utc).strftime(date_format)


def result_creator(data_item):
    list_keys = dict(data_item).keys()
    list(map(lambda ky: str(ky).replace(' ', ''), list_keys))
    return data_item['name'], from_iso_date_to_str(data_item['expirationDate']), data_item['recordType'], data_item['highBid']


def fill_tree_data(data, tree):
    # Data
    list(map(lambda tti: tree.delete(tti), tree.get_children()))
    list(map(lambda dt: tree.insert("", 'end', text="L" + str(data.index(dt)+1), values=dt), data))


def submit(search: str, remaining: int, label, res, tree):
    try:
        label.config(text='', fg='#000')
        remaining = int(remaining)
        search = str(search)

        result = main_function(search_parameters=search)
        result_obj = json.loads(result.text)
        table_data = result_obj['result']['items']

        filtered_list = list(filter(lambda dt: day_difference_with_today(dt['expirationDate']) <= remaining, table_data))
        result = list(map(lambda fd: result_creator(fd), filtered_list))

        fill_tree_data(result, tree)

    except (ValueError, TypeError):
        result = []
        label.config(text='ERROR: Remaining days must be number (count of days) or some thing went wrong', fg='#f00')
    return result


window = tkinter.Tk()

window.title("Backordering the domains")
frame = tkinter.Frame(window, padx=10, pady=10)
frame.pack()
window.resizable(False, False)
window.geometry('950x550')
image = PhotoImage(file="turkey.png")
window.iconphoto(False, image)

# create TreeView widget
tree = ttk.Treeview(window, selectmode='browse')
tree.pack(side='left', padx=60, pady=20)

# style tree
style = ttk.Style()
style.configure("Treeview.Heading", font=(None, 14))
style.configure("Treeview", font=(None, 12))

# scrollbar
scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
scrollbar.pack(side='left', fill=Y)
tree.configure(yscrollcommand=scrollbar.set)

# Number of columns
tree["columns"] = ("1", "2", "3", "4")

# Headings
tree['show'] = 'headings'

# Columns configuration
tree.column("1", width=220, anchor='nw')
tree.column("2", width=220, anchor='c')
tree.column("3", width=220, anchor='c')
tree.column("4", width=110, anchor='c')

# Headings
tree.heading("1", text="Name")
tree.heading("2", text="Expiration date")
tree.heading("3", text="Record type")
tree.heading("4", text="High bid")
tree.pack(fill="x")

#  1st head TAB label
website_title = tkinter.LabelFrame(frame)
website_title.grid(row=0, column=0)
website_name = tkinter.Label(website_title, text="This App can get data from www.dropcatch.com only!",  fg='#f00', pady=10, padx=10, font=10)
website_name.grid(row=0, column=0)

# 2nd head big TAB label
head_label = tkinter.LabelFrame(frame, text="Backorder your domains", pady=10, padx=10, font=14)
head_label.grid(row=1, column=0)

search_label = tkinter.Label(head_label, text="Search:", font=10)
search_label.grid(row=0, column=0)

search_box = tkinter.Entry(head_label, font=3)
search_box.grid(row=0, column=1)

remaining_days_label = tkinter.Label(head_label, text="Remaining days:", font=10, padx=20)
remaining_days_label.grid(row=0, column=2)

remaining_days = tkinter.Entry(head_label, font=3)
# remaining_days.insert(0, 10)
remaining_days.grid(row=0, column=3)

# 3rd TAB label
# footer_tab = tkinter.LabelFrame(frame, pady=30, padx=10, font=10)
# footer_tab.grid(row=2, column=0)


# error TAB
error_label_tab = tkinter.LabelFrame(frame, pady=5, padx=5)
# result TAB
result_label_tab = tkinter.LabelFrame(frame, padx=5, pady=5)

error_label_tab.grid(row=2, column=0, pady=20)

error_label = tkinter.Label(error_label_tab, text="", padx=10, pady=10, width=100)
error_label.grid(row=0, column=0)

submit_button = tkinter.Button(error_label_tab, text="Search & get result!", font=10, command=lambda: submit(search=search_box.get(), remaining=remaining_days.get(), label=error_label,
                                                                                                             res=window, tree=tree))
submit_button.grid(row=1, column=0, sticky="news")

# create_tree_v_layout(window)

window.mainloop()




