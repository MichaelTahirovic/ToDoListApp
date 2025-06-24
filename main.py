import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
try:
    from tkcalendar import DateEntry
except ImportError:
    # Fallback if tkcalendar is not available
    DateEntry = None
from datetime import datetime, timedelta
import json
import os
try:
    from PIL import Image, ImageTk
except ImportError:
    # Fallback if PIL is not available
    Image = None
    ImageTk = None

import math

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("1400x900")  # Increased window size
        self.root.configure(bg='#f0f0f0')
        
        # Data storage
        self.categories = {}
        self.tasks = []
        self.dark_mode = False
        
        # Load data
        self.load_data()
        
        # Create UI
        self.create_header()
        self.create_main_content()
        
        # Apply initial theme
        self.apply_theme()
        
    def load_data(self):
        """Load data from JSON file if it exists"""
        if os.path.exists('todo_data.json'):
            try:
                with open('todo_data.json', 'r') as f:
                    data = json.load(f)
                    self.categories = data.get('categories', {})
                    self.tasks = data.get('tasks', [])
            except:
                self.categories = {}
                self.tasks = []
        else:
            self.categories = {}
            self.tasks = []
    
    def save_data(self):
        """Save data to JSON file"""
        data = {
            'categories': self.categories,
            'tasks': self.tasks
        }
        with open('todo_data.json', 'w') as f:
            json.dump(data, f, indent=2)
    
    def create_header(self):
        """Create the header with logo placeholder, navigation, and buttons"""
        self.header = tk.Frame(self.root, height=80, bg='#ffffff')
        self.header.pack(fill='x', padx=10, pady=5)
        self.header.pack_propagate(False)
        
        # Logo placeholder (left)
        self.logo_frame = tk.Frame(self.header, bg='#e0e0e0', width=60, height=60)
        self.logo_frame.place(x=10, y=10)
        self.logo_frame.pack_propagate(False)
        
        logo_label = tk.Label(self.logo_frame, text="LOGO", bg='#e0e0e0', fg='#666666')
        logo_label.pack(expand=True)
        
        # Dark/Light mode button (left of logo)
        self.theme_btn = tk.Button(self.header, text="🌙", font=('Arial', 16), 
                                 command=self.toggle_theme, bg='#ffffff', bd=0,
                                 cursor='hand2')  # Add cursor pointer
        self.theme_btn.place(x=80, y=20)
        
        # Add New button (right)
        self.add_btn = tk.Button(self.header, text="+ Add New", font=('Arial', 12, 'bold'),
                               command=self.show_add_dialog, bg='#4CAF50', fg='white',
                               bd=0, padx=20, pady=10, relief='flat', cursor='hand2')
        self.add_btn.place(relx=1.0, x=-120, y=20)
        
        # Tab navigation (center)
        self.tab_frame = tk.Frame(self.header, bg='#ffffff')
        self.tab_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        self.tabs = ['Main', 'Tasks for the Day', 'Timeline']
        self.current_tab = tk.StringVar(value='Main')
        
        for tab in self.tabs:
            btn = tk.Button(self.tab_frame, text=tab, font=('Arial', 11),
                          command=lambda t=tab: self.switch_tab(t),
                          bg='#ffffff', bd=0, padx=15, pady=8, cursor='hand2')
            btn.pack(side='left', padx=5)
    
    def create_main_content(self):
        """Create the main content area"""
        self.main_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create tab content frames
        self.tab_content = {}
        
        # Main tab
        self.tab_content['Main'] = tk.Frame(self.main_frame, bg='#f0f0f0')
        self.create_main_tab()
        
        # Tasks for the Day tab
        self.tab_content['Tasks for the Day'] = tk.Frame(self.main_frame, bg='#f0f0f0')
        self.create_tasks_for_day_tab()
        
        # Timeline tab
        self.tab_content['Timeline'] = tk.Frame(self.main_frame, bg='#f0f0f0')
        self.create_timeline_tab()
        
        # Show main tab initially
        self.show_tab('Main')
    
    def create_main_tab(self):
        """Create the main tab with category grid"""
        # Categories container
        self.categories_frame = tk.Frame(self.tab_content['Main'], bg='#f0f0f0')
        self.categories_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.update_categories_display()
    
    def create_tasks_for_day_tab(self):
        """Create the tasks for the day tab"""
        # Title
        title_label = tk.Label(self.tab_content['Tasks for the Day'], 
                             text="Tasks for Today", font=('Arial', 20, 'bold'),
                             bg='#f0f0f0', fg='#333333')
        title_label.pack(pady=20)
        
        # Tasks list
        self.tasks_for_day_frame = tk.Frame(self.tab_content['Tasks for the Day'], bg='#f0f0f0')
        self.tasks_for_day_frame.pack(fill='both', expand=True, padx=20)
        
        self.update_tasks_for_day()
    
    def create_timeline_tab(self):
        """Create the timeline tab with Gantt chart"""
        # Title
        title_label = tk.Label(self.tab_content['Timeline'], 
                             text="Project Timeline", font=('Arial', 20, 'bold'),
                             bg='#f0f0f0', fg='#333333')
        title_label.pack(pady=20)
        
        # Timeline container with fixed height
        timeline_container = tk.Frame(self.tab_content['Timeline'], bg='#f0f0f0', height=500)
        timeline_container.pack(fill='x', padx=20, pady=10)
        timeline_container.pack_propagate(False)
        
        # Timeline canvas with scrollbars
        self.timeline_canvas = tk.Canvas(timeline_container, bg='white', 
                                       relief='solid', bd=1, height=400)
        
        # Horizontal scrollbar for timeline
        h_scrollbar = ttk.Scrollbar(timeline_container, orient="horizontal", command=self.timeline_canvas.xview)
        
        # Vertical scrollbar for tasks
        v_scrollbar = ttk.Scrollbar(timeline_container, orient="vertical", command=self.timeline_canvas.yview)
        
        # Configure canvas scrolling
        self.timeline_canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        # Pack scrollbars and canvas
        h_scrollbar.pack(side='bottom', fill='x')
        v_scrollbar.pack(side='right', fill='y')
        self.timeline_canvas.pack(side='left', fill='both', expand=True)
        
        self.update_timeline()
    
    def update_categories_display(self):
        """Update the categories grid display"""
        # Clear current category tracking
        if hasattr(self, 'current_category_id'):
            delattr(self, 'current_category_id')
        
        # Clear existing widgets
        for widget in self.categories_frame.winfo_children():
            widget.destroy()
        
        if not self.categories:
            # Show empty state
            empty_label = tk.Label(self.categories_frame, 
                                 text="No categories yet. Click 'Add New' to create one!",
                                 font=('Arial', 14), bg='#f0f0f0', fg='#666666')
            empty_label.pack(expand=True)
            return
        
        # Create grid
        row = 0
        col = 0
        max_cols = 4
        
        for cat_id, category in self.categories.items():
            # Category rectangle
            cat_frame = tk.Frame(self.categories_frame, bg=category['color'], 
                               relief='solid', bd=1, padx=20, pady=15)
            cat_frame.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
            
            # Category name
            name_label = tk.Label(cat_frame, text=category['name'], 
                                font=('Arial', 14, 'bold'), bg=category['color'],
                                fg='white')
            name_label.pack()
            
            # Task count
            task_count = len([t for t in self.tasks if t['category_id'] == cat_id])
            count_label = tk.Label(cat_frame, text=f"{task_count} tasks", 
                                 font=('Arial', 10), bg=category['color'], fg='white')
            count_label.pack()
            
            # Bind click event
            cat_frame.bind('<Button-1>', lambda e, cid=cat_id: self.expand_category(cid))
            name_label.bind('<Button-1>', lambda e, cid=cat_id: self.expand_category(cid))
            count_label.bind('<Button-1>', lambda e, cid=cat_id: self.expand_category(cid))
            
            # Update grid position
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Configure grid weights
        for i in range(max_cols):
            self.categories_frame.columnconfigure(i, weight=1)
    
    def expand_category(self, category_id):
        """Expand a category to show its tasks"""
        # Store current category for navigation
        self.current_category_id = category_id
        
        # Clear existing widgets
        for widget in self.categories_frame.winfo_children():
            widget.destroy()
        
        category = self.categories[category_id]
        
        # Create expanded category header
        header_frame = tk.Frame(self.categories_frame, bg=category['color'], 
                              relief='solid', bd=1, padx=20, pady=15)
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Back button
        back_btn = tk.Button(header_frame, text="← Back", font=('Arial', 10),
                           command=self.update_categories_display, bg=category['color'],
                           fg='white', bd=0, cursor='hand2')
        back_btn.pack(side='left')
        
        # Category name
        name_label = tk.Label(header_frame, text=category['name'], 
                            font=('Arial', 16, 'bold'), bg=category['color'], fg='white')
        name_label.pack(side='left', padx=20)
        
        # Edit category button (only shown when expanded)
        edit_btn = tk.Button(header_frame, text="Edit Category", font=('Arial', 10),
                           command=lambda: self.edit_category(category_id), bg=category['color'],
                           fg='white', bd=1, relief='solid', padx=10, pady=2, cursor='hand2')
        edit_btn.pack(side='right')
        
        # Tasks container with scrollbar
        tasks_container = tk.Frame(self.categories_frame, bg=self.lighten_color(category['color']))
        tasks_container.pack(fill='both', expand=True)
        
        # Create canvas for scrollable tasks
        canvas = tk.Canvas(tasks_container, bg=self.lighten_color(category['color']), highlightthickness=0)
        scrollbar = ttk.Scrollbar(tasks_container, orient="vertical", command=canvas.yview)
        scrollable_tasks_frame = tk.Frame(canvas, bg=self.lighten_color(category['color']))
        
        scrollable_tasks_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_tasks_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Get tasks for this category
        category_tasks = [t for t in self.tasks if t['category_id'] == category_id]
        
        if not category_tasks:
            empty_label = tk.Label(scrollable_tasks_frame, text="No tasks in this category yet.",
                                 font=('Arial', 12), bg=self.lighten_color(category['color']))
            empty_label.pack(pady=50)
        else:
            # Create task list
            for task in category_tasks:
                self.create_task_widget(scrollable_tasks_frame, task, category['color'])
    
    def create_task_widget(self, parent, task, category_color):
        """Create a widget for displaying a task"""
        # Choose background color based on status
        status_colors = {
            'Not Started': '#ffebee',  # Light red
            'In Progress': '#fff8e1',  # Light yellow
            'Completed': '#e8f5e8',    # Light green
            'On Hold': '#f3e5ab'       # Light yellow-brown
        }
        bg_color = status_colors.get(task['status'], 'white')
        
        task_frame = tk.Frame(parent, bg=bg_color, relief='solid', bd=1, padx=15, pady=10)
        task_frame.pack(fill='x', pady=5, padx=10)
        
        # Task header
        header_frame = tk.Frame(task_frame, bg=bg_color)
        header_frame.pack(fill='x')
        
        # Task name
        name_label = tk.Label(header_frame, text=task['name'], font=('Arial', 12, 'bold'),
                            bg=bg_color, fg='#333333')
        name_label.pack(side='left')
        
        # Priority with updated colors
        priority_colors = {'High': '#ff4444', 'Medium': '#ffaa00', 'Low': '#ffdd00'}  # Low is now yellow
        priority_label = tk.Label(header_frame, text=task['priority'], 
                                font=('Arial', 10), bg=priority_colors.get(task['priority'], '#cccccc'),
                                fg='white', padx=8, pady=2, relief='solid', bd=1)
        priority_label.pack(side='right', padx=(5, 0))
        
        # Status box
        status_box_colors = {
            'Not Started': '#ff4444',
            'In Progress': '#ffaa00', 
            'Completed': '#44aa44',
            'On Hold': '#8B4513'  # Brown
        }
        status_label = tk.Label(header_frame, text=task['status'], 
                              font=('Arial', 10), bg=status_box_colors.get(task['status'], '#cccccc'),
                              fg='white', padx=8, pady=2, relief='solid', bd=1)
        status_label.pack(side='right', padx=(5, 0))
        
        # Progress box with color gradient
        progress = task['progress']
        if progress <= 25:
            progress_color = '#ff4444'  # Red
        elif progress <= 50:
            progress_color = '#ff8800'  # Orange
        elif progress <= 75:
            progress_color = '#ffaa00'  # Yellow
        else:
            progress_color = '#44aa44'  # Green
            
        progress_label = tk.Label(header_frame, text=f"{progress}%", 
                                font=('Arial', 10), bg=progress_color,
                                fg='white', padx=8, pady=2, relief='solid', bd=1)
        progress_label.pack(side='right', padx=(5, 0))
        
        # Task details
        details_frame = tk.Frame(task_frame, bg=bg_color)
        details_frame.pack(fill='x', pady=(5, 0))
        
        # Dates
        dates_text = f"Start: {task['start_date']} | Due: {task['due_date']}"
        if task.get('date_completed'):
            dates_text += f" | Completed: {task['date_completed']}"
        
        dates_label = tk.Label(details_frame, text=dates_text, font=('Arial', 9),
                             bg=bg_color, fg='#666666')
        dates_label.pack(side='left')
        
        # Comments
        if task.get('comments'):
            comment_label = tk.Label(task_frame, text=f"Comments: {task['comments']}", 
                                   font=('Arial', 9), bg=bg_color, fg='#666666',
                                   wraplength=600, justify='left')  # Increased wraplength
            comment_label.pack(anchor='w', pady=(5, 0))
        
        # Buttons frame
        buttons_frame = tk.Frame(task_frame, bg=bg_color)
        buttons_frame.pack(anchor='e', pady=(5, 0))
        
        # Check if task is in today's list
        is_in_today = hasattr(self, 'today_tasks') and any(t['id'] == task['id'] for t in self.today_tasks)
        
        # Add to Today / Remove from Today button
        if is_in_today:
            today_btn = tk.Button(buttons_frame, text="Doing Today", font=('Arial', 9),
                                command=lambda: self.remove_from_today(task), bg='#87CEEB',  # Light blue
                                fg='white', bd=0, padx=10, pady=2, cursor='hand2')
        else:
            today_btn = tk.Button(buttons_frame, text="Add to Today", font=('Arial', 9),
                                command=lambda: self.add_to_today(task), bg='#2196F3',
                                fg='white', bd=0, padx=10, pady=2, cursor='hand2')
        today_btn.pack(side='right', padx=(5, 0))
        
        # Complete Task button (only show if not completed)
        if task['status'] != 'Completed':
            complete_btn = tk.Button(buttons_frame, text="Complete Task", font=('Arial', 9),
                                   command=lambda: self.complete_task(task), bg='#4CAF50',
                                   fg='white', bd=0, padx=10, pady=2, cursor='hand2')
            complete_btn.pack(side='right', padx=(5, 0))
        
        # Edit button
        edit_btn = tk.Button(buttons_frame, text="Edit", font=('Arial', 9),
                           command=lambda: self.edit_task(task), bg='#FF9800',
                           fg='white', bd=0, padx=10, pady=2, cursor='hand2')
        edit_btn.pack(side='right')
    
    def complete_task(self, task):
        """Complete a task by setting status to completed, progress to 100%, and adding completion date"""
        task['status'] = 'Completed'
        task['progress'] = 100
        task['date_completed'] = datetime.now().strftime('%Y-%m-%d')
        
        # Update the task in today's list if it exists there
        if hasattr(self, 'today_tasks'):
            for today_task in self.today_tasks:
                if today_task['id'] == task['id']:
                    today_task['status'] = 'Completed'
                    today_task['progress'] = 100
                    today_task['date_completed'] = datetime.now().strftime('%Y-%m-%d')
                    break
        
        self.save_data()
        self.update_all_displays()
        messagebox.showinfo("Success", f"Task '{task['name']}' marked as completed!")

    def remove_from_today(self, task):
        """Remove a task from the 'Tasks for the Day' list"""
        if hasattr(self, 'today_tasks'):
            self.today_tasks = [t for t in self.today_tasks if t['id'] != task['id']]
            self.update_tasks_for_day()
            messagebox.showinfo("Success", f"Task '{task['name']}' removed from today's list!")

    def add_to_today(self, task):
        """Add a task to the 'Tasks for the Day' list"""
        # Check if task is already in today's list
        if not hasattr(self, 'today_tasks'):
            self.today_tasks = []
        
        # Check if task is already added
        for today_task in self.today_tasks:
            if today_task['id'] == task['id']:
                messagebox.showinfo("Info", "This task is already in your today's list!")
                return
        
        # Add task to today's list
        self.today_tasks.append(task.copy())
        messagebox.showinfo("Success", f"Task '{task['name']}' added to today's list!")
        
        # Update all displays to reflect the change immediately
        self.update_all_displays()
    
    def update_tasks_for_day(self):
        """Update the tasks for the day display"""
        # Clear existing widgets
        for widget in self.tasks_for_day_frame.winfo_children():
            widget.destroy()
        
        # Check if we have today's tasks
        if not hasattr(self, 'today_tasks') or not self.today_tasks:
            empty_label = tk.Label(self.tasks_for_day_frame, 
                                 text="No tasks added for today. Use the 'Add to Today' button on tasks to add them here!",
                                 font=('Arial', 14), bg='#f0f0f0', fg='#666666')
            empty_label.pack(expand=True)
            return
        
        # Title with count
        title_frame = tk.Frame(self.tasks_for_day_frame, bg='#f0f0f0')
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(title_frame, text=f"Tasks for Today ({len(self.today_tasks)} tasks)", 
                             font=('Arial', 20, 'bold'), bg='#f0f0f0', fg='#333333')
        title_label.pack(side='left')
        
        # Clear all button
        clear_btn = tk.Button(title_frame, text="Clear All", font=('Arial', 10),
                            command=self.clear_today_tasks, bg='#f44336', fg='white',
                            bd=0, padx=15, pady=5, cursor='hand2')
        clear_btn.pack(side='right')
        
        # Create scrollable container for tasks
        tasks_container = tk.Frame(self.tasks_for_day_frame, bg='#f0f0f0')
        tasks_container.pack(fill='both', expand=True)
        
        # Create canvas for scrollable tasks
        canvas = tk.Canvas(tasks_container, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(tasks_container, orient="vertical", command=canvas.yview)
        scrollable_tasks_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        scrollable_tasks_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_tasks_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Display today's tasks
        for task in self.today_tasks:
            category = self.categories.get(task['category_id'], {})
            self.create_task_widget(scrollable_tasks_frame, task, 
                                  category.get('color', '#cccccc'))
    
    def clear_today_tasks(self):
        """Clear all tasks from today's list"""
        if hasattr(self, 'today_tasks') and self.today_tasks:
            result = messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks from today's list?")
            if result:
                self.today_tasks = []
                self.update_tasks_for_day()
                messagebox.showinfo("Success", "All tasks cleared from today's list!")
        else:
            messagebox.showinfo("Info", "No tasks to clear!")
    
    def update_timeline(self):
        """Update the timeline/Gantt chart with enhanced features"""
        self.timeline_canvas.delete('all')
        
        if not self.tasks:
            self.timeline_canvas.create_text(400, 200, text="No tasks to display",
                                          font=('Arial', 14), fill='#666666')
            return
        
        # Calculate timeline dimensions
        canvas_width = max(800, len(self.tasks) * 200)  # Minimum width
        canvas_height = 400
        
        # Find date range
        all_dates = []
        for task in self.tasks:
            all_dates.extend([task['start_date'], task['due_date']])
        
        if all_dates:
            min_date = min(all_dates)
            max_date = max(all_dates)
            
            # Convert dates to datetime objects
            min_dt = datetime.strptime(min_date, '%Y-%m-%d')
            max_dt = datetime.strptime(max_date, '%Y-%m-%d')
            
            # Expand to full months
            start_month = datetime(min_dt.year, min_dt.month, 1)
            if max_dt.month == 12:
                end_month = datetime(max_dt.year + 1, 1, 1)
            else:
                end_month = datetime(max_dt.year, max_dt.month + 1, 1)
            
            # Calculate total days
            total_days = (end_month - start_month).days
            
            # Set canvas scroll region
            self.timeline_canvas.configure(scrollregion=(0, 0, canvas_width, canvas_height))
            
            # Draw timeline
            margin_left = 150  # Space for task names
            margin_top = 50    # Space for date headers
            chart_width = canvas_width - margin_left
            chart_height = canvas_height - margin_top
            
            # Draw horizontal axis (dates)
            self.draw_date_axis(start_month, end_month, margin_left, margin_top, chart_width)
            
            # Draw vertical axis (task names)
            self.draw_task_axis(margin_left, margin_top, chart_height)
            
            # Draw task bars
            y_spacing = chart_height / (len(self.tasks) + 1)
            for i, task in enumerate(self.tasks):
                y = margin_top + (i + 1) * y_spacing
                
                # Calculate bar position
                start_dt = datetime.strptime(task['start_date'], '%Y-%m-%d')
                end_dt = datetime.strptime(task['due_date'], '%Y-%m-%d')
                
                start_x = margin_left + ((start_dt - start_month).days / total_days) * chart_width
                end_x = margin_left + ((end_dt - start_month).days / total_days) * chart_width
                
                # Choose color based on status
                status_colors = {
                    'Not Started': '#ff4444',
                    'In Progress': '#ffaa00',
                    'Completed': '#44aa44',
                    'On Hold': '#8B4513'
                }
                color = status_colors.get(task['status'], '#cccccc')
                
                # Draw task bar
                self.timeline_canvas.create_rectangle(start_x, y - 10, end_x, y + 10,
                                                   fill=color, outline='black', width=2)
                
                # Add task name on the left (always visible)
                self.timeline_canvas.create_text(margin_left - 5, y, text=task['name'],
                                              anchor='e', font=('Arial', 9))

    def draw_date_axis(self, start_month, end_month, margin_left, margin_top, chart_width):
        """Draw the date axis with months and days"""
        current_month = start_month
        x_offset = 0
        
        while current_month < end_month:
            # Get days in current month
            if current_month.month == 12:
                next_month = datetime(current_month.year + 1, 1, 1)
            else:
                next_month = datetime(current_month.year, current_month.month + 1, 1)
            
            days_in_month = (next_month - current_month).days
            month_width = (days_in_month / (end_month - start_month).days) * chart_width
            
            # Draw month header
            month_name = current_month.strftime('%B %Y')
            self.timeline_canvas.create_text(margin_left + x_offset + month_width/2, margin_top/2, 
                                          text=month_name, font=('Arial', 10, 'bold'), anchor='center')
            
            # Draw day markers (every 5 days for readability)
            for day in range(1, days_in_month + 1, 5):
                day_date = datetime(current_month.year, current_month.month, day)
                day_x = margin_left + x_offset + ((day_date - start_month).days / (end_month - start_month).days) * chart_width
                
                # Draw day marker
                self.timeline_canvas.create_line(day_x, margin_top - 5, day_x, margin_top + 5, 
                                              fill='black', width=1)
                
                # Draw day number
                self.timeline_canvas.create_text(day_x, margin_top + 15, text=str(day), 
                                              font=('Arial', 8), anchor='center')
            
            x_offset += month_width
            current_month = next_month
        
        # Draw main axis line
        self.timeline_canvas.create_line(margin_left, margin_top, margin_left + chart_width, margin_top,
                                      fill='black', width=2)

    def draw_task_axis(self, margin_left, margin_top, chart_height):
        """Draw the task axis with task names"""
        # Draw vertical axis line
        self.timeline_canvas.create_line(margin_left, margin_top, margin_left, margin_top + chart_height,
                                      fill='black', width=2)
    
    def show_add_dialog(self):
        """Show dialog to add new category or task"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New")
        dialog.geometry("400x300")
        dialog.configure(bg='#f0f0f0')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog safely
        try:
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
            y = (dialog.winfo_screenheight() // 2) - (300 // 2)
            dialog.geometry(f"400x300+{x}+{y}")
        except:
            # Fallback centering
            dialog.geometry("400x300+100+100")
        
        # Title
        title_label = tk.Label(dialog, text="What would you like to add?", 
                             font=('Arial', 16, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=20)
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg='#f0f0f0')
        btn_frame.pack(expand=True)
        
        category_btn = tk.Button(btn_frame, text="New Category", font=('Arial', 12),
                               command=lambda: [dialog.destroy(), self.add_category()],
                               bg='#2196F3', fg='white', padx=30, pady=15, bd=0, cursor='hand2')
        category_btn.pack(pady=10)
        
        task_btn = tk.Button(btn_frame, text="New Task", font=('Arial', 12),
                           command=lambda: [dialog.destroy(), self.add_task()],
                           bg='#4CAF50', fg='white', padx=30, pady=15, bd=0, cursor='hand2')
        task_btn.pack(pady=10)
    
    def add_category(self):
        """Add a new category"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Category")
        dialog.geometry("400x250")
        dialog.configure(bg='#f0f0f0')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (250 // 2)
        dialog.geometry(f"400x250+{x}+{y}")
        
        # Form
        form_frame = tk.Frame(dialog, bg='#f0f0f0')
        form_frame.pack(expand=True, padx=20, pady=20)
        
        # Category name
        tk.Label(form_frame, text="Category Name:", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w')
        name_entry = tk.Entry(form_frame, font=('Arial', 12), width=30)
        name_entry.pack(fill='x', pady=(5, 15))
        
        # Color selection
        tk.Label(form_frame, text="Color:", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w')
        color_frame = tk.Frame(form_frame, bg='#f0f0f0')
        color_frame.pack(fill='x', pady=(5, 15))
        
        selected_color = tk.StringVar(value='#4CAF50')
        color_preview = tk.Frame(color_frame, bg=selected_color.get(), width=30, height=30)
        color_preview.pack(side='left', padx=(0, 10))
        
        def choose_color():
            color = colorchooser.askcolor(title="Choose Category Color")[1]
            if color:
                selected_color.set(color)
                color_preview.configure(bg=color)
        
        color_btn = tk.Button(color_frame, text="Choose Color", command=choose_color,
                            bg='#2196F3', fg='white', bd=0, padx=15, pady=5)
        color_btn.pack(side='left')
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg='#f0f0f0')
        btn_frame.pack(fill='x', pady=(20, 0))
        
        def save_category():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter a category name")
                return
            
            cat_id = str(len(self.categories) + 1)
            self.categories[cat_id] = {
                'name': name,
                'color': selected_color.get()
            }
            
            self.save_data()
            self.update_categories_display()
            dialog.destroy()
            messagebox.showinfo("Success", "Category added successfully!")
        
        save_btn = tk.Button(btn_frame, text="Save", command=save_category,
                           bg='#4CAF50', fg='white', bd=0, padx=20, pady=8)
        save_btn.pack(side='right', padx=(10, 0))
        
        cancel_btn = tk.Button(btn_frame, text="Cancel", command=dialog.destroy,
                             bg='#f44336', fg='white', bd=0, padx=20, pady=8)
        cancel_btn.pack(side='right')
    
    def add_task(self):
        """Add a new task"""
        if not self.categories:
            messagebox.showwarning("Warning", "Please create a category first!")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Task")
        dialog.geometry("800x900")  # Increased size significantly
        dialog.configure(bg='#f0f0f0')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog safely
        try:
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (800 // 2)
            y = (dialog.winfo_screenheight() // 2) - (900 // 2)
            dialog.geometry(f"800x900+{x}+{y}")
        except:
            # Fallback centering
            dialog.geometry("800x900+100+100")
        
        # Main container with scrollbar
        main_container = tk.Frame(dialog, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(main_container, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Form
        form_frame = tk.Frame(scrollable_frame, bg='#f0f0f0')
        form_frame.pack(expand=True, padx=20, pady=20)
        
        # Task name
        tk.Label(form_frame, text="Task Name:", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w')
        name_entry = tk.Entry(form_frame, font=('Arial', 12), width=70)  # Increased width significantly
        name_entry.pack(fill='x', pady=(5, 15))
        
        # Category selection
        tk.Label(form_frame, text="Category:", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w')
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(form_frame, textvariable=category_var, 
                                    values=[cat['name'] for cat in self.categories.values()],
                                    font=('Arial', 12), state='readonly')
        category_combo.pack(fill='x', pady=(5, 15))
        
        # Priority
        tk.Label(form_frame, text="Priority:", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w')
        priority_var = tk.StringVar(value='Medium')
        priority_combo = ttk.Combobox(form_frame, textvariable=priority_var,
                                    values=['High', 'Medium', 'Low'], font=('Arial', 12),
                                    state='readonly')
        priority_combo.pack(fill='x', pady=(5, 15))
        
        # Start date
        tk.Label(form_frame, text="Start Date:", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w')
        if DateEntry:
            start_date_entry = DateEntry(form_frame, font=('Arial', 12), width=35)
        else:
            start_date_entry = tk.Entry(form_frame, font=('Arial', 12), width=35)
            start_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        start_date_entry.pack(anchor='w', pady=(5, 15))
        
        # Due date
        tk.Label(form_frame, text="Due Date:", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w')
        if DateEntry:
            due_date_entry = DateEntry(form_frame, font=('Arial', 12), width=35)
        else:
            due_date_entry = tk.Entry(form_frame, font=('Arial', 12), width=35)
            due_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        due_date_entry.pack(anchor='w', pady=(5, 15))
        
        # Progress
        tk.Label(form_frame, text="Progress (%):", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w')
        progress_var = tk.IntVar(value=0)
        progress_scale = tk.Scale(form_frame, from_=0, to=100, orient='horizontal',
                                variable=progress_var, bg='#f0f0f0', length=600)
        progress_scale.pack(fill='x', pady=(5, 15))
        
        # Status
        tk.Label(form_frame, text="Status:", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w')
        status_var = tk.StringVar(value='Not Started')
        status_combo = ttk.Combobox(form_frame, textvariable=status_var,
                                  values=['Not Started', 'In Progress', 'Completed', 'On Hold'],
                                  font=('Arial', 12), state='readonly')
        status_combo.pack(fill='x', pady=(5, 15))
        
        # Comments
        tk.Label(form_frame, text="Comments:", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w')
        comments_text = tk.Text(form_frame, height=8, font=('Arial', 12))  # Increased height
        comments_text.pack(fill='x', pady=(5, 15))
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg='#f0f0f0')
        btn_frame.pack(fill='x', pady=(20, 0))
        
        def save_task():
            name = name_entry.get().strip()
            category_name = category_var.get()
            priority = priority_var.get()
            if DateEntry and hasattr(start_date_entry, 'get_date'):
                start_date = start_date_entry.get_date().strftime('%Y-%m-%d')
                due_date = due_date_entry.get_date().strftime('%Y-%m-%d')
            else:
                start_date = start_date_entry.get()
                due_date = due_date_entry.get()
            progress = progress_var.get()
            status = status_var.get()
            comments = comments_text.get('1.0', 'end-1c').strip()
            
            if not name or not category_name:
                messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            # Find category ID
            category_id = None
            for cat_id, cat in self.categories.items():
                if cat['name'] == category_name:
                    category_id = cat_id
                    break
            
            task = {
                'id': str(len(self.tasks) + 1),
                'name': name,
                'category_id': category_id,
                'priority': priority,
                'start_date': start_date,
                'due_date': due_date,
                'progress': progress,
                'status': status,
                'comments': comments,
                'date_completed': None
            }
            
            self.tasks.append(task)
            self.save_data()
            self.update_all_displays()
            dialog.destroy()
            messagebox.showinfo("Success", "Task added successfully!")
        
        save_btn = tk.Button(btn_frame, text="Save", command=save_task,
                           bg='#4CAF50', fg='white', bd=0, padx=20, pady=8, cursor='hand2')
        save_btn.pack(side='right', padx=(10, 0))
        
        cancel_btn = tk.Button(btn_frame, text="Cancel", command=dialog.destroy,
                             bg='#f44336', fg='white', bd=0, padx=20, pady=8, cursor='hand2')
        cancel_btn.pack(side='right')
    
    def edit_task(self, task):
        """Edit an existing task"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Task")
        dialog.geometry("900x900")  # Increased size significantly
        dialog.configure(bg='#f0f0f0')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog safely
        try:
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (900 // 2)
            y = (dialog.winfo_screenheight() // 2) - (900 // 2)
            dialog.geometry(f"900x900+{x}+{y}")
        except:
            # Fallback centering
            dialog.geometry("900x900+100+100")
        
        # Main container with scrollbar
        main_container = tk.Frame(dialog, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(main_container, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Form
        form_frame = tk.Frame(scrollable_frame, bg='#f0f0f0')
        form_frame.pack(expand=True, padx=20, pady=20)
        
        # Task name
        tk.Label(form_frame, text="Task Name:", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w')
        name_entry = tk.Entry(form_frame, font=('Arial', 12), width=80)  # Increased width significantly
        name_entry.insert(0, task['name'])
        name_entry.pack(fill='x', pady=(5, 15))
        
        # Category selection
        tk.Label(form_frame, text="Category:", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w')
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(form_frame, textvariable=category_var, 
                                    values=[cat['name'] for cat in self.categories.values()],
                                    font=('Arial', 12), state='readonly')
        category_combo.pack(fill='x', pady=(5, 15))
        
        # Set current category
        current_category = self.categories.get(task['category_id'], {})
        category_var.set(current_category.get('name', ''))
        
        # Priority
        tk.Label(form_frame, text="Priority:", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w')
        priority_var = tk.StringVar(value=task['priority'])
        priority_combo = ttk.Combobox(form_frame, textvariable=priority_var,
                                    values=['High', 'Medium', 'Low'], font=('Arial', 12),
                                    state='readonly')
        priority_combo.pack(fill='x', pady=(5, 15))
        
        # Start date
        tk.Label(form_frame, text="Start Date:", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w')
        if DateEntry:
            start_date_entry = DateEntry(form_frame, font=('Arial', 12), width=40)
            start_date_entry.set_date(datetime.strptime(task['start_date'], '%Y-%m-%d'))
        else:
            start_date_entry = tk.Entry(form_frame, font=('Arial', 12), width=40)
            start_date_entry.insert(0, task['start_date'])
        start_date_entry.pack(anchor='w', pady=(5, 15))
        
        # Due date
        tk.Label(form_frame, text="Due Date:", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w')
        if DateEntry:
            due_date_entry = DateEntry(form_frame, font=('Arial', 12), width=40)
            due_date_entry.set_date(datetime.strptime(task['due_date'], '%Y-%m-%d'))
        else:
            due_date_entry = tk.Entry(form_frame, font=('Arial', 12), width=40)
            due_date_entry.insert(0, task['due_date'])
        due_date_entry.pack(anchor='w', pady=(5, 15))
        
        # Progress
        tk.Label(form_frame, text="Progress (%):", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w')
        progress_var = tk.IntVar(value=task['progress'])
        progress_scale = tk.Scale(form_frame, from_=0, to=100, orient='horizontal',
                                variable=progress_var, bg='#f0f0f0', length=700)
        progress_scale.pack(fill='x', pady=(5, 15))
        
        # Status
        tk.Label(form_frame, text="Status:", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w')
        status_var = tk.StringVar(value=task['status'])
        status_combo = ttk.Combobox(form_frame, textvariable=status_var,
                                  values=['Not Started', 'In Progress', 'Completed', 'On Hold'],
                                  font=('Arial', 12), state='readonly')
        status_combo.pack(fill='x', pady=(5, 15))
        
        # Date completed
        tk.Label(form_frame, text="Date Completed (optional):", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w')
        if DateEntry:
            completed_date_entry = DateEntry(form_frame, font=('Arial', 12), width=40)
            if task.get('date_completed'):
                completed_date_entry.set_date(datetime.strptime(task['date_completed'], '%Y-%m-%d'))
        else:
            completed_date_entry = tk.Entry(form_frame, font=('Arial', 12), width=40)
            if task.get('date_completed'):
                completed_date_entry.insert(0, task['date_completed'])
        completed_date_entry.pack(anchor='w', pady=(5, 15))
        
        # Comments
        tk.Label(form_frame, text="Comments:", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w')
        comments_text = tk.Text(form_frame, height=10, font=('Arial', 12))  # Increased height
        comments_text.insert('1.0', task.get('comments', ''))
        comments_text.pack(fill='x', pady=(5, 15))
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg='#f0f0f0')
        btn_frame.pack(fill='x', pady=(20, 0))
        
        def save_changes():
            # Update task
            task['name'] = name_entry.get().strip()
            task['priority'] = priority_var.get()
            if DateEntry and hasattr(start_date_entry, 'get_date'):
                task['start_date'] = start_date_entry.get_date().strftime('%Y-%m-%d')
                task['due_date'] = due_date_entry.get_date().strftime('%Y-%m-%d')
            else:
                task['start_date'] = start_date_entry.get()
                task['due_date'] = due_date_entry.get()
            task['progress'] = progress_var.get()
            task['status'] = status_var.get()
            task['comments'] = comments_text.get('1.0', 'end-1c').strip()
            
            # Update category
            category_name = category_var.get()
            for cat_id, cat in self.categories.items():
                if cat['name'] == category_name:
                    task['category_id'] = cat_id
                    break
            
            # Update completion date
            try:
                if DateEntry and hasattr(completed_date_entry, 'get_date'):
                    task['date_completed'] = completed_date_entry.get_date().strftime('%Y-%m-%d')
                else:
                    task['date_completed'] = completed_date_entry.get() or None
            except:
                task['date_completed'] = None
            
            # Update task in today's list if it exists there
            if hasattr(self, 'today_tasks'):
                for today_task in self.today_tasks:
                    if today_task['id'] == task['id']:
                        today_task.update(task.copy())
                        break
            
            self.save_data()
            self.update_all_displays()
            dialog.destroy()
            messagebox.showinfo("Success", "Task updated successfully!")
        
        save_btn = tk.Button(btn_frame, text="Save Changes", command=save_changes,
                           bg='#4CAF50', fg='white', bd=0, padx=20, pady=8, cursor='hand2')
        save_btn.pack(side='right', padx=(10, 0))
        
        cancel_btn = tk.Button(btn_frame, text="Cancel", command=dialog.destroy,
                             bg='#f44336', fg='white', bd=0, padx=20, pady=8, cursor='hand2')
        cancel_btn.pack(side='right')
    
    def switch_tab(self, tab_name):
        """Switch between tabs"""
        # Store current category state before switching
        if hasattr(self, 'current_category_id'):
            self.remembered_category_id = self.current_category_id
        
        self.current_tab.set(tab_name)
        self.show_tab(tab_name)
    
    def show_tab(self, tab_name):
        """Show the specified tab"""
        # Hide all tabs
        for tab in self.tab_content.values():
            tab.pack_forget()
        
        # Show selected tab
        self.tab_content[tab_name].pack(fill='both', expand=True)
        
        # Update tab-specific content
        if tab_name == 'Main':
            # Check if we should restore a remembered category
            if hasattr(self, 'remembered_category_id'):
                self.expand_category(self.remembered_category_id)
            else:
                self.update_categories_display()
        elif tab_name == 'Tasks for the Day':
            self.update_tasks_for_day()
        elif tab_name == 'Timeline':
            self.update_timeline()
    
    def update_all_displays(self):
        """Update all displays after data changes"""
        # Store current view state
        current_tab = self.current_tab.get()
        current_category = getattr(self, 'current_category_id', None)
        
        # Update all displays
        self.update_categories_display()
        self.update_tasks_for_day()
        self.update_timeline()
        
        # If we were in a category view, restore it
        if current_category:
            self.current_category_id = current_category
            self.expand_category(current_category)
        
        # Restore tab if needed
        if current_tab != self.current_tab.get():
            self.switch_tab(current_tab)
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.dark_mode = not self.dark_mode
        self.apply_theme()
    
    def apply_theme(self):
        """Apply the current theme"""
        if self.dark_mode:
            # Dark theme colors
            bg_color = '#2d2d2d'
            fg_color = '#ffffff'
            header_bg = '#3d3d3d'
            button_bg = '#555555'
            self.theme_btn.configure(text="☀️")
        else:
            # Light theme colors
            bg_color = '#f0f0f0'
            fg_color = '#333333'
            header_bg = '#ffffff'
            button_bg = '#ffffff'
            self.theme_btn.configure(text="🌙")
        
        # Apply colors
        self.root.configure(bg=bg_color)
        self.header.configure(bg=header_bg)
        self.main_frame.configure(bg=bg_color)
        
        for tab in self.tab_content.values():
            tab.configure(bg=bg_color)
    
    def lighten_color(self, color, factor=0.3):
        """Lighten a color by a factor"""
        # Convert hex to RGB
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        
        # Lighten
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        
        # Convert back to hex
        return f'#{r:02x}{g:02x}{b:02x}'

    def edit_category(self, category_id):
        """Edit an existing category"""
        category = self.categories[category_id]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Category")
        dialog.geometry("400x250")
        dialog.configure(bg='#f0f0f0')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog safely
        try:
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
            y = (dialog.winfo_screenheight() // 2) - (250 // 2)
            dialog.geometry(f"400x250+{x}+{y}")
        except:
            # Fallback centering
            dialog.geometry("400x250+100+100")
        
        # Form
        form_frame = tk.Frame(dialog, bg='#f0f0f0')
        form_frame.pack(expand=True, padx=20, pady=20)
        
        # Category name
        tk.Label(form_frame, text="Category Name:", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w')
        name_entry = tk.Entry(form_frame, font=('Arial', 12), width=30)
        name_entry.insert(0, category['name'])
        name_entry.pack(fill='x', pady=(5, 15))
        
        # Color selection
        tk.Label(form_frame, text="Color:", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w')
        color_frame = tk.Frame(form_frame, bg='#f0f0f0')
        color_frame.pack(fill='x', pady=(5, 15))
        
        selected_color = tk.StringVar(value=category['color'])
        color_preview = tk.Frame(color_frame, bg=selected_color.get(), width=30, height=30)
        color_preview.pack(side='left', padx=(0, 10))
        
        def choose_color():
            color = colorchooser.askcolor(title="Choose Category Color")[1]
            if color:
                selected_color.set(color)
                color_preview.configure(bg=color)
        
        color_btn = tk.Button(color_frame, text="Choose Color", command=choose_color,
                            bg='#2196F3', fg='white', bd=0, padx=15, pady=5, cursor='hand2')
        color_btn.pack(side='left')
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg='#f0f0f0')
        btn_frame.pack(fill='x', pady=(20, 0))
        
        def save_category():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter a category name")
                return
            
            self.categories[category_id] = {
                'name': name,
                'color': selected_color.get()
            }
            
            self.save_data()
            self.update_categories_display()
            dialog.destroy()
            messagebox.showinfo("Success", "Category updated successfully!")
        
        save_btn = tk.Button(btn_frame, text="Save", command=save_category,
                           bg='#4CAF50', fg='white', bd=0, padx=20, pady=8, cursor='hand2')
        save_btn.pack(side='right', padx=(10, 0))
        
        cancel_btn = tk.Button(btn_frame, text="Cancel", command=dialog.destroy,
                             bg='#f44336', fg='white', bd=0, padx=20, pady=8, cursor='hand2')
        cancel_btn.pack(side='right')

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 