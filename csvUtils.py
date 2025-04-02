import threading
import pandas

import printUtils

## parallel ##

class CsvReader:
    def __init__(self, sizeProgress = 100):
        self.actualRow = 0
        self.lastRow = -1
        self.sizeProgress = sizeProgress
        self.csv = None
        self.header = []
        self.csvName = ""

    def readCsv(self, filePath, separator, header=0):
        self.csv = pandas.read_csv(filePath, sep=f"[{separator}]", engine="python", header=header)
        self.csvName = filePath.split("/")[-1].replace(".csv", "")
        self.actualRow = 0
        self.lastRow = self.csv.shape[0]
        if header is not None:
            self.header = self.csv.columns.str.strip().tolist()

    def nextRow(self):
        if self.actualRow < self.lastRow:
            row = self.csv.iloc[self.actualRow].to_list()
            self.actualRow += 1
            return row
        else:
            return None
    def hasNextRow(self):
        return self.actualRow < self.lastRow

    def columnValue(self, row, header):
        try:
            return row[self.header.index(header)]
        except:
            return None

class CsvProcessor:
    def __init__(self, csvReader, module, linesToProcess = 100, moduleProcessMode="all"):
        self.csvReader = csvReader
        self.linesToProcess = linesToProcess
        self.module = module
        self.moduleProcessMode = moduleProcessMode

    def processCsv(self, threadsNumber = 4, progressFunc=printUtils.printProgressBar):
        """
        Starts the first X threads.
        """
        """
        For each thread that has finished, one is recreated for next request.
        """

        threads = []

        if progressFunc is not None:
            progressFunc(self.csvReader.actualRow, self.csvReader.lastRow, self.csvReader.sizeProgress)
        while self.csvReader.actualRow < self.csvReader.lastRow:
            for indexThread in range(threadsNumber):
                if self.csvReader.actualRow < self.csvReader.lastRow:
                    if len(threads) == indexThread or not threads[indexThread].is_alive():
                        thread = threading.Thread(target=self.process)
                        thread.start()
                        if len(threads) == indexThread:
                            threads.append(thread)
                        else:
                            threads[indexThread] = thread
                        if self.csvReader.actualRow + self.linesToProcess <= self.csvReader.lastRow:
                            self.csvReader.actualRow += self.linesToProcess
                        else:
                            self.csvReader.actualRow = self.csvReader.lastRow
                        if progressFunc is not None:
                            progressFunc(self.csvReader.actualRow, self.csvReader.lastRow, self.csvReader.sizeProgress)

        for thread in threads:
            thread.join()

    def collectRows(self):
        rows = []
        for i in range(self.linesToProcess):
            if (self.csvReader.actualRow + i < self.csvReader.lastRow):
                rowValues = self.csvReader.csv.iloc[self.csvReader.actualRow + i].to_list()
                rows.append(rowValues)
        return rows

    def process(self):
        if self.moduleProcessMode =="all":
            self.processAllRows()
        elif self.moduleProcessMode =="each":
            self.processByRow()


    def processByRow(self):
        rows = self.collectRows()
        for row in rows:
            self.module.process(row)

    def processAllRows(self):
        self.module.process(self.collectRows())