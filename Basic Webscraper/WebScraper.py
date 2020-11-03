# import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# grab all pages 
for i in range(0,3):

	# Target url to scrape
	my_url = "https://www.newegg.com/p/pl?d=computer+monitor&N=100160979%20600030620&PageSize=96".format(i)

	# opening connection, grabbing the page
	uClient = uReq(my_url)

	# offloads content of uClient to a variable
	page_html = uClient.read()

	# close the client
	uClient.close()

	# html parsing
	page_soup = soup(page_html, "html.parser")

	#grabs each product
	containers = page_soup.findAll("div", {"class":"item-container"})
	container = containers[0]

	filename = "monitors.csv"
	f = open(filename, "w")

	headers = "brand, product_name, reg_price, current_price\n"
	f.write(headers)

	# Grabs information from html to convert to CSV file
	for container in containers:
		# grabs brand of product
		# needed to set brand to "None" as default bc not all items had img
		brand = "None"
		_img = container.div.div.a.img
		if _img:
			brand = _img["title"]

		# grabs name of product
		title_container = container.findAll("a", {"class":"item-title"})
		product_name = title_container[0].text

		# grabs regular price of product
		regPrice_container = container.findAll("li", {"class":"price-was"})
		reg_price = regPrice_container[0].text

		# grabs current/discount price of product
		discPrice_container = container.findAll("li", {"class":"price-current"})
		current_price = discPrice_container[0].text

		# grab link to product
		#link_container = container.findAll("a", href = true)


		# prints information to add to CSV file
		print("Brand: " + brand)
		print("Product Name: " + product_name)
		print("Reg Price: " + reg_price)
		print("Current Price: " + current_price)

		#prints text in Excel
		f.write(brand +  "," + product_name.replace(",", "|") + "," + reg_price + "," + current_price + "\n")

#close the program
f.close()