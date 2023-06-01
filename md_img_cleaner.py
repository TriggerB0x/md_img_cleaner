# -*-coding:utf-8 -*-
import re
import shutil
import os

import urllib.parse

pattern=re.compile('\!\[.*\]\(.*\..*\)')

copy_dirs=[]
del_dirs=[]


for root,dirs,files in os.walk('./'):
    for file in files:
        if file.endswith('.md'):
            md_str=open(root+'/'+file,'r',encoding='utf-8').read() #read md file and store it in a string.
            results=pattern.findall(md_str)
            for result in results:
                md_image_path=result[result.index('](')+2:result.rindex(')')]
                path=''
                if not md_image_path.startswith(root):
                    # './' or '/' both may be use
                    if md_image_path.startswith('./'):
                        path=md_image_path.replace('./',root+'/')
                    else:
                        path=root+'/'+md_image_path
                is_file=False
                if os.path.exists(path):
                    is_file=True
                elif os.path.exists(urllib.parse.unquote(path)):
                    is_file=True
                    path=urllib.parse.unquote(path)
                if is_file:
                    dir_path=path[0:path.rindex('/')]+'==copy=='
                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)
                        copy_dirs.append(dir_path)
                        del_dirs.append(path[0:path.rindex('/')])
                    shutil.move(path,dir_path+'/'+os.path.basename(path))
    
for del_dir in del_dirs:
    if os.listdir(del_dir):
        os.rename(del_dir,del_dir+'_archive')
    else:
        os.rmdir(del_dir)
    
for copy_dir in copy_dirs:
    os.rename(copy_dir,copy_dir.strip('==copy=='))

print('Clear End!')