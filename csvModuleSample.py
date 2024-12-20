#this module is an example that copy the csv in new csv file using threads
import threading

import fileUtils

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