#!/usr/bin/env python3
"""
Simple Vibegame Site Updater
Run this script to update your website content easily
"""

import json
import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from PIL import Image, ImageTk
import subprocess

class VibegameUpdater:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.projects = [
            {
                "title": "Bratwurst Bomber",
                "description": "Schieß Würstchen auf Viren und Pfizer – rette die Galaxie vor der Corona-Psyop!",
                "image": "images/bratwurst.jpg",
                "url": "https://bratwurst.snicklink.de",
                "color": "#D946EF",
                "featured": True,
                "new": True,
                "order": 1
            },
            {
                "title": "Kanzlersimulator",
                "description": "Wähl dich 2025 durch Chaos, PR-Pannen und Perks – wer wird Kanzler?",
                "image": "images/kanzler.jpg",
                "url": "https://kanzler.snicklink.de",
                "color": "#3B82F6",
                "featured": False,
                "new": False,
                "order": 2
            },
            {
                "title": "Chemtrail Fighter",
                "description": "Flieg gegen Reptiloid-Jets und Schwab – säuber den Himmel von Chemtrails!",
                "image": "images/chems.jpg",
                "url": "https://chemtrailfighter.com",
                "color": "#F97316",
                "featured": False,
                "new": False,
                "order": 3
            },
            {
                "title": "Call of Blackrock: Merz Mayhem",
                "description": "Verschwende Kredite mit Merz – ruiniere die Wirtschaft, so schnell du kannst!",
                "image": "images/blackrock.jpg",
                "url": "https://fritz.snicklink.de",
                "color": "#EF4444",
                "featured": False,
                "new": False,
                "order": 4
            }
        ]
        self.setup_gui()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("🎮 Vibegame Site Updater")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a2e')

        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#1a1a2e', foreground='white')
        style.configure('TButton', background='#4ecdc4')
        style.configure('TEntry', background='#16213e', foreground='white')
        style.configure('TText', background='#16213e', foreground='white')

        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = ttk.Label(main_frame, text="🎮 Vibegame Site Updater", 
                               font=("Arial", 20, "bold"))
        title_label.pack(pady=(0, 20))

        # Instructions
        instructions = ttk.Label(main_frame, 
                                text="Update your projects below, then click 'Update Website & Deploy'",
                                font=("Arial", 12))
        instructions.pack(pady=(0, 20))

        # Projects frame with scrollbar
        projects_frame = ttk.Frame(main_frame)
        projects_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(projects_frame, bg='#1a1a2e')
        scrollbar = ttk.Scrollbar(projects_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.projects_container = scrollable_frame
        self.render_projects()

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(20, 0))

        ttk.Button(buttons_frame, text="➕ Add New Project", 
                  command=self.add_project).pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(buttons_frame, text="🚀 Update Website & Deploy", 
                  command=self.update_and_deploy).pack(side=tk.RIGHT)

    def render_projects(self):
        # Clear existing widgets
        for widget in self.projects_container.winfo_children():
            widget.destroy()

        for i, project in enumerate(self.projects):
            self.create_project_widget(i, project)

    def create_project_widget(self, index, project):
        # Project frame
        project_frame = ttk.LabelFrame(self.projects_container, text=f"Project {index + 1}", 
                                      padding=15)
        project_frame.pack(fill=tk.X, pady=(0, 15))

        # Image section
        image_frame = ttk.Frame(project_frame)
        image_frame.pack(fill=tk.X, pady=(0, 10))

        # Try to load and display image
        try:
            img_path = self.script_dir / project['image']
            if img_path.exists():
                img = Image.open(img_path)
                img.thumbnail((150, 150))
                photo = ImageTk.PhotoImage(img)
                img_label = ttk.Label(image_frame, image=photo)
                img_label.image = photo  # Keep a reference
                img_label.pack(side=tk.LEFT, padx=(0, 10))
        except Exception:
            ttk.Label(image_frame, text="No Image").pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(image_frame, text="Change Image", 
                  command=lambda: self.change_image(index)).pack(side=tk.LEFT)

        # Form fields
        fields_frame = ttk.Frame(project_frame)
        fields_frame.pack(fill=tk.X)

        # Title
        ttk.Label(fields_frame, text="Title:").grid(row=0, column=0, sticky=tk.W, pady=5)
        title_entry = ttk.Entry(fields_frame, width=50)
        title_entry.insert(0, project['title'])
        title_entry.grid(row=0, column=1, sticky=tk.EW, padx=(10, 0), pady=5)
        title_entry.bind('<KeyRelease>', lambda e: self.update_project(index, 'title', title_entry.get()))

        # Description
        ttk.Label(fields_frame, text="Description:").grid(row=1, column=0, sticky=tk.NW, pady=5)
        desc_text = tk.Text(fields_frame, height=3, width=50)
        desc_text.insert('1.0', project['description'])
        desc_text.grid(row=1, column=1, sticky=tk.EW, padx=(10, 0), pady=5)
        desc_text.bind('<KeyRelease>', lambda e: self.update_project(index, 'description', desc_text.get('1.0', tk.END).strip()))

        # URL
        ttk.Label(fields_frame, text="URL:").grid(row=2, column=0, sticky=tk.W, pady=5)
        url_entry = ttk.Entry(fields_frame, width=50)
        url_entry.insert(0, project['url'])
        url_entry.grid(row=2, column=1, sticky=tk.EW, padx=(10, 0), pady=5)
        url_entry.bind('<KeyRelease>', lambda e: self.update_project(index, 'url', url_entry.get()))

        # Color
        color_frame = ttk.Frame(fields_frame)
        color_frame.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        ttk.Label(fields_frame, text="Color:").grid(row=3, column=0, sticky=tk.W, pady=5)
        color_label = tk.Label(color_frame, text="  ", bg=project['color'], width=4)
        color_label.pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(color_frame, text="Change Color", 
                  command=lambda: self.change_color(index, color_label)).pack(side=tk.LEFT)

        # Checkboxes
        checkbox_frame = ttk.Frame(fields_frame)
        checkbox_frame.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)

        featured_var = tk.BooleanVar(value=project['featured'])
        ttk.Checkbutton(checkbox_frame, text="Featured", variable=featured_var,
                       command=lambda: self.update_project(index, 'featured', featured_var.get())).pack(side=tk.LEFT, padx=(0, 20))

        new_var = tk.BooleanVar(value=project['new'])
        ttk.Checkbutton(checkbox_frame, text="New", variable=new_var,
                       command=lambda: self.update_project(index, 'new', new_var.get())).pack(side=tk.LEFT)

        # Delete button
        ttk.Button(fields_frame, text="🗑️ Delete", 
                  command=lambda: self.delete_project(index)).grid(row=5, column=1, sticky=tk.W, padx=(10, 0), pady=10)

        fields_frame.columnconfigure(1, weight=1)

    def update_project(self, index, field, value):
        if index < len(self.projects):
            self.projects[index][field] = value

    def change_image(self, index):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.webp")]
        )
        if file_path:
            # Copy image to images folder
            images_dir = self.script_dir / "images"
            images_dir.mkdir(exist_ok=True)
            
            file_name = Path(file_path).name
            destination = images_dir / file_name
            shutil.copy2(file_path, destination)
            
            self.projects[index]['image'] = f"images/{file_name}"
            self.render_projects()
            messagebox.showinfo("Success", f"Image updated: {file_name}")

    def change_color(self, index, color_label):
        color = colorchooser.askcolor(title="Choose Color")[1]
        if color:
            self.projects[index]['color'] = color
            color_label.configure(bg=color)

    def add_project(self):
        new_project = {
            "title": "New Project",
            "description": "Project description",
            "image": "images/placeholder.jpg",
            "url": "",
            "color": "#D946EF",
            "featured": False,
            "new": False,
            "order": len(self.projects) + 1
        }
        self.projects.append(new_project)
        self.render_projects()

    def delete_project(self, index):
        if messagebox.askyesno("Confirm Delete", f"Delete '{self.projects[index]['title']}'?"):
            self.projects.pop(index)
            self.render_projects()

    def generate_index_html(self):
        projects_js = json.dumps(self.projects, indent=16)
        
        return f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Snicklink Vibe Schwurbling</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
