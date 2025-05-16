import numpy as np
import matplotlib.pyplot as plt

data=np.random.randint(27,size=(10,12))
sunnydayyear = np.sum(data, 1)
sunnydaymonth = np.average(data, 0)
spring = np.sum(data[:,0:3])
summer = np.sum(data[:,3:6])
autumn = np.sum(data[:,6:9])
winter = np.sum(data[:,9:12])
sizes = [spring, summer, autumn, winter]

labels = 'spring', 'summer', 'autumn', 'winter'
year = np.arange(1990, 2000, 1)
month = np.arange(1,13,1)

fig = plt.figure(figsize=(8,15))
ax1 = fig.add_subplot(3,1,1)
ax1.plot(year, sunnydayyear,'r-')
ax1.set_title('Sunny Days in Each Year')
ax1.set_xticks(year)
ax1.set_ylabel('days')
ax1.set_xlabel('year')

ax2 = fig.add_subplot(3,1,2)
ax2.bar(month, sunnydaymonth)
ax2.set_title('Average Sunny Days in Each Month')
ax2.set_xticks(month)
ax2.set_ylabel('days')
ax2.set_xlabel('month')

ax3 = fig.add_subplot(3,1,3)
ax3.pie(sizes, labels=labels, autopct='%1.1f%%')
ax3.set_title('Seasonal Share of Sunny Days')

fig.suptitle('Sunny Days Analysis 1990-1999')
plt.savefig('overleaf/67fe68e723632af9fad1411b/figures/lab2ex3.png')