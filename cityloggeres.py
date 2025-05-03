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

city_names = ['Aspen', 'Boulder', 'Colorado Springs', 'Denver', 'GCE', 'SKY']


#this is going to be hidden but visible in text file
distances = {
    ('Aspen', 'Boulder'): 210,
    ('Aspen', 'Colorado Springs'): 265,
    ('Aspen', 'Denver'): 198,
    ('Boulder', 'Colorado Springs'): 103,
    ('Boulder', 'Denver'): 30,
    ('Colorado Springs', 'Denver'): 69,
}
# Reverse the permutations (Myko look at this math, ensures you only need to enter school list once ie "one axis of the train timetable")
for (a, b), d in list(distances.items()):
    distances[(b, a)] = d

class CityLogger:
    def __init__(self, master): 
        self.master = master
        self.master.title("City Travel Logger Entertainment System")

        self.log = []
        self.is_logging = False
        self.last_city = None
        self.total_miles = 0 #initial mile tracker number
        self.city_buttons = [] #Create list to store city buttons

        # Creates city buttons 
        for city in city_names:
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
        self.log_message(f"Your CityLog has been saved to {filename}")
    
    def city_click(self, key):
        if not self.is_logging:
            self.log_message("Click Start to begin your CityLog")
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
    app = CityLogger(root)
    root.mainloop()

            
        
