import tkinter as tk
from tkinter import messagebox
import json

# tasks.json dosyasındaki veriler tasks listesine aktarılır
def load_data_task():
    try:
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []
    return tasks


# completed.json dosyasındaki veriler completed listesine aktarılır
def load_data_completed():
    try:
        with open("completed.json", "r") as file:
            completed = json.load(file)
    except FileNotFoundError:
        completed = []
    return completed


# Arayüzdeki görevler listesini listeler
def update_task_listbox(task_listbox, tasks):
    task_listbox.delete(0, tk.END)
    i = 1
    for task in tasks:
        task_listbox.insert(tk.END, str(i) + ")  [  ] " + task['task'])
        i += 1


# Arayüzdeki tamamlananlar listesini listeler
def update_completed_listbox(completed_listbox, completed):
    completed_listbox.delete(0, tk.END)
    i = 1
    for c in completed:
        completed_listbox.insert(tk.END, str(i) + ")  [X] " + c['task'])
        i += 1


# Görev ekler
def add_task(task_entry, details_entry, task_listbox, tasks):
    new_task = task_entry.get()
    details = details_entry.get("1.0", tk.END).strip()
    if len(new_task) > 25:
        task_entry.delete(0, tk.END)
        details_entry.delete("1.0", tk.END)
        messagebox.showwarning("Uyarı", "Başlık 25 karakterden uzun olmamalıdır.")
    else:
        if new_task:
            tasks.append({"task": new_task, "details": details, "completed": False})
            update_task_listbox(task_listbox, tasks)
            save_data_task(tasks)
            task_entry.delete(0, tk.END)
            details_entry.delete("1.0", tk.END)
            tk.messagebox.showinfo("Mesaj", "Görev başarıyla eklendi.")
        else:
            tk.messagebox.showwarning("Uyarı", "Başlık boş olamaz.")


# Görevi tamamlandı olarak işaretler ve görevler listesinin tarafından tamamlananlar listesinin tarafına geçirir
def complete(task_listbox, completed_listbox, tasks, completed):
    selected_index = task_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        tasks[index]["completed"] = True
        completed.append(tasks[index])
        del tasks[index]
        update_task_listbox(task_listbox, tasks)
        save_data_task(tasks)
        update_completed_listbox(completed_listbox, completed)
        save_data_completed(completed)
    else:
        messagebox.showwarning("Uyarı", "Lütfen tamamlanmamış bir görev seçiniz.")


# Görevi tamamlanmadı olarak işaretler ve tamamlananlar listesinin tarafından görevler listesinin tarafına geçirir
def uncomplete(task_listbox, completed_listbox, tasks, completed):
    selected_index = completed_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        completed[index]["completed"] = False
        tasks.append(completed[index])
        del completed[index]
        update_task_listbox(task_listbox, tasks)
        save_data_task(tasks)
        update_completed_listbox(completed_listbox, completed)
        save_data_completed(completed)
    else:
        messagebox.showwarning("Uyarı", "Lütfen bir tamamlanmış bir görev seçiniz.")


# Görevi siler
def delete(task_listbox, completed_listbox, tasks, completed):
    selected_index_task = task_listbox.curselection()
    selected_index_completed = completed_listbox.curselection()
    if selected_index_task:
        index = selected_index_task[0]
        confirm = messagebox.askyesno("Onay", "Seçilen görevi silmek istediğinizden emin misiniz?")
        if confirm:
            del tasks[index]
            update_task_listbox(task_listbox, tasks)
            save_data_task(tasks)
    elif selected_index_completed:
        index = selected_index_completed[0]
        confirm = messagebox.askyesno("Onay", "Seçilen görevi silmek istediğinizden emin misiniz?")
        if confirm:
            del completed[index]
            update_completed_listbox(completed_listbox, completed)
            save_data_completed(completed)
    else:
        messagebox.showwarning("Uyarı", "Lütfen silmek için bir görev seçiniz.")


