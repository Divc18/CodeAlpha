import nltk
from nltk.chat.util import Chat, reflections
import spacy
import tkinter as tk
from tkinter import scrolledtext, ttk


nlp = spacy.load("en_core_web_sm")

pairs = [
    [
        r"(hi|hello|hey|hola|howdy)(.*)",
        ["Hello! How can I assist you today?", "Hi there, how can I help?"]
    ],
    [
        r"what is your name ?",
        ["I am a chatbot created by a Python enthusiast. You can call me ChatBot."]
    ],
    [
        r"how are you ?",
        ["I'm just a bunch of code, but I'm functioning as expected! How about you?", "I'm doing great, thank you! How are you doing?"]
    ],
    [
        r"sorry (.*)",
        ["It's alright.", "No problem at all!", "Don't worry about it."]
    ],
    [
        r"I am (.*) (good|well|okay|ok)",
        ["Glad to hear that!", "Good to know!", "That's great!"]
    ],
    [
        r"(.*) (help|assistance|support)",
        ["Sure, I'm here to help! What do you need assistance with?", "I'm here for you. What do you need help with?"]
    ],
    [
        r"(.*) (created|made|built) (.*)",
        ["I was created by a Python enthusiast. Pretty cool, right?", "I'm a result of some nifty programming."]
    ],
    [
        r"(.*) (weather|temperature) in (.*)",
        ["I can't provide real-time weather updates right now, but you can check a weather website for that information."]
    ],
    [
        r"quit",
        ["Bye! Take care.", "Goodbye! Have a great day!"]
    ],
    [
        r"(.*)",
        ["I'm sorry, I don't understand that. Could you please rephrase?", "Could you please say that in a different way?", "Let's talk about something else!"]
    ]
]


chatbot = Chat(pairs, reflections)
context = {}

def process_input(user_input):
    doc = nlp(user_input)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def respond(user_input):
    entities = process_input(user_input)
    if entities:
        for entity in entities:
            if entity[1] == "PERSON":
                context['name'] = entity[0]
                return f"Nice to meet you, {entity[0]}! How can I assist you today?"
            elif entity[1] == "GPE":
                context['location'] = entity[0]
                return f"How's the weather in {entity[0]}? How can I assist you today?"
    
    response = chatbot.respond(user_input)
    return response

def send_message(event=None):
    user_input = user_input_var.get()
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, "You: " + user_input + "\n", "user")
    user_input_var.set("")
    
    if user_input.lower() == "quit":
        chat_log.insert(tk.END, "ChatBot: Goodbye! Have a great day!\n", "bot")
        root.after(2000, root.quit)
    else:
        response = respond(user_input)
        chat_log.insert(tk.END, "ChatBot: " + response + "\n", "bot")
    
    chat_log.config(state=tk.DISABLED)
    chat_log.yview(tk.END)

# Tkinter
root = tk.Tk()
root.title("ChatBot")
root.geometry("500x600")
root.configure(bg="#2e2e2e")


style = ttk.Style()
style.configure("TFrame", background="#2e2e2e")
style.configure("TLabel", background="#2e2e2e", foreground="#ffffff")
style.configure("TButton", background="#4caf50", foreground="#ffffff", font=("Helvetica", 10, "bold"))

# frames
top_frame = ttk.Frame(root, padding="10")
top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

bottom_frame = ttk.Frame(root, padding="10")
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Chat log
chat_log = scrolledtext.ScrolledText(top_frame, state=tk.DISABLED, height=20, width=60, wrap=tk.WORD, bg="#1e1e1e", fg="#ffffff", font=("Helvetica", 12))
chat_log.pack(fill=tk.BOTH, expand=True)

# Entry box
user_input_var = tk.StringVar()
entry_box = ttk.Entry(bottom_frame, textvariable=user_input_var, width=50, font=("Helvetica", 12))
entry_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

send_button = ttk.Button(bottom_frame, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT)

root.bind("<Return>", send_message)

chat_log.tag_config("user", foreground="#4caf50", font=("Helvetica", 12, "bold"))
chat_log.tag_config("bot", foreground="#42a5f5", font=("Helvetica", 12, "italic"))

root.mainloop()
