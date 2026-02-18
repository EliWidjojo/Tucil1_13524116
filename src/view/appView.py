import tkinter as tk
import random
import colorsys
import time
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont
from src.logic.readWriteFile import readFile, writeFile
from src.logic.dataManipulation import cleanData, printData, isDataValid
from src.logic.solveQueen import solve, solveMurni

cleaned = None
currentQueens = None
currentResult = None
isSolving = False

def updateVisual(tempBoard):
    queens = []
    n = len(tempBoard)

    for i in range(n):
        for j in range(n):
            if tempBoard[i][j] == '#':
                queens.append((i, j))

    displayBoard(cleaned, queens)
    root.update()


def saveAsImage():
    global cleaned, mapColor, currentQueens

    if not cleaned:
        statusLabel.config(text="Board belum di-input.", fg="red")
        return

    n = len(cleaned)
    cell_size = 80

    img = Image.new("RGB", (n*cell_size, n*cell_size), "white")
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("seguisym.ttf", int(cell_size/2))

    for i in range(n):
        for j in range(n):
            char = cleaned[i][j]
            color = mapColor[char]

            x0 = j * cell_size
            y0 = i * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size

            draw.rectangle([x0, y0, x1, y1], fill=color, outline="black")

            if currentQueens and (i, j) in currentQueens:
                bbox = draw.textbbox((0, 0), "♛", font = font)
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                draw.text(
                    (x0 + (cell_size - w)/2, y0 + (cell_size - h)/2),
                    "♛",
                    fill="black",
                    font=font
                )

    filePath = filedialog.asksaveasfilename(defaultextension=".jpeg", filetypes=[("JPEG files", "*.jpeg"), ("All files", "*.*")])
    if filePath:
        img.save(filePath, "JPEG")
        statusLabel.config(text=f"Board berhasil disimpan sebagai {filePath}", fg="green")


def randomColor():
    h = random.random()
    s = random.uniform(0.2, 0.5)
    v = 0.7 + 0.3*random.random()

    r,g,b = colorsys.hsv_to_rgb(h, s, v)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"


