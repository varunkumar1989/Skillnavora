"""Product Design for Product Managers: basic to advanced, with e-commerce, fintech and service-industry use cases, and interview prep."""
from coursekit import ill_flow, ill_cycle, ill_quad, ill_stack, _txt, _fig, E

def wires(screens, caption):
    """Mini phone wireframes. screens = [(title, [(kind, label), ...])] where kind in bar, img, text, card, btn, row, input, tabs."""
    W = 20 + len(screens) * 150; H = 330; s = ""
    for i, (title, items) in enumerate(screens):
        x = 14 + i * 150
        s += f'<rect x="{x}" y="12" width="132" height="290" rx="16" fill="#fff" stroke="#14112a" stroke-width="2"/><rect x="{x+8}" y="22" width="116" height="270" rx="10" fill="#faf9ff" stroke="#e3e0f2"/>'
        y = 30
        for kind, label in items:
            if kind == "bar":
                s += f'<rect x="{x+12}" y="{y}" width="108" height="20" rx="5" fill="#2E3192"/><text x="{x+66}" y="{y+14}" text-anchor="middle" font-family="Inter,Arial" font-size="9.5" font-weight="700" fill="#fff">{E(label)}</text>'; y += 26
            elif kind == "img":
                s += f'<rect x="{x+12}" y="{y}" width="108" height="46" rx="6" fill="#e9e5ff" stroke="#c9c4ea"/><text x="{x+66}" y="{y+28}" text-anchor="middle" font-family="Inter,Arial" font-size="9" fill="#55607a">{E(label)}</text>'; y += 52
            elif kind == "card":
                s += f'<rect x="{x+12}" y="{y}" width="108" height="30" rx="6" fill="#fff" stroke="#c9c4ea"/><text x="{x+66}" y="{y+19}" text-anchor="middle" font-family="Inter,Arial" font-size="9" fill="#14112a">{E(label)}</text>'; y += 36
            elif kind == "input":
                s += f'<rect x="{x+12}" y="{y}" width="108" height="22" rx="5" fill="#fff" stroke="#8a86a8"/><text x="{x+18}" y="{y+15}" font-family="Inter,Arial" font-size="9" fill="#8a86a8">{E(label)}</text>'; y += 28
            elif kind == "btn":
                s += f'<rect x="{x+12}" y="{y}" width="108" height="26" rx="13" fill="#6C4CF5"/><text x="{x+66}" y="{y+17}" text-anchor="middle" font-family="Inter,Arial" font-size="10" font-weight="700" fill="#fff">{E(label)}</text>'; y += 32
            elif kind == "row":
                s += f'<text x="{x+14}" y="{y+12}" font-family="Inter,Arial" font-size="9" fill="#14112a">{E(label.split("|")[0])}</text><text x="{x+118}" y="{y+12}" text-anchor="end" font-family="Inter,Arial" font-size="9" font-weight="700" fill="#14112a">{E(label.split("|")[-1])}</text>'; y += 18
            else:
                s += f'<text x="{x+14}" y="{y+11}" font-family="Inter,Arial" font-size="9" fill="#55607a">{E(label)}</text>'; y += 16
        s += f'<text x="{x+66}" y="322" text-anchor="middle" font-family="Inter,Arial" font-size="11" font-weight="700" fill="#2E3192">{E(title)}</text>'
    return _fig(s, W, 332, caption, min(760, W))

def tpl(name, rows): return f"<h3>{name}</h3><table><tr><th>Field</th><th>Fill in</th></tr>" + "".join(f"<tr><td>{r}</td><td></td></tr>" for r in rows) + "</table>"

