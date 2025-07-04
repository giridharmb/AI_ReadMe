from graphviz import Digraph

# Create a Digraph with styling
dot = Digraph(
    comment='Fancy ADK-RAG-MCP-LLM Interaction Diagram',
    format='png',
    graph_attr={
        'rankdir': 'TB',  # Top to bottom layout
        'splines': 'ortho',  # Straight, orthogonal edges
        'bgcolor': 'lightblue:lightyellow',  # Gradient background
        'fontcolor': 'black',
        'fontsize': '14',
        'pad': '0.5',  # Padding around graph
        'nodesep': '0.5',  # Node separation
        'ranksep': '1.0'  # Rank separation
    },
    node_attr={
        'style': 'filled',
        'fontsize': '12',
        'fontcolor': 'black',
        'penwidth': '2'
    },
    edge_attr={
        'color': 'darkblue',
        'penwidth': '2',
        'fontsize': '10',
        'fontcolor': 'darkblue'
    }
)

# Define nodes with custom shapes, colors, and labels
dot.node(
    'User',
    'User\n(Query Input)',
    shape='ellipse',
    fillcolor='lightgreen',
    color='darkgreen'
)
dot.node(
    'ADK',
    'Google ADK\n(LlmAgent, SequentialAgent)',
    shape='box',
    fillcolor='lightyellow',
    color='goldenrod',
    style='filled,rounded'
)
dot.node(
    'RAG',
    'RAG\n(Vector Store, Knowledge Base)',
    shape='diamond',
    fillcolor='lightpink',
    color='crimson'
)
dot.node(
    'MCP',
    'MCP Server\n(Tools: YouTube, Database)',
    shape='hexagon',
    fillcolor='lightcyan',
    color='teal'
)
dot.node(
    'LLM',
    'LLM\n(Gemini, Gemma 3)',
    shape='parallelogram',
    fillcolor='lavender',
    color='purple'
)
dot.node(
    'Response',
    'Response\n(Answer Output)',
    shape='ellipse',
    fillcolor='lightgreen',
    color='darkgreen'
)

# Define edges with labels for interactions
dot.edge('User', 'ADK', label='Submits Query', color='darkgreen')
dot.edge('ADK', 'RAG', label='Retrieve Data', color='crimson')
dot.edge('ADK', 'MCP', label='Access Tools', color='teal')
dot.edge('RAG', 'LLM', label='Augmented Data', color='purple')
dot.edge('MCP', 'LLM', label='Tool Outputs', color='purple')
dot.edge('LLM', 'Response', label='Generate Answer', color='darkblue')
dot.edge('Response', 'User', label='Deliver Response', color='darkgreen', style='dashed')

# Render the diagram
dot.render('adk_fancy_diagram', cleanup=False)