# Görevi görüntüler (Bunun için show_detail_window fonksiyonundan yardım alır)
def wiew(task_listbox, completed_listbox, tasks, completed):
    selected_index_task = task_listbox.curselection()
    selected_index_completed = completed_listbox.curselection()
    if selected_index_task:
        index = selected_index_task[0]
        task_title = tasks[index].get("task", "Ayrıntı bulunamadı.")
        task_details = tasks[index].get("details", "Ayrıntı bulunamadı.")
        show_details_window("Görev Ayrıntıları", task_title, task_details)
    elif selected_index_completed:
        index = selected_index_completed[0]
        task_title = completed[index].get("task", "Ayrıntı bulunamadı.")
        task_details = completed[index].get("details", "Ayrıntı bulunamadı.")
        show_details_window("Görev Ayrıntıları", task_title, task_details)
    else:
        messagebox.showwarning("Uyarı", "Lütfen görüntülemek için bir görev seçiniz.")


# Görevi görüntülemek için yeni penecere oluşturur
def show_details_window(title, task_title, task_details):
    details_window = tk.Tk()
    details_window.geometry("400x400")
    details_window.title(title)

    title_label = tk.Label(details_window, text="Görev: " + task_title, padx=10, pady=10, font="bold")
    title_label.grid(row=0, column=0, padx=10, pady=0, sticky="w")

    details_text = tk.Text(details_window, width=40, height=10, bg="#aaffff")
    details_text.insert(tk.END, task_details)
    details_text.grid(row=1, column=0, padx=10, pady=10)
    details_text.configure(state="disabled")

    details_window.mainloop()


# Görevin önem sırasını arttırır
def move_up(task_listbox, completed_listbox, tasks, completed):
    selected_index_task = task_listbox.curselection()
    selected_index_completed = completed_listbox.curselection()
    if selected_index_task:
        index = selected_index_task[0]
        if index > 0:
            tasks[index], tasks[index - 1] = tasks[index - 1], tasks[index]
            update_task_listbox(task_listbox, tasks)
            save_data_task(tasks)
            task_listbox.selection_clear(0, tk.END)
            task_listbox.select_set(index - 1)
    elif selected_index_completed:
        index = selected_index_completed[0]
        if index > 0:
            completed[index], completed[index - 1] = completed[index - 1], completed[index]
            update_completed_listbox(completed_listbox, completed)
            save_data_completed(completed)
            completed_listbox.selection_clear(0, tk.END)
            completed_listbox.select_set(index - 1)
    else:
        messagebox.showwarning("Uyarı", "Lütfen taşımak için bir görev seçiniz.")


# Görevin önem sırasını azaltır
def move_down(task_listbox, completed_listbox, tasks, completed):
    selected_index_task = task_listbox.curselection()
    selected_index_completed = completed_listbox.curselection()
    if selected_index_task:
        index = selected_index_task[0]
        if index < len(tasks) - 1:
            tasks[index], tasks[index + 1] = tasks[index + 1], tasks[index]
            update_task_listbox(task_listbox, tasks)
            save_data_task(tasks)
            task_listbox.selection_clear(0, tk.END)
            task_listbox.select_set(index + 1)
    elif selected_index_completed:
        index = selected_index_completed[0]
        if index < len(completed) - 1:
            completed[index], completed[index + 1] = completed[index + 1], completed[index]
            update_completed_listbox(completed_listbox, completed)
            save_data_completed(completed)
            completed_listbox.selection_clear(0, tk.END)
            completed_listbox.select_set(index + 1)
    else:
        messagebox.showwarning("Uyarı", "Lütfen taşımak için bir görev seçiniz.")


