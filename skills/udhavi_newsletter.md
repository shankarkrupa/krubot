# add a new newsletter for the udhavi website
- newsletters are pdf files
- there will be only one newsletter pdf present for each month at max
- each pdf file belongs to an issue ; issue 1, issue 2, ...., issue x
- 

## 📝 Newsletter Page Structure Template (Issue 8 structure)

Each issue page (`/newsletter/issueX/`) contains:
- Header with navigation
- Main content area
- **Title**: "Issue X" centered and bold
- **PDF download button** linking to `/images/newsletter/jannews.pdf` or similar
- **PDF viewer using Mozilla PDF.js** library

---

## 🚀 Actions Needed for Issue 9  (August 2029)

### Step 1: Create Individual Issue Page

Create this HTML file at `https://www.udhavi.net/newsletter/issue9/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UDHAVI</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="//unpkg.com/alpinejs" defer></script>
    <!-- PDF viewer dependencies -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.4.168/pdf_viewer.min.css">
</head>
<body>
    <!-- Header with logo and navigation (same as issue 8) -->

    <!-- Main content area -->
<div class="bg-white px-6 py-32 lg:px-8">
  <div class="mx-auto max-w-5xl text-base leading-7 text-gray-700">
    <h1 class="mt-2 text-3xl font-bold tracking-tight text-center text-gray-900 sm:text-4xl">Issue 9</h1>

    <!-- PDF Section -->
    <div class="mt-6">
        <a href="/images/newsletter/augnews.pdf" class="text-green-500 font-semibold" target="_blank">
            Click to download pdf
        </a>

        <!-- PDF viewer controls will go here -->
</div>

    <!-- Footer with navigation (same as other pages) -->
</div>

<!-- PDF.js scripts would be loaded from CDN -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.6.347/pdf.worker.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.6.347/pdf.min.js"></script>
```

---

### Step 2: Add to Homepage Newsletter List

The main newsletter page needs to be updated to include Issue 9's card entry BEFORE Issue 8 in the grid.

**Location**: Update the `article` cards on `/newsletter/` to include Issue 9:
```html
<article class="flex flex-col items-start justify-between">
    <a href="/newsletter/issue9/">
        <img src="/images/newsletter/9.jpeg" alt="" ...>
    </div>
    <h3><a href="/newsletter/issue9/">Issue 9</a></h3>
    <p>August 2026</p>
</article>
```

---

## 📁 File Structure Required

| File | Location | Purpose |
|------|----------|---------|
| `index.html` | `/newsletter/issue9/index.html` | Main issue page content |
| `9.jpeg` | `/images/newsletter/9.jpeg` | Thumbnail for homepage |
| `augnews.pdf` | `/images/newsletter/augnews.pdf` | Full PDF newsletter |

