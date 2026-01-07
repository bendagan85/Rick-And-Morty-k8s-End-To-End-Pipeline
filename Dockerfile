# 1. Base Image - אנחנו מתחילים מלינוקס שכבר מותקן עליו פייתון 3.9
# משתמשים בגרסת slim כי היא קלה ומהירה יותר
FROM python:3.9-slim

# 2. Work Directory - מגדירים את תיקיית העבודה בתוך הקונטיינר
WORKDIR /app

# 3. Copy Requirements - מעתיקים קודם רק את קובץ הדרישות
# למה? כדי לנצל את ה-Cache של דוקר. אם לא שינית ספריות, השלב הזה לא ירוץ מחדש
COPY requirements.txt .

# 4. Install Dependencies - מתקינים את הספריות
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy Code - עכשיו מעתיקים את שאר הקוד (main.py) לתוך הקונטיינר
COPY . .

# 6. Expose Port - מצהירים שהקונטיינר מאזין בפורט 8080
EXPOSE 8080

# 7. Command - הפקודה שתרוץ כשהקונטיינר יעלה
CMD ["python", "app.py"]
