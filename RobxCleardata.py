import os

# Path to RobloxCookies.dat
cookie_file = os.path.join(os.environ['LOCALAPPDATA'], "Roblox", "LocalStorage", "RobloxCookies.dat")

if os.path.exists(cookie_file):
    try:
        os.remove(cookie_file)
        print("RobloxCookies.dat deleted successfully.")
    except Exception as e:
        print("Error deleting RobloxCookies.dat:", e)
else:
    print("RobloxCookies.dat not found.")