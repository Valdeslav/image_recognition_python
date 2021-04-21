import os
import tkinter as tk
from dotenv import load_dotenv
from app.app import App

if __name__ == "__main__":
    dotenv_path = os.path.join(os.path.dirname(__file__), 'project.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    app = App()
    tk.mainloop()


#i = Image.open('images/rect.png')
#resized_img = i.resize((10, 10))
#iar = np.array(resized_img)
#print(iar)

#plt.imshow(iar)

#plt.show()