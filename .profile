##################################################################
#  File: /usr/local/share/ecmwf/share/.profile_ecgate
#
#  Purpose: Shared setups for Bourne & Korn Shell users.
#           Read in once when you log in.
#           Specific version for RHEL ecgate
#
##################################################################
#Set umask
umask 027

# Set Path and check if /etc/profile is loaded (is it really necessary????)

# Don't set /usr/local/share !!  PAD 20130419
#export PATH=$PATH:/usr/local/share

# don't do this either !  PAD 20130419
#if test -z "$PROFILEREAD" ; then
## We've not gone through /etc/profile so add /usr/local/bin and $HOME/bin
#  export PATH=$PATH:/usr/local/bin
## LOGNAME is not set either - but do not export (see /etc/profile) !
#  LOGNAME=$USER
#fi

HOSTNAME=$(hostname)
OLD_PROFILE=/usr/local/share/ecmwf/share/.profile_ancient
case $HOSTNAME in
     lxa*|lxb*|hdr*)
        . $OLD_PROFILE
        return 0
        ;;
     *)
        ;;
esac

if [ -f /etc/SuSE-release ]; then
  _suse_version=$(cat /etc/SuSE-release | grep VERSION | awk '{ print $3 }')
  if [[ "$_suse_version" = "11.3" || $(echo $_suse_version | cut -d. -f1) -lt 11 ]]; then
    . $OLD_PROFILE
    return 0
  fi
fi

unset OLD_PROFILE

# echo "DEBUG: New profile"

# Check environment mode, initialize to interactive by default
[ "$ENVIRONMENT" != "BATCH" ] &&  export ENVIRONMENT=INTERACTIVE;

# Set several variables

ARCH=$(arch)                        ; export ARCH
ARCH_OS_MAJOR=$(uname -r | cut -c1) ; export ARCH_OS_MAJOR 
if [ $(uname) = "Linux" ]; then
   ARCH=linux
fi

which os_version  > /dev/null 2>&1 && OS_VERSION=$(os_version);    export OS_VERSION
which cpu_type  > /dev/null 2>&1 && CPU_TYPE=$(cpu_type) ;       export CPU_TYPE
which object_mode  > /dev/null 2>&1 && OBJECT_MODE=$(object_mode);  export OBJECT_MODE

[ -f /usr/local/apps/.ecplatform ] && export ECPLATFORM=$(cat /usr/local/apps/.ecplatform)

ECMWFHOME=/usr/local/share/ecmwf   ; export ECMWFHOME
[ -z "$SCRATCH" ] && SCRATCH=$(echo $HOME | sed -e 's,/home/,/scratch/,'); export SCRATCH
[ -z "$PERM" ] && PERM=$(echo $HOME | sed -e 's,/home/,/perm/,'); export PERM

[ -z "$EDITOR" ] && EDITOR=vi      ; export EDITOR

VISUAL=/bin/vi                 ; export VISUAL
HOST=$(uname -n | awk -F- '{print $1}'); export HOST
HOSTPROMPT=$HOST                   ; export HOSTPROMPT
[ -z "$GROUP" ] && GROUP=$(id |cut -d\( -f3 |cut -d\) -f1) ;export GROUP
[ -z "$PAGER" ] && PAGER='/usr/bin/less -x4efisM'; export PAGER

WSHOME=$HOME                       ; export WSHOME
MAIL=/var/mail/$USER; export MAIL

# Set the X11 app-defaults directory for locally installed apps.  P.Dando 20130531
 
if [ -d /usr/local/apps/X11/app-defaults ] ; then
  XAPPLRESDIR=/usr/local/apps/X11/app-defaults
  export XAPPLRESDIR
fi

# following retains behaviour of sort and ls from 7.3
export LC_COLLATE=POSIX # ???

# Set the default number of OpenMP threads to 1
export OMP_NUM_THREADS=1

