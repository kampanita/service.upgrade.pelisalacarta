import time 
import xbmc
import xbmcaddon
import xbmcgui
import urllib
import urllib2
import base64
import zipfile
import os
import shutil
import errno
 
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
icon = addon.getAddonInfo('icon')

path= addon.getSetting('temp')
path2=xbmc.translatePath('special://home/')
tiempo = addon.getSetting('tiempo')  
notify = addon.getSetting('notify')    


time = 7000 #in miliseconds
time2= 100
num_files=0
num_files2=0

def copydir(source, dest, indent = 0):
    notify2 = addon.getSetting('notify2')
    """Copy a directory structure overwriting existing files"""
    num_files2=0
    dialog  = xbmcgui.DialogProgressBG()
    dialog.create('UpdPelisAlacarta - copy files')
    
    for root, dirs, files in os.walk(source):
        if not os.path.isdir(root):
            os.makedirs(root)
        for each_file in files:
            rel_path = root.replace(source, '').lstrip(os.sep)
            dest_path = os.path.join(dest, rel_path, each_file)
            xbmc.log(os.path.join(root, each_file)+' -> '+dest_path)
            shutil.copyfile(os.path.join(root, each_file), dest_path)
            num_files2+=1
            
            if notify2:
                #xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,each_file, time2, icon))                                                
                dialog.update(int(num_files2/num_files)*100,rel_path,each_file)
                
    dialog.update(-1)
    dialog.close
    
def upgrade():  

    notify = addon.getSetting('notify') 
    tiempo = addon.getSetting('tiempo')     
    path= addon.getSetting('temp')
    
    if notify:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"checking git-master", time, icon))
    
    file = urllib2.urlopen("https://codeload.github.com/tvalacarta/pelisalacarta/zip/master")
    file_int = int(file.info()['Content-Length'])
    file_int=1
    try :    
        file_local = int(os.path.getsize(xbmc.translatePath(path+'pelis.zip.old')))
        
    except :    
        file_local = 0        
        xbmc.log("No encuentro el fichero");
        
    if file_int <> file_local:
        
        if notify:
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"downloading new version", time, icon))            
        
        try:
           
           ###
           #urllib.urlretrieve ("https://codeload.github.com/tvalacarta/pelisalacarta/zip/master",  xbmc.translatePath(path+'pelis.zip'))
           #
           ###
           
           url = "https://codeload.github.com/tvalacarta/pelisalacarta/zip/master"
           f = urllib2.urlopen(url)
           with open(xbmc.translatePath(path+'pelis.zip'), "wb") as code: 
               code.write(f.read())
               code.close()
           if notify:
               xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"DOWNLOADED", time, icon))                           
           ###
           num_files=0
           fh = open( xbmc.translatePath(path+'pelis.zip'), 'rb')
           z = zipfile.ZipFile(fh)
           
           for name in z.namelist():
               if "main-classic" in str(name):
                   
                   z.extract(name,xbmc.translatePath(path))                
                   num_files+=1
                   
           fh.close()
           
           if notify:
               xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"Files extracted from zip", time, icon))            
           
           ori = xbmc.translatePath(path+'pelisalacarta-master/python/main-classic')
           dest =  xbmc.translatePath(path2+'addons/plugin.video.pelisalacarta')

           try:
               copydir(ori,dest)	
               xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"upgraded from git-master", 2*time , icon))    
           
           except Exception as exp:
               s=str(exp)
               xbmc.log('UpdPelisALaCarta - Error en el proceso '+s)  
               xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"Error upgrade "+s, time*3, icon))
           
           shutil.rmtree(xbmc.translatePath(path+'pelisalacarta-master'))
           os.remove(xbmc.translatePath(path+'pelis.zip.old'))
           os.rename(xbmc.translatePath(path+'pelis.zip'),xbmc.translatePath(path+'pelis.zip.old'))
        
        except Exception as e:
           s = str(e)
           xbmc.log('UpdPelisALaCarta - Error en el proceso '+s)  
           xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"Error upgrade", time, icon))
   
    else:
        if notify:
           xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"No need to upgrade", time , icon))
           
    if notify:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"HOSTIE finished checking", time, icon))
    
    return;

def test():
	
    xbmc.log('inicio el proceso')    
    return;
  
#test()

upgrade()

if __name__ == '__main__':

    monitor = xbmc.Monitor()
 
    while not monitor.abortRequested():
        # Sleep/wait for abort for 10 seconds ( media hora )
        if monitor.waitForAbort(60*int(tiempo)):
            # Abort was requested while waiting. We should exit
            break
        upgrade()
