# ToDo-App
Todo list app made with Python
___________________________________________
To bundle executable version of this program:
1. Install pyinstaller package
2. Open this project folder in terminal
3. Run the following command:  
    `pyinstaller --hidden-import babel.numbers --onedir -w main.py --runtime-hook addlib.py`
4. After some minutes, these things will be generated inside the project folder:
   - A file named *main.spec*
   - A folder named *build*
   - A folder named *dist*, which has our *main* program folder inside.
5. Copy the *img* folder and paste it inside the *dist/main* folder.
The *img* folder **MUST** be in the same folder as *main.exe* 
6. Now you can open *dist/main* and run the file *main.exe*
7. To make the program folder tidier:
    - Create a folder name ***lib*** inside *dist/main* (You MUST name this folder ***lib***)
    - Move all the **FILES** (NOT folders) inside *dist/main* into *lib* folder, except:
      - *base_library.zip*
      - *main.exe*
      - *python38.dll*
8. Now you can rename the program folder (*dist/main*) to anything you'd like.
___________________________________________
# Change log:
- 01/17/2022: 
  - Created the GUI.
  - Added login and logout features.
- 01/18/2022:
  - Users can now sign up.
  - Admin can now add new user accounts.
  - Users can now update their information in the "Profile" tab.
  - Admin can now manage users properly (add, remove, edit, restrict).
- 01/19/2022:
  - Added various functionalities to the main to-do list, including:
    - Add new task.
    - Delete task.
    - Mark as finished.
    - View and edit task information.
    - Filter tasks by date (using the calendar).
    - Filter overlapping tasks.
  - Added an option to minimize the program to system tray instead of exiting.
  - Task can now be repeatable daily, weekly, monthly or annually.
  - Release v1.0.