CLASSES = [
 ("basic", "What product design is, and what a PM owns", "Understand the craft, the team and the PM's role.", ill_flow(["Discover: understand people", "Define: pick the right problem", "Develop: explore solutions", "Deliver: build, test, launch"], "The Double Diamond: diverge, converge, twice") + r"""
<p><b>Product design</b> is deciding <i>how a product works and feels</i> so that real people can solve a real problem easily. It is more than visuals. It covers research, structure, flows, interface, words, behaviour, testing and the way all of this is built and measured.</p>
<table><tr><th>Layer (Garrett's five planes)</th><th>Question</th><th>E-commerce example</th></tr>
<tr><td><b>Strategy</b></td><td>Why does this exist? Who is it for?</td><td>Help busy shoppers find and buy the right product fast</td></tr>
<tr><td><b>Scope</b></td><td>What features and content?</td><td>Search, filters, reviews, wishlist, returns</td></tr>
<tr><td><b>Structure</b></td><td>How is it organised and how do users move?</td><td>Categories, product page, cart, checkout flow</td></tr>
<tr><td><b>Skeleton</b></td><td>Where does each element go?</td><td>Wireframes: where the price, the delivery date and the buy button sit</td></tr>
<tr><td><b>Surface</b></td><td>How does it look and sound?</td><td>Colours, type, photos, button labels</td></tr></table>
<h3>Who does what</h3><table><tr><th>PM</th><th>Designer</th><th>Engineer</th></tr><tr><td>Problem, goals, priorities, trade-offs, success metrics</td><td>Research, flows, interface, prototypes, usability</td><td>Feasibility, performance, building, quality</td></tr></table>
<div class="box">The PM does <b>not</b> pick fonts or draw screens. The PM makes sure the team solves the right problem, for the right user, with a clear measure of success, and keeps design, engineering and business aligned.</div>""",
  ["Product design covers the whole experience, not only looks.", "Five planes: strategy, scope, structure, skeleton, surface.", "PM owns the problem and outcomes; designer owns the solution craft; both own the user."], "Pick an app you use daily and write its strategy, scope and structure in one line each."),

 ("basic", "Know your users: research methods and when to use them", "Choose the right way to learn from users.", ill_quad("Attitudes (what people say)  to  Behaviour (what they do)", "Qualitative (why)  to  Quantitative (how many)", ["Interviews, diary studies", "Usability tests, field visits", "Surveys, card sorts", "Analytics, A/B tests"], "Research methods map") + r"""
<table><tr><th>Method</th><th>Use it to</th><th>Example</th></tr>
<tr><td><b>User interviews</b></td><td>Understand needs, motives and context</td><td>Ask 8 shoppers how they choose a phone, and what made them abandon the last cart</td></tr>
<tr><td><b>Usability testing</b></td><td>See where people get stuck</td><td>Watch 5 first-time investors try to complete KYC</td></tr>
<tr><td><b>Surveys</b></td><td>Measure opinions at scale</td><td>CSAT after a delivery</td></tr>
<tr><td><b>Analytics</b></td><td>See what people do, and where they drop</td><td>Funnel from product page to payment</td></tr>
<tr><td><b>Session recordings, heatmaps</b></td><td>Spot confusion and rage taps</td><td>Users tapping a non-clickable image</td></tr>
<tr><td><b>Card sort / tree test</b></td><td>Fix navigation and labels</td><td>Where would you look for "returns"?</td></tr>
<tr><td><b>Support tickets and reviews</b></td><td>Find recurring pain</td><td>Top 10 complaint themes</td></tr></table>
<h3>Turning research into design inputs</h3><ul><li><b>Jobs To Be Done (JTBD):</b> "When I [situation], I want to [motivation], so I can [outcome]." Example: "When I run out of milk at 8 am, I want it in 10 minutes, so I can make breakfast."</li><li><b>Persona:</b> a short profile of a user type based on real data, not a made-up character.</li><li><b>Journey map:</b> the steps, feelings and pain points across time.</li><li><b>Insight format:</b> observation, reason, opportunity. Not "users want a faster checkout" but "6 of 8 users abandoned at address entry because typing long addresses on a phone is slow; offer map pin and autofill".</li></ul>
<div class="box">Five users find most big usability problems in one round (Nielsen Norman Group). Test early with few people, fix, then test again.</div>""",
  ["Mix qualitative (why) and quantitative (how many).", "JTBD and journey maps turn research into design direction.", "Test small and often."], "Plan a 5-person usability test for the checkout of an app you know: goals, tasks and what you will measure."),

 ("basic", "The product design process, step by step", "Follow a repeatable path from problem to launch.", ill_cycle(["Discover", "Define", "Ideate", "Prototype", "Test", "Ship and learn"], "The design loop") + r"""
<table><tr><th>Stage</th><th>What happens</th><th>Output the PM reviews</th></tr>
<tr><td><b>1. Discover</b></td><td>Research users, data, competitors, constraints</td><td>Insights and opportunity areas</td></tr>
<tr><td><b>2. Define</b></td><td>Frame the problem and the success measure</td><td>Problem statement, "How might we…?", metric target</td></tr>
<tr><td><b>3. Ideate</b></td><td>Explore many solutions before choosing</td><td>Sketches, flows, 3 options with trade-offs</td></tr>
<tr><td><b>4. Prototype</b></td><td>Make something testable</td><td>Clickable Figma prototype</td></tr>
<tr><td><b>5. Test</b></td><td>Usability tests, feedback, small experiments</td><td>Findings and changes</td></tr>
<tr><td><b>6. Build and ship</b></td><td>Specs, design QA, release, monitor</td><td>Shipped feature and dashboards</td></tr>
<tr><td><b>7. Learn</b></td><td>Measure outcomes, iterate</td><td>Impact review, next bets</td></tr></table>
<h3>Useful formats</h3><ul><li><b>Problem statement:</b> "[User] struggles to [goal] because [barrier], which causes [business impact]."</li><li><b>How Might We:</b> turns a pain into an open question: "How might we make address entry take under 10 seconds?"</li><li><b>Design sprint (5 days):</b> map, sketch, decide, prototype, test, for a big question in one week.</li><li><b>Lean version:</b> a 1 to 2 week loop: one assumption, one prototype, five tests.</li></ul>
<div class="box">The most common failure is jumping from problem to a favourite solution. Insist on at least three options and a clear reason for the pick.</div>""",
  ["Design is a loop, not a handoff.", "Define the problem and metric before screens.", "Compare at least three options."], "Write a problem statement and three 'How might we' questions for reducing cart abandonment."),

 ("basic", "Core UX principles every PM must know", "Learn the rules of thumb that predict good and bad design.", r"""
<h3>Nielsen's 10 usability heuristics (with examples)</h3>
<table><tr><th>Heuristic</th><th>Good example</th><th>Bad example</th></tr>
<tr><td>Visibility of system status</td><td>"Order packed, rider on the way", with live map</td><td>Spinner with no message after paying</td></tr>
<tr><td>Match with the real world</td><td>"Add to bag", "Wallet"</td><td>"Instantiate transaction"</td></tr>
<tr><td>User control and freedom</td><td>Undo send, cancel order</td><td>No way to remove a coupon</td></tr>
<tr><td>Consistency and standards</td><td>Same button position and wording on every screen</td><td>"Submit", "Done", "OK" for the same action</td></tr>
<tr><td>Error prevention</td><td>Confirm before sending a large UPI payment; disable Pay while processing</td><td>Easy double-tap on Pay</td></tr>
<tr><td>Recognition over recall</td><td>Saved addresses, recent searches</td><td>Retyping card details every time</td></tr>
<tr><td>Flexibility and efficiency</td><td>Shortcuts, reorder in one tap</td><td>Same long flow for every visit</td></tr>
<tr><td>Aesthetic, minimalist design</td><td>One main action per screen</td><td>Five competing banners</td></tr>
<tr><td>Help users recover from errors</td><td>"Card declined: your bank rejected it. Try UPI?"</td><td>"Error 4021"</td></tr>
<tr><td>Help and documentation</td><td>Contextual tips, searchable FAQ</td><td>A 40-page PDF</td></tr></table>
<h3>Laws of UX in plain words</h3>
<table><tr><th>Law</th><th>Meaning</th><th>Design use</th></tr>
<tr><td><b>Hick's law</b></td><td>More choices, slower decisions</td><td>Limit options; group and filter</td></tr>
<tr><td><b>Fitts's law</b></td><td>Bigger, closer targets are easier to hit</td><td>Large thumb-reach buttons (at least 44 to 48 px)</td></tr>
<tr><td><b>Miller's law</b></td><td>People hold about 7 items in short-term memory</td><td>Chunk numbers: 4-4-4-4 card input</td></tr>
<tr><td><b>Jakob's law</b></td><td>Users expect your app to work like others they know</td><td>Use familiar patterns (cart icon top right)</td></tr>
<tr><td><b>Von Restorff effect</b></td><td>The different item is remembered</td><td>One highlighted primary button</td></tr>
<tr><td><b>Peak-end rule</b></td><td>People judge by the peak and the ending</td><td>Delight on success screens; smooth refunds</td></tr>
<tr><td><b>Doherty threshold</b></td><td>Responses under about 400 ms feel instant</td><td>Skeleton screens, optimistic updates</td></tr>
<tr><td><b>Zeigarnik effect</b></td><td>Unfinished tasks stay on the mind</td><td>Progress bars, "complete your profile 80%"</td></tr></table>""",
  ["Heuristics are a fast review checklist.", "Fewer choices and bigger targets improve completion.", "Feedback, forgiveness and familiarity beat cleverness."], "Review one checkout against the 10 heuristics and list the 3 worst violations."),

 ("intermediate", "Information architecture and navigation", "Organise content so people can find things without thinking.", ill_stack([("Home", "the few things most users need now"), ("Sections", "categories, tabs, hubs"), ("Lists and search", "browse, filter, sort"), ("Detail pages", "product, account, transaction"), ("Actions", "buy, pay, share, support")], "Information architecture from broad to specific") + r"""
<p><b>Information architecture (IA)</b> is how content and features are grouped, labelled and connected. Good IA means users find what they need in few steps, using words they would use.</p>
<table><tr><th>Pattern</th><th>When it works</th><th>Example</th></tr>
<tr><td>Bottom tab bar (3 to 5 items)</td><td>Frequent switching between main areas on mobile</td><td>Home, Orders, Wallet, Profile</td></tr>
<tr><td>Search-first</td><td>Huge catalogue</td><td>Marketplaces, grocery</td></tr>
<tr><td>Hub and spoke</td><td>Distinct tasks from one place</td><td>Banking super-app: pay, recharge, invest</td></tr>
<tr><td>Hamburger or drawer</td><td>Rarely used items only</td><td>Settings, legal pages</td></tr>
<tr><td>Wizard / stepper</td><td>Long, linear tasks</td><td>KYC, loan application</td></tr></table>
<h3>How to design and test IA</h3><ul><li><b>Card sorting:</b> ask users to group cards (products or features) and name the groups.</li><li><b>Tree testing:</b> give users a text-only menu and a task; measure if they reach the right place.</li><li><b>Labels:</b> use customer words ("Refund status") not internal ones ("Reverse logistics").</li><li><b>Depth:</b> aim for the most common task in 3 taps or fewer.</li></ul>
<div class="box"><b>Example:</b> An e-commerce app that hid "Track order" under Profile, then Orders, then Details saw many "where is my order?" support calls. Moving a live order card to the Home screen reduced the calls and added a trust signal.</div>""",
  ["IA is grouping, labelling and linking.", "Three to five bottom tabs, search for big catalogues.", "Test with card sorts and tree tests, not opinions."], "Redesign the top-level navigation for a food delivery app and test it with three friends."),

 ("intermediate", "Interaction design: flows, states, forms and microcopy", "Design the moments between the screens.", wires([("Product", [("bar", "Shoes"), ("img", "Photo"), ("text", "Rs 2,499 · free delivery"), ("btn", "Add to bag")]), ("Cart", [("bar", "Bag (2)"), ("card", "Running shoe  Rs 2,499"), ("row", "Delivery|Free"), ("row", "Total|Rs 2,499"), ("btn", "Checkout")]), ("Address", [("bar", "Address"), ("input", "Pincode"), ("card", "Use my location"), ("input", "House, street"), ("btn", "Deliver here")]), ("Pay", [("bar", "Payment"), ("card", "UPI  (recommended)"), ("card", "Card"), ("card", "Cash on delivery"), ("btn", "Pay Rs 2,499")])], "A four-screen purchase flow: one primary action per screen") + r"""
<ul><li><b>User flow:</b> the path from a goal to its completion, with decisions and exits. Draw the happy path first, then errors and edge cases.</li><li><b>Screen states:</b> every screen needs <b>empty</b> ("No orders yet, browse deals"), <b>loading</b> (skeleton), <b>error</b> ("No internet. Try again"), <b>partial</b>, <b>success</b>, and <b>offline</b>.</li><li><b>Forms:</b> ask only what you need, one column, correct keyboard type, inline validation, smart defaults, autofill, show password option.</li><li><b>Microcopy:</b> short, specific, human. "Pay Rs 2,499" beats "Submit". Say what happens next.</li><li><b>Feedback and motion:</b> acknowledge every tap within 100 ms; use motion to explain, not decorate.</li><li><b>Progressive disclosure:</b> show the essentials, reveal detail on demand.</li><li><b>Onboarding:</b> let users reach value fast; ask permissions in context ("Allow location to show nearby stores").</li></ul>
<table><tr><th>Bad copy</th><th>Better copy</th></tr><tr><td>Invalid input</td><td>Enter a 10-digit mobile number</td></tr><tr><td>Transaction failed</td><td>Payment not completed. Your money is safe. Try again or use UPI.</td></tr><tr><td>Are you sure? Yes / No</td><td>Delete this address? Delete / Keep</td></tr></table>
<div class="box">Ask your designer for the "state sheet": every state of every screen. Missing states cause most production bugs and support tickets.</div>""",
  ["Design flows and all states, not only the happy path.", "One primary action per screen; specific microcopy.", "Reduce form effort with defaults, autofill and the right keyboard."], "List all states for an order tracking screen and write the microcopy for each."),

 ("intermediate", "Visual design and design systems for PMs", "Read a screen like a designer and know what a design system buys you.", ill_stack([("Tokens", "colour, type, spacing, radius, shadow values"), ("Components", "button, input, card, nav bar, modal"), ("Patterns", "login, checkout, search, empty states"), ("Templates / screens", "assembled pages"), ("Guidelines", "usage, accessibility, content, governance")], "Layers of a design system") + r"""
<table><tr><th>Concept</th><th>What to look for</th></tr>
<tr><td><b>Hierarchy</b></td><td>The eye should land on the most important thing first (size, weight, colour, space)</td></tr>
<tr><td><b>Grid and spacing</b></td><td>Consistent 4 or 8-pixel steps; alignment; breathing room</td></tr>
<tr><td><b>Typography</b></td><td>Two typefaces at most, 3 to 4 sizes, readable body text (at least 16 px on mobile)</td></tr>
<tr><td><b>Colour</b></td><td>One brand colour for actions; meaning colours (red errors, green success); never colour alone</td></tr>
<tr><td><b>Contrast</b></td><td>Text contrast at least 4.5:1 (WCAG AA)</td></tr>
<tr><td><b>Imagery and icons</b></td><td>Real, consistent, with labels where meaning is unclear</td></tr>
<tr><td><b>Dark mode and themes</b></td><td>Separate palette, not an inverted copy</td></tr></table>
<h3>Why design systems matter</h3><ul><li><b>Speed:</b> teams assemble screens from ready parts.</li><li><b>Consistency:</b> the whole product feels like one product.</li><li><b>Quality and accessibility</b> are built into components once.</li><li><b>Cheaper change:</b> change a token (the brand blue) once, update everywhere.</li></ul>
<p>Examples to study: Google Material Design, Apple Human Interface Guidelines, Atlassian, Polaris (Shopify), and India examples like Razorpay Blade and Zomato Sushi.</p>
<div class="box">PM tip: when a designer says "this is not in the system", ask the cost of a new component versus reusing an existing one. Custom UI is slower to build, test and maintain.</div>""",
  ["Hierarchy, spacing, contrast and consistency make most of the difference.", "A design system is tokens, components and patterns with rules.", "Reuse beats reinvent unless the user value is clear."], "Audit three screens for hierarchy and contrast and write five fixes."),

 ("intermediate", "Prototyping and usability testing", "Test ideas cheaply before engineers build them.", ill_flow(["Sketch idea", "Low-fidelity wireframe", "Clickable prototype", "Test with 5 users", "Fix and re-test", "Hand off"], "From idea to tested design") + r"""
<table><tr><th>Fidelity</th><th>Use</th><th>Tool</th></tr><tr><td>Paper or whiteboard</td><td>Compare ideas in minutes</td><td>Pen, Miro</td></tr><tr><td>Low-fi wireframe</td><td>Test structure and flow, no visual distraction</td><td>Figma, Balsamiq</td></tr><tr><td>High-fi prototype</td><td>Test look, copy and interactions</td><td>Figma, ProtoPie</td></tr><tr><td>Coded prototype / beta</td><td>Test real data and performance</td><td>Lovable, Replit, feature flags</td></tr></table>
<h3>A simple usability test</h3><ol><li><b>Goal:</b> "Can new users buy a phone in under 3 minutes?"</li><li><b>Tasks:</b> "Find a phone under Rs 20,000 and buy it with UPI." Do not give hints.</li><li><b>Think aloud:</b> ask users to say what they are thinking.</li><li><b>Observe:</b> task success, time, errors, confusion, quotes.</li><li><b>Prioritise:</b> severity = how many users and how bad (blocker, major, minor).</li><li><b>Report:</b> top 5 issues, evidence clips, proposed fixes.</li></ol>
<ul><li><b>Measures:</b> task success rate, time on task, error rate, the <b>SUS</b> questionnaire (System Usability Scale, 68 is about average), and satisfaction.</li><li><b>Usability test vs A/B test:</b> usability tests explain <i>why</i> with few people; A/B tests measure <i>how much</i> with many. Use both.</li><li><b>Remote tools:</b> Maze, UserTesting, Lookback, or a simple video call with screen share.</li></ul>
<div class="box">Do not ask "Do you like it?". Ask people to <b>do</b> something and watch. Opinions are weak evidence; behaviour is strong.</div>""",
  ["Match fidelity to the question.", "Five users, real tasks, think aloud.", "Usability tests find why; A/B tests find how much."], "Write a test script with three tasks for a prototype you have, and run it with two people."),

 ("intermediate", "Accessibility and inclusive design (with India in mind)", "Design for everyone, including low-end phones and many languages.", r"""
<table><tr><th>Area</th><th>What to do</th><th>Why</th></tr>
<tr><td>Contrast</td><td>Text at least 4.5:1; large text 3:1</td><td>Low vision, sunlight</td></tr>
<tr><td>Touch targets</td><td>At least 44 by 44 pt (iOS) or 48 by 48 dp (Android)</td><td>Motor impairments, big thumbs</td></tr>
<tr><td>Screen readers</td><td>Labels for every control, logical order, alt text</td><td>Blind and low-vision users (TalkBack, VoiceOver)</td></tr>
<tr><td>Text scaling</td><td>Layout works at 200% font size</td><td>Older users</td></tr>
<tr><td>Not colour alone</td><td>Icons and text with status colours</td><td>Colour blindness</td></tr>
<tr><td>Captions and transcripts</td><td>For audio and video</td><td>Deaf users, noisy places</td></tr>
<tr><td>Reduced motion</td><td>Respect system setting</td><td>Vestibular conditions</td></tr></table>
<h3>Designing for India and emerging markets</h3><ul><li><b>Languages:</b> Hindi and regional languages, mixed-language text, longer strings that break layouts, voice input.</li><li><b>Low-end phones and poor networks:</b> small app size, lite mode, skeleton screens, offline states, compressed images.</li><li><b>Trust and literacy:</b> icons plus text, clear amounts in rupees, no jargon, help in the user's language, human support.</li><li><b>Shared devices:</b> families sharing one phone; protect payments with PIN or biometrics.</li><li><b>Payments:</b> UPI-first, COD option for e-commerce, clear pending and failed states.</li></ul>
<div class="box">Accessibility is also a business and legal issue: more customers, better SEO and usability for everyone, and compliance in many markets (WCAG 2.2 AA is the common target; India's Rights of Persons with Disabilities Act applies to digital services).</div>""",
  ["Accessibility benefits all users and the business.", "Contrast, targets, labels, text scaling are the basics.", "In India, design for language, low-end devices and low-trust contexts."], "Run an accessibility check on your favourite app: contrast, target size, font scaling and screen reader labels."),

 ("intermediate", "E-commerce product design: use cases and how it works", "Design discovery, product pages, cart and checkout that convert and build trust.", wires([("Search", [("bar", "Search"), ("input", "running shoes"), ("card", "Filters: price, size, brand"), ("card", "Sort: relevance"), ("img", "Results grid")]), ("Product page", [("img", "Gallery, video"), ("text", "Rs 2,499  4.4 stars (3,210)"), ("card", "Size, colour"), ("card", "Delivery to 560001: Tue"), ("btn", "Add to bag")]), ("Checkout", [("bar", "Checkout"), ("card", "Address (saved)"), ("card", "UPI, card, COD"), ("row", "Items|Rs 2,499"), ("btn", "Place order")])], "E-commerce core screens") + r"""
<table><tr><th>Stage</th><th>Use case</th><th>How the design works</th><th>Metric</th></tr>
<tr><td><b>Discovery</b></td><td>"I need running shoes under Rs 3,000"</td><td>Search with autosuggest and typo tolerance, filters that match how people decide (size, price, rating), good sort defaults, category pages, personalised rows</td><td>Search success, zero-result rate, click-through</td></tr>
<tr><td><b>Product page</b></td><td>"Is this the right one, and can I trust it?"</td><td>Big photos and video, price and offers visible, size guide, delivery date by pincode, reviews with photos, return policy, "add to bag" always visible</td><td>Add-to-cart rate, bounce</td></tr>
<tr><td><b>Cart</b></td><td>"What will I pay in total?"</td><td>Show full cost early (delivery, taxes), edit quantity, save for later, coupon field that does not distract, stock warnings</td><td>Cart-to-checkout rate</td></tr>
<tr><td><b>Checkout</b></td><td>"Pay quickly and safely"</td><td>Guest or one-tap login by OTP, saved address, address autofill, UPI first, trust badges, one primary button, clear errors</td><td>Checkout completion, payment success rate</td></tr>
<tr><td><b>After purchase</b></td><td>"Where is my order? I want to return it."</td><td>Live tracking, proactive updates, easy returns and refunds</td><td>Support contacts per 100 orders, repeat rate</td></tr></table>
<h3>What research says</h3><p>Across 50 studies, Baymard Institute's list puts the average documented cart abandonment rate at about <b>70%</b>, and its checkout research finds the average large store has dozens of fixable usability problems. The usual causes: surprise costs, forced account creation, long or confusing forms, limited payment methods and trust worries. <a href="https://baymard.com/research/cart-abandonment-rate">Source: Baymard Institute</a>.</p>
<h3>Quick commerce and marketplace twists</h3><ul><li><b>Quick commerce:</b> speed promise (10 minutes), live stock, minimal choice per category, one-screen cart, accurate ETA, substitutions policy.</li><li><b>Two-sided marketplaces:</b> design for buyer and seller; seller tools (listing, pricing, inventory, payouts) need the same care as the buyer app.</li><li><b>Trust:</b> genuine reviews, clear seller info, easy return policy, secure payment signs.</li></ul>
<div class="box"><b>Common mistakes:</b> forced sign-up before checkout, delivery cost revealed at the last step, hidden coupon fields that send users off to search for codes, tiny tap targets, and the "Pay" button that can be tapped twice.</div>""",
  ["Every stage has a user question to answer.", "Show total cost and delivery date early; fewer fields at checkout.", "Measure each stage: search, add-to-cart, checkout, payment success, returns."], "Write the top five checkout friction points of any shopping app and propose one fix with a metric for each."),

 ("intermediate", "Fintech product design: use cases and how it works", "Design money moments that feel safe, clear and fast.", wires([("Pay", [("bar", "Pay to Ravi"), ("input", "Amount  Rs 500"), ("card", "From: HDFC ****1234"), ("btn", "Pay")]), ("PIN", [("bar", "Enter UPI PIN"), ("text", "Paying Rs 500 to Ravi"), ("input", "- - - -"), ("btn", "Confirm")]), ("Result", [("bar", "Paid"), ("text", "Rs 500 sent to Ravi"), ("row", "UPI Ref|4021..."), ("row", "Time|10:42 am"), ("btn", "Done")])], "A UPI payment: three steps, each with clear status") + r"""
<table><tr><th>Use case</th><th>How it works</th><th>Design principles</th></tr>
<tr><td><b>Onboarding and KYC</b></td><td>Mobile OTP, PAN, Aadhaar eKYC or video KYC, bank link</td><td>Explain why each item is needed, show progress, save and resume, allow camera retry tips, fast approval status</td></tr>
<tr><td><b>Pay with UPI</b></td><td>Pick payee, enter amount, authenticate with UPI PIN, bank confirms, receipt</td><td>Verify the payee name before paying, protect against wrong amounts, show "pending" honestly, never hide the reference number</td></tr>
<tr><td><b>Cards and wallets</b></td><td>Tokenised card, 3-D Secure OTP, wallet balance</td><td>Never ask for card details twice, show masked numbers, clear failure reasons and "money is safe" copy</td></tr>
<tr><td><b>Lending and BNPL</b></td><td>Eligibility check, offer, agreement, disbursal, EMI</td><td>Show full cost (rate, fees, total repayable) before consent; no dark patterns; reminders before due dates</td></tr>
<tr><td><b>Investing</b></td><td>Risk profile, product choice, order, portfolio</td><td>Plain-language risk warnings, no gamified over-trading, long-term framing, regulated disclosures (SEBI)</td></tr>
<tr><td><b>Insurance</b></td><td>Quote, buy, claim</td><td>Simple coverage summary, easy claim steps and status</td></tr></table>
<h3>Fintech design rules</h3><ul><li><b>Clarity of money:</b> amounts, fees and totals in plain numbers, with currency, never hidden.</li><li><b>Trust and security:</b> biometrics, PIN, device binding, visible security cues, fraud warnings ("Do not share OTP").</li><li><b>Honest status:</b> success, pending, failed, with what to do next and when money returns. Failed-but-debited is the most stressful state; design it with care.</li><li><b>Error prevention:</b> confirm payee name, limit warnings, recent-payee safety checks.</li><li><b>Compliance by design:</b> consent screens, data localisation, RBI and SEBI rules, DPDP Act privacy. Collaborate with legal early.</li><li><b>Fraud-aware UX:</b> friction in the right place (new payee, large amount), not everywhere.</li></ul>
<div class="box"><b>Metrics:</b> KYC completion and time, first-transaction rate, payment success rate by method and bank, failure reasons, support contacts, fraud rate, activation (first money in) and retention.</div>""",
  ["Money UX is about clarity, trust and honest status.", "Design the pending and failed states most carefully.", "Add friction only where risk is high."], "Draw the 'failed but money debited' screen for a UPI payment and write the copy."),

 ("intermediate", "Other industries: delivery, mobility, SaaS, health and education", "See the same principles applied to different services.", r"""
<table><tr><th>Industry</th><th>Core use case</th><th>How the design works</th><th>Key design focus</th></tr>
<tr><td><b>Food delivery</b></td><td>Order dinner and know when it arrives</td><td>Search by cuisine and restaurant, menu with photos, customise items, live tracking of order and rider, ETA updates</td><td>Accurate ETA, trust, reorder in one tap, clear fees</td></tr>
<tr><td><b>Ride hailing</b></td><td>Get a cab in minutes</td><td>Pickup pin, fare estimate, driver match, live map, OTP to start, rating</td><td>Reassurance while waiting, safety (SOS, share trip), fare transparency</td></tr>
<tr><td><b>B2B SaaS</b></td><td>Complete work faster</td><td>Dashboard, tables, filters, bulk actions, roles and permissions, onboarding checklists, empty states with sample data</td><td>Efficiency, learnability, time to value, enterprise needs</td></tr>
<tr><td><b>Healthcare</b></td><td>Book a doctor and manage records</td><td>Doctor search and slots, video visit, prescriptions, reminders, reports</td><td>Privacy, clarity, accessibility, reduce anxiety</td></tr>
<tr><td><b>Education</b></td><td>Learn and stay consistent</td><td>Course path, lessons, quizzes, progress, streaks, community</td><td>Motivation, progress visibility, short sessions</td></tr>
<tr><td><b>Travel and tickets</b></td><td>Book seats or rooms</td><td>Search by date and place, filters, price transparency, seat map, hold timer, payment, e-ticket</td><td>Price clarity, hold and timeout design, urgency without false claims</td></tr>
<tr><td><b>Social and content</b></td><td>Discover and share content</td><td>Feed, follow, create, notifications, safety tools</td><td>Relevance, creators' needs, notification control, well-being</td></tr></table>
<h3>Patterns that repeat across industries</h3><ul><li><b>Search, filter, sort:</b> food, products, doctors, flights.</li><li><b>Live status and ETA:</b> delivery, rides, orders, payments.</li><li><b>Trust cues:</b> ratings, verified badges, secure labels, clear policies.</li><li><b>Reorder and shortcuts</b> for repeat users.</li><li><b>Empty, loading and error states</b> everywhere.</li></ul>
<div class="box">When designing for a new industry, learn the <b>vocabulary</b>, the <b>risks</b> (money, safety, health) and the <b>regulation</b> first. Then reuse proven patterns instead of inventing new ones.</div>""",
  ["The same principles apply across industries.", "Learn the domain's risks and rules before designing.", "Reuse proven patterns: search, status, trust, repeat."], "Pick an industry you do not know. List its three biggest user risks and one design pattern for each."),

 ("advanced", "Behaviour design, growth and the ethics of persuasion", "Use habit and motivation design without manipulating users.", ill_cycle(["Trigger", "Action", "Variable reward", "Investment"], "The Hook model (Nir Eyal)") + r"""
<table><tr><th>Concept</th><th>Meaning</th><th>Example</th></tr>
<tr><td><b>Fogg behaviour model</b></td><td>Behaviour = motivation x ability x prompt</td><td>Make the action easy (one tap), prompt at the right time</td></tr>
<tr><td><b>Hook model</b></td><td>Trigger, action, variable reward, investment</td><td>Notification, open app, new content, save preferences</td></tr>
<tr><td><b>Streaks and goals</b></td><td>Loss aversion, progress</td><td>Duolingo streak; fitness streak with a weekly freeze</td></tr>
<tr><td><b>Social proof</b></td><td>People follow others</td><td>"1,200 bought this week"</td></tr>
<tr><td><b>Defaults and nudges</b></td><td>The default is chosen most often</td><td>Pre-selected UPI, a recommended plan</td></tr>
<tr><td><b>Activation</b></td><td>The first moment of real value</td><td>First order delivered, first investment made</td></tr></table>
<h3>Dark patterns to avoid (they hurt trust and invite regulation)</h3><ul><li><b>Fake urgency</b> ("only 2 left" when untrue) and <b>drip pricing</b> (fees added at the end).</li><li><b>Confirmshaming</b> ("No, I do not want to save money").</li><li><b>Forced continuity</b> and hard-to-cancel subscriptions; <b>basket sneaking</b>; <b>disguised ads</b>.</li><li>India's Central Consumer Protection Authority has issued guidelines on dark patterns, and the DPDP Act requires clear consent.</li></ul>
<div class="box"><b>Test:</b> would you be comfortable showing this design and its metric to your user's family, a regulator and the press? If not, redesign it.</div>""",
  ["Make the right behaviour easy and well-prompted.", "Habits come from value plus a repeatable loop.", "Avoid dark patterns; trust is a long-term metric."], "Redesign a subscription cancel flow that is clear and fair, and note what metric you would watch."),

 ("advanced", "Measuring design: metrics, experiments and impact", "Prove that design work moves outcomes.", ill_stack([("Business outcome", "revenue, retention, cost to serve"), ("Product metrics", "activation, conversion, repeat rate"), ("Experience metrics", "task success, time, errors, CSAT, SUS"), ("Behaviour data", "clicks, scroll, funnel steps, recordings")], "Metrics ladder from behaviour to business") + r"""
<table><tr><th>Framework</th><th>What it contains</th></tr>
<tr><td><b>HEART (Google)</b></td><td>Happiness, Engagement, Adoption, Retention, Task success; define goals, signals and metrics for each</td></tr>
<tr><td><b>Funnel analysis</b></td><td>Steps from entry to goal; find the biggest drop and ask why</td></tr>
<tr><td><b>Usability benchmarks</b></td><td>SUS, task success, time on task, error rate, tracked release over release</td></tr>
<tr><td><b>A/B testing</b></td><td>Compare versions with random users; one clear primary metric, guardrails, enough sample</td></tr>
<tr><td><b>Qualitative signals</b></td><td>Support tickets, reviews, interviews, session recordings</td></tr></table>
<h3>Example: redesigning checkout</h3><ul><li><b>Hypothesis:</b> showing delivery date and total cost earlier will increase checkout completion.</li><li><b>Primary metric:</b> checkout completion rate. <b>Guardrails:</b> payment success rate, refund rate, page speed.</li><li><b>Design:</b> run an A/B test on 50% of traffic for two full weeks; segment by new vs returning users and by device.</li><li><b>Read-out:</b> lift with confidence interval, plus qualitative review of drop-offs.</li><li><b>Decision:</b> ship, iterate or roll back.</li></ul>
<div class="box">Not every design change can be A/B tested (small traffic, big navigation shifts). Then use usability studies, staged rollouts, before-and-after comparisons and customer feedback, and be honest about uncertainty.</div>""",
  ["Link design changes to outcome metrics and guardrails.", "Use HEART to cover happiness and task success, not only clicks.", "Combine experiments with qualitative understanding."], "Define goals, signals and metrics (HEART) for a new onboarding flow."),

 ("advanced", "Scaling design: systems, collaboration and design debt", "Run design well across teams and over time.", r"""
<ul><li><b>Working with designers:</b> bring problems, constraints and data; not solutions. Share the goal and success metric early. Review in critiques; give feedback as user impact, not taste ("users may miss this action because it blends with the background").</li><li><b>Design critique:</b> present the goal, show options, ask specific questions, record decisions.</li><li><b>Handoff and design QA:</b> annotated specs, states, tokens, responsive behaviour; check the built UI against design before release.</li><li><b>Design debt:</b> inconsistent components, old patterns and missing states. Track it like tech debt; reserve capacity; link fixes to metrics (speed, error rate, conversion).</li><li><b>Design ops:</b> tools, libraries, research repository, rituals, consistent processes.</li><li><b>Scaling across platforms:</b> iOS, Android, web, tablet, foldables; shared logic, platform-specific behaviour.</li><li><b>Localisation:</b> languages, formats, right-to-left text, cultural symbols.</li><li><b>Build vs buy vs adapt</b> for components and design kits.</li></ul>
<table><tr><th>Situation</th><th>Good PM response</th></tr><tr><td>Designer and engineer disagree on effort</td><td>Ask for options and trade-offs, pick by user impact and cost, document the decision</td></tr><tr><td>Stakeholder wants a banner on the home screen</td><td>Ask the goal; test impact on core tasks; propose placement and rules</td></tr><tr><td>Deadline pressure</td><td>Cut scope, not quality of core flow; use a smaller first release</td></tr><tr><td>Design feels inconsistent</td><td>Audit components, fix the top 5, add to the system</td></tr></table>""",
  ["Bring problems and data to design, not solutions.", "Give feedback as user impact.", "Manage design debt like tech debt."], "Write a design critique brief for a feature you are working on: goal, options, questions."),

 ("advanced", "AI-era product design", "Design AI features that users can trust and control.", r"""
<ul><li><b>Set expectations:</b> say what the AI can and cannot do; show confidence or sources where useful.</li><li><b>Keep the human in control:</b> preview, edit, undo, approve before actions with consequences.</li><li><b>Handle errors gracefully:</b> AI will be wrong sometimes; give easy ways to correct it and report issues.</li><li><b>Conversational UI:</b> suggestions and quick replies reduce blank-page anxiety; combine chat with structured UI (cards, forms) for actions like payments.</li><li><b>Personalisation with privacy:</b> explain why a recommendation is shown; offer controls and opt-outs.</li><li><b>Latency and streaming:</b> show progress; stream answers.</li><li><b>Safety:</b> guardrails, escalation to humans for sensitive topics (money, health).</li></ul>
<table><tr><th>Industry</th><th>AI design example</th></tr><tr><td>E-commerce</td><td>Visual search, size advice, review summaries, an assistant that compares products with sources</td></tr><tr><td>Fintech</td><td>Spend insights, fraud alerts with explanation, a support assistant that hands over to humans for disputes</td></tr><tr><td>Support</td><td>RAG chatbot with citations and a "talk to an agent" button</td></tr></table>
<p>See the <a href="ai-ux-design.html">Designing AI Experiences (AI UX)</a> course for the full method.</p>""",
  ["Set expectations, show sources, keep humans in control.", "Design for AI mistakes, not only success.", "Combine chat with structured UI."], "Design the error and correction flow for an AI shopping assistant."),

 ("advanced", "Product design interviews: how to answer and what interviewers want", "Practise the common formats with a clear structure.", r"""
<table><tr><th>Question type</th><th>Example</th><th>What they test</th></tr>
<tr><td><b>Design X for Y</b></td><td>"Design a savings app for college students."</td><td>User empathy, structure, prioritisation, trade-offs</td></tr>
<tr><td><b>Improve an existing product</b></td><td>"How would you improve Swiggy's search?"</td><td>Critique, problem finding, metrics</td></tr>
<tr><td><b>Critique</b></td><td>"What do you like and dislike about this checkout?"</td><td>Design vocabulary, user thinking</td></tr>
<tr><td><b>Open-ended object</b></td><td>"Design an alarm clock for the blind."</td><td>Constraints, creativity, inclusion</td></tr>
<tr><td><b>Collaboration</b></td><td>"A designer disagrees with your priority. What do you do?"</td><td>Communication, influence, outcomes</td></tr>
<tr><td><b>Metrics</b></td><td>"How would you measure a redesign's success?"</td><td>Goal-metric-guardrail thinking</td></tr></table>
<h3>A structure you can use (state it out loud)</h3><ol><li><b>Clarify:</b> product, platform, scope, goal, constraints. Ask 3 or 4 questions.</li><li><b>Users:</b> pick 2 or 3 segments, choose one, and say why.</li><li><b>Needs and pain points:</b> top 3, in their words.</li><li><b>Prioritise:</b> pick one problem by impact and effort.</li><li><b>Solutions:</b> 3 options, a pick with reasons.</li><li><b>Flow and key screens:</b> describe the happy path and one edge case, with states.</li><li><b>Metrics:</b> goal, success metric, guardrails.</li><li><b>Risks and next steps:</b> experiments, rollout, what you would learn first.</li></ol>
<h3>Worked answer: "Design a savings app for college students"</h3><ul><li><b>Clarify:</b> India, 18 to 24, Android first; goal: first-time savers.</li><li><b>Users:</b> hostel students with irregular pocket money; part-time earners. Pick the first.</li><li><b>Pains:</b> money disappears on small spends, no habit, distrust of apps, no minimum balance.</li><li><b>Prioritise:</b> a painless way to save small amounts automatically.</li><li><b>Options:</b> round-up savings on UPI spends; a savings goal with friends; a weekly fixed auto-save.</li><li><b>Pick:</b> round-ups plus a visible goal ring; trust through bank partners and clear withdrawals anytime.</li><li><b>Flow:</b> link UPI, set goal, see round-ups, celebrate milestones; states for failed link and low balance.</li><li><b>Metrics:</b> activation (first round-up), weekly active savers, average saved per month; guardrails: withdrawals within 24 hours, complaints, overdraft.</li></ul>
<div class="box">Tips: think aloud, use real product examples, talk about trade-offs, name risks, keep to the structure but be flexible when the interviewer redirects, and end with metrics and learning plan.</div>""",
  ["Use a clear structure and say it out loud.", "Choose one user and one problem, justified.", "Always finish with metrics, risks and next steps."], "Record a 5-minute answer to 'Design a savings app for college students' using the structure."),

 ("advanced", "Final project: a product design case study", "Create a portfolio-quality case that shows your thinking.", r"""<p>Pick one real problem in e-commerce, fintech or another service you use (examples: reduce checkout drop-off, make UPI failures less stressful, improve order tracking). Produce a 10-slide or 2-page case with:</p>
<ol><li>Problem, user and goal with the evidence (analytics, reviews, 5 interviews).</li><li>Current journey map and the three biggest friction points.</li><li>Three solution options and the pick.</li><li>Key screens (sketch or Figma), all states and microcopy.</li><li>Accessibility and inclusion check.</li><li>Test plan: prototype test with 5 users and a proposed A/B test.</li><li>Metrics: primary, secondary, guardrails, expected impact.</li><li>Risks, trade-offs and rollout plan.</li></ol>
<p>Present it for five minutes to a friend, record their questions and update the case.</p>""",
  ["A good case shows problem, evidence, options and impact.", "Show trade-offs and what you would test.", "Practise presenting the story in five minutes."], "Complete the case study and share it with a designer for feedback."),
]

