import json
from markdown import markdown


def parse_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def generate_html(data):
    html = '''
    <html>
    <head>
        <title>Security Findings</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
            }
            h1 {
                text-align: center;
            }
            #toc {
                margin-bottom: 20px;
            }
            #toc ul {
                list-style-type: none;
                padding-left: 0;
            }
            #toc a {
                text-decoration: none;
            }
            .finding {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 20px;
            }
            .finding h2 {
                margin-top: 0;
            }
            .finding p {
                margin-bottom: 10px;
                white-space: pre-line;
            }
            .finding pre {
                background-color: #f4f4f4;
                padding: 10px;
                overflow-x: auto;
                white-space: pre-wrap;
            }
            .finding .metaprompt {
                background-color: #e6f2ff;
                padding: 10px;
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <h1>Security Findings</h1>
        <div id="toc">
            <h2>Table of Contents</h2>
            <ul>
    '''

    for finding in data[0]:
        title = finding['title'][0]
        html += f'''
                <li><a href="#{title}">{title}</a></li>
        '''

    html += '''
            </ul>
        </div>
    '''

    for finding in data[0]:
        title = finding['title'][0]
        description = finding['description'][0]
        solution_claude = markdown(finding['solution']['long_description'],
                                   extensions=['fenced_code', 'mdx_truly_sane_lists'])
        solution_gpt4 = markdown(data[1][data[0].index(finding)]['solution']['long_description'],
                                 extensions=['fenced_code', 'mdx_truly_sane_lists'])
        solution_llama = markdown(data[2][data[0].index(finding)]['solution']['long_description'],
                                  extensions=['fenced_code', 'mdx_truly_sane_lists'])
        metaprompt_claude = finding['solution']['metadata']['prompt_long_breakdown']['meta_prompts']
        metaprompt_gpt4 = data[1][data[0].index(finding)]['solution']['metadata']['prompt_long_breakdown'][
            'meta_prompts']
        metaprompt_llama = data[2][data[0].index(finding)]['solution']['metadata']['prompt_long_breakdown'][
            'meta_prompts']

        html += f'''
            <div class="finding" id="{title}">
                <h2>{title}</h2>
                <p>{description}</p>
                <h3>Solution (Claude):</h3>
                <pre>{solution_claude}</pre>
                <h3>Solution (GPT-4):</h3>
                <pre>{solution_gpt4}</pre>
                <h3>Solution (Llama):</h3>
                <pre>{solution_llama}</pre>
                <div class="metaprompt">
                    <h4>Metaprompt (Claude):</h4>
                    <pre>{metaprompt_claude}</pre>
                </div>
                <div class="metaprompt">
                    <h4>Metaprompt (GPT-4):</h4>
                    <pre>{metaprompt_gpt4}</pre>
                </div>
                <div class="metaprompt">
                    <h4>Metaprompt (Llama):</h4>
                    <pre>{metaprompt_llama}</pre>
                </div>
            </div>
        '''

    html += '''
    </body>
    </html>
    '''

    with open('security_findings.html', 'w') as file:
        file.write(html)


# Parse the JSON files
claude_data = parse_json('VulnerabilityReport_10_claude-3-opus.json')
gpt4_data = parse_json('VulnerabilityReport_10_gpt-4o.json')
llama_data = parse_json('VulnerabilityReport_10_llama3_instruct.json')

# Generate the HTML page
generate_html([claude_data, gpt4_data, llama_data])