#On the workstations define webeditroot
case $(ypmatch $(hostname) workstations  2>/dev/null | awk '{print $5}') in
  *client) 
    WEBEDITROOT=/var/tmp/$USER/www ; export WEBEDITROOT
    if [ ! -d $WEBEDITROOT ]; then
        mkdir -p $WEBEDITROOT
    fi
  ;;
esac


#
# Start of accounting variables definition

# Define the main accounting file
__ECACCT_FILE="/usr/local/share/project_accounts/accounts_per_user"

# If accounting file exists and not empty
if [[ -s ${__ECACCT_FILE} ]] ; then

#  Get the list of accounts for the relevant ${USER} 
   ECACCOUNTLIST=$( awk  -F':' '{ if ( $1 ~ /^'${USER}'$/ ) {gsub(/,/," ",$2) ;  print $2; exit  } }' ${__ECACCT_FILE} )

#  Get the the first account (and avoid a call to awk): this is the default account
   for ECACCOUNT in ${ECACCOUNTLIST} ; do  break ; done 

#  If no account found
   [[ "${ECACCOUNT}" = "" ]] && ECACCOUNT="ecnoaccount"
   
# Otherwise main accounting file is missing or empty

else 
    ECACCOUNTLIST=""
    ECACCOUNT="ecnoaccount"
fi

# Export important variables and cleanup
unset __ECACCT_FILE 
export ECACCOUNT ECACCOUNTLIST

#
# End of accounting variables definition
#

# set SCRATCHDIR and TMPDIR

if [ -z "$ENVONLY" ]
then
  if [ "X$SLURM_JOBID" != "X" ]; then
    TMPDIRNAME=$ECPLATFORM.slurm.$SLURM_JOBID
    SCRATCHDIRNAME=$TMPDIRNAME
  else    
    TMPDIRNAME=jtmp.$$
    SCRATCHDIRNAME=$HOST.$$ 
  fi

  TMPDIR=/var/tmp/tmpdir/$USER/$TMPDIRNAME; export TMPDIR
  if [ ! -d /var/tmp/tmpdir ]; then
    /usr/local/bin/root create_tmpdir
  fi
  if [ -d /var/tmp/tmpdir/$USER ]; then
    touch /var/tmp/tmpdir/$USER 2> /dev/null || /usr/local/bin/root create_tmpdir chown
  fi
  if [ "X$SCRATCH" != "X" ]; then
    SCRATCHDIR=$SCRATCH/scratchdir/$SCRATCHDIRNAME ; export SCRATCHDIR
  fi


  # Create SCRATCHDIR, TMPDIR

  # set SCRATCHDIR that will be deleted by the epilog on logout
  TRUESCRATCHDIR="" ; export TRUESCRATCHDIR
#  if [ "X$SCRATCH" != "X" ]; then
   if [ "X$SCRATCH" != "X" -a -d "$SCRATCH" ]; then
    if [ -x /usr/local/bin/timeout ]; then
      /usr/local/bin/timeout 20 mkdir -p $SCRATCHDIR
    else
      mkdir -p $SCRATCHDIR
    fi

    if [ $? -ne 0 ]; then
      echo "Failed to create/access $SCRATCHDIR, setting"
      echo "\$SCRATCHDIR to \$SCRATCH"
      echo ""
      SCRATCHDIR=$SCRATCH
      TRUESCRATCHDIR=""
      export TRUESCRATCHDIR
      echo ""
      echo "$SCRATCH may presently not be available,"
      echo "Please contact ECMWF Calldesk (calldesk@ecmwf.int)"
      echo ""
    elif [ -d $SCRATCHDIR ]; then
      TRUESCRATCHDIR=$SCRATCHDIR
      export TRUESCRATCHDIR
    else
      echo "Failed to create/access $SCRATCHDIR, setting"
      echo "\$SCRATCHDIR to \$SCRATCH"
      echo ""
      echo "Setting SCRATCHDIR to $SCRATCH"
      SCRATCHDIR=$SCRATCH
      TRUESCRATCHDIR=""
      export TRUESCRATCHDIR
    fi
  fi

  # set TMPDIR

  TRUE_TMPDIR="" ; export TRUE_TMPDIR
  #echo "$0: TMPDIR set to: " $TMPDIR
  if [ ! -d  $TMPDIR ]; then
    mkdir -p $TMPDIR
    if [ $? -ne 0 ]; then
      echo "Could not create $TMPDIR"
      echo "Please contact ECMWF Calldesk (calldesk@ecmwf.int)"
      TMPDIR=$SCRATCHDIR
      TRUE_TMPDIR="" ; export TRUE_TMPDIR
    else
      TRUE_TMPDIR=$TMPDIR; export TRUE_TMPDIR
    fi
  else 
    TRUE_TMPDIR=$TMPDIR; export TRUE_TMPDIR
  fi

  if [ "$ENVIRONMENT" != BATCH ]; then
    HISTFILE=$TMPDIR/.ksh_hist_$$; export HISTFILE
    rm -f $HISTFILE
    touch $HISTFILE
    HISTSIZE=100; export HISTSIZE
  fi
