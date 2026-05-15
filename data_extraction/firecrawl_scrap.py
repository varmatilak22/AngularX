import os
import json
from urllib.parse import urlparse
from firecrawl import FirecrawlApp
from dotenv import load_dotenv

load_dotenv()

# Initialize Firecrawl App
fire_crawl_api_key=os.getenv("FIRE_CRAWL_API_KEY")
app = FirecrawlApp(api_key=fire_crawl_api_key)

# List of Angular documentation URLs to scrape
urls=[
    #"https://angular.dev/roadmap",
     # "https://angular.dev/api",
     # "https://angular.dev/cli",
     # "https://angular.dev/errors",
     # "https://angular.dev/errors/NG0100",
     # "https://angular.dev/errors/NG01101",
     # "https://angular.dev/errors/NG01203",
     # "https://angular.dev/errors/NG0200",
     # "https://angular.dev/errors/NG0201",
     # "https://angular.dev/errors/NG0203",
     # "https://angular.dev/errors/NG0209",
     # "https://angular.dev/errors/NG02200",
     # "https://angular.dev/errors/NG02800",
     # "https://angular.dev/errors/NG0300",
     # "https://angular.dev/errors/NG0300",
     # "https://angular.dev/errors/NG0302",
      #"https://angular.dev/errors/NG0301"
      #"https://angular.dev/errors/NG0403"
      #"https://angular.dev/errors/NG0500",
      #"https://angular.dev/errors/NG05000",
      #"https://angular.dev/errors/NG0501",
      #"https://angular.dev/errors/NG0502",
      #"https://angular.dev/errors/NG0502",
      #"https://angular.dev/errors/NG0504",
      #"https://angular.dev/errors/NG0505",
      #"https://angular.dev/errors/NG0506",
      #"https://angular.dev/errors/NG0507",
      #"https://angular.dev/errors/NG05104",
      #"https://angular.dev/errors/NG0602",
      #"https://angular.dev/errors/NG0750",
      #"https://angular.dev/errors/NG0751",
      #"https://angular.dev/errors/NG0910",
      #"https://angular.dev/errors/NG0912",
      #"https://angular.dev/errors/NG0913",
      #"https://angular.dev/errors/NG0950",
      #"https://angular.dev/errors/NG0951",
      #"https://angular.dev/errors/NG0955",
      #"https://angular.dev/errors/NG0956",
      #"https://angular.dev/errors/NG1001",
      #"https://angular.dev/errors/NG1001",
      #"https://angular.dev/errors/NG2009",
      #"https://angular.dev/errors/NG2009",
      #"https://angular.dev/errors/NG3003",
      #"https://angular.dev/errors/NG6100",
      #"https://angular.dev/errors/NG8001",
      #"https://angular.dev/errors/NG8002",
      #"https://angular.dev/errors/NG8003",
      
      #"https://angular.dev/extended-diagnostics",
      #"https://angular.dev/extended-diagnostics/NG8101",
      #"https://angular.dev/extended-diagnostics/NG8102",
      #"https://angular.dev/extended-diagnostics/NG8103",
      #"https://angular.dev/extended-diagnostics/NG8104",
      #"https://angular.dev/extended-diagnostics/NG8105",
      #"https://angular.dev/extended-diagnostics/NG8106",
      #"https://angular.dev/extended-diagnostics/NG8107",
      #"https://angular.dev/extended-diagnostics/NG8108",
      #"https://angular.dev/extended-diagnostics/NG8109",
      #"https://angular.dev/extended-diagnostics/NG8111",
      #"https://angular.dev/extended-diagnostics/NG8113",
      #"https://angular.dev/reference/releases",
      #"https://angular.dev/reference/versions",
      #"https://angular.dev/reference/configs/file-structure",
      #"https://angular.dev/reference/configs/workspace-config",
      #"https://angular.dev/reference/configs/npm-packages",
      #"https://angular.dev/reference/configs/angular-compiler-options",
      
      #"https://angular.dev/reference/migrations",
      #"https://angular.dev/reference/migrations/standalone",
      #"https://angular.dev/reference/migrations/control-flow",
      #"https://angular.dev/reference/migrations/inject-function",
      #"https://angular.dev/reference/migrations/route-lazy-loading",
      #"https://angular.dev/reference/migrations/signal-inputs",
      #"https://angular.dev/reference/migrations/outputs",
      #"https://angular.dev/reference/migrations/signal-queries",
      #"https://angular.dev/reference/migrations/cleanup-unused-imports",
     # "https://angular.dev/reference/migrations/self-closing-tagsS",
      
      #"https://angular.dev/cli/add",
      #"https://angular.dev/cli/analytics",
      #"https://angular.dev/cli/analytics/disable",
     # "https://angular.dev/cli/analytics/enable",
      #"https://angular.dev/cli/analytics/info",
      #"https://angular.dev/cli/analytics/prompt"
      #"https://angular.dev/cli/analytics/prompt",
      #"https://angular.dev/cli/cache",
      
      #"https://angular.dev/cli/cache/clean",
      #"https://angular.dev/cli/cache/disable",
      #"https://angular.dev/cli/cache/enable",
      #"https://angular.dev/cli/cache/info",
      
      #"https://angular.dev/cli/completion",
      #"https://angular.dev/cli/completion/script",
      
      #"https://angular.dev/cli/config",
      #"https://angular.dev/cli/deploy",
      #"https://angular.dev/cli/e2e",
      #"https://angular.dev/cli/extract-i18n",
      #"https://angular.dev/cli/generate",
      #"https://angular.dev/cli/generate/app-shell",
      #"https://angular.dev/cli/generate/application",
      #"https://angular.dev/cli/generate/class",
      #"https://angular.dev/cli/generate/component",
      #"https://angular.dev/cli/generate/config",
      #"https://angular.dev/cli/generate/directives",
      #"https://angular.dev/cli/generate/enum",
      #"https://angular.dev/cli/generate/environments",
      #"https://angular.dev/cli/generate/guard",
      #"https://angular.dev/cli/generate/interceptor",
      #"https://angular.dev/cli/generate/interface",
      #"https://angular.dev/cli/generate/library",
      #"https://angular.dev/cli/generate/module",
      #"https://angular.dev/cli/generate/pipe",
      #"https://angular.dev/cli/generate/resolver",
      #"https://angular.dev/cli/generate/service-worker",
      #"https://angular.dev/cli/generate/service",
      #"https://angular.dev/cli/generate/web-worker",
      #"https://angular.dev/cli/lint",
      #"https://angular.dev/cli/new",
      #"https://angular.dev/cli/run",
      #"https://angular.dev/cli/serve",
      #"https://angular.dev/cli/test",
      #"https://angular.dev/cli/update",
      #"https://angular.dev/cli/version",
      #"https://github.com/angular/angularfire#readme",
     # "https://github.com/angular/components/tree/main/src/google-maps#readme",
      #"https://github.com/google-pay/google-pay-button#angular",
      #"https://github.com/angular/components/blob/main/src/youtube-player/README.md",
      #"https://angular.dev/tutorials/learn-angular",
      #"https://angular.dev/tutorials/learn-angular/1-components-in-angular",
      #"https://angular.dev/tutorials/learn-angular/2-updating-the-component-class",
      #"https://angular.dev/tutorials/learn-angular/3-composing-components",
      #"https://angular.dev/tutorials/learn-angular/4-control-flow-if",
      #"https://angular.dev/tutorials/learn-angular/5-control-flow-for",
      #"https://angular.dev/tutorials/learn-angular/6-property-binding",
      #"https://angular.dev/tutorials/learn-angular/8-input",
      #"https://angular.dev/tutorials/learn-angular/6-property-binding",
      #"https://angular.dev/tutorials/learn-angular/9-output",
      #"https://angular.dev/tutorials/learn-angular/9-output",
      ##"https://angular.dev/tutorials/learn-angular/11-optimizing-images",
      #"https://angular.dev/tutorials/learn-angular/12-enable-routing",
      #"https://angular.dev/tutorials/learn-angular/13-define-a-route",
      ##"https://angular.dev/tutorials/learn-angular/14-routerLink",
      #"https://angular.dev/tutorials/learn-angular/15-forms",
      #"https://angular.dev/tutorials/learn-angular/16-form-control-values",
      #"https://angular.dev/tutorials/learn-angular/17-reactive-forms",
      #"https://angular.dev/tutorials/learn-angular/18-forms-validation",
      #"https://angular.dev/tutorials/learn-angular/19-creating-an-injectable-service",
      #"https://angular.dev/tutorials/learn-angular/20-inject-based-di",
      #"https://angular.dev/tutorials/learn-angular/21-constructor-based-di",
      #"https://angular.dev/tutorials/learn-angular/22-pipes",
      #"https://angular.dev/tutorials/learn-angular/23-pipes-format-data",
      #"https://angular.dev/tutorials/learn-angular/24-create-a-pipe",
      #"https://angular.dev/tutorials/learn-angular/25-next-steps",
     # 
      #"https://angular.dev/tutorials/first-app",
      #"https://angular.dev/tutorials/first-app/01-hello-world",
      #"https://angular.dev/tutorials/first-app/02-HomeComponent",
     # "https://angular.dev/tutorials/first-app/03-HousingLocation",
      #"https://angular.dev/tutorials/first-app/04-interfaces",
      #"https://angular.dev/tutorials/first-app/05-inputs",
      #"https://angular.dev/tutorials/first-app/06-property-binding",
      "https://angular.dev/tutorials/first-app/07-dynamic-template-values",
      #"https://angular.dev/tutorials/first-app/08-ngFor",
      #"https://angular.dev/tutorials/first-app/10-routing",
      #"https://angular.dev/tutorials/first-app/11-details-page",
      #"https://angular.dev/tutorials/first-app/12-forms",
      #"https://angular.dev/tutorials/first-app/13-search",
      #"https://angular.dev/tutorials/first-app/14-http",
      #"https://angular.dev/tutorials/deferrable-views",
      #"https://angular.dev/tutorials/deferrable-views/1-what-are-deferrable-views",
      #"https://angular.dev/tutorials/deferrable-views/2-loading-error-placeholder",
      #"https://angular.dev/tutorials/deferrable-views/3-defer-triggers"
]

import os
import json
import time
from urllib.parse import urlparse

output_dir = "raw_scraped_docs"
os.makedirs(output_dir, exist_ok=True)

for url in urls:
    try:
        # scrape with all 3 formats
        response = app.scrape_url(url=url, formats=['markdown', 'html', 'screenshot'])

        # pull out metadata fields
        meta = response.metadata
        scrape_id = meta.get("scrapeId") or getattr(response, "scrape_id", None)
        source_url = meta.get("sourceURL", url)
        status_code = meta.get("statusCode", None)

        # build result in Playground-style shape
        result = {
            "scrapeId": scrape_id,
            "sourceURL": source_url,
            "statusCode": status_code,
            "data": {
                "markdown": response.markdown,
                "screenshot": response.screenshot
            },
            "metadata": meta
        }

        # safe filename
        path = urlparse(url).path.strip('/')
        file_name = path.replace('/', '-') + '.json'

        # write out
        with open(os.path.join(output_dir, file_name), 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"✅ Saved Playground-style JSON: {file_name}")

        # wait 20 seconds
        time.sleep(10)

    except Exception as e:
        print(f"❌ Failed to scrape {url}: {e}")
