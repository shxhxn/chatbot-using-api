import os
import sqlite3
from typing import Optional

from google import genai

DATABASE_PATH = "chat.db"


def initialize_database(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
        """
    )
    connection.commit()


def create_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Copy .env.example to .env and export the value "
            "before starting the app."
        )
    return genai.Client(api_key=api_key)


def read_command() -> Optional[int]:
    print("\n---------- Commands ----------")
    print("1 = Ask the AI a question")
    print("2 = View history")
    print("4 = Exit")
    print("------------------------------")

    try:
        return int(input("Enter command: ").strip())
    except ValueError:
        print("Please enter a number.")
        return None


def ask_question(client: genai.Client, connection: sqlite3.Connection) -> None:
    question = input("Ask the AI: ").strip()
    if not question:
        print("Question cannot be empty.")
        return

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=question,
        )
        answer = response.text or "The model returned no text."
    except Exception as error:
        print(f"Request failed: {error}")
        return

    print(f"\n{answer}")
    connection.execute(
        "INSERT INTO chats (question, answer) VALUES (?, ?)",
        (question, answer),
    )
    connection.commit()


def show_history(connection: sqlite3.Connection) -> None:
    rows = connection.execute(
        "SELECT id, question, answer FROM chats ORDER BY id"
    ).fetchall()

    if not rows:
        print("No history found.")
        return

    for chat_id, question, answer in rows:
        print(f"\n--- Chat #{chat_id} ---")
        print(f"Question: {question}")
        print(f"Answer: {answer}")


def main() -> None:
    try:
        client = create_client()
    except RuntimeError as error:
        print(error)
        return

    with sqlite3.connect(DATABASE_PATH) as connection:
        initialize_database(connection)

        while True:
            command = read_command()

            if command == 1:
                ask_question(client, connection)
            elif command == 2:
                show_history(connection)
            elif command == 4:
                print("Goodbye!")
                break
            elif command is not None:
                print("Unknown command. Choose 1, 2, or 4.")


if __name__ == "__main__":
    main()
