# Android Manifest Analyzer
A Python tool to analyze Android APK manifest files (AndroidManifest.xml) and display:

- Permissions (system & custom)

- Components (activity, service, receiver, provider)

- Meta-data for components

- Queries (<queries>: intents, packages, providers)

Everything is displayed in a colorful console using the Rich ##library
.
## Features
- Show all permissions, marking dangerous and signature permissions with symbols

- List all components (activities, services, receivers, providers)

- Display meta-data for each component

- Parse and show queries: intents, packages, providers

- Interactive menu to explore each component individually

- Easy-to-read emoji/symbol-based visualization for quick inspection

## Installation
1. Clone this repository:
   ```
   git clone https://github.com/vicky4421/androfest.git
   cd androfest
2. Install dependencies:
   ```
   pip install -r requirements.txt
## Usage
```
python androfest.py [path to file]
```

## Example Output
```
🔹 Permissions
💀 android.permission.READ_CONTACTS
🔒 com.example.CUSTOM_PERMISSION [signature]
🟢 android.permission.INTERNET

📄 com.example.MainActivity
    ♦ com.example.API_KEY: 12345
📄 com.example.SecondActivity

🔸 Queries
🔗 Provider -> authorities=com.facebook.katana.provider.PlatformProvider
➡️ Intent -> action=android.intent.action.VIEW, scheme=http
📦 Package -> com.instagram.android