CHEAT = [("Double Diamond", "Discover, Define, Develop, Deliver"), ("JTBD", "Jobs To Be Done: situation, motivation, outcome"), ("IA", "Information architecture: grouping and labelling content"), ("Heuristic evaluation", "Expert review against usability principles"),
 ("Hick's law", "More choices, slower decisions"), ("Fitts's law", "Large, near targets are easier to hit"), ("Jakob's law", "Users expect familiar patterns"), ("Peak-end rule", "People remember the peak and the end"),
 ("Wireframe", "Low-fidelity layout of a screen"), ("Prototype", "Clickable model for testing"), ("Design system", "Tokens, components, patterns and rules"), ("Design token", "A named design value such as a colour or spacing step"),
 ("SUS", "System Usability Scale questionnaire"), ("HEART", "Happiness, Engagement, Adoption, Retention, Task success"), ("A/B test", "Random comparison of two versions"), ("Dark pattern", "A deceptive design that tricks users"),
 ("WCAG", "Web Content Accessibility Guidelines; AA is the common target"), ("Skeleton screen", "Placeholder shape shown while content loads"), ("Progressive disclosure", "Reveal detail only when needed"), ("Empty state", "Screen with no data yet, with guidance")]

GLOSSARY = [("Affordance", "A cue showing how something can be used"), ("Cognitive load", "Mental effort needed to use an interface"), ("Information scent", "Cues that tell users a link leads to what they want"), ("Mental model", "How users think a system works"),
 ("Persona", "Research-based profile of a user type"), ("Journey map", "Steps, feelings and pain points over time"), ("User flow", "Path from goal to completion"), ("Card sorting", "Users group items to reveal their mental model"),
 ("Tree testing", "Testing a text-only menu for findability"), ("Think-aloud", "Users speak thoughts while using a product"), ("Task success rate", "Share of users who complete a task"), ("Hamburger menu", "Hidden navigation icon with three lines"),
 ("Bottom navigation", "Tab bar at the bottom of a mobile screen"), ("Microcopy", "Small interface text such as buttons and errors"), ("Responsive design", "Layout adapts to screen sizes"), ("Fidelity", "How close a mockup is to the final product"),
 ("Onboarding", "Guiding new users to first value"), ("Activation", "The moment a new user first gets real value"), ("Friction", "Anything that slows or stops a user"), ("Conversion rate", "Share of users who complete a goal"),
 ("Drop-off", "Users leaving at a funnel step"), ("Nudge", "A gentle push toward a choice"), ("Confirmshaming", "Guilt-based opt-out wording"), ("Accessibility", "Usable by people with a wide range of abilities"),
 ("Touch target", "Tappable area of a control"), ("Contrast ratio", "Difference between text and background colour"), ("Component", "Reusable interface part"), ("Design debt", "Accumulated inconsistencies and shortcuts"),
 ("Handoff", "Passing design details to engineering"), ("Design QA", "Checking the built UI against the design")]