# Görevi düzenler (Bunun için confirm ve open_confirm_page fonksiyonlarından yardım alır)
def edit(root, task_listbox, completed_listbox, tasks):
    selected_index_task = task_listbox.curselection()
    selected_index_completed = completed_listbox.curselection()
    if selected_index_task:
        index = selected_index_task[0]
        old_title = tasks[index]["task"]
        old_details = tasks[index].get("details", "")

        edit_window = tk.Toplevel(root)
        edit_window.geometry("700x400")
        edit_window.title("Düzenle")

        title = tk.Label(edit_window, text="Başlık :")
        title.grid(row=0, column=0, padx=10, pady=0)

        task_entry = tk.Entry(edit_window, width=68, bg="#aaffff")
        task_entry.grid(row=0, column=1, padx=10, pady=10)
        task_entry.insert(0, old_title)

        text = tk.Label(edit_window, text="Ayrıntılar :")
        text.grid(row=1, column=0, padx=10, pady=0)

        details_entry = tk.Text(edit_window, width=51, height=5, bg="#aaffff")
        details_entry.grid(row=1, column=1, padx=10, pady=10)
        details_entry.insert(tk.END, old_details)

        confirm_button = tk.Button(edit_window, text="Onayla", command=lambda: confirm(index, task_entry, details_entry, edit_window, root, task_listbox, completed_listbox, tasks))
        confirm_button.grid(row=2, column=1, padx=10, pady=10, sticky="e")

        edit_window.mainloop()

    elif selected_index_completed:
        messagebox.showwarning("Uyarı", "Tamamlanmış bir görev seçtiniz.")
    else:
        messagebox.showwarning("Uyarı", "Lütfen düzenlemek için bir görev seçiniz.")


# Yapılacak değişiklikler sonucunda başlığın uygun olup olmadığını kontrol eder.
def confirm(index, task_entry, details_entry, edit_window, root, task_listbox, completed_listbox, tasks):
    new_title = task_entry.get()
    new_details = details_entry.get("1.0", tk.END).strip()
    if len(new_title) > 25:
        messagebox.showwarning("Uyarı", "Başlık 25 karakterden uzun olmamalıdır.")
        edit_window.destroy()
        open_confirm_page(index, root, task_listbox, completed_listbox, tasks)
    else:
        if new_title:
            tasks[index]["task"] = new_title
            tasks[index]["details"] = new_details
            update_task_listbox(task_listbox, tasks)
            save_data_task(tasks)
            edit_window.destroy()
            messagebox.showinfo("Mesaj", "Değişiklikler kaydedildi.")
        else:
            messagebox.showwarning("Uyarı", "Başlık boş olamaz.")
            edit_window.destroy()
            open_confirm_page(index, root, task_listbox, completed_listbox, tasks)

# Girilen başlık eğer uygun değilse confirm fonksiyonundan buraya aktarılır ve burada tekrar girmesi istenir.
def open_confirm_page(index, root, task_listbox, completed_listbox, tasks):
    old_title = tasks[index]["task"]
    old_details = tasks[index].get("details", "")

    edit_window = tk.Toplevel(root)
    edit_window.geometry("700x400")
    edit_window.title("Düzenle")

    title = tk.Label(edit_window, text="Başlık :")
    title.grid(row=0, column=0, padx=10, pady=0)

    task_entry = tk.Entry(edit_window, width=68, bg="#aaffff")
    task_entry.grid(row=0, column=1, padx=10, pady=10)
    task_entry.insert(0, old_title)

    text = tk.Label(edit_window, text="Ayrıntılar :")
    text.grid(row=1, column=0, padx=10, pady=0)

    details_entry = tk.Text(edit_window, width=51, height=5, bg="#aaffff")
    details_entry.grid(row=1, column=1, padx=10, pady=10)
    details_entry.insert(tk.END, old_details)

    confirm_button = tk.Button(edit_window, text="Onayla", command=lambda: confirm(index, task_entry, details_entry, edit_window, root, task_listbox, completed_listbox, tasks))
    confirm_button.grid(row=2, column=1, padx=10, pady=10, sticky="e")

    edit_window.mainloop()


# tasks listesindeki değerleri tasks.json dosyasına kayıt eder.
def save_data_task(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)


# completed listesindeki değerleri tasks.json dosyasına kayıt eder.
def save_data_completed(completed):
    with open("completed.json", "w") as file:
        json.dump(completed, file)
