import tkinter as tk
from tkinter import messagebox
import os
import random
import string
import time
import threading

class SecretCodeChallenge:
    def __init__(self, root):
        self.root = root
        self.root.title("!!! WARNUNG !!!")
        self.root.configure(bg="black")
        self.root.state("zoomed")  # Fenster maximiert

        # Zufälligen 5-stelligen Code erzeugen
        self.secret_code = ''.join(random.choices(string.digits, k=5))
        self.create_secret_file()

        self.time_remaining = 5 * 60  # 5 Minuten für den Timer

        # UI Elemente
        self.label = tk.Label(
            root,
            text="Es wurde ein geheimes Text-Dokument in deinem Explorer erstellt.\n"
                "Finde es und schreibe den Code hier rein.",
            font=("Courier", 16),
            fg="green",  # Schriftfarbe grün
            bg="black",
            justify="center"
        )
        self.label.pack(pady=50)

        self.entry = tk.Entry(root, font=("Courier", 14), fg="green", bg="black", insertbackground="green", width=30)
        self.entry.pack()

        self.submit_button = tk.Button(root, text="Eingeben", command=self.check_code, fg="green", bg="black")
        self.submit_button.pack(pady=10)

        self.timer_label = tk.Label(root, text="", font=("Courier", 14), fg="green", bg="black")
        self.timer_label.pack(pady=20)

        # Überwachungs-Label
        self.watch_label = tk.Label(root, text="Du wirst beobachtet...", font=("Courier", 16), fg="green", bg="black")
        self.watch_label.pack(side="bottom", pady=10)

        self.update_timer()

        # Thread für "Du wirst beobachtet"-Effekt
        self.watch_thread = threading.Thread(target=self.watch_effect)
        self.watch_thread.daemon = True
        self.watch_thread.start()

        # Thread für "Fenster flackern"
        self.flicker_thread = threading.Thread(target=self.flicker_effect)
        self.flicker_thread.daemon = True
        self.flicker_thread.start()

        # Thread für "Textanimationen"
        self.text_animation_thread = threading.Thread(target=self.text_animation)
        self.text_animation_thread.daemon = True
        self.text_animation_thread.start()

        # Geheimnisvolle Nachrichten
        self.secret_messages = [
            "Der Code... er verändert sich mit dir.",
            "Bist du sicher, dass du den richtigen Code hast?",
            "Warum hast du noch nicht gefunden, was du suchst?",
            "Die Zeit läuft... schneller als du denkst."
        ]
        self.secret_message_thread = threading.Thread(target=self.display_secret_messages)
        self.secret_message_thread.daemon = True
        self.secret_message_thread.start()

    def create_secret_file(self):
        # Desktop-Pfad des Benutzers ermitteln
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        filename = "SECRET_CODE.txt"
        filepath = os.path.join(desktop_path, filename)

        # Datei mit Code auf dem Desktop erstellen
        with open(filepath, "w") as file:
            file.write(f"CODE: {self.secret_code}\n\nFinde mich und tippe den Code in das Programm ein...")

        # Geben Sie den Pfad der erstellten Datei im Terminal aus
        print(f"Die geheime Datei wurde gespeichert unter: {filepath}")

    def check_code(self):
        user_input = self.entry.get().strip()
        if user_input == self.secret_code:
            messagebox.showinfo("Erfolg", "✅ Richtig! Du hast den geheimen Code gefunden!")
            self.root.quit()
        else:
            # Fehlerfeedback – Fenster flackert, wenn der Code falsch ist
            self.flicker_error_effect()
            messagebox.showerror("Falsch", "❌ Falscher Code. Versuch es nochmal.")

    def flicker_effect(self):
        """Fenster flackert alle paar Sekunden zwischen verschiedenen Farben."""
        while True:
            time.sleep(random.randint(1, 5))
            self.root.configure(bg="black")
            self.label.config(bg="black")
            time.sleep(random.randint(1, 3))
            self.root.configure(bg="red")
            self.label.config(bg="red")

    def flicker_error_effect(self):
        """Fehlerfeedback: Fenster flackert rot, wenn der Code falsch ist."""
        for _ in range(5):
            self.root.configure(bg="red")
            self.label.config(bg="red")
            time.sleep(0.2)
            self.root.configure(bg="black")
            self.label.config(bg="black")
            time.sleep(0.2)

    def update_timer(self):
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        self.timer_label.config(text=f"Zeit verbleibend: {minutes:02d}:{seconds:02d}")

        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.root.after(1000, self.update_timer)  # Wiederholt sich jede Sekunde
        else:
            messagebox.showwarning("Zeit abgelaufen", "⏰ Die Zeit ist um! Du hast versagt...")
            self.root.quit()

    def watch_effect(self):
        """Dieser Effekt zeigt einen 'Du wirst beobachtet'-Hinweis an, der in zufälligen Intervallen verschwindet und erscheint."""
        while True:
            time.sleep(random.randint(5, 10))  # Der Hinweis erscheint zufällig alle 5-10 Sekunden
            self.watch_label.config(fg="red")  # Textfarbe rot für mehr Dramatik
            time.sleep(1)
            self.watch_label.config(fg="green")  # Textfarbe zurück auf grün
            time.sleep(2)

    def text_animation(self):
        """Text wird animiert, indem er Zeichen für Zeichen erscheint."""
        text = "Finde den geheimen Code und überlebe die Herausforderung..."
        for i in range(len(text)):
            self.label.config(text=text[:i+1])
            time.sleep(0.1)

    def display_secret_messages(self):
        """Zeigt geheimnisvolle Nachrichten zufällig an."""
        while True:
            time.sleep(random.randint(10, 20))  # Nachrichten erscheinen alle 10-20 Sekunden
            message = random.choice(self.secret_messages)
            self.label.config(text=message)
            time.sleep(3)
            self.label.config(text="Es wurde ein geheimes Text-Dokument in deinem Explorer erstellt.\n"
                                   "Finde es und schreibe den Code hier rein.")  # Originaltext zurücksetzen

# Startpunkt
if __name__ == "__main__":
    root = tk.Tk()
    app = SecretCodeChallenge(root)
    root.mainloop()
