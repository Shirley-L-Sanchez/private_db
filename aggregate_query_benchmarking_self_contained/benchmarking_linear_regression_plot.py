import matplotlib.pyplot as plt
import numpy as np 
from scipy import stats, optimize
import pandas as pd
from sklearn import metrics

data1 = pd.read_csv("benchmarking_system_1.csv")
data2 = pd.read_csv("benchmarking_system_2.csv")
data3 = pd.read_csv("benchmarking_system_3.csv")
data4 = pd.read_csv("benchmarking_system_4.csv")
data5 = pd.read_csv("benchmarking_system_5.csv")
#Filter out insignificant number of outliers (~7 points)
data5 = data5[data5["User Execution Time with Bloom Filters (s)"] < 4.6]
data6 = pd.read_csv("benchmarking_system_6.csv")
data = [data1, data2, data3, data4, data5, data6]

real_optimized = pd.concat([df["User Execution Time with Bloom Filters (s)"] + df["System Execution Time with Bloom Filters (s)"] for df in data])

num_users = pd.concat([df["Number of Users in System"] for df in data])

real_unoptimized = pd.concat([df["User Execution Time without Bloom Filters (s)"] + df["System Execution Time without Bloom Filters (s)"] for df in data])

#plt.scatter(num_users, real_optimized, s=15, color="yellow")
z = np.polyfit(num_users, real_optimized, 1)
mymodel1 = np.poly1d(z)
y = [mymodel1(u) for u in np.linspace(0, 1000000, 100)]
plt.plot(np.linspace(0, 1000000, 100), y, linestyle='--', color='orangered', label="System with Bloom Filters (2)")
y = [mymodel1(u) for u in num_users]
print(real_optimized[:5])
print(y[:5])
r2 = metrics.r2_score(real_optimized, y)
print("R squared for optimized: ", r2)

#plt.scatter(num_users, real_unoptimized, s=15, color="lightblue")
z = np.polyfit(num_users, real_unoptimized, 1)
mymodel = np.poly1d(z)
y = [mymodel(u) for u in np.linspace(0, 1000000, 100)]
plt.plot(np.linspace(0, 1000000, 100), y, linestyle='--', color='blue', label="System without Bloom Filters (1)")
y = [mymodel(u) for u in num_users]
r2 = metrics.r2_score(real_unoptimized, y)
print("R squared for unoptimized: ", r2)

#plt.scatter(num_users, real_unoptimized - real_optimized, s=15, color="lightgreen")
y = [mymodel(u) - mymodel1(u) for u in np.linspace(0, 1000000, 100)]
plt.plot(np.linspace(0, 1000000, 100), y, linestyle='--', color='green', label="Difference between (1) and (2)")
y = [mymodel(u) for u in num_users]


plt.title("Execution Time of Aggregate Query for Different Number of Users")
plt.xlabel("Number of Users")
plt.ylabel("Execution Time (s)")
plt.legend()
plt.show()
plt.savefig('Linear Regression Plot.png')