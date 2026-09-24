"""Purpose first: source intention and its concrete use in VITA-FL."""
import common as c


def heading(s, text, x, y, width, color=c.INK):
    c.text(s, text, x, y, width, .36, 15, color, True)


def scope(s, value):
    c.text(s, value, .73, 5.67, 11.85, .34, 15, c.MUTED)


def node(s, title, x, y, width, color=c.BLUE, height=.61, size=18):
    c.panel(s, x, y, width, height, color)
    c.text(s, title, x+.12, y+.06, width-.24, height-.12, size, color, True, True)


def a_sello(prs):
    s = c.page(prs, 'A · Sello', 'Sello: make the agent’s actions accountable', 'sello')
    c.text(s, 'An agent controls its own history. Its owner may never see an omitted action.',
           .68, 1.53, 11.96, .54, 21)

    c.panel(s, .68, 2.34, 4.25, 3.03, c.INK, c.WHITE)
    heading(s, 'THE PAPER’S INTENTION', .89, 2.49, 3.80)
    c.text(s, 'Independent audit\nof agent actions',
           .90, 3.03, 3.79, .88, 23, c.INK, True)
    node(s, 'Service records the action', .90, 4.10, 3.81, c.INK, .51, 16.5)
    c.route(s, [(2.81,4.64),(2.81,4.81)], c.INK)
    c.text(s, 'Owner recovers a private record', .91, 4.88, 3.78, .33, 16)

    c.panel(s, 5.17, 2.34, 7.47, 3.03, c.BLUE, c.WHITE)
    heading(s, 'WHAT I IMPLEMENTED IN VITA-FL', 5.40, 2.49, 6.98, c.BLUE)
    c.text(s, 'An auditable record of the\nthree model-use steps.',
           5.40, 3.03, 6.96, .88, 23, c.BLUE, True)
    for x,title in [(5.40,'Load\nmodel'),(7.80,'Select\nX-ray'),(10.20,'Run\ninference')]:
        node(s, title, x, 4.06, 2.17, c.BLUE, .76, 17)
    for x in [7.60, 10.00]:
        c.route(s, [(x,4.44),(x+.16,4.44)], c.BLUE, 1.5)
    c.text(s, 'Receiver records each call before returning success.',
           5.42, 4.95, 6.92, .33, 15.5)
    scope(s, 'Scope: receipts are checked inside the agent service; independent owner oversight remains open.')
    c.source(s, 'sello')
    return s


def a_air(prs):
    s = c.page(prs, 'A · AIR', 'AIR: trace a prediction back to the model used', 'air')
    c.text(s, 'A prediction alone does not show which model processed which input.',
           .68, 1.53, 11.96, .54, 21)

    c.panel(s, .68, 2.34, 4.25, 3.03, c.INK, c.WHITE)
    heading(s, 'THE DRAFT’S INTENTION', .89, 2.49, 3.80)
    c.text(s, 'Make one inference\ncheckable by others.',
           .90, 3.03, 3.79, .88, 23, c.INK, True)
    node(s, 'Model + input + result', .90, 4.13, 3.81, c.INK, .52, 17)
    c.route(s, [(2.81,4.68),(2.81,4.84)], c.INK)
    c.text(s, 'Linked to execution evidence', .91, 4.92, 3.78, .33, 16)

    c.panel(s, 5.17, 2.34, 7.47, 3.03, c.BLUE, c.WHITE)
    heading(s, 'WHAT I IMPLEMENTED IN VITA-FL', 5.40, 2.49, 6.98, c.BLUE)
    c.text(s, 'Connect the published DFL model\nto its later use by the agent.',
           5.40, 3.03, 6.96, .88, 23, c.BLUE, True)
    node(s, 'Published\nDFL model', 5.40, 4.09, 2.32, c.GREEN, .77, 17)
    node(s, 'Selected X-ray\n+ prediction', 8.13, 4.09, 2.77, c.BLUE, .77, 17)
    c.route(s, [(7.77,4.47),(8.07,4.47)], c.BLUE)
    c.route(s, [(10.95,4.47),(11.27,4.47)], c.PURPLE)
    node(s, 'Audit\nrecord', 11.32, 4.09, 1.08, c.PURPLE, .77, 14.5)
    c.text(s, 'Preserve the checked evidence for later review.',
           5.42, 4.97, 6.92, .33, 15.5)
    scope(s, 'Adaptation: integrated with DFL and later auditing; execution trust relies on worker admission.')
    c.source(s, 'air')
    return s


