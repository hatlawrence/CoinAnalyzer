import requests
import json
import operator
import dominate
from dominate.tags import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

print("begin harvesting")
while True:
    #print time for testing purposes
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)

    #set up connection to google sheet
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("cryptodata").sheet1

    #get crypto data from site
    siteDataDownload = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false").text
    #convert to json and store as python dictionary
    siteDataDownload = json.loads(siteDataDownload)
    #get length of dictionary
    listLength = len(siteDataDownload)

    #declare necessary variables
    counter = 0
    ratioList = []

    #create coin data object
    class coinDataObj:
        def __init__(self, id, ratio):
            self.id = id
            self.ratio = ratio

    while counter < listLength:
        #get current coinID in variable
        coinID = siteDataDownload[counter]['id']

        if siteDataDownload[counter]['market_cap'] == 0:
            #exclude coins with 0 cap to prevent float division error 
            #if we ever need to exclude coins for any reason, we can do it here
            #add something like coinID == 'compound-usd-coin' to exclude
            counter += 1
        else:
            #variables for volume and market cap
            coinCap = siteDataDownload[counter]['market_cap']
            coinVol = siteDataDownload[counter]['total_volume']

            #calculate ratio
            volRatio = (coinVol/coinCap) * 100

            #create object for current coin
            currentCoin = coinDataObj(coinID, volRatio)

            #append current coin to ratio list
            ratioList.append(currentCoin)

            #counter up
            counter += 1


    #we are going to use the sorted list again!
    #this tracks a unique metric worth saving...
    #sort list by id of ratio
    sortedList = sorted(ratioList, key=operator.attrgetter("ratio"))

    #get length of list
    spreadListLength = len(sortedList)

    #print(spreadListLength)


    #begin google sheet entry
    #this takes our list of coins, ranked by the cap / vol ratio
    #and stores it in a spreadsheet
    #it finds a column for the coin, or creates one
    #then starts stacking ratios at the bottom of the data set
    #Harold Train-Lawrence

    #create counter for adding data to spreadsheet
    spreadCounter = 249

    #get number of columns
    numCols = sheet.col_count

    #pause so we don't exceed free drive api limits
    time.sleep(2)

    #get number of rows
    numRows = sheet.row_count

    #pause so we don't exceed free drive api limits
    time.sleep(2)

    #go through top 25 by market cap and dump the stats
    while spreadCounter > 224:
        currentCoinID = sortedList[spreadCounter].id
        currentCoinRatio = sortedList[spreadCounter].ratio

        #print place in list
        print(spreadCounter)
        #print data for testing purposes
        print(currentCoinID)
        print(currentCoinRatio)
        #print time for testing purposes
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        
        print(current_time)
        

        

        #create counter for going through column headers
        colCounter = 1

        #flag for detecting new coins
        columnMatch = False

        #hard code counter jumps for efficiency?
        #could be done here
        #order of sheets in spreadsheet would need to stay same
        

        #check each column for the coins name
        while colCounter < numCols:
            #errors happen here, so we are going to try/except for connectoin error
            try:
                cell = sheet.cell(1, colCounter).value
            except ConnectionError as error:
                        print("Error: ", error)
            except gspread.exceptions.APIError as error:
                        print("Error: ", error)


            #pause so we don't exceed drive api limits
            time.sleep(3)
            
            
            

            if currentCoinID == cell:
                print("match found, appending ratio")
                #append currentCoinRatio to current column
                ratioAddCounter = 2

                while ratioAddCounter < numRows:
                    #check 10 cells ahead to see if it is blank
                    tenCellsAhead = ratioAddCounter + 10

                    #errors happen here, so we are going to try/except for connectoin error

                    try:
                        checkerCell = sheet.cell(tenCellsAhead, colCounter).value
                    except ConnectionError as error:
                        print("Error: ", error)
                    except gspread.exceptions.APIError as error:
                        print("Error: ", error)


                    #pause so we don't exceed drive api limits
                    time.sleep(1.5)

                    #if it is not blank, then we set the counter to that value to skip ahead
                    if checkerCell != None:  
                        ratioAddCounter = tenCellsAhead

                    
                    #check current cell
                    #errors happen here, so we are going to try/except for connectoin error
                    try:
                        ratioCell = sheet.cell(ratioAddCounter, colCounter).value
                    except ConnectionError as error:
                        print("Error: ", error)
                    except gspread.exceptions.APIError as error:
                        print("Error: ", error)
                    


                    #pause so we don't exceed drive api limits
                    time.sleep(1.5)

                    if ratioCell == None:
                        #check current cell
                        #errors happen here, so we are going to try/except for connectoin error

                        try:
                            sheet.update_cell(ratioAddCounter, colCounter, currentCoinRatio)
                        except ConnectionError as error:
                            print("Error: ", error)
                        except gspread.exceptions.APIError as error:
                            print("Error: ", error)


                        #pause so we don't exceed drive api limits
                        time.sleep(1.5)
                        ratioAddCounter = numRows

                    ratioAddCounter += 1

                #max the counter to exit
                colCounter = numCols
            elif cell == None:
                print("creating new column at end")
                #errors happen here, so we are going to try/except for connectoin error

                try:
                    sheet.update_cell(1, colCounter, currentCoinID)
                except ConnectionError as error:
                    print("Error: ", error)
                except gspread.exceptions.APIError as error:
                    print("Error: ", error)

                #append ratio to this column
                ratioAddCounter = 2
                while ratioAddCounter < numRows:
                    #errors happen here, so we are going to try/except for connectoin error
                
                    try:
                        ratioCell = sheet.cell(ratioAddCounter, colCounter).value
                    except ConnectionError as error:
                        print("Error: ", error)
                    except gspread.exceptions.APIError as error:
                        print("Error: ", error)
                    
                    #pause so we don't exceed drive api limits
                    time.sleep(1.5)

                    if ratioCell == None:
                        #errors happen here, so we are going to try/except for connectoin error
                
                        try:
                            sheet.update_cell(ratioAddCounter, colCounter, currentCoinRatio)
                        except ConnectionError as error:
                            print("Error: ", error)
                        except gspread.exceptions.APIError as error:
                            print("Error: ", error)
                        
                        #pause so we don't exceed drive api limits
                        time.sleep(1.5)
                        ratioAddCounter = numRows

                    ratioAddCounter += 1
                
                colCounter = numCols
            colCounter += 1

        #coin should've been added or appended
        print("done checking all columns for")
        print(currentCoinID)
        print("moving to next coin")
        spreadCounter -= 1


    #print time for testing purposes
    print("end of script")
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)
    print("sleeping for 60 minutes")
    time.sleep(3600)
    print("restart harvesting")





    
    