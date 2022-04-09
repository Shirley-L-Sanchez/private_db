import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
from scipy import stats

data1 = pd.read_csv("benchmarking_system_1.csv")
data2 = pd.read_csv("benchmarking_system_2.csv")
data3 = pd.read_csv("benchmarking_system_3.csv")
data4 = pd.read_csv("benchmarking_system_4.csv")
data5 = pd.read_csv("benchmarking_system_5.csv")
#Filter an insignifant number of outliers
data5 = data5[data5["User Execution Time with Bloom Filters (s)"] < 4.6]
data6 = pd.read_csv("benchmarking_system_6.csv")

data = [data1, data2, data3, data4, data5, data6]

real_optimized = pd.concat([df["User Execution Time with Bloom Filters (s)"] + df["System Execution Time with Bloom Filters (s)"] for df in data])

num_users = pd.concat([df["Number of Users in System"] for df in data])

real_unoptimized = pd.concat([df["User Execution Time without Bloom Filters (s)"] + df["System Execution Time without Bloom Filters (s)"] for df in data])


plt.scatter(num_users, real_unoptimized, s=15, label = "System without Bloom Filters (1)")
plt.scatter(num_users, real_optimized, s=15, label = "System with Bloom Filters (2)")
plt.scatter(num_users, real_unoptimized - real_optimized, s= 15, label="Difference in Execution Times between (1) and (2)")

#slope, intercept, r_value, p_value, std_err = stats.linregress(num_users,real_unoptimized)
#plt.annotate('y = {:.3e}x - {:.3e}\nR\u00b2 = {:.3f}'.format(slope, abs(intercept), r_value**2), xy=(0.46, 0.65), xycoords='figure fraction', color='darkblue', size=7)
#plt.plot(num_users, slope*num_users+intercept, linestyle='--', color='darkblue')

#slope, intercept, r_value, p_value, std_err = stats.linregress(num_users,real_optimized)
#plt.annotate('y = {:.3e}x - {:.3e}\nR\u00b2 = {:.3f}'.format(slope, abs(intercept), r_value**2), xy=(0.69, 0.60), xycoords='figure fraction', color='orangered', size=7)
#plt.plot(num_users, slope*num_users+intercept, linestyle='--', color='orangered')

#slope, intercept, r_value, p_value, std_err = stats.linregress(num_users,real_unoptimized - real_optimized)
#plt.annotate('y = {:.3e}x + {:.3e}\nR\u00b2 = {:.3f}'.format(slope, intercept, r_value**2), xy=(0.57, 0.25), xycoords='figure fraction', color='limegreen', size=7)
#plt.plot(num_users, slope*num_users+intercept, linestyle='--', color='limegreen')

plt.title("Execution Time of Aggregate Query for Different Number of Users")
plt.xlabel("Number of Users")
plt.ylabel("Execution Time (s)")
plt.legend()
plt.show()
plt.savefig('Scatter Plot.png')