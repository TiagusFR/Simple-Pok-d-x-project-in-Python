import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk


class Window(tk.Frame):
        def __init__(self, df, master=None):
                super().__init__(master)
                master.title('Simple Pokédex')
                master.geometry('500x700')
                self.df = df
                self.pack()
                self.app_widgets()
                 
                
                
        def app_widgets(self):
                
                #Defines background standar color 
                red_bg = '#DC143C'
                dark_red_bg = '#8B0000'
                light_red_bg = '#F08080'
                
                #Sets the first frame where the logo goes
                frame1 = tk.Frame(self, width=500, height=170, bg=red_bg)
                frame1.pack()
                frame1.pack_propagate(False)
                
                logo_img = ImageTk.PhotoImage(file='pokemon_logo.png')
                logo_widget = tk.Label(frame1, image=logo_img, bg=red_bg)
                logo_widget.image = logo_img
                logo_widget.pack()
                
                #Sets the treeview where the xlsx goes
                frame2 = tk.Frame(self)
                frame2.pack(fill=tk.BOTH, expand=True)
                
                #Defines columns for the Tree Widget
                self.treev = ttk.Treeview(frame2)
                self.treev['columns'] = tuple(df.columns)
                
                #Sets column headings 
                for col in df.columns:
                        self.treev.heading(col, text=col)
                        
                #Add rows of data to the Tree widget 
                for i, row in df.iterrows():
                        self.treev.insert('', 'end',i, text=f"{i}", values=tuple(row))
                        self.treev.pack(fill= tk.BOTH, expand=True)
                        
                #Hiding the excel standard row column 
                self.treev['show'] = 'headings'
                
                #Setting scrollbar                
                hsb = ttk.Scrollbar(frame2, orient='horizontal', command=self.treev.xview)
                self.treev.configure(xscrollcommand=hsb.set)
                hsb.pack(side='bottom', fill='x')

                #Setting the bottom frame 
                frame3 = tk.Frame(self, width=500, height=290, bg=red_bg)
                frame3.pack()
                frame3.pack_propagate(False)

                #Serach widgets 
                tk.Label(frame3, pady=10,
                                     text="Serach Pokémon by it's name or number:", 
                                     font=('TkMenuFont', 14), fg='white', bg=red_bg).pack()
                self.txtPoke = tk.Entry(frame3, width=25, font=("Arial", 14))
                self.txtPoke.pack(pady=10)
                
        
               #Button 
                btnCheck = tk.Button(frame3, text='Check', 
                                     font=('TkMenuFont', 18), 
                                     fg='white', 
                                     bg=dark_red_bg,
                                     activebackground=light_red_bg, 
                                     activeforeground='black', 
                                     cursor='hand2',
                                     command = self.search_pokemon)
                btnCheck.pack()
                
        def search_pokemon(self):
                #Get the text entered in the entry widget 
                search_term = self.txtPoke.get().strip().lower()
                
                if not search_term:
                        messagebox.showwarning('Not Found', f'No Pokemon found with the name "{search_term}"')
                
                #Clear previous search results
                self.treev.delete(*self.treev.get_children())
                
                #Get all rows that contain the search item either the name or number columns
                search_results = df[(df['Name'].str.lower().str.contains(search_term)) |
                                       (df['No.'].astype(str).str.contains(search_term))]
                
                if search_results.empty:
                        messagebox.showinfo('No matches', f"No Pokémon match '{search_term}'")
                        return
                
                #Add search results to the Treeview
                for i, row in search_results.iterrows():
                        self.treev.insert('', 'end', i, text=f"{i}", values=tuple(row))
                self.treev.pack(fill=tk.BOTH, expand=True)
                        
    

                        

                        
root = tk.Tk()
root.resizable(False, False)
df = pd.read_excel("dex.xlsx")
app = Window(df, master=root)
app.mainloop()   