QA = [("What is product design, and how is it different from UI design?", "Product design covers the whole experience: problem, research, structure, flows, interface, content, testing and measurement. UI design is the visual layer inside it."),
 ("What is the role of a PM in product design?", "Define the problem, users, goals and metrics, set constraints and priorities, enable research and testing, and align design, engineering and business. The PM does not dictate the visuals."),
 ("Walk me through your design process.", "Discover users and data, define the problem and metric, ideate several options, prototype, test with users, ship, measure and iterate."),
 ("How do you decide which problem to solve?", "Combine evidence from users and data, size the impact on the business goal, check feasibility and strategic fit, and prioritise by impact versus effort."),
 ("Design a savings app for college students.", "Clarify scope, pick a user (hostel students), name top pains, prioritise automatic small savings, compare options (round-ups, goals, auto-save), pick one, describe flow and states, and define activation and retention metrics with guardrails."),
 ("How would you improve checkout on an e-commerce app?", "Look at the funnel, find the biggest drop, show total cost and delivery date earlier, reduce form fields with saved addresses and autofill, offer UPI first, add trust cues, prevent double payment, and measure completion and payment success."),
 ("What makes a good fintech UX?", "Clarity of money, honest status, security cues, error prevention, plain language, and compliance by design. Handle pending and failed states with care."),
 ("A payment failed but money was debited. What should the screen say?", "State what happened, that the money is safe, when it returns or will be confirmed, a reference number, and the next action. Keep the order pending until the gateway confirms."),
 ("How do you reduce cart abandonment?", "Remove surprises (costs, forced sign-up), simplify forms, offer more payment options, add trust, recover with reminders, fix speed, and use research to find the real reasons."),
 ("How do you measure a redesign's success?", "Set a primary outcome metric, supporting experience metrics (task success, time), and guardrails. Use A/B tests where possible, plus usability studies and qualitative signals."),
 ("Usability test or A/B test?", "Usability tests with few users explain why people struggle; A/B tests measure how much a change matters at scale. Use both."),
 ("How many users do you need for a usability test?", "About five users find most major issues in a round; repeat with new users after fixes."),
 ("Explain Hick's law with an example.", "More options increase decision time. A checkout with ten payment methods shown equally is slower than showing the top three and grouping the rest."),
 ("What are dark patterns? Give examples.", "Deceptive designs such as fake urgency, hidden fees, confirmshaming and hard-to-cancel subscriptions. They harm trust and attract regulation."),
 ("How do you design for accessibility?", "Meet contrast and target size, label controls for screen readers, support text scaling, do not rely on colour alone, caption media, and test with assistive tech."),
 ("How do you design for low-end phones and poor networks in India?", "Small app size, lite modes, skeleton screens, offline states, compressed images, vernacular languages, voice input and clear status messages."),
 ("What is a design system and why does it matter?", "Reusable tokens, components and patterns with rules. It speeds delivery, improves consistency and accessibility, and lowers cost of change."),
 ("A designer disagrees with your priorities. What do you do?", "Listen, restate the goal and evidence, ask for their user-impact reasoning, explore options and trade-offs, decide with data, and document it."),
 ("A stakeholder wants a promotional banner on the home screen.", "Clarify the business goal, test the impact on core task completion, propose limits (placement, frequency), and measure with guardrails."),
 ("How do you prioritise design debt against new features?", "Quantify the user and business impact (conversion, errors, speed, support tickets), reserve a regular share of capacity, and bundle fixes with related feature work."),
 ("What is the Double Diamond?", "A model with two diverge-converge phases: discover and define the problem, then develop and deliver the solution."),
 ("What are JTBD and how do you use them?", "A way to describe what users want to achieve in a situation. Use it to frame problems and compare alternatives, including non-product alternatives."),
 ("How do you design an onboarding flow?", "Get users to first value fast, ask only essential info, ask permissions in context, show progress, let users skip, and measure activation."),
 ("How would you improve search in a food delivery app?", "Study queries and zero-result searches, add autosuggest and typo tolerance, support cuisine, dish and restaurant intents, show relevant filters, personalise, and measure search success and conversion."),
 ("How do you design for trust in a marketplace?", "Verified sellers, real reviews with photos, clear policies, secure payments, transparent pricing and quick support."),
 ("How should an AI assistant be designed in a shopping app?", "Set expectations, show sources, let users edit and undo, combine chat with product cards, give easy escalation and handle errors gracefully."),
 ("What is the HEART framework?", "Google's framework: Happiness, Engagement, Adoption, Retention, Task success, each with goals, signals and metrics."),
 ("How would you test a prototype before engineering builds it?", "Create a clickable prototype, give 5 users realistic tasks, observe, fix, and repeat; then plan a staged rollout or A/B test."),
 ("Describe a design you would remove from a product.", "Choose a feature that adds clutter or friction without value (for example a forced sign-up wall), explain the evidence and the metric you would watch after removing it."),
 ("What would you do in your first 30 days as PM on a design-heavy product?", "Meet users and designers, review research and analytics, audit key flows against heuristics, find top friction, agree on goals and metrics, and ship one small improvement.")]

