# How to Update GitHub After Making Changes

## Every time you change code and want to update GitHub:

1. **Save your files in VS Code**

2. **Open terminal in project folder:**
   ```powershell
   cd C:\Users\Deepika\Downloads\ai-nutrition-advisor3-main\ai-nutrition-advisor3-main
   ```

3. **Check what changed:**
   ```powershell
   git status
   ```

4. **Add all changes:**
   ```powershell
   git add .
   ```

5. **Commit with a message:**
   ```powershell
   git commit -m "describe what you changed"
   ```
   Examples:
   - `git commit -m "Fixed chatbot error"`
   - `git commit -m "Added new recipe feature"`
   - `git commit -m "Updated README"`

6. **Push to GitHub:**
   ```powershell
   git push
   ```

## That's it! Your changes are now live on GitHub! 🚀

---

## For your teammates to get your updates:

```bash
git pull origin main
```

---

## API Key Setup (For Each Teammate)

Each person should:
1. Go to https://aistudio.google.com/app/apikey
2. Create their OWN free API key
3. Use it when running:
   ```powershell
   $env:GEMINI_API_KEY="their_own_key"; python flask_app.py
   ```

**Don't share API keys!** Everyone gets unlimited free keys! 🔑
