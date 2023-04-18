import csv
import time
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

links_toscrapre=[]
Name_dentist= []
Profile_link=[]
Profile_email=[]
Street_D=[]
Street_D2=[]

City_D=[]
State_D=[]
Zip_D=[]


for page in range(0, 1):
    URL = f"https://iaomt.org/search-by-region/region/inside-us-canada/page/6/"
    time.sleep(2)
    
    website = requests.get(URL, headers=HEADERS)
    website.encoding = 'UTF-8'  
    doc = BeautifulSoup(website.content, 'html.parser')

for names in doc.find_all("div", attrs={"class": "listing-title"}):
    name = names.text.strip()
    if "DDS" in name:
        href = names.find('a').get('href')
        links_toscrapre.append(href)


count = 0
for links in links_toscrapre:
    URL2 = links
    New_Page= requests.get(URL2, headers=HEADERS)
    New_Page.encoding = 'UTF-8'  
    dentist_profile= BeautifulSoup(New_Page.content, 'html.parser')
    #Name
    for name_element in dentist_profile.find("h1", attrs={"class": "entry-title"}):
        if name_element:
            name = name_element.text.strip()
            Name_dentist.append(name)
            print(name)
        else:
            print("Name not found")
    #url
    try:
        url_element = dentist_profile.find('div', class_='wpbdp-field-display wpbdp-field wpbdp-field-value field-display field-value wpbdp-field-website_url wpbdp-field-meta wpbdp-field-type-url wpbdp-field-association-meta').find('a')
        if url_element:
            href = url_element.text.strip()
            if not href.startswith('http://') and not href.startswith('https://'):
                href = 'https://' + href
            Profile_link.append(href)
            print(href)
    except AttributeError:
        print("Website not found")
        Profile_link.append("Website not available")
    #Email 
    try:
        for email_element in dentist_profile.find('div', class_="wpbdp-field-display wpbdp-field wpbdp-field-value field-display field-value wpbdp-field-office_email wpbdp-field-meta wpbdp-field-type-textfield wpbdp-field-association-meta").find('a'):
                email = email_element.text.strip()
                Profile_email.append(email)
                print(email)
    except AttributeError:
            print("Email not found")
            Profile_email.append("Email not available")
    #Phisical Address Street 1
    try:
        Street_element = dentist_profile.find('div', class_="wpbdp-field-display wpbdp-field wpbdp-field-value field-display field-value wpbdp-field-street_1 wpbdp-field-meta wpbdp-field-type-textfield wpbdp-field-association-meta")
        if Street_element is not None:
            for street in Street_element:
                street = street.text.strip()
                Street_D.append(street)
                print(street)
                
        else:
            raise AttributeError("Street address not found")
    except AttributeError as e:
        print("Street not found")
        Street_D.append(" ")  
    except TypeError as e:
        print("Second streen not found")
        Street_D.append(" ") 

    #Address Street 2 
    try:
        Street_element2 = dentist_profile.find('div', class_="wpbdp-field-display wpbdp-field wpbdp-field-value field-display field-value wpbdp-field-street_2 wpbdp-field-meta wpbdp-field-type-textfield wpbdp-field-association-meta")
        if Street_element2 is not None:
            for street2 in Street_element2:
                street2 = street2.text.strip()
                Street_D2.append(street2)
                print(street2)
                
        else:
            raise AttributeError("Second street address not found")
    except AttributeError as e:
        print("Second streen not found")
        Street_D2.append(" ")  
    except TypeError as e:
        print("Second streen not found")
        Street_D2.append(" ") 
    #City 
    try:
        for City_element in dentist_profile.find('div', class_="wpbdp-field-display wpbdp-field wpbdp-field-value field-display field-value wpbdp-field-city wpbdp-field-meta wpbdp-field-type-textfield wpbdp-field-association-meta"):
                City = City_element.text.strip()
                City_D.append(City)
                print(City)
    except AttributeError:
        print("City not found")
        City_D.append(" ")
    except TypeError as e:
        print("City not found")
        City_D.append(" ")     
    #State
    try:
        for State_element in dentist_profile.find('div', class_="wpbdp-field-display wpbdp-field wpbdp-field-value field-display field-value wpbdp-field-state wpbdp-field-meta wpbdp-field-type-textfield wpbdp-field-association-meta"):
                State = State_element.text.strip()
                State_D.append(State)
                print(State)
    except AttributeError:
        print("State not found")
        State_D.append(" ")
    except TypeError as e:
        print("State not found")
        State_D.append(" ")       
    #Zip
    try:
        for Zip_element in dentist_profile.find('div', class_="wpbdp-field-display wpbdp-field wpbdp-field-value field-display field-value wpbdp-field-zip__postal_code wpbdp-field-meta wpbdp-field-type-textfield wpbdp-field-association-meta"):
                Zip = Zip_element.text.strip()
                Zip_D.append(Zip)
                print(Zip)
    except AttributeError as e:
        print("Zip not found")
        Zip_D.append(" ")  
    except TypeError as e:
        print("Zip not found")
        Zip_D.append(" ") 



    count += 1
    print(count)


with open('result6D.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name', 'Profile Link', 'Profile Email',"Street",'Street 2', 'City','State','Zip Code'])
    for i in range(len(Name_dentist)):
        writer.writerow([Name_dentist[i], Profile_link[i], Profile_email[i],Street_D[i],Street_D2[i],City_D[i],State_D[i],Zip_D[i]])