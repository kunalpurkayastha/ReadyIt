from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import shutil
from sys import exit
from tkinter import messagebox
def browseFileDownload():
    try:
            import requests
    except ImportError:
        print('Requests must be installed. PLease run: pip install requests')
        exit()
    def makeUrl(afterID, subreddit):
            newUrl = subreddit.split('/.json')[0] + "/.json?after={}".format(afterID)
            return newUrl
    def splitUrl(imageUrl):
            if 'jpg' or 'gif' or 'gifv' or 'png' or 'mp4' or 'm4v' in imageUrl:
                return imageUrl.split('/')[-1]
    def downloadImage(imageUrl, imageAmount, download_progress):
            filename = splitUrl(imageUrl)
            if filename:
                r = requests.get(imageUrl, stream=True)
                with open(f"{folder_location}/{filename}", 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                download_progress.step(1)
                app.update()
            return imageAmount
    def run():
    	limit = int(count_input.get())
    	empty_message.pack()
    	app.geometry('600x500')
    	app.update()
    	download_progress = ttk.Progressbar(app, maximum=int(count_input.get()), length=200)
    	download_progress.pack()
    	waiting_message = Label(app, text=f"\nDownloading, please wait", font=('Poppins Regular', 13))
    	waiting_message.pack()
    	subreddit = url_input.get()
    	subJson = ''
    	x = 0
    	download_progress.start()
    	while x < limit:
    		if not subJson:
    			url = makeUrl('', subreddit)
    			subJson = requests.get(url, headers={'User-Agent': 'MyRedditScraper'}).json()
    			post = subJson['data']['children']
    			postCount = range(len(post))
    		else:
    			url = makeUrl(subJson['data']['after'], subreddit)
    		for i in postCount:
    			waiting_message.config(text=f"\nDownloading {x+1}/{limit}, please wait")
    			app.update()
    			imageUrl = (post[i]['data']['url'])
    			_imageUrls = []
    			_imageUrls.append(imageUrl)
    			x = downloadImage(_imageUrls[0], x+1, download_progress)
    			if x == limit:
    				break
    	download_progress.stop()
    	messagebox.showinfo("Success","Downlaoded")
    	app.geometry('600x400')
    	app.update()
    	waiting_message.pack_forget()
    	download_progress.pack_forget()
    folder_location = filedialog.askdirectory()
    run()
app = Tk()
app.title("ReadyIt")
app.geometry('600x400')
url_text = Label(app, text="\n\nEnter the subreddit URL", font=('Poppins Regular', 13))
url_input = Entry(app, width=40, font=('Poppins Regular', 13))
count_text = Label(app, text="\nEnter the number of photos you want to download:", font=('Poppins Regular', 13))
count_input = Entry(app, width=8, font=('Poppins Regular', 13))
browse_text = Label(app, text="\nBrowse location to save files", font=('Poppins Regular', 13))
browse_button = Button(app, text="Browse Location", font=('Poppins Regular', 11), command=lambda:browseFileDownload())
empty_message = Label(app, text="\n", font=('Poppins Regular', 13))
url_text.pack()
url_input.pack()
count_text.pack()
count_input.pack()
browse_text.pack()
browse_button.pack()
app.mainloop()