LINKS = [("Nielsen Norman Group: 10 usability heuristics", "https://www.nngroup.com/articles/ten-usability-heuristics/"), ("Laws of UX", "https://lawsofux.com/"), ("Baymard Institute: cart abandonment research", "https://baymard.com/research/cart-abandonment-rate"),
 ("Baymard: checkout usability benchmark", "https://baymard.com/research/checkout-usability"), ("Design Council: the Double Diamond", "https://www.designcouncil.org.uk/our-resources/the-double-diamond/"), ("Google Material Design 3", "https://m3.material.io/"),
 ("Apple Human Interface Guidelines", "https://developer.apple.com/design/human-interface-guidelines/"), ("W3C WCAG overview", "https://www.w3.org/WAI/standards-guidelines/wcag/"), ("The Design Sprint (book site)", "https://www.thesprintbook.com/"),
 ("NN/g: why 5 users are enough", "https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/"), ("Figma Learn", "https://help.figma.com/hc/en-us"), ("Refactoring UI (visual design for developers and PMs)", "https://www.refactoringui.com/"),
 ("Google HEART framework (research paper)", "https://research.google/pubs/measuring-the-user-experience-on-a-large-scale-user-centered-metrics-for-web-applications/"), ("Deceptive design (formerly dark patterns)", "https://www.deceptive.design/")]

