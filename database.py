# Simple in-memory storage (no MongoDB)

storage = {}

def save_notes(topic, notes):
    storage[topic] = notes

def get_notes(topic):
    return storage.get(topic)