import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from scipy.interpolate import interp1d


def plotResults(reached=[], missed=[], nGames=200):
    if reached == []:
        reached = [3, 9, 10, 7, 15, 12, 16, 9, 9, 7, 13, 5, 10, 10, 10, 13, 16, 7, 14, 4, 7, 11, 7, 15, 13, 11, 19, 13, 16, 12, 19, 12, 15, 15, 16, 11, 11, 9, 18, 16, 14, 16, 14, 20, 23, 16, 16, 23, 20, 14, 15, 12, 23, 16, 15, 20, 22, 22, 20, 13, 14, 22, 11, 13, 14, 22, 17, 17, 19, 20, 26, 21, 18, 26, 18, 24, 31, 24, 21, 18, 19, 25, 24, 32, 18, 21, 34, 19, 20, 24, 24, 27, 24, 29, 19, 26, 19, 21, 23, 19, 25, 21, 24, 26, 27, 27, 26, 28, 25, 19, 27, 26, 33, 27, 27, 27, 26, 27, 30, 28, 24, 28, 34, 31, 30, 28, 32, 31, 30, 31, 29, 31, 31, 33, 30, 39, 31, 31, 28, 32, 30, 33, 33, 27, 35, 36, 33, 33, 35, 34, 32, 33, 36, 29, 37, 30, 34, 39, 37, 35, 33, 37, 29, 37, 34, 42, 43, 38, 41, 39, 45, 44, 43, 31, 39, 47, 42, 42, 42, 43, 33, 40, 42, 35, 43, 45, 40, 43, 41, 44, 43, 43, 45, 41, 35, 39, 44, 36, 41, 48]
    if missed == []:
        missed = [47, 41, 40, 43, 35, 38, 34, 41, 41, 43, 37, 45, 40, 40, 40, 37, 34, 43, 36, 46, 43, 39, 43, 35, 37, 39, 31, 37, 34, 38, 31, 38, 35, 35, 34, 39, 39, 41, 32, 34, 36, 34, 36, 30, 27, 34, 34, 27, 30, 36, 35, 38, 27, 34, 35, 30, 28, 28, 30, 37, 36, 28, 39, 37, 36, 28, 33, 33, 31, 30, 24, 29, 32, 24, 32, 26, 19, 26, 29, 32, 31, 25, 26, 18, 32, 29, 16, 31, 30, 26, 26, 23, 26, 21, 31, 24, 31, 29, 27, 31, 25, 29, 26, 24, 23, 23, 24, 22, 25, 31, 23, 24, 17, 23, 23, 23, 24, 23, 20, 22, 26, 22, 16, 19, 20, 22, 18, 19, 20, 19, 21, 19, 19, 17, 20, 11, 19, 19, 22, 18, 20, 17, 17, 23, 15, 14, 17, 17, 15, 16, 18, 17, 14, 21, 13, 20, 16, 11, 13, 15, 17, 13, 21, 13, 16, 8, 7, 12, 9, 11, 5, 6, 7, 19, 11, 3, 8, 8, 8, 7, 17, 10, 8, 15, 7, 5, 10, 7, 9, 6, 7, 7, 5, 9, 15, 11, 6, 14, 9, 2]
    c = []
    d = []
    k = 0
    vet = np.linspace(0, nGames, int(nGames/10))
    for i in range(int(nGames/10)):
        c.append(np.sum(reached[k:10+k])/10)
        d.append(np.sum(missed[k:10+k])/10)
        k += 10
    
    plt.title("Endless Runner Game 1.0")
    plt.ylabel("Coins")
    plt.xlabel("Number of games")

    newX = np.linspace(vet.min(), vet.max(), 200)
    spl1 = interp1d(vet, c, kind='quadratic')
    spl2 = interp1d(vet, d, kind='quadratic')
    smoothVet1 = spl1(newX)    
    smoothVet2 = spl2(newX)

    plt.scatter(range(int(nGames)), missed, c="r", marker='x', s=12)
    plt.plot(newX, smoothVet2, c="r")

    plt.scatter(range(int(nGames)), reached, c="g", marker='o', s=12)
    plt.plot(newX, smoothVet1, c="g",label='1')

    plt.legend(('Missed - Smooth line', 'Reached - Smooth line', 'Missed', 'Reached'))

    plt.show()

