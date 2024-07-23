from cx_Freeze import setup, Executable

# Define the executable
executables = [Executable("alarm_analyzer.py", base="Win32GUI", icon="zte_logo.ico")]

# Setup configuration
setup(
    name="YourAppName",
    version="1.0",
    description="analyzer",
    options={
        "build_exe": {
            "packages": [],
            "excludes": [],
            "include_files": ["zte_logo.jpeg"],  # Include the image file
        }
    },
    executables=executables
)
