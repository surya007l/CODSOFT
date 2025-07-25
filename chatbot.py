import datetime
import random

def simple_chatbot():
    
    rules = {
        ("hello", "hi", "hey", "greetings"): [
            "Hello there! How can I help you today?",
            "Hi! What can I do for you?",
            "Hey! Nice to meet you."
        ],
        ("how are you", "how's it going"): [
            "I'm just a bunch of code, but I'm doing great! Thanks for asking.",
            "I'm functioning as expected. How about you?",
            "Doing well, thank you!"
        ],
        ("what is your name", "who are you"): [
            "I am a simple rule-based chatbot created to assist you.",
            "You can call me ChatBot.",
            "I'm your friendly neighborhood chatbot."
        ],
        ("what can you do", "help"): [
            "I can answer simple questions based on my rules.",
            "You can ask me things like 'what is your name', 'how are you', 'what time is it', or say 'hello'.",
            "I'm here to have a simple conversation with you. Try asking me something!"
        ],
        ("time", "what time is it"): [
            f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}.",
        ],
        ("date", "what is the date"): [
            f"Today's date is {datetime.datetime.now().strftime('%A, %B %d, %Y')}.",
        ],
        ("bye", "goodbye", "exit"): [
            "Goodbye! Have a great day.",
            "Farewell! Come back soon.",
            "Bye-bye!"
        ],
        
        "default": [
            "I'm sorry, I don't understand that. Could you rephrase?",
            "I'm not sure how to respond to that.",
            "My apologies, I didn't get that. Can you ask me something else?"
        ]
    }

    print("Chatbot: Hello! I'm a simple chatbot. Type 'bye' to exit.")
    print("---------------------------------------------------------")

    
    while True:
       
        user_input = input("You: ").lower().strip()

        
        response = ""
        for keywords, responses in rules.items():
            
            if isinstance(keywords, tuple):
                for keyword in keywords:
                    if keyword in user_input:
                        response = random.choice(responses)
                        break
            if response:
                break

        
        if not response:
            response = random.choice(rules["default"])

        
        print(f"Chatbot: {response}")

        
        if any(exit_word in user_input for exit_word in ("bye", "goodbye", "exit")):
            break

if __name__ == "__main__":
    simple_chatbot()