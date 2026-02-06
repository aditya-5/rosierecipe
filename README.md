# Recipe Collection Website - Deployment Guide

## 📦 What You Have

A lightweight, searchable recipe website with:
- ✅ Searchable recipe index
- ✅ PDF viewer built-in
- ✅ Copy text from PDF button
- ✅ Links to original Rosie's website
- ✅ Ready for Instagram links (future)
- ✅ 100% free hosting

## 🚀 Quick Deployment Steps

### Step 1: Prepare Your Files

1. **Generate recipes.json** from your PDFs:
   ```bash
   python generate_recipe_json.py
   ```

2. **Copy all your PDFs** to the website folder:
   ```bash
   # Copy all PDFs from my_recipes to recipe-website/public/recipes/
   cp my_recipes/*.pdf recipe-website/public/recipes/
   ```

3. Your folder structure should look like:
   ```
   recipe-website/
   ├── index.html
   ├── recipes.json
   ├── package.json
   └── public/
       └── recipes/
           ├── 001_Banoffee_Cupcakes.pdf
           ├── 002_Red_Velvet_Mocha_Cake.pdf
           └── ... (all your PDFs)
   ```

### Step 2: Deploy to Vercel (Recommended - Easiest)

1. **Install Vercel CLI** (optional):
   ```bash
   npm install -g vercel
   ```

2. **Deploy via Website** (easier):
   - Go to https://vercel.com
   - Sign up with GitHub
   - Click "New Project"
   - Drag and drop the `recipe-website` folder
   - Click "Deploy"
   - Done! ✅

3. **Or deploy via CLI**:
   ```bash
   cd recipe-website
   vercel
   ```

### Step 3: Alternative - Deploy to Netlify

1. **Via Website**:
   - Go to https://netlify.com
   - Sign up
   - Drag and drop `recipe-website` folder
   - Done! ✅

2. **Via CLI**:
   ```bash
   npm install -g netlify-cli
   cd recipe-website
   netlify deploy --prod
   ```

## 📊 Where to Store PDFs

**Option 1: With Your Website (Simplest)**
- Store PDFs in `recipe-website/public/recipes/`
- Deploy everything together
- ✅ Pros: Simple, works offline, fast
- ⚠️ Cons: Larger deployment size (~100-200MB for 120 recipes)

**Option 2: Separate Cloud Storage (Future)**
- Upload PDFs to Cloudflare R2 / Backblaze B2 (free tier)
- Update `recipes.json` with cloud URLs
- ✅ Pros: Faster deployments, unlimited storage
- ⚠️ Cons: More setup, requires cloud account

**Recommendation for Personal Use:** Use Option 1 (include PDFs with website). Vercel supports up to 100MB per file and Netlify up to 200MB total is fine for ~120 recipes.

## 🔗 Adding Instagram Links (Future)

Edit `recipes.json` and add Instagram URLs:
```json
{
  "number": 1,
  "title": "Banoffee Cupcakes",
  "pdf": "recipes/001_Banoffee_Cupcakes.pdf",
  "url": "https://www.recipebyrosie.com/post/banoffee-cupcakes",
  "instagram": "https://www.instagram.com/p/ABC123/"
}
```

The website will automatically show Instagram links when they're present.

## 🎨 Customization

Edit `index.html` to customize:
- Change colors (search for `#d4497d` - Rosie's pink color)
- Modify title
- Add your name
- Change layout

## 📱 Features

- **Search**: Type in the search box to filter recipes instantly
- **View PDF**: Click any recipe card to open PDF viewer
- **Copy Text**: Click "Copy Text" button to extract all text from PDF
- **Original Link**: Click "Original Recipe" to visit Rosie's website
- **Mobile Friendly**: Works on phones and tablets
- **Fast**: Lightweight, no frameworks, just vanilla JavaScript

## 🐛 Troubleshooting

**PDFs not loading?**
- Make sure PDFs are in `public/recipes/` folder
- Check `recipes.json` has correct paths

**Search not working?**
- Check browser console for errors
- Make sure `recipes.json` loaded correctly

**Deploy failed?**
- Check folder size isn't too large
- Make sure all files are included

## 💾 Backup

Keep backups of:
1. All original PDFs in `my_recipes/` folder
2. `recipes.json` file
3. `recipe_progress.txt` (tracks downloaded recipes)

## 📝 Notes

- This is a static website - no server needed
- All processing happens in the browser
- PDFs are loaded directly, no conversion needed
- Free forever on Vercel/Netlify free tier
- Can handle 1000+ recipes easily
