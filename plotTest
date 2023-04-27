import numpy as np
import matplotlib.pyplot as plt

# dane
x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
y = np.array([20,25,20,25,25,30,32.5,30,35,30,32.5,30])


x_smooth = np.linspace(x.min(), x.max(), 200)
y_smooth = np.interp(x_smooth, x, y)


# obliczanie współczynników prostej regresji
slope, intercept = np.polyfit(x, y, 1)

# generowanie punktów przewidywań
x_pred = np.array([12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])
y_pred = slope * x_pred + intercept

# narysowanie wykresu
plt.scatter(x, y)
plt.plot(x_pred, y_pred, color='blue', linestyle='dashed')
plt.plot(x_smooth, y_smooth)
plt.show()