def speech(s, message):
    c.panel(s, .69, 1.60, 11.95, .79, c.BLUE)
    c.icon(s, 'agent', .91, 1.78, .42, c.BLUE)
    c.text(s, 'Agent reports', 1.52, 1.81, 2.11, .34, 17, c.BLUE, True)
    c.text(s, '“'+message+'”', 3.72, 1.74, 8.65, .49, 22, c.BLUE, True)


def b_sello(prs):
    s = c.page(prs, 'B · Sello', 'Sello: back the agent’s report with a service record', 'sello')
    speech(s, 'I loaded the model and ran the inference.')
    heading(s, 'PAPER’S AIM', .72, 2.64, 2.34)
    c.text(s, 'The owner can privately audit actions without trusting the agent or its operator.',
           3.02, 2.53, 9.54, .73, 20)
    c.b.add_divider(s, .71, 3.29, 11.92, 'D9E0E4', .012)
    heading(s, 'MY IMPLEMENTATION', .72, 3.51, 4.02, c.BLUE)
    c.text(s, 'The receiver records the three steps.',
           5.00, 3.46, 7.55, .52, 20, c.BLUE, True)

    for x,title in [(.72,'Model loaded'),(4.79,'X-ray selected'),(8.86,'Inference run')]:
        node(s, title, x, 4.16, 3.75, c.BLUE, .58, 20)
        c.route(s, [(x+1.875,4.78),(x+1.875,5.08)], c.PURPLE)
    c.route(s, [(4.53,4.45),(4.73,4.45)], c.BLUE)
    c.route(s, [(8.60,4.45),(8.80,4.45)], c.BLUE)
    c.panel(s, .72, 5.14, 11.89, .38, c.PURPLE)
    c.text(s, 'Receipts are logged before success is returned; the agent checks them.',
           .93, 5.17, 11.47, .32, 17, c.PURPLE, True, True)
    scope(s, 'Scope: receipts are checked inside the agent service; independent owner oversight remains open.')
    c.source(s, 'sello')
    return s


def b_air(prs):
    s = c.page(prs, 'B · AIR', 'AIR: give the prediction a traceable origin', 'air')
    speech(s, 'Our shared model produced this result.')
    heading(s, 'DRAFT’S AIM', .72, 2.64, 2.34)
    c.text(s, 'Make one result traceable to its model, input and execution.',
           3.02, 2.53, 9.54, .73, 20)
    c.b.add_divider(s, .71, 3.29, 11.92, 'D9E0E4', .012)
    heading(s, 'MY IMPLEMENTATION', .72, 3.51, 4.02, c.BLUE)
    c.text(s, 'Link the DFL model to its later use.',
           5.00, 3.46, 7.55, .52, 20, c.BLUE, True)

    node(s, 'Published DFL model', .72, 4.16, 3.51, c.GREEN, .67, 19)
    node(s, 'This X-ray + this prediction', 4.77, 4.16, 4.25, c.BLUE, .67, 18)
    node(s, 'Later review', 9.56, 4.16, 3.05, c.PURPLE, .67, 19)
    c.route(s, [(4.29,4.50),(4.71,4.50)], c.BLUE)
    c.route(s, [(9.08,4.50),(9.50,4.50)], c.PURPLE)
    c.panel(s, .72, 5.14, 11.89, .38, c.PURPLE)
    c.text(s, 'The agent checks the linked evidence and preserves it in the transparency log.',
           .93, 5.17, 11.47, .32, 17, c.PURPLE, True, True)
    scope(s, 'Scope: trust in the executing service relies on its prior admission as a worker.')
    c.source(s, 'air')
    return s
