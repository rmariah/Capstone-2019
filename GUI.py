import tkinter

window = tkinter.Tk()
window.title("News Feed Generator")

def displayTwitter():
	window = tkinter.Tk()
	window.title("Related Tweets")
	
	top_frame = tkinter.Frame(window).grid()
	bottom_frame = tkinter.Frame(window).grid(columnspan = 7, row = 10)
	
	tkinter.Label(window, text = "This is the twitter page!").grid(columnspan = 10, row = 2)
	
def displayNews():
	window = tkinter.Tk()
	window.title("Related News")
	
	top_frame = tkinter.Frame(window).grid()
	bottom_frame = tkinter.Frame(window).grid(columnspan = 7, row = 10)
	
	tkinter.Label(window, text = "This is the news page!").grid(columnspan = 10, row = 2)

# creating 2 frames TOP and BOTTOM
top_frame = tkinter.Frame(window).grid()
bottom_frame = tkinter.Frame(window).grid(columnspan = 7, row = 10)

# now, create some widgets in the top_frame and bottom_frame
tkinter.Label(window, text = "Title for the Page", fg = "white", bg = "blue").grid(columnspan = 5, row = 0, column = 2)


tkinter.Label(window, text = "Enter twitter information:", fg = "black").grid (row = 2, column = 0)
searchField = tkinter.Entry(window).grid(row = 3, column = 0)
btn1 = tkinter.Button(window, text = "Search for tweets", command = displayTwitter, fg = "black").grid (columnspan = 2, row = 4, column = 0)

tkinter.Label(window, text = "Enter news information:", fg = "black").grid (row = 2, column = 7)
searchField2 = tkinter.Entry(window).grid(row = 3, column = 7)
btn2 = tkinter.Button(window, text = "Search for news", command = displayNews, fg = "black").grid (columnspan = 2, row = 4, column = 7)


window.mainloop()