# import os
# os.remove("myfile.txt")

# import os
# if os.path.exists("myfile.txt"):
#   os.remove("myfile.txt")
# else:
#   print("The file does not exist")

import shutil
shutil.copyfile('myfile.txt', 'mynewfile.txt')