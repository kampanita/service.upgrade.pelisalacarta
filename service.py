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
time2= 1000

def copydir(source, dest, indent = 0):
    """Copy a directory structure overwriting existing files"""
    for root, dirs, files in os.walk(source):
        if not os.path.isdir(root):
            os.makedirs(root)
        for each_file in files:
            rel_path = root.replace(source, '').lstrip(os.sep)
            dest_path = os.path.join(dest, rel_path, each_file)
            shutil.copyfile(os.path.join(root, each_file), dest_path)
            #xbmc.log(root+each_file+' -> '+dest_path+each_file)
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,each_file, time2, icon))
            
def upgrade():  
    
    
    notify = addon.getSetting('notify') 
    tiempo = addon.getSetting('tiempo')     
    path= addon.getSetting('temp')
    
    if notify:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"checking git-master", time, icon))
    
    file = urllib2.urlopen("https://codeload.github.com/tvalacarta/pelisalacarta/zip/master")
    file_int = int(file.info()['Content-Length'])
    
    try :    
        file_local = int(os.path.getsize(xbmc.translatePath(path+'pelis.zip.old')))
    
    except :    
        file_local = 0        
        xbmc.log("No encuentro el fichero");
        
    if file_int <> file_local:
        
        if notify:
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"downloading new version", time, icon))            
        
        urllib.urlretrieve ("https://codeload.github.com/tvalacarta/pelisalacarta/zip/master",  xbmc.translatePath(path+'pelis.zip'))
                
        try:
           fh = open( xbmc.translatePath(path+'pelis.zip'), 'rb')
           z = zipfile.ZipFile(fh)
          
           for name in z.namelist():
               if "main-classic" in str(name):
                   
                   z.extract(name,xbmc.translatePath(path))                
                 
           fh.close()
           
           ori = xbmc.translatePath(path+'pelisalacarta-master/python/main-classic')
           dest =  xbmc.translatePath(path2+'/addons/plugin.video.pelisalacarta')
           
           copydir(ori,dest)
           
           try:
               os.remove(xbmc.translatePath(path+'pelis.zip.old'))
           except:
           	   xbmc.log('No hay pelis.zip.old')
           	   
           os.rename(xbmc.translatePath(path+'pelis.zip'),xbmc.translatePath(path+'pelis.zip.old'))
           shutil.rmtree(xbmc.translatePath(path+'pelisalacarta-master'))
           
           xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"upgraded from git-master", 2*time , icon))
        
        except Exception as e:
           s = str(e)
           xbmc.log('UpdPelisALaCarta - Error en el proceso '+s)  
           xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"Error upgrade", time, icon))
   
    else:
        if notify:
           xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"No need to upgrade", time , icon))
           
    if notify:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"finished checking", time, icon))
    
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
