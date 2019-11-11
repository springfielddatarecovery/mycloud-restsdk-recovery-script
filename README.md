# mycloud-restsdk-recovery-script
A script to recover files from MyCloud REST SDK Folder Structure

**Problem:**
MyCloud devices don't use a simple, flat filesystem like other external drives, they store files with random-seeming names and directory structures. If your MyCloud is not functioning, you will need to read the SQLite database on the device to determine the original file structure.

**Notes:**
SQLite database is stored in /restsdk/data/db/index.db. Inside the DB two main tables appear to be of interest, FILES and ImageTrans. FILES lists each file with a unique ID (primary key) and a ContentID (the name of the file when stored on the filesystem) along with the file name "My important picture.jpg" and some other metadata. I believe ImageTrans is only for thumbnailing purposes but I could be wrong about that. Importantly, the entries in FILES have a "parent" attribute which places each file in a directory structure. This script totally ignores ImageTrans.

**Solution:**
This script reads the database and a dump of the filesystem and copies the data to another location with the correct filenames and structures. This script is intended for a Linux machine where you already have the file structure and database extracted. This won't work on Windows. I know it's ugly and inefficient, I am new to python. This is tested and working with Python 3.6.

**If this script has helped you recover your data, please consider saying thanks with a Bitcoin donation**
1DqSLNR8kTgwq5rvveUFDSbYQnJp9D5gfR
