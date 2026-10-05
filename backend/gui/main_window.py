import tkinter as tk
from tkinter import *
import threading
import queue
from backend.gui.animation import start_animation

class JarvisGUI:
    def __init__(self, root, audio_engine, router):
        self.root = root
        self.audio = audio_engine
        self.router = router
        self.message_queue = queue.Queue()

        root.title("Jarvis Assistant")
        root.geometry("520x700")
        root.config(bg="black")

        title = Label(root, text="JARVIS AI", font=("Arial", 28, "bold"),
                      bg="black", fg="#00aaff")
        title.pack(pady=10)

        self.canvas = tk.Canvas(root, width=350, height=350,
                                bg="black", highlightthickness=0)
        self.canvas.pack(pady=10)
        start_animation(self.canvas, root)

        Label(root, text="User:", font=("Arial", 14, "bold"),
              bg="black", fg="#00aaff").pack()
        self.user_text = StringVar()
        Label(root, textvariable=self.user_text, font=("Arial", 12),
              bg="black", fg="white", wraplength=450).pack(pady=5)

        Label(root, text="Jarvis:", font=("Arial", 14, "bold"),
              bg="black", fg="#00aaff").pack()
        self.jarvis_text = StringVar()
        Label(root, textvariable=self.jarvis_text, font=("Arial", 12),
              bg="black", fg="#00ddff", wraplength=450).pack(pady=5)

        # STORE THE BUTTON AS AN ATTRIBUTE
        self.speak_button = Button(root, text="🎤 Speak", font=("Arial", 18, "bold"),
                                   command=self.start_assistant,
                                   bg="#00aaff", fg="black", width=15)
        self.speak_button.pack(pady=20)

        Button(root, text="❌ Exit", font=("Arial", 16, "bold"),
               command=root.destroy,
               bg="#ff0033", fg="white", width=15).pack(pady=10)

        self.poll_queue()

    def poll_queue(self):
        try:
            msg = self.message_queue.get_nowait()
            if msg["type"] == "user":
                self.user_text.set(msg["content"])
            elif msg["type"] == "jarvis":
                self.jarvis_text.set(msg["content"])
            elif msg["type"] == "exit":
                self.root.after(0, self.root.destroy)
        except queue.Empty:
            pass
        self.root.after(100, self.poll_queue)

    def display_jarvis(self, text):
        self.jarvis_text.set(text)

    def start_assistant(self):
        self.speak_button.config(state="disabled")

        def worker():
            self.message_queue.put({"type": "user", "content": "Listening..."})
            query = self.audio.listen()
            self.message_queue.put({"type": "user", "content": f"You said: {query}"})

            if query != "none":
                response, should_exit = self.router.process(query)
                self.message_queue.put({"type": "jarvis", "content": response})
                self.audio.speak(response)
                if should_exit:
                    self.message_queue.put({"type": "exit", "content": ""})
            else:
                self.message_queue.put({"type": "jarvis", "content": "I didn't catch that. Please try again."})

            # Re-enable the button on the main thread
            self.root.after(0, lambda: self.speak_button.config(state="normal"))

        threading.Thread(target=worker, daemon=True).start()