"""A: Nested image and TEE boundaries, shared custody, external agent."""
import common as c


def build(prs):
    s = c.page(prs, 'A', 'Training and inference share one verified image',
               'A shows nested boundaries: the Worker 0 TEE contains one combined '
               'dfl-worker container, two service roles and their internal key material. '
               'The agent invokes inference and receives results/evidence through the API.')
    diagram_start = len(s.shapes)
    c.panel(s, .65, 2.10, 8.55, 3.59, c.INK, 'F7F9FA', 1.7)
    c.icon(s, 'tee', .89, 2.24, .38, c.INK, 'F7F9FA')
    c.text(s, 'Worker 0 · TEE', 1.43, 2.20, 3.42, .39, 22, c.INK, True, False)
    c.text(s, 'One protected application', 5.26, 2.22, 3.59, .35, 16, c.MUTED)

    c.panel(s, .92, 2.80, 8.01, 2.63, c.INK, c.WHITE, 1.2)
    c.text(s, 'ONE dfl-worker CONTAINER · ONE IMAGE DIGEST',
           1.13, 2.95, 7.59, .34, 17, c.INK, True)

    c.panel(s, 1.17, 3.46, 3.15, .93, c.GREEN)
    c.text(s, 'DFL', 1.31, 3.53, 2.87, .38, 21, c.GREEN, True)
    c.text(s, 'Train · aggregate · publish', 1.29, 3.98, 2.91, .27, 14.5)
    c.panel(s, 5.09, 3.46, 3.56, .93, c.BLUE)
    c.text(s, 'Inference', 5.26, 3.53, 3.22, .38, 21, c.BLUE, True)
    c.text(s, 'Load model · predict · sign', 5.24, 3.98, 3.26, .27, 14.5)

    c.panel(s, 1.17, 4.78, 7.48, .43, c.PURPLE)
    c.icon(s, 'key', 1.36, 4.88, .42, c.PURPLE, c.TINT[c.PURPLE])
    c.text(s, 'Shared RSA key · separate signing keys',
           1.99, 4.82, 6.48, .33, 15, c.PURPLE, True)
    c.route(s, [(2.74,4.75),(2.74,4.43)], c.GREEN)
    c.route(s, [(6.87,4.75),(6.87,4.43)], c.BLUE)

    c.panel(s, 10.70, 3.43, 1.98, 1.12, c.BLUE)
    c.icon(s, 'agent', 11.47, 3.57, .40, c.BLUE, c.TINT[c.BLUE])
    c.text(s, 'Agent', 10.84, 4.03, 1.70, .41, 22, c.BLUE, True)
    c.route(s, [(11.68,3.38),(11.68,2.66),(9.75,2.66),(9.75,3.59),(8.69,3.59)], c.BLUE, 2)
    c.text(s, 'MCP Tool request', 9.59, 2.18, 3.09, .34, 16, c.BLUE, True)
    c.route(s, [(8.69,4.27),(10.65,4.27)], c.BLUE, 2)
    c.text(s, 'Result +\nevidence', 9.35, 3.68, 1.28, .55, 14, c.BLUE)
    c.panel(s, 10.70, 5.06, 1.98, .65, c.PURPLE)
    c.text(s, 'Transparency\nLog', 10.79, 5.11, 1.80, .53, 15, c.PURPLE, True)
    c.route(s, [(11.68,4.60),(11.68,5.01)], c.PURPLE, 1.8)
    c.text(s, 'AIR', 11.85, 4.68, .67, .27, 13.5, c.PURPLE)
    c.route(s, [(8.45,4.43),(8.45,4.59),(9.50,4.59),(9.50,5.385),(10.65,5.385)], c.PURPLE, 1.8)
    c.text(s, 'Sello', 9.55, 5.01, 1.06, .27, 14, c.PURPLE)
    # Move the diagram into the space freed by the removed introductory line.
    for shape in list(s.shapes)[diagram_start:]:
        shape.top -= c.b.Inches(.28)
    c.text(s, 'No private keys sent to the agent',
           .65, 5.78, 12.03, .42, 20, c.BLUE, True)
    return s
