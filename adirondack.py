import random

qtyChairs = 4
lumber = [
    {"len":92,"price":5.68},
    {"len":96,"price":8.27},
    {"len":104,"price":7.92},
    {"len":120,"price":8.96},
    {"len":192,"price":15.24},
    ]
cutsNeeded = [
    {"len":19.5,"qtyPerChair":5,"used":0},
    {"len":31.75,"qtyPerChair":2,"used":0},
    {"len":33.25,"qtyPerChair":2,"used":0},
    {"len":32.75,"qtyPerChair":2,"used":0},
    ]

def batchComplete():
    stop = 1
    for i in cutsNeeded:
        if i["used"] < i["qtyPerChair"] * qtyChairs:
            stop=0
    return stop

def boardUsedUp(remainingLen):
    shortestCutNeeded = 999999
    stop = 0
    for i in cutsNeeded:
        if i["used"] < i["qtyPerChair"] * qtyChairs and i["len"] < shortestCutNeeded:
            shortestCutNeeded = i["len"]
    if shortestCutNeeded > remainingLen:
        stop = 1
    return stop

def oneSingleBoard(boardsUsed):
    ### One single board
    ### pick a board and then cut pieces from it until we use up the board
    currentWood = lumber[random.randint(0,4)]
    boardsUsed.append({"board":currentWood["len"],"cuts":[]})
    remainingLen = currentWood["len"]
    while batchComplete() != 1 and boardUsedUp(remainingLen) != 1:
        currentCut = cutsNeeded[random.randint(0,3)]
        if currentCut["used"] < currentCut["qtyPerChair"] * qtyChairs and remainingLen - currentCut["len"] >= 0:
            currentCut["used"] += 1
            boardsUsed[len(boardsUsed)-1]["cuts"].append(currentCut["len"])
            remainingLen = remainingLen - currentCut["len"]
    return boardsUsed

def costOfBatch(boardsUsed):
    costOfBatch = 0
    for i in boardsUsed:
        for j in lumber:
            #print("yyy")
            if j["len"] == i["board"]:
                costOfBatch += j["price"]
    costOfBatch = round(costOfBatch,2)
    return costOfBatch

def oneBatchOfChairs():
    ### Keep picking boards until we run out of cuts to make
    ### boardsUsed will track the cuts we made for each batch of chairs
    ### example [{'board': 92, 'cuts': [19.5, 32.75, 31.75]}]
    batch = {"boards": [],"cost":0}
    boardsUsed = []
    for i in cutsNeeded:
        i["used"] = 0
    while batchComplete() != 1:
        oneSingleBoard(boardsUsed)
    batch["boards"] = boardsUsed
    batch["cost"] = costOfBatch(boardsUsed)
    batch["costPerChair"] = round(batch["cost"]/qtyChairs,2)
    return batch

def manyBatches():
    lowestCost = 9999
    i=1
    while i<99999:
        batch = oneBatchOfChairs()
        if batch["cost"] < lowestCost:
            lowestCost = batch["cost"]
            lowestCostBatch = batch
        i+=1
    outputResults(i,lowestCostBatch)

def outputResults(i,lowestCostBatch):
    print("Welcome to Adirondack chair optimizer")
    print("\n")
    print("We tried " + str(i) + " combinations of boards and cuts \n")
    print("The lowest cost for a batch of " + str(qtyChairs) + " chairs was $" + str(lowestCostBatch["cost"]) + "\n")
    print("Which is $" + str(lowestCostBatch["costPerChair"]) + " per chair\n")
    print("The boards needed are: \n")
    for j in lowestCostBatch["boards"]:
        print(str(j["board"]) + " inch board, cut into: " + str(j["cuts"]) + " inch pieces")
    print("\nThe lumber available to choose from was: \n")
    for k in lumber:
        print(str(k["len"]) + " inch 2x4 at $" + str(k["price"]))
    print("\n")
manyBatches()
