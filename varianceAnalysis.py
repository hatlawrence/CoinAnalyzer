import operator
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open("cryptodata").sheet1


#get value of cell
#cell = sheet.cell(6, 6).value


#change value of cell
#sheet.update_cell(2,2, "CHANGED")

#get number of columns and rows
numCols = sheet.col_count
numRows = sheet.row_count


#create coin data object
class coinVarianceObj:
    def __init__(self, id,):
        self.id = id
        self.varianceList = []
        self.dataList = []
    def addVariancePoint(self, variance):
        self.varianceList.append(variance)
    def addDataPoint(self, point):
        self.dataList.append(point)
    def addAverage(self, average):
        self.average = average
    def addAverageVariance(self, averageVariance):
        self.averageVariance = averageVariance

#create list of coin data objects
coinList = []




#calculate variance for every column with a name
#loop through each column
colCounter = 1
while colCounter < numCols:
    cell = sheet.cell(1, colCounter).value
    #pause for api
    time.sleep(1.5)

    rowCounter = 2
    filledCells = 0

    columnTotal = float(0)

    #if cell is blank
    if cell == None:
        colCounter = numCols
    else:
        #starting calculation for non blank columns
        #create coin object
        currentCoin = coinVarianceObj(cell)
        print(currentCoin.id)




        print("starting sum of rows")

        
        
        while rowCounter < numRows:
            #get value of row cell for summing up
            sumCell = sheet.cell(rowCounter, colCounter).value

            #pause for api
            time.sleep(1)

            #if cell is blank
            if sumCell == None:
                print("blank cell hit")
                #walk the counter back one because this cell is blank
                rowCounter -= 1

                #set to max to exit
                rowCounter = numRows
            else:
                #counter for filled cells
                filledCells += 1

                #print data for visbility
                #print(cell, " row ", filledCells)

                #log the value of this data point
                currentCoin.addDataPoint(float(sumCell))

                #calculate running total
                columnTotal = float(columnTotal) + float(sumCell)
                
                #up the row counter
                rowCounter += 1
        
        

        #get average for column
        columnAverage = float(columnTotal / filledCells)

        #add average to coin
        currentCoin.addAverage(columnAverage)

        #calculate variance of each data point, add to coin
        print("length")
        print(len(currentCoin.dataList))
        counter = 0
        while counter < len(currentCoin.dataList):
            variancePoint = float(currentCoin.dataList[counter] - currentCoin.average) * float(currentCoin.dataList[counter] - currentCoin.average)
            currentCoin.addVariancePoint(variancePoint)
            counter += 1

        
        #calculate average variance, add to coin
        counter = 0
        varianceTotal = 0
        while counter < len(currentCoin.varianceList):
            varianceTotal = float(varianceTotal + currentCoin.varianceList[counter])
            counter += 1
        varianceAverage = float(varianceTotal / len(currentCoin.varianceList))
        currentCoin.addAverageVariance(varianceAverage)

        #append coin to list of coins
        coinList.append(currentCoin)
        

        #print name of coin
        print("ID: ", currentCoin.id)
        print("Average: ", currentCoin.average)
        print("Average Variance: ", currentCoin.averageVariance)


        #total the column
        #calculate variance
        #store variance and name of coin in list
    colCounter += 1

#sort variance list
#sort list by average variance
sortedList = sorted(coinList, key=operator.attrgetter("averageVariance"))

#print variance list
counter = 0
while counter < len(sortedList):
    print(counter)
    print("ID: ", sortedList[counter].id)
    print("Average: ", sortedList[counter].average)
    print("Average Variance: ", sortedList[counter].averageVariance)
    counter += 1
    
#rank variance list
#output results

