#Storing log data and exporting as plaintext
import tkinter as tk
from datetime import datetime

skins = {
  "City Logger Entertainment System": {
      "bg": "#2e2e2e",
      "button": "#dd2020",
      "button_text": "#ffffff",
      "start": "#0d0c0c",
      "stop": "#a5a2a2",
  },
  "Super City Logger Entertainment System": {
      "bg": "#cfcfcf",
      "button": "#b5b6e4",
      "button_text": "#333333",
      "start": "#cec9cc",
      "stop": "#908a99",
  }
}

Site = ['ADM', 'TECH', 'ZEB', 'BME', 'CAN/JH', 'CME', 'GCE', 'HS', 'PVE', 'SKY']

#this is going to be hidden but visible in text file
distances = {
#ADM > TECH = 2.5
    ('ADM', 'TECH'): 2,
    ('ADM', 'ZEB'): 3,
    ('ADM', 'BME'): 2,
    ('ADM', 'CAN/JH'): 1,
    ('ADM', 'CME'): 7,
    ('ADM', 'HS'): 1,
    ('ADM', 'PVE'): 7,
    ('ADM', 'SKY'): 1,
    ('TECH', 'ZEB'): 1,
    ('TECH', "BME"): 4,
    ('TECH', 'CAN/JH'): 3,
    ('TECH', 'CME'): 7,
    ('TECH', 'GCE'): 3,
    #TECH > HS = 3.5
    ('TECH', 'HS'): 3,
    ('TECH', 'PVE'): 7,
    ('TECH', 'SKY'): 2.5,
    ('ZEB', 'BME'): 4,
    ('ZEB', 'CAN/JH'): 3,
    ('ZEB', 'CME'): 7,
    ('ZEB', 'GCE'): 2,
    ('ZEB', 'HS'): 2,
    ('ZEB', 'PVE'): 7,
    #ZEB > SKY = 2.5
    ('ZEB', 'SKY'): 2,
    ('BME', 'CAN/JH'): 2,
    ('BME', 'CME'): 4,
    ('BME', 'GCE'): 3,
    #BME > HS = 2.5
    ('BME', 'HS'): 2,
    ('BME', 'PVE'): 4,
    #BME > SKY = 2.5
    ('BME', 'SKY'): 2,
    ('CAN/JH', 'CME'): 5.5,
    ('CAN/JH', 'GCE'): 1,
    ('CAN/JH', 'HS'): 1,
    #CAN/JH > PVE = 6.5
    ('CAN/JH', 'PVE'): 5,
    ('CAN/JH', 'SKY'): 1,
    ('CME', 'GCE'): 7,
    ('CME', 'HS'): 6,
    # CME > HS = 6.5
    ('CME', 'PVE'): 1,
    # CME > SKY = 6.5
    ('CME', 'SKY'): 6,
    ('GCE', 'HS'): 1,
    ('GCE', 'PVE'): 1,
    ('GCE', 'SKY'): 1,
    # HS > PVE = 6.5
    ('HS', 'PVE'): 6,
    ('HS', 'SKY'): 1,
    #PVE > SKY = 6.5
    ('PVE', 'SKY'): 6,

}

for (a, b), d in list(distances.items()):
    distances[(b, a)] = d

class SiteTracking:
    def __init__(self, master): 
        self.master = master
        self.master.title("Site 2 Site Tracking - Test")

        self.log = []
        self.is_logging = False
        self.last_city = None
        self.total_miles = 0 #initial mile tracker number
        self.city_buttons = [] #Create list to store city buttons

        # Creates city buttons 
        for city in Site:
            btn = tk.Button(master, text=city, width=20,
                            command=lambda c=city: self.city_click(c))
            btn.pack(pady=5)
            self.city_buttons.append(btn) # Store the button i nlist

        # Start and Stop
        self.start_btn = tk.Button(master, text="Start", bg='green', fg="white", #change to snes colors
                                   command=self.start_logging)
        self.start_btn.pack(pady=10)

        self.stop_btn = tk.Button(master, text="Stop", bg="red", fg='white',
                                  command=self.stop_logging)
        self.stop_btn.pack(pady=10)

        #Toggle Skins
        tk.Button(master, text="CTLES", bg="#dd2020", fg="white",
                  command=lambda: self.apply_skin("City Logger Entertainment System")).pack(pady=2)
                  
        tk.Button(master, text="Super CTLES", bg="#b5b6e4", fg="black",
                  command=lambda: self.apply_skin("Super City Logger Entertainment System")).pack(pady=2)

        #Message display on bottom
        self.output_box = tk.Text(master, height=10, width=50, state='disabled', bg='#f0f0f0')
        self.output_box.pack(pady=10)

    #Skins start 
        self.apply_skin("City Logger Entertainment System")

    #Apply skin to GUI
    def apply_skin(self, skin_name):
        skin = skins[skin_name]
        self.master.configure(bg=skin["bg"])
        self.output_box.configure(bg="white", fg="black")

        for btn in self.city_buttons:
            btn.configure(bg=skin["button"], fg=skin["button_text"])
        
        self.start_btn.configure(bg=skin["start"], fg="white")
        self.stop_btn.configure(bg=skin["stop"], fg="white")

        self.master.update_idletasks()
    
    # Message output on GUI
    def log_message(self, message):
        self.output_box.config(state='normal')
        self.output_box.insert(tk.END, message + '\n')
        self.output_box.see(tk.END)
        self.output_box.config(state='disabled')

    def start_logging(self):
        self.is_logging = True
        self.log = []
        self.last_city = None
        self.log_message("You are now logging your travel")

    def stop_logging(self):
        self.is_logging = False
        filename = f"travel_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            for entry in self.log:
                f.write(f"{entry}\n")
            f.write(f"\nTotal miles traveled: {self.total_miles} mi\n")
        self.log_message(f"Your Mileage has been saved to {filename}")
    
    def city_click(self, key):
        if not self.is_logging:
            self.log_message("Click Start to begin tracking.")
            return
        
        if self.last_city is None:
            self.last_city = key
            self.log_message(f"Starting at {self.last_city}")
        else: 
            current_city = key
            entry = f"{self.last_city} to {current_city}"

            distance = distances.get((self.last_city, current_city), 0)
            self.total_miles += distance
            
            self.log.append(f"{entry} ({distance} mi)")
            self.log_message(f"Logged: {entry}")
            
            self.last_city = current_city # Continue from the current selection

if __name__ == "__main__":
    root = tk.Tk()
    app = SiteTracking(root)
    root.mainloop()

            
        
