from functions import *

# Pencere oluşturulur
window = tk.Tk()
window.geometry("750x550")
window.title("To-Do List")

# Verileri tutmak için listeler tanımlanıp kayıtta olan veriler listelere atanır
tasks = load_data_task()
completed = load_data_completed()

# Görev ekleme paneli
frame_add = tk.Frame(window)
frame_add.grid(row=0, column=0, padx=10, pady=10)

title_label = tk.Label(frame_add, text="Başlık :")
title_label.grid(row=0, column=0, padx=10, pady=0)

task_entry = tk.Entry(frame_add, width=68, bg="#aaffff")
task_entry.grid(row=0, column=1, padx=10, pady=10)

text_label = tk.Label(frame_add, text="Ayrıntılar :")
text_label.grid(row=1, column=0, padx=10, pady=0)

details_entry = tk.Text(frame_add, width=51, height=5, bg="#aaffff")
details_entry.grid(row=1, column=1, padx=10, pady=10)

add_button = tk.Button(frame_add, text="Ekle", command=lambda: add_task(task_entry, details_entry, task_listbox, tasks))
add_button.grid(row=1, column=2, padx=10, pady=10)

# Görev listeleme paneli
frame_tasks = tk.Frame(window)
frame_tasks.grid(row=1, column=0, padx=10, pady=1, sticky="nsew")

label_tasks = tk.Label(frame_tasks, text="Görevler")
label_tasks.grid(row=0, column=0, padx=10, pady=0, sticky="w")

label_completed = tk.Label(frame_tasks, text="Tamamlananlar")
label_completed.grid(row=0, column=1, padx=10, pady=0, sticky="w")

task_listbox = tk.Listbox(frame_tasks, width=38, height=20, bg="#aaffff")
task_listbox.grid(row=1, column=0, padx=10, pady=0)

completed_listbox = tk.Listbox(frame_tasks, width=40, height=20, bg="#aaffff")
completed_listbox.grid(row=1, column=1, padx=10, pady=0)

# Butonlar paneli
frame_buttons = tk.Frame(window)
frame_buttons.grid(row=1, column=1, padx=10, pady=0)

complete_button = tk.Button(frame_buttons, text="Tamamla", command=lambda: complete(task_listbox, completed_listbox, tasks, completed))
complete_button.grid(row=0, column=0, padx=10, pady=10)

uncomplete_button = tk.Button(frame_buttons, text="Tamamlamayı Kaldır", command=lambda: uncomplete(task_listbox, completed_listbox, tasks, completed))
uncomplete_button.grid(row=1, column=0, padx=10, pady=10)

delete_button = tk.Button(frame_buttons, text="Sil", command=lambda: delete(task_listbox, completed_listbox, tasks, completed))
delete_button.grid(row=2, column=0, padx=10, pady=10)

view_button = tk.Button(frame_buttons, text="Görüntüle", command=lambda: wiew(task_listbox, completed_listbox, tasks, completed))
view_button.grid(row=3, column=0, padx=10, pady=10)

move_up_button = tk.Button(frame_buttons, text="Yukarı Taşı", command=lambda: move_up(task_listbox, completed_listbox, tasks, completed))
move_up_button.grid(row=4, column=0, padx=10, pady=10)

move_down_button = tk.Button(frame_buttons, text="Aşağı Taşı ", command=lambda: move_down(task_listbox, completed_listbox, tasks, completed))
move_down_button.grid(row=5, column=0, padx=10, pady=10)

edit_button = tk.Button(frame_buttons, text="Düzenle", command=lambda: edit(window, task_listbox, completed_listbox, tasks))
edit_button.grid(row=6, column=0, padx=10, pady=10)

update_task_listbox(task_listbox, tasks)
update_completed_listbox(completed_listbox, completed)

window.mainloop()
