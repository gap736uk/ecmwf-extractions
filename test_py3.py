--- submit_job_rsync_netcdf_era5_new.py	(original)
+++ submit_job_rsync_netcdf_era5_new.py	(refactored)
@@ -45,8 +45,14 @@
 the period of 18:00 on 3rd Jan 1999 until 00:00 on 3rd Feb 1999.
 
 """
+from __future__ import division
+from __future__ import print_function
 
 # Import required standard modules
+from builtins import str
+from builtins import range
+from builtins import object
+from past.utils import old_div
 import os
 import sys
 import string
@@ -87,12 +93,12 @@
     """
     Nice error message that also prints usage string.
     """
-    print __doc__
-    print "\n",error,"\n"
+    print(__doc__)
+    print("\n",error,"\n")
     sys.exit()
 
 
-class MarsJob:
+class MarsJob(object):
   """
   Class to create and execute operational MARS jobs.
   """
@@ -109,7 +115,7 @@
     self.template = os.path.join(templatedir, self.superset, dataset)
     self.job_script = []  
     
-    if 'target_dir' not in kw.keys():
+    if 'target_dir' not in list(kw.keys()):
 
 
       if self.dparts[-1] == 'mm':
@@ -120,7 +126,7 @@
 
     # Set keywords as instance attributes
     
-    for key in kw.keys():
+    for key in list(kw.keys()):
         setattr(self, key, kw[key])
 
     # Create a list of dates if keyword 'end' provided
@@ -136,14 +142,14 @@
 
     # Run each method
     self.compileParts()
-    print self.writeJobFile()
+    print(self.writeJobFile())
 
 
     self.submitJob()
 
 
   def __setattribute__(self, att, value):
-    apply(setattr, att, value)
+    setattr(*att, **value)
     return    
 
 
@@ -178,23 +184,23 @@
                 loop_comm = ""
             
                 # Work out how many variables we should define for dates
-                nvars = int(len(self.datelist))/stream_div[self.dataset]
+                nvars = old_div(int(len(self.datelist)),stream_div[self.dataset])
                 vars=[]
                 if (len(self.datelist)%stream_div[self.dataset]) != 0: 
                     nvars = nvars+1
-                print "NCVARS", nvars
+                print("NCVARS", nvars)
                 
                 
                 for n in range(0,nvars):
                     s = n*stream_div[self.dataset]
                     dates = ""
                     for i in range(s,s+stream_div[self.dataset]):
-                        print i, n
+                        print(i, n)
                         if i == (len(self.datelist)):
                             break
                         else:
                             dates = dates+"%s/" % (self.datelist[i]) 
-                    print dates
+                    print(dates)
                         
                     loop_comm = loop_comm+"\nV%d='%s'\n" % (n, dates[:-1])
                 '''
@@ -278,7 +284,7 @@
 
 if __name__=="__main__":
     args = sys.argv
-    print "\nExecuting '%s' with arguments: " % args[0], args[1:],"\n"
+    print("\nExecuting '%s' with arguments: " % args[0], args[1:],"\n")
     if len(args) < 2:
        exitNicely("Not enough arguments given.")
     keywords = {}
@@ -316,11 +322,11 @@
         elif arg in ["--qos"]:
                 keywords['qos'] = args[args.index(arg) + 1]
         
-    if not keywords.has_key('start') and not keywords.has_key('ago'):
+    if 'start' not in keywords and 'ago' not in keywords:
     
        #exitNicely("No start date or 'ago' argument provided.")
        keywords['ago'] = '10'
-    if not keywords.has_key('qos'):
+    if 'qos' not in keywords:
         keywords['qos'] = 'normal'
     
     x = MarsJob(dataset, keywords) 
