from google import genai
import sqlite3

conn = sqlite3.connect("chat.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               question TEXT,
               answer TEXT)
               """)

conn.commit()

client = genai.Client(api_key="AIzaSyCUsnfSswjWmcz7MA7O7hIN6JB3LVutmJ8")

while True:
  print("----------commands----------")
  print("1 = Ask the AI question.")
  print("2 = View History.")
  print("4 = Exit.")
  print("----------------------------")
  cmd = int(input("Enter command : "))

  if cmd == 1:
    question = input("Ask question to the AI : ")
    response = client.models.generate_content(
      model = 'gemini-2.5-flash',
      contents = question
    )
    print(response.text) 
    cursor.execute(
      """
     INSERT INTO chats (question, answer)
     VALUES(? , ?)
      """,
      (question, response.text)
    )
    conn.commit()

  elif cmd == 4:
    break

  elif cmd == 2:
    print("Fetching chat history...")
    cursor.execute("""
    SELECT id, question, answer
    FROM chats
    ORDER BY id
    """)

    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No history found.")

    else:
        for row in rows:
            print("\n--------------------")
            print(f"Chat #{row[0]}")
            print("Question:", row[1])
            print("Answer:", row[2])
            print("--------------------")


  
  else :
    print("Enter valid commands only.")