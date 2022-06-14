import os
base_dir = 'D:\BackUp\origin'
for dirs in os.listdir(os.path.join(base_dir)):
    for institutions in os.listdir(os.path.join(base_dir,dirs)):
        if os.path.isdir(os.path.join(os.path.join(base_dir,dirs),institutions)):
            for file in os.listdir(os.path.join(os.path.join(base_dir,dirs),institutions)):
                if institutions == '中信建投两融账户':
                    print(file)