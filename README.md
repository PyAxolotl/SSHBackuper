# SSHBackuper
Python script that can be used to back up data from a directory located at a distant/local machine to another directory located at a distant/local machine using ssh via fabric python package

# Usage
sshbackup [-h] [--log LOG_TARGET] [--rm] [--sP SOURCE_PORT] [--sip SOURCE_ADDRESS] [--sp SOURCE_PASS] [--su SOURCE_USER] [--tP TARGET_PORT] [--tip TARGET_ADDRESS] [--tp TARGET_PASS] [--tu TARGET_USER] [--verbose] sdir tdir

positional arguments:  

  sdir                  Source directory  
  tdir                  Target directory  

optional arguments:  
  -h, --help            show this help message and exit  
  --log LOG_TARGET      Path for the logging directory/file.  
  --rm                  Remove data from source after a successful backup  
  --sP SOURCE_PORT      SSH port for the source machine  
  --sip SOURCE_ADDRESS  Source ip address or domain name (local machine will picked as source if nothing is specified)  
  --sp SOURCE_PASS      Password for the source machine  
  --su SOURCE_USER      Username for the source machine  
  --tP TARGET_PORT      SSH port for the target machine  
  --tip TARGET_ADDRESS  Target ip address or domain name (local machine will picked as target if nothing is specified)  
  --tp TARGET_PASS      Password for the target machine  
  --tu TARGET_USER      Username for the target machine  
  --verbose, -v         Verbose  
  
# Notes
* If you specify a distant source or target directory you can leave the option --sp or --tp empty and the program will ask you to enter them silently.
* Work still in progress: 
    * For now only the local -> local backup works and the distant -> local (with some bugs relative to permissions)
    * The only tested distant machines have ubuntu distribution and probably this script will need more work to include other OSes.

# Contribution
Send me a mail at abdellatifzied.saada@gmail.com