fi


###  Check for expired password:
if [ "$ENVIRONMENT" = INTERACTIVE ]; then 
    $ECMWFHOME/share/check_pw_expired.ecksh
# XA 2014-10-14: We were cating the motd when the .hushlogin was present
#    [ -f "$HOME/.hushlogin" ] && cat /etc/motd
#    [ ! -f "$HOME/.hushlogin" ] && cat /etc/motd
fi

trap 1 2 3

# force execution of the shared .epilog 
# when the login session/job terminates - this will delete the 
# TMPDIR SCRATCHDIR created

[ -z "$ENVONLY" -a $LOGNAME != "root" ] && trap '. /usr/local/share/ecmwf/share/.epilog.ecksh' 0 15

# Now load default modules:
#export CURRENT_SHELL=$(echo $0 | tr -d "-")
export CURRENT_SHELL=$(ps -p $$ -oargs= | cut -d" " -f1 | tr -d "-" | rev | cut -d"/" -f1 | rev)
#export CURRENT_SHELL=$(ps | grep -i $$ | grep -v grep | awk '{print $4}')
#source /usr/local/apps/module/init/$CURRENT_SHELL
[ -f /usr/local/apps/module/init/$CURRENT_SHELL ] && source /usr/local/apps/module/init/$CURRENT_SHELL
[ "$CURRENT_SHELL" != "bash" ] && export BASH_ENV=/usr/local/apps/module/init/bash

# If ecfs is not loaded by modules, make sure we have at least the ECFS_SYS_PATH defined
[ -z "$ECFS_SYS_PATH" ] && export ECFS_SYS_PATH=/usr/local/ecfs/prodn

# Ensure that infoboard system tray icon (infoicon) will be started
# automatically when logging in with KDE
if [ ! -z "$XDG_CURRENT_DESKTOP" ]; then
    [ ! -d $HOME/.kde/Autostart ] && mkdir -p $HOME/.kde/Autostart
    [ -f /usr/local/apps/infoboard/current/infoicon ] && ln -f -s /usr/local/apps/infoboard/current/infoicon $HOME/.kde/Autostart/infoicon
    [ ! -d $HOME/.kde4/Autostart ] && mkdir -p $HOME/.kde4/Autostart
    [ -f /usr/local/apps/infoboard/current/infoicon ] && ln -f -s /usr/local/apps/infoboard/current/infoicon $HOME/.kde4/Autostart/infoicon
fi

# Set user custom options
if test -z "$PROFILEREAD" ; then
# We've not been through /etc/profile so need to add $HOME/bin to PATH
# if it exists
  [ -d $HOME/bin ] && PATH=$PATH:$HOME/bin
fi

[ -d $HOME/bin/$ARCH ] && PATH=$PATH:$HOME/bin/$ARCH

[ -d "$UNIXTOOLS" ] && PATH=${PATH}:$UNIXTOOLS/bin
export PATH

# If the file $HOME/.user_profile exists and is executable then
# "dot" it
#
[ -f $HOME/.user_profile ] && . $HOME/.user_profile