TEMPLATES = (tpl("Problem statement", ["User and context", "Goal they want to achieve", "Barrier or pain (with evidence)", "Business impact", "Success metric", "Constraints"])
 + tpl("Usability test plan", ["Goal", "Participants (5) and recruitment", "Tasks (3)", "Success criteria", "What we will measure", "Findings and decisions"])
 + tpl("Design review checklist", ["Goal and metric clear?", "Happy path and edge cases?", "All states (empty, loading, error, offline)?", "Accessibility (contrast, targets, labels)?", "Microcopy reviewed?", "Analytics events defined?", "Trust and compliance reviewed?"])
 + tpl("Product design interview answer", ["Clarify", "Users and segment", "Pain points", "Priority problem", "Three options and the pick", "Flow and states", "Metrics and guardrails", "Risks and next steps"]))

COURSE = {"slug": "product-design", "pdf": "Product_Design_for_PMs_Complete_Guide.pdf", "page": "product-design-for-pms.html",
 "title": "Product Design for PMs: Complete Guide", "kicker": "SkillNavora · Product Management · Design from basic to advanced",
 "intro": "How great products are designed and how PMs lead that work: research, process, UX principles, flows, visual systems, testing, accessibility, e-commerce and fintech use cases, behaviour design, metrics and interview prep.",
 "oneline": "Product design is deciding how a product works and feels so real people can solve a real problem easily. PMs do not draw screens; they own the problem, the users and the outcomes, and they work with designers to get there.",
 "tutor_q": "Teach me product design from basic to advanced with e-commerce and fintech examples",
 "extra_btn": '<a class="btn btn-line" href="ai-academy.html">All AI Skills Academy courses</a>', "cheat_title": "Product design cheat sheet",
 "classes": CLASSES, "cheat": CHEAT, "qa": QA, "glossary": GLOSSARY, "links": LINKS, "templates_html": TEMPLATES}
