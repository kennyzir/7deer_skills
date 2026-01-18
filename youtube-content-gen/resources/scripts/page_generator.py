import os
import jinja2

def generate_page_files(data: dict, template_dir: str, output_base_dir: str) -> dict:
    """
    Renders the page.tsx and page.module.css files from templates.
    """
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    
    # 1. Prepare Output Directory
    slug = data.get('slug', 'temp-guide')
    output_dir = os.path.join(output_base_dir, 'app', 'guides', slug)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 2. Render Page.tsx
    template_tsx = env.get_template('page.tsx.j2')
    content_tsx = template_tsx.render(data)
    path_tsx = os.path.join(output_dir, 'page.tsx')
    
    with open(path_tsx, 'w', encoding='utf-8') as f:
        f.write(content_tsx)

    # 3. Render CSS
    template_css = env.get_template('page.module.css.j2')
    content_css = template_css.render(data)
    path_css = os.path.join(output_dir, 'page.module.css')
    
    with open(path_css, 'w', encoding='utf-8') as f:
        f.write(content_css)

    return {
        "page_path": path_tsx,
        "css_path": path_css,
        "slug": slug
    }
