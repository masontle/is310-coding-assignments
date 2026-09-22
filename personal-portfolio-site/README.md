# Personal portfolio site

This is a plain HTML/CSS/JavaScript site designed for GitHub Pages.

## Personalize it

Open `index.html` and replace:

- `Your Name` with your name
- `yourusername` with your GitHub username
- `hello@example.com` with your email address
- the introduction, project descriptions, and links with your own details

The visual styling lives in `styles.css`. The small mobile navigation and footer year are handled by `script.js`.

## Publish on GitHub Pages

1. Create a public repository named exactly `yourusername.github.io`.
2. In this folder, run:

   ```powershell
   git init
   git add .
   git commit -m "Initial commit: add personal portfolio site"
   git branch -M main
   git remote add origin https://github.com/yourusername/yourusername.github.io.git
   git push -u origin main
   ```

3. Open **Settings → Pages** in the repository and choose **Deploy from a branch**, `main`, and `/ (root)` if GitHub Pages is not already enabled.
4. Visit `https://yourusername.github.io` after GitHub finishes deploying.