</head>
<body>
    <header>
        <div class="logo">
            <img src="images/snick_vibe_logo.png" alt="Snicklink Vibe Logo">
        </div>
        <nav>
            <a href="#spiele">Spiele</a>
            <a href="#vibecoding">Vibecoding</a>
            <a href="#magazin">Magazin</a>
        </nav>
    </header>

    <section class="hero">
        <div class="hero-logo">
            <img src="images/snick_vibe_logo.png" alt="Snicklink Vibe Logo">
        </div>
        <h1>Vibecoding Walhalla</h1>
        <p>Meine aktuellsten Schwurbel-Games</p>
        <div class="featured-game" id="featuredGame">
            <!-- Featured game will be inserted here -->
        </div>
    </section>

    <section id="spiele" class="game-grid" id="gamesGrid">
        <!-- Games will be inserted here -->
    </section>

    <section id="vibecoding" class="vibecoding">
        <h2 style="color: #55FF99;">Vibecoding: Kunst trifft Code</h2>
        <p>Vibecoding ist mein Herzschlag – ein Mix aus Technik, Satire und purer Kreativität. Als Künstler und Schwurbler erschaffe ich Spiele, die Spaß machen und die Welt ein bisschen aufmischen. Neugierig?</p>
        <a href="vibecoding.html" class="vibe-btn">Die ganze Story</a>
    </section>

    <aside id="magazin" class="ad-space">
        <h3>Die neue Willy</h3>
        <p class="ad-subtitle">Meta-Satire trifft Hyperwahnsinn!</p>
        <a href="https://snicklink.de" class="ad-link" target="_blank" rel="noopener noreferrer">
            <img src="images/willy7jpg.jpg" alt="Snicklink Vibe Magazin Link" class="ad-thumbnail-img">
        </a>
    </aside>

    <footer>
        <p>© 2025 Snicklink Vibe Schwurbling | <a href="#">Kontakt</a> | <a href="#">Datenschutz</a></p>
    </footer>

    <script>
        const projects = {projects_js};

        function renderProjects() {{
            projects.sort((a, b) => a.order - b.order);
            
            const featured = projects.find(p => p.featured) || projects[0];
            
            document.getElementById('featuredGame').innerHTML = `
                <img src="${{featured.image}}" alt="${{featured.title}}" class="thumbnail">
                <h2 style="color: ${{featured.color}};">${{featured.title}} ${{featured.new ? '<span class="new-tag">Neu</span>' : ''}}</h2>
                <p>${{featured.description}}</p>
                <a href="${{featured.url}}" class="play-btn">Jetzt spielen</a>
            `;

            document.getElementById('gamesGrid').innerHTML = projects.map(project => `
                <div class="game">
                    <img src="${{project.image}}" alt="${{project.title}}" class="thumbnail">
                    <h3 style="color: ${{project.color}};">${{project.title}} ${{project.new ? '<span class="new-tag">Neu</span>' : ''}}</h3>
                    <p>${{project.description}}</p>
                    <a href="${{project.url}}" class="play-btn">Jetzt spielen</a>
                </div>
            `).join('');
        }}

        renderProjects();
    </script>
</body>
</html>'''

    def update_and_deploy(self):
        try:
            # Generate new index.html
            html_content = self.generate_index_html()
            
            # Write to index.html
            index_path = self.script_dir / "index.html"
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Git commands
            os.chdir(self.script_dir)
            
            # Add all changes
            subprocess.run(['git', 'add', '.'], check=True)
            
            # Commit
            subprocess.run(['git', 'commit', '-m', 'Update website content via updater tool'], check=True)
            
            # Push
            subprocess.run(['git', 'push'], check=True)
            
            messagebox.showinfo("Success!", "✅ Website updated and deployed!\n\nYour changes are now live!")
            
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Git Error", f"Git command failed: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update website: {e}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = VibegameUpdater()
    app.run()