# ArcGIS Experience Builder Menu Generator

🚀 **Reusable tool for creating beautiful, fast-loading menus for ArcGIS Experience Builder applications**

## 🎯 What This Solves

ArcGIS Experience Builder has limited CSS/HTML capabilities. This tool creates external menus that:
- ✅ Work around ArcGIS CSS limitations using external hosting
- ✅ Provide fast search, dark mode, and alphabetical sorting
- ✅ Auto-generate links using ArcGIS tokens
- ✅ Deploy easily to GitHub + PythonAnywhere
- ✅ Reuse across multiple Experience Builder projects

## 🏗️ Architecture

```
Global Config (~/.config/arcgis/.env)
    ↓
Menu Generator (Python) → menu.json
    ↓
Beautiful HTML Interface → GitHub → PythonAnywhere
    ↓
ArcGIS Experience Builder (Embed URL widget)
```

## 🚀 Quick Start

### 1. Initial Setup (One Time)
Your global config is already set up at `~/.config/arcgis/.env` with your ArcGIS credentials.

### 2. For Current Project (National Operations Summary)
```bash
# Generate menu with auto-generated links
python menu_generator.py

# Deploy to GitHub + PythonAnywhere
python deploy.py "Updated menu configuration"
```

### 3. For New Projects
```bash
# Create new project
python create_project.py

# Follow interactive prompts:
# - Project name: "Regional_Operations" 
# - Experience ID: "your-experience-builder-id"
# - Menu title: "Regional Operations Dashboard"
```

## 📁 File Structure

### Core Files
- `config.py` - Global configuration loader
- `menu_generator.py` - Automatic menu generation with ArcGIS integration
- `deploy.py` - GitHub + PythonAnywhere deployment
- `create_project.py` - New project generator

### Project Files  
- `index.html` - Beautiful menu interface (matches your screenshot)
- `menu.json` - Menu configuration data
- `editor.html` - Admin menu editor (optional)

### Global Config
- `~/.config/arcgis/.env` - Global ArcGIS credentials and API keys

## 🔧 Key Features

### ✅ Already Implemented
- **Fast Search**: Real-time filtering across all menu items
- **Dark Mode Toggle**: Light/dark theme switching with persistence
- **Alphabetical Sort**: Toggle between categorical and A-Z layouts
- **Responsive Design**: Works on all screen sizes
- **Auto-Link Generation**: Uses ArcGIS tokens to build URLs automatically
- **GitHub Integration**: One-command git deployment
- **PythonAnywhere API**: Live menu updates
- **Menu Validation**: Ensures JSON structure is correct
- **Backup System**: Auto-backup before deployments
- **Reusable Templates**: Generate new projects easily

### 🎨 Design Matches Your Screenshot
- Exact color scheme and layout from your perfect menu
- Fast performance with CSS Grid and optimized JavaScript
- Smooth animations and hover effects
- Professional Red Cross styling

## 🔄 Typical Workflow

1. **Edit menu structure**:
   ```python
   # In menu_generator.py, modify the generate_national_operations_menu() function
   # Or for new projects, edit project_config.py
   ```

2. **Generate updated menu**:
   ```bash
   python menu_generator.py
   ```

3. **Deploy everywhere**:
   ```bash
   python deploy.py "Added new DR response pages"
   ```

4. **Use in Experience Builder**:
   - Add Embed widget to your Experience Builder page
   - Set URL to: `https://menu-jfranzen.pythonanywhere.com`
   - Menu loads instantly with all features

## 🔗 ArcGIS Integration

### Automatic Link Building
```python
# Instead of manual URLs:
"href": "https://experience.arcgis.com/experience/ce0b7dc7574c49a8a82f36443fee494f/page/National"

# Use automatic generation:
create_menu_item("National", "National", "national ops")
# → Automatically builds URL using your credentials
```

### Multi-Experience Support
```python
# For different Experience Builders:
generator = MenuGenerator(experience_id="different-experience-id")
```

## 📊 Example: Adding New Menu Items

```python
# In menu_generator.py, add to any category:
categories.append(self.create_category(
    "New Category", "btn-purple", [
        {"label": "New Page", "page_id": "New-Page-ID", "search_terms": "additional search terms"},
        {"label": "Another Page", "page_id": "Another-Page-ID"}
    ]
))
```

## 🌐 Deployment Targets

- **GitHub**: Source code repository with version control
- **PythonAnywhere**: Live hosting at `menu-jfranzen.pythonanywhere.com`
- **ArcGIS Experience Builder**: Embedded via URL widget

## 🔐 Security

- Credentials stored in global config outside repositories
- API passwords for PythonAnywhere deployment
- No secrets committed to git (`.gitignore` configured)

## 📋 Next Steps

1. **Test the current menu**: Open your Experience Builder and verify the menu loads correctly
2. **Customize as needed**: Edit `menu_generator.py` to add/remove menu items
3. **Create new projects**: Use `python create_project.py` for other Experience Builders
4. **Share the tool**: Copy core files to other repositories for reuse

## 🆘 Troubleshooting

- **Menu not loading**: Check PythonAnywhere URL and API connectivity
- **Links not working**: Verify Experience Builder IDs and page names
- **Deployment fails**: Check global config at `~/.config/arcgis/.env`
- **Styling issues**: Ensure `index.html` matches your requirements

---

**🎉 You now have a powerful, reusable ArcGIS Experience Builder menu system that can be used across all your future projects!**