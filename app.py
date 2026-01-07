from flask import Flask, jsonify
import requests
import csv  # <-- הוספנו: ספרייה לעבודה עם CSV

# יצירת מופע של האפליקציה
app = Flask(__name__)

# --- לוגיקה לשליפת מידע ---
def get_rick_and_morty_data():
    url = "https://rickandmortyapi.com/api/character"
    params = {
        "status": "alive",
        "species": "human"
    }
    all_filtered_characters = []
    
    # ריצה על כל העמודים
    while url:
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            characters = data.get('results', [])
            
            for char in characters:
                origin_name = char.get('origin', {}).get('name', '')
                # בדיקה שהדמות מכדור הארץ
                if 'Earth' in origin_name:
                    character_data = {
                        "Name": char.get('name'),
                        "Location": char.get('location', {}).get('name'),
                        "Image Link": char.get('image')
                    }
                    all_filtered_characters.append(character_data)

            # מעבר לעמוד הבא
            url = data.get('info', {}).get('next')
            if url:
                params = {} 

        except Exception as e:
            print(f"Error: {e}")
            break
            
    return all_filtered_characters

# --- פונקציה לשמירת CSV (דרישת חובה במטלה) ---
def save_to_csv(data):
    filename = 'rick_and_morty_results.csv'
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ["Name", "Location", "Image Link"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(data)
        print(f"SUCCESS: CSV file '{filename}' created inside the container.")
    except Exception as e:
        print(f"ERROR: Could not save CSV: {e}")

# --- הגדרת הנתיבים (Routes) ---

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/v1/characters', methods=['GET'])
def get_characters():
    # 1. שליפת המידע
    data = get_rick_and_morty_data()
    
    # 2. שמירה לקובץ CSV (כדי לעמוד בדרישות המטלה)
    save_to_csv(data)
    
    # 3. החזרת JSON (כדי לעמוד בבונוס)
    return jsonify(data), 200

# --- הרצת השרת ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)