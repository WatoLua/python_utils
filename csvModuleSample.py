#this module is an example that copy the csv in new csv file using threads
import threading

import csvUtils
import fileUtils

##your module to import, or it can be a class

localVars = {}

def init(csvReader, csvProcessor, outputFile, separator):
    localVars["csvReader"] = csvReader
    localVars["csvProcessor"] = csvProcessor
    localVars["outputFile"] = outputFile
    localVars["separator"] = separator
    localVars["processedRows"] = []

def endProcess():
    None

def process(row):
    line = localVars["separator"].join(row)
    fileUtils.addToFile(localVars["outputFile"], line)

##end your module

def main():

    module.init()

    csvReader = csvUtils.CsvReader()
    csvProcessor = csvUtils.CsvProcessor(csvReader, module, 1, "each")
    csvReader.readCsv("your_csv", ";", None)
    csvProcessor.processCsv(1)

    module.endProcess()


main()