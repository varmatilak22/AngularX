import json
# List of your original links
links = [
    'https://material.angular.io/cdk/a11y/overview',
    'https://material.angular.io/cdk/accordion/overview',
    'https://material.angular.io/cdk/bidi/overview',
    'https://material.angular.io/cdk/clipboard/overview',
    'https://material.angular.io/cdk/coercion/overview',
    'https://material.angular.io/cdk/collections/overview',
    'https://material.angular.io/cdk/testing/overview',
    'https://material.angular.io/cdk/dialog/overview',
    'https://material.angular.io/cdk/drag-drop/overview',
    'https://material.angular.io/cdk/layout/overview',
    'https://material.angular.io/cdk/listbox/overview',
    'https://material.angular.io/cdk/menu/overview',
    'https://material.angular.io/cdk/overlay/overview',
    'https://material.angular.io/cdk/platform/overview',
    'https://material.angular.io/cdk/portal/overview',
    'https://material.angular.io/cdk/scrolling/overview',
    'https://material.angular.io/cdk/stepper/overview',
    'https://material.angular.io/cdk/table/overview',
    'https://material.angular.io/cdk/text-field/overview',
    'https://material.angular.io/cdk/tree/overview'
    
]

# Suffixes you want to generate
suffixes = ['overview', 'api', 'examples']

# Final result
generated_links = []

for link in links:
    if not link.endswith('overview'):
        continue  # skip if not ending with 'overview'
    base_link = link.rsplit('/', 1)[0]  # remove 'overview' from the end
    for suffix in suffixes:
        generated_links.append(f"{base_link}/{suffix}")

# Print all generated links
new_links=[]
for new_link in generated_links:
   new_links.append(new_link)

with open('links.json','w') as f:
    json.dump(new_links,f)