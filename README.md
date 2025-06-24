# To-Do List Desktop Application

A modern, feature-rich desktop to-do list application built with Python and Tkinter. This application provides comprehensive task management capabilities with a beautiful, intuitive interface.

## Features

### 🎯 Core Functionality
- **Category Management**: Create custom task categories with personalized names and colors
- **Task Management**: Add, edit, and organize tasks with detailed information
- **Multi-Tab Interface**: Three main views for different perspectives on your tasks

### 📋 Task Properties
Each task includes the following fields:
- **Name**: Task title/description
- **Category**: Assign tasks to custom categories
- **Priority**: High, Medium, or Low priority levels
- **Start Date**: When the task begins
- **Due Date**: When the task should be completed
- **Progress**: Percentage completion (0-100%)
- **Status**: Not Started, In Progress, Completed, or On Hold
- **Comments**: Additional notes and details
- **Date Completed**: Optional completion timestamp

### 🎨 User Interface
- **Modern Design**: Clean, rounded interface with professional styling
- **Light/Dark Mode**: Toggle between light and dark themes
- **Responsive Layout**: Adapts to different window sizes
- **Color-Coded Categories**: Visual organization with custom colors
- **Grid Layout**: Categories arranged in a 4-column grid on the main page

### 📊 Three Main Views

#### 1. Main Tab
- **Category Grid**: View all categories in a 4×n grid layout
- **Expandable Categories**: Click any category to see all its tasks
- **Visual Organization**: Categories displayed as colored rectangles
- **Task Details**: Comprehensive task information when expanded

#### 2. Tasks for the Day
- **Daily Focus**: Shows all tasks scheduled for the current day
- **Quick Overview**: Easy access to today's priorities
- **Full Task Details**: Complete information for each daily task

#### 3. Timeline (Gantt Chart)
- **Visual Timeline**: Gantt chart showing task durations
- **Status-Based Colors**: Tasks colored according to their status
- **Date Range**: Automatic scaling based on task start/end dates
- **Project Overview**: See all tasks in a timeline perspective

### 🔄 Global Updates
- **Real-time Synchronization**: Changes in any view update all other views
- **Persistent Storage**: All data saved automatically to JSON file
- **Consistent State**: Task modifications reflect everywhere immediately

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup
1. Clone or download this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Usage

### Getting Started
1. **Create Categories**: Click "Add New" → "New Category" to create your first category
2. **Add Tasks**: Click "Add New" → "New Task" to add tasks to your categories
3. **Organize**: Use the main tab to view and expand categories
4. **Track Progress**: Use the timeline to see your project overview
5. **Daily Focus**: Check "Tasks for the Day" for current priorities

### Navigation
- **Header Tabs**: Switch between Main, Tasks for the Day, and Timeline views
- **Category Expansion**: Click any category rectangle to see its tasks
- **Back Button**: Return to the category grid from expanded view
- **Theme Toggle**: Switch between light and dark modes using the moon/sun button

### Data Management
- **Automatic Saving**: All changes are saved automatically
- **Data File**: Application data stored in `todo_data.json`
- **Backup**: You can backup the JSON file to preserve your data

## Technical Details

### Architecture
- **Frontend**: Tkinter GUI framework
- **Data Storage**: JSON file-based persistence
- **Date Handling**: tkcalendar for date selection
- **Theme System**: Dynamic light/dark mode switching

### File Structure
```
ToDoListApp/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── todo_data.json      # Application data (created automatically)
└── To-Do List (3.0.0).xlsm  # Original Excel file
```

### Dependencies
- `tkinter`: GUI framework (included with Python)
- `tkcalendar`: Date picker widget
- `pillow`: Image processing (for future logo support)

## Customization

### Adding a Logo
The application includes a placeholder for a logo in the header. To add your own logo:
1. Place your logo image file in the project directory
2. Modify the logo section in `main.py` to load and display your image
3. Recommended format: PNG or JPG, 60x60 pixels

### Theme Customization
The application supports light and dark themes. You can customize colors by modifying the `apply_theme()` method in the `TodoApp` class.

## Future Enhancements

Potential features for future versions:
- Task filtering and search
- Export to Excel/PDF
- Task dependencies and relationships
- Reminder notifications
- Team collaboration features
- Data import from Excel files
- Advanced reporting and analytics

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
2. **Date Issues**: Make sure your system date is set correctly
3. **Display Problems**: Try adjusting your screen resolution or DPI settings

### Data Recovery
If the application data becomes corrupted:
1. Close the application
2. Rename or delete `todo_data.json`
3. Restart the application (it will create a new data file)

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

---

**Enjoy organizing your tasks with this modern, feature-rich to-do list application!** 🚀
