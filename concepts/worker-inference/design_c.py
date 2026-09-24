"""C: One packaged image deployed with two approved runtime profiles."""
import common as c


def build(prs):
    s = c.page(prs, 'C', 'One image, two worker roles',
               'C preserves the two-role comparison from the original slide. '
               'Both runtime profiles contain the same packaged code, while only '
               'Worker 0 starts inference and exposes the agent-facing endpoint.')

    c.panel(s, 2.74, 1.57, 7.07, 1.06, c.INK, c.WHITE, 1.6)
    c.text(s, 'SAME dfl-worker IMAGE DIGEST', 3.00, 1.69, 6.55, .35, 21, c.INK, True)
    c.text(s, 'Packaged code: DFL + native inference', 3.00, 2.14, 6.55, .31, 17)
    c.route(s, [(6.28,2.68),(6.28,2.92),(2.48,2.92),(2.48,3.14)], c.INK)
    c.route(s, [(6.28,2.92),(7.55,2.92),(7.55,3.14)], c.INK)

    c.panel(s, .65, 3.19, 3.66, 2.51, c.INK, 'F7F9FA', 1.5)
    c.icon(s, 'tee', .89, 3.35, .35, c.INK, 'F7F9FA')
    c.text(s, 'Workers 1–5', 1.35, 3.33, 2.64, .39, 20, c.INK, True, False)
    c.text(s, 'Each: one TEE · one container', .86, 3.87, 3.24, .30, 14.3, c.MUTED)
    c.panel(s, .92, 4.39, 3.12, .45, c.GREEN)
    c.text(s, 'DFL running', 1.10, 4.44, 2.76, .33, 17, c.GREEN, True)
    c.panel(s, .92, 5.02, 3.12, .45, c.INK, 'ECEFF1')
    c.text(s, 'Inference packaged · off', 1.04, 5.07, 2.88, .33, 14.5, c.MUTED)

    c.panel(s, 4.83, 3.19, 5.46, 2.51, c.INK, 'F7F9FA', 1.5)
    c.icon(s, 'tee', 5.06, 3.35, .35, c.INK, 'F7F9FA')
    c.text(s, 'Worker 0', 5.53, 3.33, 2.50, .39, 20, c.INK, True, False)
    c.text(s, 'One TEE · one combined container', 5.08, 3.87, 4.95, .30, 15, c.MUTED)
    c.panel(s, 5.10, 4.39, 1.79, .45, c.GREEN)
    c.text(s, 'DFL', 5.25, 4.44, 1.49, .33, 17, c.GREEN, True)
    c.panel(s, 7.22, 4.39, 2.80, .45, c.BLUE)
    c.text(s, 'Inference running', 7.36, 4.44, 2.52, .33, 16, c.BLUE, True)
    c.panel(s, 5.10, 5.22, 4.92, .29, c.PURPLE)
    c.text(s, 'Worker keys used inside the container', 5.24, 5.24, 4.64, .25, 13.8, c.PURPLE, True)
    c.route(s, [(6.00,5.18),(6.00,4.90)], c.GREEN, 1.5)
    c.route(s, [(8.62,5.18),(8.62,4.90)], c.BLUE, 1.5)

    c.panel(s, 11.00, 3.71, 1.67, 1.00, c.BLUE)
    c.icon(s, 'agent', 11.59, 3.84, .36, c.BLUE, c.TINT[c.BLUE])
    c.text(s, 'Agent', 11.14, 4.30, 1.39, .31, 19, c.BLUE, True)
    c.route(s, [(11.82,3.66),(11.82,3.25),(10.65,3.25),(10.65,4.52),(10.06,4.52)], c.BLUE)
    c.text(s, 'MCP', 11.00, 2.82, 1.65, .32, 15, c.BLUE, True)
    c.route(s, [(10.06,4.73),(10.64,4.73),(10.64,5.59),(12.49,5.59),(12.49,4.76)], c.BLUE)
    c.text(s, 'Result +\nevidence', 10.86, 4.88, 1.48, .58, 14.5, c.BLUE)
    c.scope(s)
    return s
