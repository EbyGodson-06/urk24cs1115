import sqlite3
from datetime import datetime

# Database connection
conn = sqlite3.connect("subscriptions.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    renewal_date TEXT NOT NULL,
    active INTEGER DEFAULT 1
)
""")
conn.commit()

def add_subscription(name, price, renewal_date):
    """Add a new subscription."""
    cursor.execute("INSERT INTO subscriptions (name, price, renewal_date) VALUES (?, ?, ?)", 
                   (name, price, renewal_date))
    conn.commit()
    print(f"Subscription '{name}' added successfully.")

def view_subscriptions():
    """View all active subscriptions."""
    cursor.execute("SELECT * FROM subscriptions WHERE active=1")
    subs = cursor.fetchall()
    if not subs:
        print("No active subscriptions.")
    else:
        print("\nActive Subscriptions:")
        for sub in subs:
            print(f"{sub[0]}. {sub[1]} - ${sub[2]:.2f}, Renew on {sub[3]}")

def cancel_subscription(sub_id):
    """Cancel a subscription."""
    cursor.execute("UPDATE subscriptions SET active=0 WHERE id=?", (sub_id,))
    conn.commit()
    print(f"Subscription ID {sub_id} canceled.")

def check_subscription(sub_id):
    """Check details of a specific subscription."""
    cursor.execute("SELECT * FROM subscriptions WHERE id=?", (sub_id,))
    sub = cursor.fetchone()
    if sub:
        status = "Active" if sub[4] else "Canceled"
        print(f"ID: {sub[0]}\nName: {sub[1]}\nPrice: ${sub[2]:.2f}\nRenewal Date: {sub[3]}\nStatus: {status}")
    else:
        print("Subscription not found.")

# Example usage
if __name__ == "__main__":
    while True:
        print("\nSubscription Management System")
        print("1. Add Subscription")
        print("2. View Active Subscriptions")
        print("3. Cancel Subscription")
        print("4. Check Subscription Details")
        print("5. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            name = input("Enter subscription name: ")
            price = float(input("Enter subscription price: "))
            renewal_date = input("Enter renewal date (YYYY-MM-DD): ")
            add_subscription(name, price, renewal_date)
        
        elif choice == "2":
            view_subscriptions()
        
        elif choice == "3":
            sub_id = int(input("Enter subscription ID to cancel: "))
            cancel_subscription(sub_id)
        
        elif choice == "4":
            sub_id = int(input("Enter subscription ID to check: "))
            check_subscription(sub_id)
        
        elif choice == "5":
            print("Exiting...")
            conn.close()
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 5.")