def displayBoard(board, queens = None):
    global currentQueens, boardFrame
    currentQueens = queens

    boardFrame.destroy()
    boardFrame = tk.Frame(root)
    boardFrame.pack(before=caraSolveFrame)
    for widget in boardFrame.winfo_children():
        widget.destroy()

    n = len(board)
    global mapColor
    cells = [[None for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        boardFrame.grid_rowconfigure(i, weight=1, uniform="row")
        boardFrame.grid_columnconfigure(i, weight=1, uniform="col")
        for j in range(n):
            char = board[i][j]
            color = mapColor[char]
            if queens and (i,j) in queens:
                label = tk.Label(boardFrame, font=("Segoe UI Symbol", 14), text="♛", borderwidth=1, relief="solid", bg=color)
            else:
                label = tk.Label(boardFrame, font=("Segoe UI Symbol", 14), text = "     ", borderwidth=1, relief="solid", bg=color)
            label.grid(row=i, column=j, sticky="nsew")
            cells[i][j] = label



def onInputButton():
    if isSolving:
        statusLabel.config(text="ERROR: Proses masih berlangsung.", fg="red")
        return
    fileName = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    lines = readFile(fileName)
    if lines:
        statusLabel.config(text="File ditemukan!", fg="green")
        global cleaned, mapColor
        cleaned = cleanData(lines)
        validity = isDataValid(cleaned)

        if (validity):
            printData(lines)
            print("")
            chars = set(char for row in cleaned for char in row)
            mapColor = {char: randomColor() for char in chars}
            displayBoard(cleaned)
            timeLabel.config(text= "")
            iterationLabel.config(text= "")
        else:
            print("Data tidak valid!")
            statusLabel.config(text="Data tidak valid!", fg="red")

    else:
        statusLabel.config(text="File tidak ada!", fg="red")

def runSolve1():
    global cleaned, currentResult, isSolving
    if not cleaned:
        statusLabel.config(text="Board belum di-input.", fg="red")
        return
    if isSolving:
        statusLabel.config(text="ERROR: Proses masih berlangsung.", fg="red")
        return
    isSolving = True
    statusLabel.config(text="Sedang mencari jawaban...", fg="orange")
    timeLabel.config(text=f"Waktu pencarian: Loading...")
    iterationLabel.config(text=f"Banyak kasus yang ditinjau: Loading...")
    root.update_idletasks()
    startTime = time.time()
    result, iteration = solve(cleaned, updateVisual)

    if result:
        currentResult = result
        queens = [(i, j) for i in range(len(result)) for j in range(len(result)) if result[i][j] == '#']
        print("=======================")
        print("Hasil:")  
        print("")
        displayBoard(cleaned, queens)
        printData(result)
        print("")
        statusLabel.config(text="Jawaban ditemukan!", fg="green")
        root.update()

    else:
        statusLabel.config(text="Tidak ada jawaban.", fg="red")
        displayBoard(cleaned) 
    endTime = time.time()
    totalTime = (endTime - startTime) * 1000
    print(f"Banyak kasus yang ditinjau: {iteration} kasus")
    print(f"Waktu pencarian: {totalTime:.2f} ms")
    timeLabel.config(text=f"Waktu pencarian: {totalTime:.2f} ms")
    iterationLabel.config(text=f"Banyak kasus yang ditinjau: {iteration} kasus")
    isSolving = False

def runSolve2():
    global cleaned, currentResult, isSolving
    if not cleaned:
        statusLabel.config(text="Board belum di-input.", fg="red")
        return
    if isSolving:
        statusLabel.config(text="ERROR: Proses masih berlangsung.", fg="red")
        return
    isSolving = True
    statusLabel.config(text="Sedang mencari jawaban...", fg="orange")
    timeLabel.config(text=f"Waktu pencarian: Loading...")
    iterationLabel.config(text=f"Banyak kasus yang ditinjau: Loading...")
    root.update_idletasks()
    startTime = time.time()
    result, iteration = solveMurni(cleaned, updateVisual)

    if result:
        currentResult = result
        queens = [(i, j) for i in range(len(result)) for j in range(len(result)) if result[i][j] == '#']
        displayBoard(cleaned, queens)
        print("=======================")
        print("Hasil:")  
        print("")
        printData(result)
        print("")
        statusLabel.config(text=f"Jawaban ditemukan!", fg="green")
        root.update()
        
    else:
        statusLabel.config(text="Tidak ada jawaban.", fg="red")
        displayBoard(cleaned) 
    endTime = time.time()
    totalTime = (endTime - startTime) * 1000
    print(f"Banyak kasus yang ditinjau: {iteration} kasus")
    print(f"Waktu pencarian: {totalTime:.2f} ms")
    timeLabel.config(text=f"Waktu pencarian: {totalTime:.2f} ms")
    iterationLabel.config(text=f"Banyak kasus yang ditinjau: {iteration} kasus")
    isSolving = False

def saveToFile():
    global currentResult

    if not currentResult:
        statusLabel.config(text="Board belum di-input.", fg="red")
        return
    
    filePath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if filePath:
        writeFile(filePath, currentResult)
        statusLabel.config(text=f"Board berhasil disimpan sebagai {filePath}", fg="green")

def GUI():
    global root, boardFrame, statusLabel, timeLabel, iterationLabel, caraSolveFrame, inputEntry
    root = tk.Tk()

    root.title("Queens Game Solver")
    root.geometry("800x500")

    title = tk.Label(root, text ="Queens Game Solver", font=("Arial", 18))
    title.pack(pady=30)

    inputButton = tk.Button(root, text="Open TXT File", font=("Arial", 14), command=onInputButton)
    inputButton.pack(pady="5px")

    statusLabel = tk.Label(root, text="", font=("Arial", 8))
    statusLabel.pack()

    boardFrame = tk.Frame(root)
    boardFrame.pack()

    #Pilih cara Solve
    caraSolveFrame = tk.Frame(root)
    caraSolveFrame.pack(pady="5px")

    solve1Button = tk.Button(caraSolveFrame, text="Algoritma 1", font = ("Arial", 14), command = runSolve1)
    solve1Button.pack(side = tk.LEFT)

    solve2Button = tk.Button(caraSolveFrame, text="Algoritma 2", font = ("Arial", 14), command = runSolve2)
    solve2Button.pack(padx="5px")

    penjelasanLabel = tk.Label(root, text = "(Algoritma 1 lebih cepat dari 2)", font = ("Arial", 8))
    penjelasanLabel.pack()

    penjelasan2Label = tk.Label(root, text = "(Untuk  menghentikan pencarian, quit software)", font = ("Arial", 8))
    penjelasan2Label.pack()

    saveFrame = tk.Frame(root)
    saveFrame.pack(pady=5)


    inputButton = tk.Button(saveFrame, text="Save to TXT File", font=("Arial", 14), command=saveToFile)
    inputButton.pack(side = tk.LEFT)

    downloadImageButton = tk.Button(saveFrame, text="Download as JPEG", font=("Arial", 14), command=saveAsImage)
    downloadImageButton.pack(padx = "5px")

    timeLabel = tk.Label(root, text="", font= ("Arial",14))
    timeLabel.pack(pady = "5px")
    iterationLabel = tk.Label(root, text="", font=("Arial", 14))
    iterationLabel.pack()

    root.mainloop()