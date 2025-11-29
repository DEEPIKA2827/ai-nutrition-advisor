# 🚨 SECURITY ALERT - API KEY EXPOSED FIX

## ⚠️ YOUR API KEY WAS PUBLICLY EXPOSED ON GITHUB!

GitHub detected your Gemini API key in the repository. **Anyone can use it now!**

---

## ✅ WHAT TO DO RIGHT NOW (Step-by-Step):

### Step 1: Revoke the Old Key (MOST IMPORTANT!)
1. Go to: **https://aistudio.google.com/app/apikey**
2. Find your exposed key
3. Click **DELETE** or **REVOKE** button
4. Click **"Create API Key"** to generate a NEW one
5. Copy the new key (looks like: `AIzaSy...`)

### Step 2: Remove Key from Git History
```powershell
cd C:\Users\Deepika\Downloads\ai-nutrition-advisor3-main\ai-nutrition-advisor3-main

# Commit the fixed files (key removed)
git add RUN_COMMANDS.md .gitignore
git commit -m "Security fix: Remove exposed API key"
git push
```

### Step 3: Use Environment Variables (Secure Method)
Create a file named `.env` in your project folder:
```
GEMINI_API_KEY=your_new_api_key_here
```

**NEVER commit the `.env` file to GitHub!** (Already added to .gitignore)

### Step 4: Run App Securely
```powershell
# Set your NEW API key (replace with actual key)
$env:GEMINI_API_KEY="YOUR_NEW_KEY_HERE"

# Run the app
python flask_app.py
```

---

## 📋 SECURITY CHECKLIST:

- [ ] Revoked old API key from Google AI Studio
- [ ] Generated NEW API key
- [ ] Removed key from RUN_COMMANDS.md
- [ ] Created .gitignore file
- [ ] Committed and pushed changes
- [ ] Tested app with NEW key
- [ ] Never shared API key in files again

---

## ⚡ QUICK FIX COMMAND:

After getting your NEW API key from https://aistudio.google.com/app/apikey:

```powershell
cd C:\Users\Deepika\Downloads\ai-nutrition-advisor3-main\ai-nutrition-advisor3-main
$env:GEMINI_API_KEY="paste_your_NEW_key_here"
python flask_app.py
```

---

## 🛡️ PREVENTION (For Future):

**NEVER put API keys in:**
- ❌ .md files
- ❌ .py files (hardcoded)
- ❌ git commits
- ❌ screenshots

**ALWAYS use:**
- ✅ Environment variables (`$env:GEMINI_API_KEY`)
- ✅ .env file (added to .gitignore)
- ✅ Secure credential managers

---

## 📞 Need Help?

If someone already used your old key:
1. Check Google AI Studio usage dashboard
2. Generate a new key immediately
3. Update your local environment

**Your data is safe - just the API key was exposed!**
