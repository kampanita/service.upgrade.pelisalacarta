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
import time 

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
icon = addon.getAddonInfo('icon')

#Para ver que branches tenemos en el git
#'href="/tvalacarta/pelisalacarta/tree'
# data = scrapertools.cache_page('https://github.com/tvalacarta/pelisalacarta/branches')
# patron='href="/tvalacarta/pelisalacarta/tree/(.*?)"'
# matches = re.compile(patron,re.DOTALL).findall(data)
# for rel_url in matches:
#     addon.setSetting('id_url','https://github.com/tvalacarta/pelisalacarta/tree/'+rel_url)

path= addon.getSetting('temp')
path2=xbmc.translatePath('special://home/')
tiempo = addon.getSetting('tiempo')  
notify = addon.getSetting('notify')    


__time__ = 7000 #in miliseconds
num_files=0
num_files2=0

def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

def copydir(source, dest, num_files, indent = 0):
 
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
            
            try:         
               dir_destino=os.path.join(dest, rel_path)   
               
               if not os.path.isdir(dir_destino):             
                    try:            
                        os.mkdir(dir_destino)               
                        xbmc.log('!!!!! Creado '+dir_destino+' que no existia !!!!!')
                    except:
                        xbmc.log('Error creando '+dir_destino)
               
               shutil.copyfile(xbmc.translatePath(os.path.join(root, each_file)), xbmc.translatePath(dest_path))               
               
               xbmc.log('Copied '+dest_path)
               
            except Exception as x:               
               xbmc.log(str(num_files2)+"/"+str(num_files)+" !! "+str(x)+' '+xbmc.translatePath(dest_path))         
                  
            num_files2+=1
            
            if notify2:
                 progreso=int(float(num_files2)/float(num_files))*100                                
                 dialog.update(progreso,str(num_files2)+'/'+str(num_files)+' '+rel_path,each_file)
                 time.sleep(50/1000)                    
                 
    dialog.close
    
def upgrade():  
    #me traigo los valores del settings.xml
    notify = addon.getSetting('notify') 
    tiempo = addon.getSetting('tiempo')     
    path= addon.getSetting('temp')
    what= addon.getSetting('what')
    version_plugin= addon.getSetting('version_plugin')    
    version_to_download=addon.getSetting('version_to_download')
    
    if notify:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"Checking git-"+version_to_download, __time__, icon))
    
    try:
        file = urllib2.urlopen("https://github.com/tvalacarta/pelisalacarta/archive/"+version_to_download+".zip")
        file_int = int(file.info()['Content-Length'])       
    except:                
        xbmc.log("Error bajando "+"https://github.com/tvalacarta/pelisalacarta/archive/"+version_to_download+".zip")
        return;            
    
    try:    
        file_local = int(os.path.getsize(xbmc.translatePath(os.path.join(path,'pelis.zip.old'))))
      
    except :    
        file_local = 0                
        xbmc.log("No encuentro el fichero pelis.zip.old");
        touch(xbmc.translatePath(os.path.join(path,'pelis.zip.old')))
        
    if file_int <> file_local:
        
        if notify:
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"Downloading new version from "+version_to_download, __time__, icon))            
        
        try:
           
           url = "https://github.com/tvalacarta/pelisalacarta/archive/"+version_to_download+".zip"
           f = urllib2.urlopen(url)
           with open(xbmc.translatePath(os.path.join(path,'pelis.zip')), "wb") as code: 
               code.write(f.read())
               code.close()
           if notify:
               xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"Downloaded "+version_to_download, __time__, icon))                           
                      
           num_files=0
           fh = open( xbmc.translatePath(os.path.join(path,'pelis.zip')), 'rb')
           z = zipfile.ZipFile(fh)
           
                     
           for name in z.namelist():
               if ((what=="todo") or (version_plugin=="classic")):
                   if "main-classic" in str(name):
                       
                       z.extract(name,xbmc.translatePath(path))                
                       num_files+=1
                       #xbmc.log("Numero de ficheros en el zip "+str(num_files))
               else:
                   if "channels" in str(name):
                       
                       z.extract(name,xbmc.translatePath(path))                
                       num_files+=1
                       #xbmc.log("Numero de ficheros en el zip "+str(num_files))
               
           fh.close()
           
           if notify:
               xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,str(num_files)+" files extracted from "+version_to_download+".zip ", __time__, icon))            
           
           
           
           if version_plugin=="classic":
              if what=="todo":
                  ori = xbmc.translatePath(os.path.join(path,'pelisalacarta-'+version_to_download+'/python/main-classic'))
                  dest =  xbmc.translatePath(os.path.join(path2,'addons/plugin.video.pelisalacarta'))
              else:
                  ori = xbmc.translatePath(os.path.join(path,'pelisalacarta-'+version_to_download+'/python/main-classic/channels'))
                  dest =  xbmc.translatePath(os.path.join(path2,'addons/plugin.video.pelisalacarta/channels'))
           
           else:           
           
              ori = xbmc.translatePath(os.path.join(path,'pelisalacarta-'+version_to_download+'/python/main-classic/channels'))
              dest =  xbmc.translatePath(os.path.join(path2,'addons/plugin.video.pelisalacarta-ui/channels'))
           
           try:
               copydir(ori,dest,num_files)	                                            
           
           except Exception as exp:
               s=str(exp)
               xbmc.log('UpdPelisALaCarta - Error en el proceso '+s)  
               xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"Error upgrading "+s, __time__*3, icon))
           
           shutil.rmtree(xbmc.translatePath(os.path.join(path,'pelisalacarta-'+version_to_download)))
           
           try:
               os.remove(xbmc.translatePath(os.path.join(path,'pelis.zip.old')))
           except:
               xbmc.log('no existia pelis.zip.old')
           
           os.rename(xbmc.translatePath(os.path.join(path,'pelis.zip')),xbmc.translatePath(os.path.join(path,'pelis.zip.old')))
        
           xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"Upgraded from git-"+version_to_download, 2*__time__ , icon))    
        
        except Exception as e:
           s = str(e)
           xbmc.log('UpdPelisALaCarta - Error en el proceso '+s)  
           xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"Error upgrading", __time__, icon))
   
    else:
        if notify:
           xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"No need to upgrade", __time__ , icon))
           
    #if notify:
    #    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,"Finished checking", __time__, icon))
    
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
