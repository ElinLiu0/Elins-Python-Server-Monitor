import os
result = os.popen("netsh advfirewall firewall show rule name=all").readlines()
for i in range(len(result)):
    print(result[i].replace("                               ","").replace("                             ","")[0:4])
# print(result[1].replace("                               ","").replace("                             ","")[0:5] == "规则名称")