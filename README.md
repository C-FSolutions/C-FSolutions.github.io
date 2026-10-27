# C-FSolutions.github.io

The C&F Solutions LLC website: home page, Privacy Policy and Terms of Use for the site. Published by GitHub Pages at https://c-fsolutions.github.io/. Each product's own policies live on its site (Pyllar: https://pyllarhq.com/privacy, https://pyllarhq.com/terms).

## Editing

Edit `content/` (`site.json` for the name, tagline, about text, contact address, effective date and products; `privacy.html` and `terms.html` for the policy bodies, which take `{email}`, `{legal_name}`, `{pyllar_privacy}` and `{pyllar_terms}`), then:

```bash
python3 -I build.py
```

and commit the rebuilt pages. Change `effective` in `site.json` whenever a policy changes.

The contact address never appears in the built pages: each email link carries it encoded, and an inline script rebuilds the `mailto:` link in the browser. The build fails if the plain address is left in any page.

## Custom domain

Add a `CNAME` file holding the domain, point the domain's DNS at GitHub Pages, set it under Settings → Pages, and update `SITE_URL` in `build.py`.
