# Input below the city or town in quotation marks that you would like to search
# Then enter the profession you are looking for below that in quoatation marks as well


area = "vaughan"

profession = "accountant"



# You can also input below the range in km that you would like to search from
# the area you selected above
# You can choose distances of 30, 40, 50, 60, 70, 80, 90, or 100

distance = "30"

# Run the code

starturl = "http://411.ca/search/?lang=en&q=" + profession + "+" + area + "&fdist=" + distance + "&st=business&p="

import urllib

# Getting Number of Pages

htmlfile3 = urllib.urlopen(starturl)
htmltext3 = htmlfile3.read()

start_quote3 = htmltext3.find('timing_business">')
end_quote3 = htmltext3.find(' r', start_quote3)
totalcount = htmltext3[start_quote3 + 29:end_quote3]

if totalcount.find(',') != -1:
    totalcount = list(totalcount)
    totalcount.remove(',')
    totalcount = ''.join(totalcount)

# Changes a string of numbers to an integer
def num(s):
    try:
        return int(s)
    except ValueError:
        import sys
        print "No results found, ensure correct spelling"
        sys.exit("No results found, ensure correct spelling")

totalcount = num(totalcount)

if totalcount % 25 == 0:
    InputNumberOfPagesHere = totalcount / 25
else:
    InputNumberOfPagesHere = (totalcount / 25 + 1)



# Getting the source codes

def mainfunction(numberofpages):
    n = 1
    peoplecount = 25
    finalstring = ""
    while n <= numberofpages:
        urlstring = starturl + str(n)
        htmlfile = urllib.urlopen(urlstring)
        htmltext = htmlfile.read()
        print "Extracting page " + str(n) + " of " + str(numberofpages)
        n += 1

        # Counting the number of people on the page
        
        if n == numberofpages:
            peoplecount = htmltext.count('itemprop="name" content', 0, len(htmltext))

        #Creating an array for the links of people on each page
        def target(page):
            a = 1
            x = []
            while a <= peoplecount:
                a = a+1
                if n == 2 and a == 9:
                    start_link = page.find('<div class="ltitle">')
                    page = page[start_link+1:]

                    start_link = page.find('<div class="ltitle">')
                    start_quote = page.find('href', start_link)+6
                    end_quote = page.find('"', start_quote)
                    url = page[start_quote:end_quote]
                    page = page[end_quote:]
                    x.append( "http://www.411.ca" + url)
                else:
                    start_link = page.find('<div class="ltitle">')
                    start_quote = page.find('href', start_link)+6
                    end_quote = page.find('"', start_quote)
                    url = page[start_quote:end_quote]
                    page = page[end_quote:]
                    x.append( "http://www.411.ca" + url)
                
            return x
        


        # Setting array of links to variable
        
        y = target(htmltext)

        # Extracting from personal pages
        
        def extract():
            counter = 0
            k = ""
            while counter < peoplecount:
                z = ""
                htmlfile2 = urllib.urlopen(y[counter])
                htmltext2 = htmlfile2.read()
                
                # Name
                start_quote = htmltext2.find('itemprop="name">')
                end_quote = htmltext2.find('</h1>', start_quote)
                name = htmltext2[start_quote + 16:end_quote]
                if name.find(',') != -1:
                        name = list(name)
                        name = [x for x in name if x != ","]
                        name = ''.join(name)
                z = name + ","

                # CityIn
                start_quote = htmltext2.find('addressLocality')
                if start_quote > 0:
                    end_quote = htmltext2.find('</span>', start_quote)
                    cityin = htmltext2[start_quote + 17:end_quote]
                    if cityin.find(',') != -1:
                        cityin = list(cityin)
                        cityin = [x for x in cityin if x != ","]
                        cityin = ''.join(cityin)
                    z = z + cityin + ","
                else:
                    cityin = "No City Listed"
                    z = z + cityin + ","


                # Adress
                start_quote = htmltext2.find('streetAddress')
                if start_quote > 0:
                    end_quote = htmltext2.find('</div>', start_quote)
                    adress = htmltext2[start_quote + 15:end_quote]
                    if adress.find(',') != -1:
                        adress = list(adress)
                        adress = [x for x in adress if x != ","]
                        adress = ''.join(adress)
                    z = z + adress + ","
                    
                else:
                    adress = "No Adress Listed"
                    z = z + adress + ","

                # Postalcode
                start_quote = htmltext2.find('"postalCode"')
                if start_quote > 0 :
                    end_quote = htmltext2.find('</div>', start_quote)
                    postalcode = htmltext2[start_quote + 13:end_quote]
                    if postalcode.find(',') != -1:
                        postalcode = list(postalcode)
                        postalcode = [x for x in postalcode if x != ","]
                        postalcode = ''.join(postalcode)
                    z = z + postalcode + ","
                else:
                    postalcode = "No Postal Code Listed"
                    z = z + postalcode + ","

                # Telephone
                start_quote = htmltext2.find('telephone"')
                if start_quote > 0 :
                    end_quote = htmltext2.find('</span>', start_quote)
                    phone = htmltext2[start_quote + 11:end_quote]
                    z = z + phone + ","
                else:
                    phone = "No Phone Number Listed"
                    z = z + phone + ","

                # Email
                start_quote = htmltext2.find('mailto:')
                if start_quote > 0 :
                    end_quote = htmltext2.find('"', start_quote)
                    email = htmltext2[start_quote + 7:end_quote]
                    z = z + email
                else:
                    email = "No Email Listed"
                    z = z + email
                    
                k = k + z + "\n"
                counter = counter+1
            
            return k
    
        
        finalstring = finalstring + extract()
    
    return finalstring


final = mainfunction(InputNumberOfPagesHere)



# Exporting

with open(area + ".csv", "w") as text_file:
    text_file.write(final)



print "Done, you can now open the file in Microsoft Excel"

# this is the end of the program and an excel document with all of the results will be saved to the same folder in which this code is saved


# End of Code
