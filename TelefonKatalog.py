import tkinter as tk
from tkinter import messagebox
import os

telefonkatalog = []  # Listeformat ["fornavn", "etternavn", "telefonnummer", "kallenavn"]
data_file = "telefonkatalog.txt"

class TelefonKatalogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Telefonkatalog")
        self.root.geometry("400x400")
        self.root.configure(bg="lightblue")

        # Load existing contacts
        self.loadContacts()

        # Main menu buttons
        self.title_label = tk.Label(root, text="Telefonkatalog", font=("Arial", 18), bg="lightblue")
        self.title_label.pack(pady=10)

        self.add_btn = tk.Button(root, text="1. Legg til ny person", command=self.registrerPerson)
        self.add_btn.pack(pady=5)

        self.view_btn = tk.Button(root, text="2. Vis alle personer", command=self.visAllePersoner)
        self.view_btn.pack(pady=5)

        self.exit_btn = tk.Button(root, text="3. Avslutt", command=self.exitApp)
        self.exit_btn.pack(pady=5)

    def registrerPerson(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Registrer Person")
        self.new_window.geometry("300x300")
        self.new_window.configure(bg="lightgreen")

        tk.Label(self.new_window, text="Skriv inn fornavn:", bg="lightgreen").pack(pady=5)
        self.fornavn_entry = tk.Entry(self.new_window)
        self.fornavn_entry.pack(pady=5)

        tk.Label(self.new_window, text="Skriv inn etternavn:", bg="lightgreen").pack(pady=5)
        self.etternavn_entry = tk.Entry(self.new_window)
        self.etternavn_entry.pack(pady=5)

        tk.Label(self.new_window, text="Skriv inn telefonnummer (8 siffer):", bg="lightgreen").pack(pady=5)
        self.telefonnummer_entry = tk.Entry(self.new_window)
        self.telefonnummer_entry.pack(pady=5)

        # Checkbox for adding a nickname
        self.kallenavn_var = tk.IntVar()
        self.kallenavn_checkbox = tk.Checkbutton(self.new_window, text="Legg til kallenavn", variable=self.kallenavn_var, command=self.toggleKallenavn, bg="lightgreen")
        self.kallenavn_checkbox.pack(pady=5)

        # Nickname entry (initially disabled)
        self.kallenavn_entry = tk.Entry(self.new_window, state="disabled")
        self.kallenavn_entry.pack(pady=5)

        tk.Button(self.new_window, text="Registrer", command=self.savePerson).pack(pady=10)

    def toggleKallenavn(self):
        if self.kallenavn_var.get() == 1:
            self.kallenavn_entry.config(state="normal")
        else:
            self.kallenavn_entry.delete(0, tk.END)
            self.kallenavn_entry.config(state="disabled")

    def savePerson(self):
        fornavn = self.fornavn_entry.get()
        etternavn = self.etternavn_entry.get()
        telefonnummer = self.telefonnummer_entry.get()
        kallenavn = self.kallenavn_entry.get() if self.kallenavn_var.get() == 1 else "0"

        if not fornavn or not etternavn or not telefonnummer:
            messagebox.showwarning("Feil", "Alle felt må fylles ut!")
            return

        if not telefonnummer.isdigit() or len(telefonnummer) != 8:
            messagebox.showwarning("Feil", "Telefonnummer må være 8 siffer og bare inneholde tall!")
            return

        nyRegistrering = [fornavn, etternavn, telefonnummer, kallenavn]
        telefonkatalog.append(nyRegistrering)
        messagebox.showinfo("Suksess", f"{fornavn} {etternavn} er registrert med telefonnummer {telefonnummer}")
        self.saveContacts()
        self.new_window.destroy()

    def visAllePersoner(self):
        self.view_window = tk.Toplevel(self.root)
        self.view_window.title("Vis Alle Personer")
        self.view_window.geometry("400x300")
        self.view_window.configure(bg="lightyellow")

        # Search bar and button
        self.search_entry = tk.Entry(self.view_window)
        self.search_entry.place(x=10, y=10, width=250)
        self.search_btn = tk.Button(self.view_window, text="Søk", command=self.searchPerson)
        self.search_btn.place(x=270, y=7)

        # Listbox to display contacts
        self.listbox = tk.Listbox(self.view_window, width=50, height=12)
        self.listbox.pack(pady=40)
        
        # Edit button
        self.edit_btn = tk.Button(self.view_window, text="Rediger", command=self.openPersonDetails)
        self.edit_btn.pack(pady=5)

        # Initially populate the listbox with all contacts
        self.updateListbox(telefonkatalog)

    def updateListbox(self, data):
        self.listbox.delete(0, tk.END)
        for person in data:
            display_name = person[3] if person[3] != "0" else f"{person[0]} {person[1]}"
            self.listbox.insert(tk.END, f"Navn: {display_name}, Telefonnummer: {person[2]}")

    def searchPerson(self):
        search_term = self.search_entry.get().strip().lower()
        filtered_contacts = []
        for person in telefonkatalog:
            display_name = person[3] if person[3] != "0" else f"{person[0]} {person[1]}"
            if (search_term in person[0].lower() or  # fornavn
                search_term in person[1].lower() or  # etternavn
                search_term in display_name.lower()):  # kallenavn
                filtered_contacts.append(person)
        self.updateListbox(filtered_contacts)

    def openPersonDetails(self):
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Feil", "Vennligst velg en person først.")
            return
        selected_index = selected_indices[0]
        selected_person = telefonkatalog[selected_index]

        self.details_window = tk.Toplevel(self.root)
        self.details_window.title("Detaljer for person")
        self.details_window.geometry("300x250")
        self.details_window.configure(bg="lightgray")

        tk.Label(self.details_window, text=f"Fornavn: {selected_person[0]}", bg="lightgray").pack(pady=5)
        tk.Label(self.details_window, text=f"Etternavn: {selected_person[1]}", bg="lightgray").pack(pady=5)
        tk.Label(self.details_window, text=f"Telefonnummer: {selected_person[2]}", bg="lightgray").pack(pady=5)
        
        kallenavn = selected_person[3] if selected_person[3] != "0" else "Ingen"
        tk.Label(self.details_window, text=f"Kallenavn: {kallenavn}", bg="lightgray").pack(pady=5)

        tk.Button(self.details_window, text="Rediger kallenavn", command=lambda: self.editNickname(selected_index)).pack(pady=5)
        tk.Button(self.details_window, text="Slett person", command=lambda: self.deletePerson(selected_index)).pack(pady=5)
        tk.Button(self.details_window, text="Tilbake", command=self.details_window.destroy).pack(pady=5)

    def editNickname(self, index):
        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Rediger Kallenavn")
        self.edit_window.geometry("250x150")
        self.edit_window.configure(bg="lightblue")

        tk.Label(self.edit_window, text="Skriv inn nytt kallenavn:", bg="lightblue").pack(pady=5)
        self.new_nickname_entry = tk.Entry(self.edit_window)
        self.new_nickname_entry.pack(pady=5)

        tk.Button(self.edit_window, text="Lagre", command=lambda: self.saveNewNickname(index)).pack(pady=10)

    def saveNewNickname(self, index):
        new_nickname = self.new_nickname_entry.get().strip()
        if new_nickname:
            telefonkatalog[index][3] = new_nickname
            self.saveContacts()
            messagebox.showinfo("Suksess", "Kallenavn er oppdatert!")
            
            # Close the edit window
            self.edit_window.destroy()
            
            # Close the details window after editing
            if self.details_window:
                self.details_window.destroy()
            
            # Update the view window listbox
            self.updateListbox(telefonkatalog)

            # After saving, update the view window if it is open
            self.updateViewAndDetailsWindows()

    def deletePerson(self, index):
        if messagebox.askyesno("Bekreftelse", "Er du sikker på at du vil slette denne personen?"):
            del telefonkatalog[index]
            self.saveContacts()
            messagebox.showinfo("Slettet", "Personen er slettet fra katalogen.")
        
            # Close the details window after deleting
            if hasattr(self, 'details_window') and self.details_window.winfo_exists():
                self.details_window.destroy()
        
            # Update the view window listbox
            self.updateListbox(telefonkatalog)

            # After deleting, update the view window if it is open
            self.updateViewAndDetailsWindows()

    def updateViewAndDetailsWindows(self):
        # If the view window exists, destroy it first
        if hasattr(self, 'view_window') and self.view_window.winfo_exists():
            self.view_window.destroy()
    
        # Re-open the "Vis Alle Personer" window
        self.visAllePersoner()


    def saveContacts(self):
        with open(data_file, "w") as f:
            for person in telefonkatalog:
                f.write(",".join(person) + "\n")

    def loadContacts(self):
        if os.path.exists(data_file):
            with open(data_file, "r") as f:
                for line in f:
                    person_data = line.strip().split(",")
                    telefonkatalog.append(person_data)

    def exitApp(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = TelefonKatalogApp(root)
    root.mainloop()
